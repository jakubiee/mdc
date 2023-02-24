import cv2
from mdc.utilities.kmeans import Kmeans
import numpy as np
import matplotlib.pyplot as plt
import os
import colorsys


def image(args):
    _get_centroids(args)


def _get_centroids(args):
    img_path = args.image_name[0]
    if not os.path.isfile(img_path):
        raise Exception("Incorrect file path")
    if args.t:
        img_title = args.t
    else:
        img_basename = os.path.basename(img_path)
        parts = []
        for p in img_basename.split("."):
            parts.append(p)
        img_title = parts[0]

    img = cv2.imread(img_path)
    img = cv2.resize(img, (600, 400))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = img.reshape((img.shape[0] * img.shape[1], 3))
    kmeans = Kmeans()

    centroids, clusters = kmeans.kmeans(img, k=args.c)
    _get_palette(centroids, img_title, args)


def _get_palette(centroids, img_title, args):
    start = 0
    width = int(args.c * 150)
    height = int(width / args.c)
    text_box_height = 35
    if args.hex:
        pallete = np.zeros((height + text_box_height, width, 3), np.uint8)
    else:
        pallete = np.zeros((height, width, 3), np.uint8)
    font = cv2.FONT_HERSHEY_DUPLEX
    font_scale = 0.9
    for centroid in centroids:
        r, g, b = int(centroid[0]), int(centroid[1]), int(centroid[2])
        end = start + height
        cv2.rectangle(pallete, (start, 0), (int(end), height), (r, g, b), -1)
        if args.hex:
            cv2.rectangle(
                pallete,
                (start, height),
                (int(end), height + text_box_height),
                (255, 255, 255),
                -1,
            )
            h, s, v = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)
            rgb_color = colorsys.hsv_to_rgb(h, s, v)
            hex_color = "#{:02x}{:02x}{:02x}".format(
                int(rgb_color[0] * 255),
                int(rgb_color[1] * 255),
                int(rgb_color[2] * 255),
            )
            text = hex_color.upper()
            text_size = cv2.getTextSize(text, font, font_scale, 1)[0]
            text_x = start + int((height - text_size[0]) / 2)
            text_y = int(height + 25)
            cv2.putText(pallete, text, (text_x, text_y), font, font_scale, (0, 0, 0), 1)
        start = end
    plt.figure()
    plt.axis("off")
    plt.title(img_title, fontdict={"fontweight": "bold"})
    plt.imshow(pallete)
    plt.savefig(img_title)
    plt.show()
