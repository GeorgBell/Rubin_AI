# -*- coding: utf-8 -*-
"""
Created on Fri Mar  9 21:14:37 2018

@author: Georg
"""

from scipy import ndimage
from skimage import morphology
import numpy as np

def Edge(image):
    img_dilat = morphology.dilation(image)
    img_result = img_dilat - image
    F2 = ndimage.sum(img_result)
    return F2