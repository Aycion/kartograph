from numba import jit, int32, vectorize, Callable
import numpy as np
from opensimplex import OpenSimplex
from timeit import default_timer as timer


def func1(a):
    for i in range(10000000):
        a[i] += 1


@jit(nopython=True)
def func2(a):
    a += 1
    return a


@vectorize
def func3(a):
    a += 1
    return a


@vectorize([int32(int32,int32,Callable)])
def noisetest(x, y, noisefn):
    return noisefn(x,y)


if __name__ == "__main__":
    noise = OpenSimplex().noise2d
    # a = np.ones(n, dtype=np.float64)
    # b = np.ones(n, dtype=np.float32)
    # c = np.ones(n, dtype=np.float32)
    a = np.arange(0, 256, 1)
    b = np.arange(0, 256, 1)

    start = timer()
    c = noisetest(a, b, noise)
    print(c)
    print("jit:", timer() - start)


