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
    with Pool(2) as pool:
        map_results = [pool.apply_async(f.create, (passes, )) for f in [topogen, climagen]]
        maps = [res.get() for res in map_results]

    topo, biome = maps

    return WorldEngine.rescale(topo + biome)


def main():
    logging.basicConfig(level=logging.INFO)
    cfg = CONFIG.copy()
    res = (cfg.get('renderer').get('resolution'),)*2
    worldmap = app(res)

    plot_with_colors(worldmap)
    # plot_with_colors(biomes, 'Blues')
    hmap_im_color = heightmap_to_color_img(worldmap)
    # display_image(hmap_im_color)
    save_image(hmap_im_color)


if __name__ == '__main__':
    main()
