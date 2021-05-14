"""This module governs generating noise for a 2D array which can be
converted to an image, heightmap, or similar application.

Info sources:
    `Definitions <http://libnoise.sourceforge.net/glossary/>`_

"""

import numpy as np
from opensimplex import OpenSimplex
from noise import perlin
import logging
from abc import ABC, abstractmethod


class FractalNoiseController:

    def __new__(cls, *args, **kwargs):
        """Modify the class with a vectorized version of the fractal noise function.

        """
        inst = super().__new__(cls)
        inst.fractal_noise = np.vectorize(inst.fractal_noise_scalar)

        return inst

    def __init__(self, engine='opensimplex', seed=0, cfg=None):
        """

        :param engine:
        :param seed:
        """
        self.wavefn = WaveFunction.from_cfg(cfg)
        # noise_lib = NoiseLibWrapper(engine, seed)
        try:
            self.engine = NoiseLibWrapper.init_2d_engine(engine=engine, seed=seed)
        except KeyError as e:
            raise ValueError('Invalid option for noise engine') from e

    def configure_wavefunction(self, frequency=None, amplitude=None, lacunarity=None, gain=None):
        """Set the mathematical parameters that govern the behavior of the wave function.

        :param frequency:
        :param amplitude:
        :param lacunarity:
        :param gain:
        :return:
        """
        self.wavefn.frequency = frequency or self.wavefn.frequency
        self.wavefn.amplitude = amplitude or self.wavefn.amplitude
        self.wavefn.lacunarity = lacunarity or self.wavefn.lacunarity
        self.wavefn.gain = gain or self.wavefn.gain

    def fractal_noise_scalar(self, X, Y, Z):
        """Calculate and return the 2D-noise value corresponding to the coordinate (X,Y), scaled
            to an octave according to the Z-value and the parameters that define the WaveFunction.

        :param X:
        :param Y:
        :param Z:
        :return:
        """
        amp, freq, gain, lacu = (
            self.wavefn.amplitude,
            self.wavefn.frequency,
            self.wavefn.gain,
            self.wavefn.lacunarity
        )

        return amp * (gain ** Z) * self.engine.eval2d(
            X * (freq * (lacu ** Z)),
            Y * (freq * (lacu ** Z))
        )


class NoiseLibWrapper(ABC):
    """Wrapper to encapsulate different noise libraries

    """

    def __init__(self, seed=None):
        self.seed = seed or 0
        self.callmap = {
            2: self.eval2d,
            3: self.eval3d
        }

    @abstractmethod
    def eval2d(self, x, y):
        pass

    @abstractmethod
    def eval3d(self, x, y, z):
        pass

    def eval4d(self, x, y, z, w):
        raise NotImplementedError

    @staticmethod
    def init_2d_engine(engine, seed=0):
        if engine == 'opensimplex':
            return OpenSimplexWrapper(seed)
        elif engine == 'pynoise':
            return perlin.SimplexNoise()
        else:
            raise ValueError('Invalid option for noise library.')


class OpenSimplexWrapper(NoiseLibWrapper):

    def __init__(self, seed=0):
        super().__init__(seed)
        self.corelib = OpenSimplex(seed)

    def eval2d(self, x, y):
        return self.corelib.noise2d(x, y)

    def eval3d(self, x, y, z):
        return self.corelib.noise3d(x, y, z)

    def eval4d(self, x, y, z, w):
        return self.corelib.noise4d(x, y, z, w)


class PyNoiseWrapper(NoiseLibWrapper):
    def __init__(self, seed=None):
        super().__init__(seed)
        self.corelib = perlin.SimplexNoise()

    def eval2d(self, x, y):
        return self.corelib.noise2(x, y)

    def eval3d(self, x, y, z):
        return self.corelib.noise3(x, y, z)

    def eval4d(self, x, y, z, d):
        raise NotImplementedError('Python noise library does not support 4-dimensional noise.')


class WaveFunction:

    def __init__(self, amplitude=1.0, frequency=0.01,
                 gain=0.5, lacunarity=2.0):

        self.amplitude = amplitude
        self.frequency = frequency
        self.gain = gain
        self.lacunarity = lacunarity

    @classmethod
    def from_cfg(cls, cfg):
        wave = cfg.get('accumulator').get('wave')
        return cls(**wave)

    def __setattr__(self, key, value):
        if isinstance(value, (float, int, np.float64)):
            super().__setattr__(key, value)
        else:
            logging.warning(f'Tried to assign attribute illegal value: {value}')

    def shift_octave(self, offset):
        """Shift this wave function by the given ``offset``,
        according to the current function's base attributes.

        For any offset, the new wave has the same gain and
            lacunarity as the current. The new wave's amplitude
            and frequency are equal to a multiple of their base values.
            Frequency is multiplied by lacunarity once for each offset,
            and the same relationship applies to amplitude and gain.

        Simplifying for any offset:
            ``frequency = frequency * (lacunarity ^ offset)``

            ``amplitude = amplitude * (gain ^ offset)``

        For example, shifting a wave with frequency=1 and
            lacunarity=2 by two octaves returns a wave with equal
            lacunarity and frequency=1*(2^2)=4. The same relationship
            exists between amplitude and gain.


        :param int offset: The number of octaves to move up or down from
            the current WaveFunction

        :return: The new WaveFunction according to offset
        :rtype: WaveFunction
        """
        if offset == 0:
            return self

        return WaveFunction(
            amplitude=(self.amplitude * (self.gain ** offset)),
            frequency=(self.frequency * (self.lacunarity ** offset)),
            gain=self.gain, lacunarity=self.lacunarity
        )

    def __repr__(self):
        return (
            'Wave Function with '
            f'(Amplitude={self.amplitude}; '
            f'Gain={self.gain}; '
            f'Frequency={self.frequency}; '
            f'Lacunarity={self.lacunarity})'
        )
