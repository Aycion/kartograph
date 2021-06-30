import numpy as np


class WorldMap:

    def __new__(cls, canvas=None, params=None):
        return super().__new__(cls)

    def __init__(self, canvas=None, params=None):
        self.canvas = canvas
        self.params = params

    def __call__(self):
        """

        :param planetology.factory_core.WorldFactory factory:
        :return:
        """
        return self.canvas

    @classmethod
    def from_canvas(cls, canvas, params):
        """
        :param numpy.ndarray canvas:
        :param GlobalParameters params:
        :return:
        """
        return cls(canvas, params)

    def combine_with_layer(self, map_layer, weights=None):
        if weights is None:
            weights = np.ones_like(map_layer)

    def __add__(self, other):
        summed = self.canvas + other.canvas
        return WorldMap(canvas=summed, params=self.params)

    def __radd__(self, other):
        summed = other.canvas + self.canvas
        return WorldMap(canvas=summed, params=other.params)


class EnginePipe:
    def __init__(self, dataspace, operator=None):
        self.dataspace = dataspace
        self.input = list()
        self.output = list()
        self.operator = [*operator] if operator else [lambda x: x, ]

    def __call__(self, *args, **kwargs):
        pass
