import copy


class GlobalParameters(object):
    """An object that provides access to a set of parameters defining a
    context for an entire operation.
    """
    def __init__(self, dict_cfg):
        self.engine = {}
        """dict: context for the wrapper on the underlying noise library"""
        self.output = {}
        """dict: context for the output array: rank, aspect ratio, and shape"""
        self.controller = {}
        """dict: context for the default_controller generating output"""
        self._cfg_carbon = copy.copy(dict_cfg)
        """dict: deep copy of the original configuration"""
        self.__dict__.update({d: copy.copy(v) for d,v in dict_cfg.items()})

        self.x = self.output.get('shape')[0]
        self.y = self.output.get('shape')[1]

    @property
    def name(self):
        return self.output.get('name')

    @name.setter
    def name(self, value):
        self.output.update(name=value)

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
    def shape(self):
        return self.output.get('shape')

    @property
    def octaves(self):
        return self.controller.get('octaves')

    @octaves.setter
    def octaves(self, val):
        if isinstance(val, int):
            self.controller.update(octaves=val)
    @property
    def seed(self):
        return self.engine.get('seed')

    @seed.setter
    def seed(self, value):
        self.engine.update(seed=value)
