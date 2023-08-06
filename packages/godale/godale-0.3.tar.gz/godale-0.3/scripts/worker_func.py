import numpy as np
import rasterio


# main class holding much data in memory
class SomeDataClass():

    def __init__(self):
        # creates a ~76MB array
        self.data = np.arange(10000000, dtype=np.float)


def worker_func(a, b, data=None):
    with rasterio.open("cleantopo_br.tif", "r") as src:
        a = src.read()
    try:
        data.any()
    except:
        pass
    # cpu intensive
    987239478234879 ** 5872
    return a * b
