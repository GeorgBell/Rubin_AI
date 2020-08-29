# -*- coding: utf-8 -*-
"""
Created on Sat Mar  3 21:06:28 2018

@author: Georg
"""

from scipy import ndimage
import numpy as np

def Variance(image):
    return ndimage.variance(image)

def Variance_normal(image):
    H, W = image.shape
    int_mean = ndimage.mean(image)
    F2 = (ndimage.variance(image)/(H*W*int_mean))
    return F2