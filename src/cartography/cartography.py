from src.math.noise import FractalNoiseController
from configuration import *
from functools import *


class WorldMap:

    def __init__(self, mapdata, params=None):
        if not isinstance(self.params, WorldParameters):
            raise AttributeError

        self.mapdata = mapdata
        self.params = params

    @classmethod
    def create_map(cls, gen, params=None):
        layers = None
        params = params or CONFIG

        map = gen(params)
        return cls.__init__(map)


class EnginePipe:
    def __init__(self, dataspace, operator=None):
        self.dataspace = dataspace
        self.input = list()
        self.output = list()
        self.operator = [*operator] if operator else [lambda x: x, ]

    def __call__(self, *args, **kwargs):
        pass


class WorldParameters(object):
    def __init__(self, dict_cfg):
        self.cfg = dict_cfg
        self.enginename = self.cfg.get('engine').get('lib')
        self.seed = self.cfg.get('engine').get('seed')
        self.dims = self.cfg.get('renderer', {}).get('space', {}).get('shape')

        self.controller = FractalNoiseController(cfg=self.cfg, seed=self.seed, engine=self.enginename)

    @property
    def enginename(self):
        return self.__enginename

    @enginename.setter
    def enginename(self, value):
        self.__enginename = value

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    @property
    def dims(self):
        return self._dims

    @dims.setter
    def dims(self, value):
        self.x = value[0]
        self.y = value[1]
        self._dims = value

    @property
    def seed(self):
        return self._seed

    @seed.setter
    def seed(self, value):
        self._seed = value
