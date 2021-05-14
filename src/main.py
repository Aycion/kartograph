import argparse

from multiprocessing import Pool

from planetology.engine import WorldEngine
from src.cartography.climatology import MoistureMap
from src.renderer import *
from src.configuration import *

import logging


def app(res):
    """

    :param ndarray res:
    :param dict options:
    :return:
    :rtype:
    """
    cfg = CONFIG.copy()

    topogen = WorldEngine(res, engine='opensimplex', cfg=cfg)
    climagen = MoistureMap(res, engine='opensimplex', cfg=cfg, seed=23452345)

    passes = cfg.get('accumulator')['octaves']
    # topogen.config_noise(**(cfg.get('wave', cfg.get('accumulator')['wave'])))
    # topo = topogen.create(passes=cfg.get('accumulator')['octaves'])
    # biome = climagen.create(passes=cfg.get('accumulator')['octaves'])
    # return topogen.create(passes)
    with Pool(2) as pool:
        map_results = [pool.apply_async(f.create, (passes, )) for f in [topogen, climagen]]
        maps = [res.get() for res in map_results]

    topo, biome = maps

    return topo, biome


def main():
    logging.basicConfig(level=logging.INFO)
    cfg = CONFIG.copy()
    res = (cfg.get('renderer').get('resolution'),)*2
    topo, biome = app(res)
    worldmap = WorldEngine.rescale(topo + biome)

    plot_with_colors(worldmap)
    # plot_with_colors(biomes, 'Blues')
    cworld = heightmap_to_color_img(worldmap)
    ctopo = heightmap_to_color_img(topo)
    cbiome = heightmap_to_color_img(biome, colormap="Blues")
    # display_image(hmap_im_color)
    save_image(cworld, name="compound.png")
    save_image(ctopo, name="topo.png")
    save_image(cbiome, name="biome.png")


if __name__ == '__main__':
    main()
