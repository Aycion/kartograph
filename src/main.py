import random

from generator.cartography.cartography import WorldMap
from generator.planetology.factory_core import WorldFactory
from generator.cartography.climatology import MoistureMap
from src.renderer import *
from src.configuration import *

import logging


def make_dataset(params=None, maptype=WorldMap, seed=None, name=None):
    params = params or get_root_context()
    if isinstance(seed, str) and seed == 'random':
        seed = random.getrandbits(64)
        params.seed = seed

    if isinstance(name, str):
        params.name = name

    worldgen = WorldFactory.from_params(params)
    return worldgen(maptype, params)

def app(config=None):
    """

    :param dict config:
    :return:
    :rtype:
    """
    # golden = (1 + math.sqrt(5)) / 2
    config = config or CONFIG.copy()
    topoparams = GlobalParameters(config)
    biomeparams = GlobalParameters(config)
    biomeparams.octaves = 2
    # biomeparams.seed = 23452345
    # topoparams.controller.get('wave').update(lacunarity=math.pi)

    # worldgen = WorldFactory(cfg_dict=config)

    topo = make_dataset(topoparams, maptype=WorldMap, name='topo', seed='random')
    biome = make_dataset(biomeparams, maptype=MoistureMap, name='biomes', seed='random')

    # with Pool(2) as pool:
    #     map_results = [pool.apply_async(worldgen.__call__, (canv, ), {'params': par}) for canv, par in [
    #         (WorldMap, topoparams), (MoistureMap, biomeparams)]]
    #     maps = [res.get() for res in map_results]
    # maps = [worldgen(canv, params=par) for canv, par in [(WorldMap, topoparams), (MoistureMap, biomeparams)]]
    # topo, biome = maps

    return topo, biome


def main():
    logging.basicConfig(level=logging.INFO)
    cfg = CONFIG.copy()
    topo, biome = app(cfg)
    worldmap = WorldFactory.rescale(topo() + biome())

    # plot_with_colors(worldmap)
    # plot_with_colors(biome(), 'Blues_r')

    craw = heightmap_to_image(WorldFactory.rescale(topo(), 0, 255))
    cworld = heightmap_to_color_img(worldmap)
    ctopo = heightmap_to_color_img(topo())
    cbiome = heightmap_to_color_img(biome(), colormap="Blues")
    # display_image(hmap_im_color)
    save_image(craw, name='raw.png', folder='raw')
    save_image(cworld, name="compound.png")
    save_image(ctopo, name="topo.png", folder='topo')
    save_image(cbiome, name="biome.png", folder='biome')


if __name__ == '__main__':
    main()
