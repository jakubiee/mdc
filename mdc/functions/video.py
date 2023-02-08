import cv2
from utilities.kmeans import Kmeans
import numpy as np 
import matplotlib.pyplot as plt


def video(*args):
    print("video")
    return

def get_frames(video):
    kmeans = Kmeans()
    video = cv2.VideoCapture(video)
    c = 0 
    s = True
    centroids = []
    while s:
        s, img = video.read()
        if c == 10 and s == 1:
            img = cv2.resize(img, (256,144))
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = img.reshape((img.shape[0] *img.shape[1],3))
            centroid, clusters = kmeans.kmeans(img, 1)
            centroids.append(centroid)
            c = 0
        c+=1
    centroids = np.array(centroids)
    return centroids

def plot_palette(centroids):
    start = 0
    size = centroids.shape[0] * 50
    
    pallete = np.zeros((2000,size,3), np.uint8)
    for centroid in centroids:
        end = start + 50
        r,g,b = int(centroid[0]), int(centroid[1]),int(centroid[2])
        cv2.rectangle(pallete, (start, 0), (int(end), 2000), (r,g,b), -1)
        start = end
    plt.figure()
    plt.axis("off")
    plt.imshow(pallete)
    plt.show()



