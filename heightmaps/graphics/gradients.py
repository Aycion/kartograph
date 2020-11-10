from typing import Callable

import numpy as np
import math

from heightmaps.graphics import DEFAULT_RES


def square_gradient_eval(coord, centroid, grade):
    center_distance = tuple(abs(coord[i] - centroid[i]) for i in range(len(coord)))
    pos = int(np.argmax(center_distance))
    return grade[pos] * center_distance[pos]


def circular_gradient_eval(dimensions, centroid, grade):
    grade = grade[0]
    position = math.sqrt(sum((dimensions[i] - centroid[i]) ** 2 for i in range(len(dimensions))))
    return grade * position


def subtract_gradient(alpha_map, gradient, limit=255):
    """Subtract `gradient` from `alpha`, given they have the
    same dimensions. Subtracts elements in `gradient`
     from corresponding elements in `alpha_map`.
    Args:
    :param alpha_map:
    :param gradient:
    :param limit:

    :return:

    """
    if len(alpha_map) != len(gradient) or len(alpha_map[0]) != len(gradient[0]):
        raise ValueError('Gradient and alpha channel must have same dimensions')
    bx, by = len(alpha_map), len(alpha_map[0])
    output = [[
        max(0, min(limit, alpha_map[x][y] - gradient[x][y]))
        for y in range(by)] for x in range(bx)
    ]

    return output


def gen_radial_gradient(
        rx=DEFAULT_RES,
        ry=None,
        centroid_x=int(DEFAULT_RES / 2),
        centroid_y=None,
        val_range=255,
        value_fn: Callable[[tuple, tuple, tuple], int] = square_gradient_eval,
        inner_padding=0,
        outer_padding=0
):
    """

    Args:
        rx (int): The size of the image on the x-axis
        ry (int): The size of the image along the y-axis. If not provided,
            this will default to <code>rx</code>
        centroid_x (int): The x-offset of the center.
        centroid_y (int): The y-offset of the center. If not provided,
            this will default to <code>centroid_x</code>.
        val_range (np.uint8): The range of allowable values for the graph. Defaults
            to `255` for the maximum channel value of a pixel with 8-bit color channels.
        value_fn (typing.Callable): The function to evaluate the gradient value
            at coordinates (x, y)
        inner_padding (int): The radius of the inner area in which the calculated value is
            equal to the value at the center. With a 0, only the centermost pixel
            (if `resolution` is odd) corresponds to that value.
        outer_padding (int):
    Returns:

    """

    ry = ry or rx
    centerpoint = centroid_x, centroid_y or centroid_x
    gradient = val_range / centroid_x, val_range / centroid_y
    """float: The gradient of the function; applying to a coordinate
     yields the height measured in the unit corresponding to `val_range`.
    """

    return [
        [np.uint8(value_fn((x, y), centerpoint, gradient))
         for x in range(rx)] for y in range(ry)
    ]


class Gradient:
    def __init__(self, dimensions, centroid=None, gen_fn=square_gradient_eval):
        """

        Args:
            dimensions (tuple[int]):
            gen_fn (typing.Callable):
        """
        self.dimensions = dimensions
        self.centroid = centroid or (int(d / 2) for d in dimensions)
