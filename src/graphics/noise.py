import numpy as np
from opensimplex import OpenSimplex

noise_engine = OpenSimplex()
simplex2d = noise_engine.noise2d


def noise_to_pixel(x, y, base_freq=0.01, octaves=16, persistence=0.5, valrange=(0, 255)):
    """

    Args:
        x:
        y:
        base_freq (float):
        octaves (int):
        persistence (float):
        valrange (tuple[float]):

    Returns:
        np.uint8: The brownian noise value for (x, y)

    """
    noise_low, noise_high = (-1, 1)
    """Value range for each channel (inclusive)"""

    noise = brownian(
        x, y,
        freq=base_freq, octaves=octaves, gain=persistence
    )
    """Generate the noise in range [-1,1]"""

    # adjnoise = noise - noise_low
    # slope = (high - low) / (noise_high - noise_low)
    # pixelval = (adjnoise * slope) + low
    # """Initially in [-1, 1], needs shifting to [0, 255]"""
    return np.uint8(noise)


def brownian(
        x, y, octaves=16,
        freq=0.01, amp=1.0, gain=0.5):
    """

    Args:
        x (float):
        y (float):
        octaves (int):
        freq (float):
        amp (float): The amplitude of the wave function in the first octave
        gain (float): The degree to which the amplitude diminishes
            in each successive octave. Also called persistence

    Returns:

    """

    noise_sum = 0.0
    """float: accumulator for the noise"""
    amp_sum = 0.0
    """float: accumulator for the amplitudes"""
    for octv in range(octaves):
        """Sum the noise functions over each octave"""

        scaledx, scaledy = x * freq, y * freq
        """Scale the position to the frequency"""
        noiseval = simplex2d(scaledx, scaledy) * amp
        """Simplex noise comes out as a float on [-1,1]"""

        noise_sum += noiseval
        amp_sum += amp
        amp *= gain
        freq *= 2
        """Using lacunarity of 2, meaning the frequency doubles 
        for every successive octave
        """

    # noise /= amp_sum
    return noise_sum
