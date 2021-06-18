from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from iointerface import *
from src.graphics.coloring import get_cmap


class Renderer:
    def __init__(self, build_target=None):
        """

        :param Path build_target:
        """
        if build_target:
            self.build_target = build_target.resolve()
        else:
            self.build_target = DEFAULT_IMAGE_DIR

    def save_image(self, im, name=None, folder=None):
        """

        :param Image im:
        :param name:
        :param folder:
        :return:
        """
        folder = folder or self.build_target
        if not name:
            name = 'hmap.png'
            folder /= 'tests'

        target = enumerate_basename(folder, name)
        target.parent.mkdir(parents=True, exist_ok=True)
        im.save(target.as_posix())

    def heightmap_to_image(self, heightmap):
        img = Image.fromarray(heightmap.astype(np.uint8), mode='L')
        return img

    def heightmap_to_color_img(self, heightmap, colormap=None):
        if colormap and isinstance(colormap, str):
            cmap = plt.get_cmap(colormap)
        else:
            cmap = colormap or get_cmap()
        colorized = cmap(heightmap)
        img = Image.fromarray(
            (colorized[:, :, :3] * 255).astype(np.uint8)
        )
        return img

    def display_image(self, im):
        im.show()

    def plot_heightmap(self, heightmap, colormap=None):
        plt.imshow(heightmap, cmap=colormap or 'gray', vmin=0, vmax=255, interpolation='none')
        plt.show()

    def plot_with_colors(self, heightmap, colormap=None):
        cmap = colormap or get_cmap()
        plt.imshow(heightmap, interpolation='none', cmap=cmap)
        plt.show()


default_render = Renderer()


def heightmap_to_image(heightmap):
    return default_render.heightmap_to_image(heightmap)


def heightmap_to_color_img(heightmap, colormap=None):
    return default_render.heightmap_to_color_img(heightmap, colormap)


def save_image(im, name=None, folder=None):
    default_render.save_image(im, name, folder)


def display_image(im):
    default_render.display_image(im)


def plot_heightmap(heightmap, colormap=None):
    default_render.plot_heightmap(heightmap, colormap=colormap)


def plot_with_colors(heightmap, colormap=None):
    default_render.plot_with_colors(heightmap, colormap)
