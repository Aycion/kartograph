from planetology.engine import WorldEngine


class TerrainMap(WorldEngine):

    def __init__(self, xbound, ybound, engine='opensimplex'):
        super().__init__((xbound, ybound), engine)

