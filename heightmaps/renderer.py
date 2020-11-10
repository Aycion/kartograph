from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from heightmaps.graphics.coloring import get_cmap


def heightmap_to_image(heightmap, save=False, identifier=None):
    img = Image.fromarray(heightmap, mode='L')
    if save:
        save_image(img)
    return img


def heightmap_to_color_img(heightmap, colormap=None):
    cmap = colormap or get_cmap()
    colorized = cmap(heightmap)
    img = Image.fromarray(
        (colorized[:, :, :3] * 255).astype(np.uint8)
    )
    return img
    # palette = ImagePalette(mode="RGB")


def save_image(im, name=None, folder=None):
    folder = folder or Path('./images')
    if name:
        target = (folder / name).absolute()
    else:
        target = (folder / 'tests')
        target /= f'hmap{len(list(target.iterdir()))}.png'
    target.parent.mkdir(parents=True, exist_ok=True)
    im.save(target.as_posix())


def display_image(im):
    im.show()


def plot_heightmap_np(heightmap):
    plt.imshow(heightmap, cmap='gray', vmin=0, vmax=255, interpolation='none')
    plt.show()


def plot_with_colors(heightmap, colormap=None):
    cmap = colormap or get_cmap()

    plt.imshow(heightmap, interpolation='none', cmap=cmap)
    plt.show()
