import cv2
import numpy as np
from skimage.measure import label, regionprops
import matplotlib.colors as mc


def get_color(rgb):
    closest_color = "None"
    closest_range = 196609
    for name in mc.CSS4_COLORS:
        color = mc.to_rgb(name)
        diff = abs(rgb[0] - color[2]) ** 2 + abs(rgb[1] - color[1]) ** 2 + abs(rgb[2] - color[0]) ** 2
        if (diff < closest_range):
            closest_range = diff
            closest_color = name
    return closest_color

def add(d, npar):
    t = get_color(tuple((npar / 255).tolist()))
    if t in d:
        d[t] += 1
    else:
        d[t] = 1


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
