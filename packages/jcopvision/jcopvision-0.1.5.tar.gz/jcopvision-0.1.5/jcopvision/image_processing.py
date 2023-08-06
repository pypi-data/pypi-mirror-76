import numpy as np


def clipping_mask(source, mask, background):
    if source.dtype == np.uint8:
        source = source / 255

    if mask.dtype == np.uint8:
        mask = mask / 255

    if background.dtype == np.uint8:
        background = background / 255

    result = mask * source + (1 - mask) * background
    return result
