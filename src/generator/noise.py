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

from configuration import get_root_context
from configuration.parameters import GlobalParameters
from configuration import *


class ContextFunction:
    """Defines a context for a wave function
    """
    def __init__(self, wavefn=None, params=None):
        params = params or get_root_context()
        self.waveparams = params.default_controller.get('wave')


class FBMFunction:

    def __init__(self, wavefn, lib=None, seed=None):
        """

        """

        self.wavefn = wavefn
        try:
            self.engine = NoiseLibWrapper.noise_lib_factory(libname=lib, seed=seed)
        except KeyError as e:
            raise ValueError('Invalid option for noise factory') from e

    def __new__(cls, *args, **kwargs):
        """Modify the class with a vectorized version of the fractal noise function.

        """
        inst = super().__new__(cls)
        inst.fbm3d = np.vectorize(inst.fbm_scalar)

        return inst

    @classmethod
    def from_params(cls, params, wavefn=None):
        """

        :param WaveFunction wavefn:
        :param GlobalParameters params:
        :return:
        """
        wavefn = wavefn or WaveFunction.from_params(params)
        return cls(wavefn=wavefn, **params.engine)

    def fbm_scalar(self, X, Y, Z):
        """Calculate and return the 2D-noise value at (X,Y), with periodic
        fuction parameters scaled to
        scaled to Z with their respective step functions

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

        self.amplitude = amplitude      # A
        self.frequency = frequency      # v
        self.gain = gain                # G
        self.lacunarity = lacunarity    # L

    @classmethod
    def from_params(cls, params):
        wave = params.controller.get('wave')
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
    def noise_lib_factory(libname, seed=0):
        if libname == 'opensimplex':
            return OpenSimplexWrapper(seed)
        # elif factory == 'pynoise':
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
