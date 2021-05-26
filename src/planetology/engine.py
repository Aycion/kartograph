import timeit

import numpy as np

from cartography.cartography import WorldParameters
from configuration import CONFIG
from src.math.noise import FBMFunction, WaveFunction


class WorldFactory:
    def __init__(self, cfg=None):
        self.params = WorldParameters(cfg or CONFIG)

        # TODO - extract the following block to a separate configuration validator
        # if not isinstance(dims, tuple):
        #     raise TypeError(f'Shape must be a tuple of ints, got: {dims}')

        wavefn = WaveFunction.from_cfg(cfg)
        self.controller = FBMFunction(wavefn=wavefn, **cfg.engine)
        """The controller provides an interface for accumulating noise on a 2D grid.
        """

    def __call__(self, params=None):
        params = params or self.params
        layers = params.accumulator.get('octaves')

        return self.integrate_noise(layers=layers)

    def integrate_noise(self, layers):
        """Generate one or more 2D arrays of noise evaluated
            at a base frequency and zero or more consecutive frequencies
            calculated as a multiple of the base.

            Create a 3D array with shape (num_passes, self.rowmax, self.colmax).
            The latter two dimensions are the shape of the output array (and any
            image rendered at scale), while the former is the number of discrete
            layers at which to evalute the noise.

        :param int layers: The number of layers to generate in the fractal
            noise calculation.

        :param int seed:

        :return:
        :rtype: np.ndarray
        """
        cmat = (
            np.linspace(0, self.params.y - 1, self.params.y),
            np.linspace(0, self.params.x - 1, self.params.x),
            np.linspace(0, layers - 1, layers)
        )
        px, py, pz = np.meshgrid(*cmat, indexing='xy')
        """Get the coordinate grids describing our 3D matrix of values"""
        start = timeit.default_timer()
        layers = self.controller.fbm_layer2d(px, py, pz)
        end = timeit.default_timer()
        print(f'Time: {end - start}\n')
        procedural_noise = layers.sum(axis=2)
        procedural_noise = self.rescale(procedural_noise)
        """Sum the corresponding elements of each layer and normalize the result to [0,1].
        """
        return procedural_noise


    @staticmethod
    def rescale(array, newmin=0, newmax=1):
        """Rescale an array from its current range (given by its
        minimum and maximum values) to a new range, by default to [0,1]

        :param np.ndarray array: The array of values to rescale
        :param float newmin: The lower bound for the new scale
        :param float newmax: The upper bound for the new scale
        :return:
        """
        oldmin, oldmax = np.min(array), np.max(array)
        array = ((array - oldmin) / (oldmax - oldmin))
        return (array * (newmax - newmin)) + newmin


class EngineParameters(object):
    def __init__(self, **kwargs):
        self.cfg = kwargs
        self.enginename = self.cfg.get('engine').get('lib')
