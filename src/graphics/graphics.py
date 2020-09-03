from src.graphics.noise import noise_to_pixel
from src.renderer import *
from src.graphics import DEFAULT_RES
import numpy as np


def gen_heightmap(rx=DEFAULT_RES, ry=None):
    """

    Args:
        rx (int): x-dimension of the heightmap
        ry (int): y-dimension of the heightmap–
            if this is not provided, <code>res_x</code> is
            used for both dimensions.

    Returns:
        np.ndarray:

    """
    ry = ry or rx

    noisemap = np.zeros((rx, ry), dtype=np.uint8)
    """Initialize the map as a 2D array of zeros with dimensions (rx, ry)"""
    vals = list()
    for x in range(rx):

        for y in range(ry):
            noisemap[x][y] = noise_to_pixel(x, y)
            """Calculate the noise value with Fractal Brownian 
                Motion and map the value to [0,256).
            """
            vals.append(noisemap[x][y])

    _ = plt.hist(np.asarray(vals), bins=50)
    plt.show()
    print(max(vals), min(vals))
    return noisemap


def print_range(heightmap):
    vals = heightmap.flatten()
    print(f'Values between {max(vals)} and {min(vals)}')


# square_gradient = np.asarray(gen_edge_gradient())

hmap = gen_heightmap()
# hmap_subtracted = np.asarray(subtract_gradient(hmap, square_gradient))
display_image(heightmap_to_image(hmap))
plot_heightmap_np(hmap)
