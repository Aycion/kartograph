from PIL import Image, ImagePalette
import matplotlib.pyplot as plt


def heightmap_to_image(heightmap, save=False):
    img = Image.fromarray(heightmap, mode='L')
    return img


def heightmap_to_color_img(heightmap):
    pal_array = []

    # palette = ImagePalette(mode="RGB")


def display_image(im):
    im.show()


def plot_heightmap_np(heightmap):
    plt.imshow(heightmap, cmap='gray', vmin=0, vmax=255, interpolation='none')
    plt.show()
