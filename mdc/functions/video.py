import cv2
from mdc.utilities.kmeans import Kmeans
import numpy as np
import matplotlib.pyplot as plt
import os


def video(args):
    _get_centroids(args)


def _get_centroids(args):
    kmeans = Kmeans()
    video_path = args.video_name[0]

    if not os.path.isfile(video_path):
        raise Exception("Incorrect file path")

    if args.t:
        video_title = args.t
    else:
        video_basename = os.path.basename(video_path)
        parts = []
        for p in video_basename.split("."):
            parts.append(p)
        video_title = parts[0]

    video = cv2.VideoCapture(video_path)
    fps = video.get(cv2.CAP_PROP_FPS)
    start_frame, end_frame = 0, video.get(cv2.CAP_PROP_FRAME_COUNT)
    if args.s or args.e:
        if args.s:
            start_frame = int(fps * args.s)
        if args.e:
            end_frame = int(fps * args.e)
    if end_frame <= start_frame:
        raise Exception("The end time must be greater than the start time.")

    counter, frames, status, centroids = 0, 0, True, []
    while status:
        status, img = video.read()

        if frames >= start_frame and frames <= end_frame:
            if counter == 10 and status == 1:
                img = cv2.resize(img, (256, 144))
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                img = img.reshape((img.shape[0] * img.shape[1], 3))
                centroid, clusters = kmeans.kmeans(img, 1)
                centroids.append(centroid)
                counter = 0
            counter += 1
        elif frames >= end_frame:
            break
        frames += 1
    centroids = np.array(centroids)
    _get_palette(centroids, video_title)


def _get_palette(centroids, video_title):
    start = 0
    width = centroids.shape[0] * 50
    height = int(width * (9 / 20))
    pallete = np.zeros((height, width, 3), np.uint8)
    for centroid in centroids:
        end = start + 50
        r, g, b = int(centroid[0][0]), int(centroid[0][1]), int(centroid[0][2])
        cv2.rectangle(pallete, (start, 0), (int(end), height), (r, g, b), -1)
        start = end
    plt.figure()
    plt.axis("off")
    plt.title(video_title, fontdict={"fontweight": "bold"})
    plt.imshow(pallete)
    plt.savefig(video_title)
    plt.show()
