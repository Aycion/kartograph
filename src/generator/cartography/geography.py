from generator.cartography.cartography import WorldMap


class TerrainMap(WorldMap):

    layer_boundaries = {
        'floor': 0,
        'sea-level': 60
    }
    def gen_terrain_map(self):
        pass