import numpy as np


def pdf(x, mu, sig):
    return (1 / (sig * np.sqrt(2 * np.pi))) * np.exp(-np.exp2((x - mu) / sig)/2)
