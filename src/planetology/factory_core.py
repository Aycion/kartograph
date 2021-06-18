import timeit

import numpy as np
from multiprocessing import Pool

# from contextlib import asynccontextmanager
from cartography.cartography import WorldMap
from configuration.parameters import WorldParameters
from configuration import CONFIG
from src.math.noise import FBMFunction, WaveFunction


class WorldFactory:
    def __init__(self, cfg_dict=None):
        self.default_params = WorldParameters(cfg_dict or CONFIG)

        # TODO - extract the following block to a separate configuration validator
        # if not isinstance(dims, tuple):
        #     raise TypeError(f'Shape must be a tuple of ints, got: {dims}')

        self.default_controller = self.make_fbm_tools(self.default_params)
        """The default_controller provides an interface for accumulating noise on a 2D grid.
        """

    @classmethod
    def from_params(cls, params):
        """

        :param WorldParameters params:
        :return:
        """
        inst = cls()
        inst.default_params = params

    class Illustrator:
        def __init__(self, tools):
            """
            
            :param FBMFunction tools:
            :param np.ndarray canvas_mesh:
            """
            self.tools = tools

        def __call__(self, *materials):
            """
            :param np.ndarray materials:
            :return:
            """
            start = timeit.default_timer()
            mx, my, mz = materials
            px, py = np.meshgrid(mx, my, indexing='xy')
            chunkcount = len(mz)

            with Pool(chunkcount) as pool:
                map_results = [pool.apply_async(self.do_fbm, (px, py, Z)) for Z in mz]
                maps = np.stack([res.get() for res in map_results], axis=0)

            end = timeit.default_timer()
            print(f'Time: {end - start}\n')

            # Finalize the output
            procedural_canvas = maps.sum(axis=0)
            procedural_canvas = WorldFactory.rescale(procedural_canvas)

            return procedural_canvas

        def do_fbm(self, *mesh):
            """Generate one or more 2D arrays of noise evaluated
                at a base frequency and zero or more consecutive frequencies
                calculated as a multiple of the base.

                Create a 3D array with shape (num_passes, self.rowmax, self.colmax).
                The latter two dimensions are the shape of the output array (and any
                image rendered at scale), while the former is the number of discrete
                layers at which to evalute the noise.

            :param FBMFunction tools:
            :param np.ndarray mesh:


            :return:
            :rtype: np.ndarray
            """

            layers = self.tools.fbm3d(*mesh)
            """Sum the corresponding elements of each layer and normalize the result to [0,1].
            """
            return layers

    def __call__(self, target_map: 'WorldMap', params=None):
        if params:
            controller = WorldFactory.make_fbm_tools(params)
        else:
            params = self.default_params
            controller = self.default_controller
        canvas = self.make_canvas(params)

        worker = WorldFactory.Illustrator(controller)
        return target_map.from_canvas(worker(*canvas), params)

    def assign_worker(self, target_map: 'WorldMap', params=None):
        params = params or self.default_params

    @staticmethod
    def make_fbm_tools(parameters):
        """

        :param parameters:
        :return:
        """
        wavefn = WaveFunction.from_params(parameters)
        return FBMFunction.from_params(params=parameters, wavefn=wavefn)

    def make_canvas(self, params=None):
        params = params or self.default_params
        xbound, ybound = params.space.get('shape')
        zbound = params.controller.get('octaves')

        # TODO test swapping x/y
        cmat = (
            np.linspace(0, ybound - 1, ybound),
            np.linspace(0, xbound - 1, xbound),
            np.linspace(0, zbound - 1, zbound)
        )

        return cmat

    def do_fbm(self, *mesh):
        """Generate one or more 2D arrays of noise evaluated
            at a base frequency and zero or more consecutive frequencies
            calculated as a multiple of the base.

            Create a 3D array with shape (num_passes, self.rowmax, self.colmax).
            The latter two dimensions are the shape of the output array (and any
            image rendered at scale), while the former is the number of discrete
            layers at which to evalute the noise.

        :param np.ndarray mesh:


        :return:
        :rtype: np.ndarray
        """
        layers = self.default_controller.fbm3d(*mesh)
        procedural_noise = layers.sum(axis=2)
        procedural_noise = self.rescale(procedural_noise)
        """Sum the corresponding elements of each layer and normalize the result to [0,1].
        """
        return procedural_noise

    def integrate_async(self, mesh):
        """

        :param np.ndarray mesh:
        :return:
        """

        for octv in mesh.shape[-1]:
            layer = mesh[:, :, octv]

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
        self.enginename = self.cfg.get('factory').get('lib')
