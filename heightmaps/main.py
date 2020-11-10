from heightmaps import DEFAULT_RES
from heightmaps.graphics.geography import TerrainGen
from heightmaps.renderer import *

import logging


def main():
    logging.basicConfig(level=logging.DEBUG)

    res = (DEFAULT_RES, DEFAULT_RES)
    tgen = TerrainGen(res, engine='opensim')
    tgen.config_noise(freq=0.005)
    hmap = tgen.gen_terrain(num_passes=8)

    # square_gradient = np.asarray(gen_edge_gradient())
    # hmap_subtracted = np.asarray(subtract_gradient(hmap, square_gradient))

    # display_image(heightmap_to_image(hmap, save=True))
    plot_with_colors(hmap)
    hmap_im_color = heightmap_to_color_img(hmap)
    display_image(hmap_im_color)
    save_image(hmap_im_color)
    # plot_heightmap_np(hmap)


if __name__ == '__main__':
    main()
