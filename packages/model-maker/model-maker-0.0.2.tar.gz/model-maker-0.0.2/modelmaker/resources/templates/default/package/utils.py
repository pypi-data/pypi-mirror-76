import cv2
import numpy as np
import random
import math

def normalize(x, lower, upper):
    _max = x.max()
    _min = x.min()
    factor =  ((upper - lower) + 1e-12)/ ((_max - _min) + 1e-12)
    return (x - _min) * factor + lower

def rescale2d(x, shape):
    return cv2.resize(x.astype('float'), shape)

def draw_square(ndarr, center, length):
    height, width = ndarr.shape
    xmin = int(center[0] - length/2)
    xmin = 0 if xmin < 0 else xmin
    xmax = int(center[0] + length/2)
    ymin = int(center[1] - length/2)
    ymin = 0 if ymin < 0 else ymin
    ymax = int(center[1] + length/2)
    ndarr[xmin:xmax, ymin:ymax] = 1
    return ndarr

def draw_circle(ndarr, center, r=50, n=100):
    contours = np.array([[
        [
            math.cos(2*math.pi/n*x)*r + center[0],
            math.sin(2*math.pi/n*x)*r + center[1]
        ] for x in range(0,n+1)
    ]]).astype('int32')
    return cv2.fillPoly(ndarr, contours, color=1)

def generate_square(shape):
    im = np.zeros(shape)
    length = random.randint(int(shape[0]/5), int(shape[0]/3))
    center = (random.randint(0, shape[0]), random.randint(0, shape[1]))
    return draw_square(im, center, length)

def generate_circle(shape):
    im = np.zeros(shape)
    center = (random.randint(0, shape[0]), random.randint(0, shape[1]))
    radius = random.randint(int(shape[0]/8), int(shape[0]/5))
    return draw_circle(im, center, r=radius)