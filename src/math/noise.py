"""This module governs generating noise for a 2D array which can be
converted to an image, heightmap, or similar application.

Info sources:
    `Definitions <http://libnoise.sourceforge.net/glossary/>`_

"""

import numpy as np
from opensimplex import OpenSimplex
# from noise import perlin
import logging
from abc import ABCMeta, abstractmethod

from cartography.cartography import WorldParameters
from configuration import *


class FractalNoiseController:

    def __new__(cls, *args, **kwargs):
        """Modify the class with a vectorized version of the fractal noise function.

        """
        inst = super().__new__(cls)
        inst.fractal_noise = np.vectorize(inst.fractal_noise_scalar)

        return inst

    def __init__(self, cfg=None):
        """

        :param WorldParameters cfg:
        """
        self.cfg = cfg or WorldParameters(CONFIG)

        enginelib = cfg.engine.get('lib')
        seed = cfg.engine.get('seed')
        self.wavefn = WaveFunction.from_cfg(cfg)
        # noise_lib = NoiseLibWrapper(engine, seed)
        try:
            self.engine = NoiseLibWrapper.init_2d_engine(libname=enginelib, seed=seed)
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


class WaveFunction:

    def __init__(self, amplitude=1.0, frequency=0.01,
                 gain=0.5, lacunarity=2.0):

        self.amplitude = amplitude
        self.frequency = frequency
        self.gain = gain
        self.lacunarity = lacunarity

    @classmethod
    def from_cfg(cls, cfg):
        wave = cfg.accumulator.get('wave')
        return cls(**wave)

    def __setattr__(self, key, value):
        if isinstance(value, (float, int, np.float64)):
            super().__setattr__(key, value)
        else:
            logging.warning(f'Tried to assign attribute illegal value: {value}')

    def __repr__(self):
        return (
            'Wave Function with '
            f'(Amplitude={self.amplitude}; '
            f'Gain={self.gain}; '
            f'Frequency={self.frequency}; '
            f'Lacunarity={self.lacunarity})'
        )


"""     -----------------------------------------------
        Wrappers for unifying different noise libraries
"""


class NoiseLibWrapper(metaclass=ABCMeta):
    """Abstract base class of a given wrapper with a factory function to get an instance
    """

    def __init__(self, seed=None):
        self.seed = seed or 0
        self.callmap = {
            2: self.eval2d,
            3: self.eval3d
        }

    @staticmethod
    def init_2d_engine(libname, seed=0):
        if libname == 'opensimplex':
            return OpenSimplexWrapper(seed)
        # elif engine == 'pynoise':
        #     return perlin.SimplexNoise()
        else:
            raise ValueError('Invalid option for noise library.')

    @abstractmethod
    def eval2d(self, x, y):
        pass

    @abstractmethod
    def eval3d(self, x, y, z):
        pass

    def eval4d(self, x, y, z, w):
        raise NotImplementedError


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
