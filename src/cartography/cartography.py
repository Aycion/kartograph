import copy

from src.math.noise import FBMFunction
from configuration import *
from functools import *


class WorldMap:

    def __new__(cls, mapdata, params=None):
        cls.params = params if params and isinstance(params, WorldParameters) else WorldParameters(CONFIG)
        return super().__new__()

    def __init__(self, mapdata, params):
        self.mapdata = mapdata
        self.params = params

    @classmethod
    def create(cls, engine, params=None):
        params = params or engine.params

        map = engine(params)
        return WorldMap(map, params)


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
        self.engine = {}
        self.space = {}
        self.accumulator = {}
        self._cfg_carbon = copy.copy(dict_cfg)
        self.__dict__.update(dict_cfg)

        self.x = self.space.get('shape')[0]
        self.y = self.space.get('shape')[1]

        self.controller = FBMFunction(cfg=self._cfg_carbon, seed=self.engine.get('seed'), engine=self.engine.get('lib'))

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
    #
    # @property
    # def dims(self):
    #     return self._dims
    #
    # @dims.setter
    # def dims(self, value):
    #     self.x = value[0]
    #     self.y = value[1]
    #     self._dims = value
    #

    @property
    def seed(self):
        return self.engine.get('seed')

    @seed.setter
    def seed(self, value):
        self.engine.update(seed=value)
