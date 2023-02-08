import cv2
from utilities.kmeans import Kmeans
import numpy as np
import matplotlib.pyplot as plt


def image(*args):
    print("image")
    return

def plot_palette(centroids):
    start = 0
    pallete = np.zeros((50,250,3), np.uint8)
    for centroid in centroids:
        end = start + 50 
        r,g,b = int(centroid[0]), int(centroid[1]),int(centroid[2])
        cv2.rectangle(pallete, (start, 0), (int(end), 50), (r,g,b), -1)
        start = end
    plt.figure()
    plt.axis("off")
    plt.imshow(pallete)
    plt.show()


# img = cv2.imread('fish.jpg')
# img = cv2.resize(img, (600, 400))
# img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
# img = img.reshape((img.shape[0] *img.shape[1],3))

# kmeans = Kmeans()
# centroids,clusters = kmeans.kmeans(img, k=5)
# plot_palette(centroids)
