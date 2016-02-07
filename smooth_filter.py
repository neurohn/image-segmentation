from scipy.signal import convolve2d
from numpy import *

def gaussian_grid(sigma, alpha=4):
    sig = max(sigma, 0.01)
    length = int(math.ceil(sig * alpha)) + 1 # min value of length = 2
    m = length / 2
    n = m + 1
    # Clever way to do a nested for loop
    x, y = mgrid[-m:n,-m:n]
    g = exp(m ** 2) * exp(-0.5 * (x**2 + y**2))
    return g / g.sum()

def filter_image(image, mask):
    layer = asarray(image).astype('float')
    layer = convolve2d(layer, mask, mode='same')
    return layer
