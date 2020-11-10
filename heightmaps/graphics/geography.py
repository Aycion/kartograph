from heightmaps.math.noise import Condenser
import numpy as np
import timeit


class TerrainGen:
    def __init__(self, dims, engine='opensim'):
        if not isinstance(dims, tuple):
            raise TypeError(f'Shape must be a tuple of ints, got: {dims}')
        x, *y = dims
        y = y[0] if y else x
        self.rowmax, self.colmax = y, x

        self.condenser = Condenser(engine=engine)
        """The Condenser
        """

    def gen_terrain(self, num_passes=1):
        terray = np.empty((num_passes, self.rowmax, self.colmax), dtype=np.float64)
        """3d-array to store all the terrain values. 
        Layers of NxM with depth K, where 
        N=``rowmax``, M=``colmax``, and K=``passes``.
        """
        for layer in range(num_passes):
            start = timeit.default_timer()
            self.condenser.map_noise_layer(imarray=terray[layer, :, :], octave=layer)
            end = timeit.default_timer()
            print(f'Time: {end - start}\n')
        print(self.condenser.cum_amp)
        terrain = self.norm_terrain(terray.sum(axis=0))
        """Sum the corresponding elements of each layer
        and normalize the result to [0,1].
        """
        return terrain

    def config_noise(self, **kwargs):
        self.condenser.configure_wavefn(**kwargs)

    def norm_terrain(self, tarray, factor=1):
        """

        :param np.ndarray tarray:
        :param int factor:
        :return:
        """
        maxi, mini = np.max(tarray), np.min(tarray)
        print(maxi, mini)
        tarray = ((tarray - mini) / (maxi - mini)) * factor
        return tarray
