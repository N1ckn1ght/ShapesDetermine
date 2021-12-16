import cv2
import numpy as np
from skimage.measure import label, regionprops
from skimage import color

def add(d, npar):
    t = tuple(npar.tolist())
    if t in d:
        d[t] += 1
    else:
        d[t] = 1


balls = {}
rects = {}

source = cv2.imread("balls_and_rects.png")
for region in regionprops(label(source)):
    y, x, _ = region.centroid
    y = int(y)
    x = int(x)
    if np.all(region.image):
        add(rects, source[y, x])
    else:
        add(balls, source[y, x])

f = open("output.txt", "w")
f.write("balls counted: " + str(len(balls)) + "\n")
for color in balls:
    f.write("\t" + str(color) + ": " + str(balls[color]) + "\n")
f.write("rects counted: " + str(len(rects)) + "\n")
for color in rects:
    f.write("\t" + str(color) + ": " + str(rects[color]) + "\n")
f.close()
