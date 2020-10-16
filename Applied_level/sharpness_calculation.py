### File description
# The file contains classical algorithms for sharpness calculation

### Packages import
from scipy import ndimage
from skimage import morphology
import numpy as np

def edge_sharpness(image):
    """
    Edge enhancement method
    """
    img_dilat = morphology.dilation(image)
    img_result = img_dilat - image
    return ndimage.sum(img_result)

def variance_sharpness(image):
    """
    Variance-based method
    """
    return ndimage.variance(image)

def variance_normal_sharpness(image):
    """
    Variance-based method with normalization
    """
    H, W = image.shape
    int_mean = ndimage.mean(image) 
    return (ndimage.variance(image)/(H*W*int_mean))