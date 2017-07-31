from collections import namedtuple
from math import sqrt
import random
from PIL import Image
import os

COLORS = [
    [0, 0, 255],   #blue
    [0, 128, 255], #light blue
    [0, 255, 255], #cyan
    [0, 255, 128], #pale green
    [0, 255, 0],   #green
    [128, 255, 0], #yellow green
    [255, 255, 0], #yellow
    [255, 128, 0], #orange
    [255, 0, 0],   #red
    [255, 0, 128], #hot pink
    [255, 0, 255], #light pink
    [128, 0, 255], #purple
    ]

rtoh = lambda rgb: '#%s' % ''.join(('%02x' % p for p in rgb))

Point = namedtuple('Point', ('coords', 'n', 'ct'))
Cluster = namedtuple('Cluster', ('points', 'center', 'n'))

def get_points(img):
    points = []
    w, h = img.size
    for count, color in img.getcolors(w * h):
        points.append(Point(color, 3, count))
    return points
    

def euclidean(p1, p2):
    return sqrt(sum([
        (p1.coords[i] - p2.coords[i]) ** 2 for i in range(p1.n)
    ]))
    

def calculate_center(points, n):
    vals = [0.0 for i in range(n)]
    plen = 0
    for p in points:
        plen += p.ct
        for i in range(n):
            vals[i] += (p.coords[i] * p.ct)
    return Point([(v / plen) for v in vals], n, 1)
    

def kmeans(points, k, min_diff):
    clusters = [Cluster([p], p, p.n) for p in random.sample(points, k)]

    while 1:
        plists = [[] for i in range(k)]

        for p in points:
            smallest_distance = float('Inf')
            for i in range(k):
                distance = euclidean(p, clusters[i].center)
                if distance < smallest_distance:
                    smallest_distance = distance
                    idx = i
            plists[idx].append(p)

        diff = 0
        for i in range(k):
            old = clusters[i]
            center = calculate_center(plists[i], old.n)
            new = Cluster(plists[i], center, old.n)
            clusters[i] = new
            diff = max(diff, euclidean(old.center, new.center))

        if diff < min_diff:
            break

    return clusters
    

def hex_to_rgb(value):
    """Return (red, green, blue) for the color given as #rrggbb."""
    value = value.lstrip('#')
    lv = len(value)
    color = []
    for i in range(0, lv, lv // 3):
        color.append(int(value[i:i + lv // 3], 16))
    return color
    

def colorz(filename, n=3):
    """
    Returns the dominant n colors, will error if there are fewer
    colors available than n
    """
    img = Image.open(filename)
    img.thumbnail((200, 200))
    w, h = img.size

    points = get_points(img)
    clusters = kmeans(points, n, 1)
    rgbs = [map(int, c.center.coords) for c in clusters]
    return list(map(rtoh, rgbs))
    

def align_to_colorwheel(color):
    """
    given 12 colors of colorwheel, find which is most similar to color
    """
    diffs = []
    for i in range(len(COLORS)):
        red_diff = abs(color[0] - COLORS[i][0])
        green_diff = abs(color[1] - COLORS[i][1])
        blue_diff = abs(color[2] - COLORS[i][2])
        difference = red_diff + green_diff + blue_diff
        diffs.append(difference)
    index = diffs.index(min(diffs))
    return COLORS[index]
    

def get_opposite(color):
    """
    given 12 colors of colorwheel, return opposite of the given color
    """
    red = abs(color[0] - 255)
    green = abs(color[1] - 255)
    blue = abs(color[2] - 255)
    return [red, green, blue]
    
    
def color_is_gray(color):
    """checks if r g b values are equidistant (black, gray, white...)"""
    rb = abs(color[0] - color[1])
    rg = abs(color[0] - color[2])
    gb = abs(color[1] - color[2])

    if rb <= 10 and rg <= 10 and gb <= 10:
        return True
    else:
        return False
        

def get_best_color(image_path):
    """
    At first, only analyze the lower half of the image
    (where the bars will be).
    
    If the image is mostly gray, white, or black, then keep trying
    to find a color in the entire image that will align with the color
    wheel and use it as the visualizer bar color, else use random color.

    If the low half image is mostly a color that aligns with the color
    wheel, then use it's opposite as the visualizer bar color.
    """

    temp = Image.open(image_path)
    left = 0
    top = int(temp.size[1] / 2)
    bottom = temp.size[1]
    right = temp.size[0]
    temp = temp.crop((left, top, right, bottom))
    img = os.path.splitext(image_path)[0] + '_temp.png'
    temp.save(img)
    
    count = 1
    while True:
        try:
            hex_code = colorz(img, n=count)[0]
            rgb = hex_to_rgb(hex_code)
            if not color_is_gray(rgb):
                os.remove(os.path.splitext(image_path)[0] + '_temp.png')

                aligned_color = align_to_colorwheel(rgb)
                if img.endswith('_temp.png'):
                    opposite = get_opposite(aligned_color)
                    return opposite
                else:
                    return aligned_color
            else:
                if img.endswith('_temp.png'):
                    img = image_path
                else:
                    count += 1
            
        except ValueError:
            index = random.randint(0, 12)
            os.remove(os.path.splitext(image_path)[0] + '_temp.png')
            return COLORS[index]
        

if __name__ == '__main__':
    rgb = get_bar_color('/home/doakey/Desktop/test.png')
    print(rgb)





