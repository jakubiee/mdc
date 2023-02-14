import cv2
from utilities.kmeans import Kmeans
import numpy as np
import matplotlib.pyplot as plt
import os


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
    width = int(args.c * 50)
    height = int(width / args.c)
    pallete = np.zeros((height, width, 3), np.uint8)
    for centroid in centroids:
        end = start + height
        r, g, b = int(centroid[0]), int(centroid[1]), int(centroid[2])
        cv2.rectangle(pallete, (start, 0), (int(end), height), (r, g, b), -1)
        start = end
    plt.figure()
    plt.axis("off")
    plt.title(img_title, fontdict={"fontweight": "bold"})
    plt.imshow(pallete)
    plt.savefig(img_title)
    plt.show()
