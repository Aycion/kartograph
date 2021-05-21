import numpy as np

from planetology.engine import WorldEngine


class MoistureMap(WorldEngine):

    def create(self, layers=None):
        moist = super().create(layers)
        u = moist.flatten().mean()
        sd = moist.flatten().std()

        moist[moist < u-sd] = np.nan
        return moist

    def gen_moisture_map(self):
        pass
