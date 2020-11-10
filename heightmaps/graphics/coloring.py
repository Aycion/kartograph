import matplotlib.colors


def get_default_colors(norm=False):
    scale = 1.0 / 255.0 if norm else 1.0
    colors = {
        # Labeled tuples of (height, r, g, b)
        'min': (0, 45, 15, 128),
        'ocean': (100, 45, 15, 128),
        'coast': (100, 194, 178, 128),
        'grass': (120, 65, 152, 10),
        'stone': (200, 136, 140, 141),
        'max':   (255, 255, 255, 255)
    }
    return {
        k: tuple(x * scale for x in y)
        for k, y in colors.items()
    }


def get_default_cdict():
    colors = get_default_colors(norm=True)
    outp = {
        'red': [],
        'green': [],
        'blue': []
    }

    for k, (h, r, g, b) in colors.items():
        outp['red'].append((h, r, r))
        outp['green'].append((h, g, g))
        outp['blue'].append((h, b, b))
    return outp


def get_cmap(cdict=None):
    cdict = cdict or get_default_cdict()
    return matplotlib.colors.LinearSegmentedColormap('terrain_cmap', cdict, 256)



class MapColoring:
    def __init__(self, colors=None):
        self.colors = colors or get_default_colors()
        self.labels = {*self.colors.keys()}

    def gaussian(self, c1, c2):
        raise NotImplementedError

    def get_gradient_form(self):
        raise NotImplementedError
