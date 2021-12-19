import cv2
import numpy as np
from skimage.measure import label, regionprops
from skimage.color import rgb2hsv

def add(d, npar):
    npar = rgb2hsv(npar)
    for i in range(len(npar)):
        npar[i] = int(npar[i] * 255)
    if npar[0] in d:
        d[npar[0]] += 1
    # precision workaround
    elif npar[0] - 1 in d:
        d[npar[0] - 1] += 1
    elif npar[0] + 1 in d:
        d[npar[0] + 1] += 1
    else:
        d[npar[0]] = 1


balls = {}
rects = {}

source = cv2.imread("balls_and_rects.png")
for region in regionprops(label(source))[::3]:
    y, x, _ = region.centroid
    y = int(y)
    x = int(x)
    if np.all(region.image):
        add(rects, source[y, x])
    else:
        add(balls, source[y, x])

f = open("output.txt", "w")
f.write("figures found: " + str(sum(balls.values()) + sum(rects.values())) + "\n")
f.write("balls counted: " + str(sum(balls.values())) + "\n")
for color in balls:
    f.write("\t" + str(color) + ": " + str(balls[color]) + "\n")
f.write("rects counted: " + str(sum(rects.values())) + "\n")
for color in rects:
    f.write("\t" + str(color) + ": " + str(rects[color]) + "\n")
f.close()