from PIL import Image
import matplotlib.pyplot as plt


def heightmap_to_image(heightmap, save=False):
    return Image.fromarray(heightmap, mode='L')


def display_image(im):
    im.show()


def plot_heightmap_np(heightmap):
    plt.imshow(heightmap, cmap='gray', vmin=0, vmax=255, interpolation='none')
    plt.show()
