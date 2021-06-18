import argparse

from multiprocessing import Pool

from cartography.cartography import WorldMap
from planetology.factory_core import WorldFactory
from src.cartography.climatology import MoistureMap
from src.renderer import *
from src.configuration import *

import logging


def app(config=None):
    """

    :param dict config:
    :return:
    :rtype:
    """
    config = config or CONFIG.copy()
    topoparams = WorldParameters(config)
    biomeparams = WorldParameters(config)
    biomeparams.octaves = 2
    biomeparams.seed = 23452345

    worldgen = WorldFactory(cfg_dict=config)

    # with Pool(2) as pool:
    #     map_results = [pool.apply_async(worldgen.__call__, (canv, ), {'params': par}) for canv, par in [
    #         (WorldMap, topoparams), (MoistureMap, biomeparams)]]
    #     maps = [res.get() for res in map_results]
    maps = [worldgen(canv, params=par) for canv, par in [(WorldMap, topoparams), (MoistureMap, biomeparams)]]
    topo, biome = maps

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
