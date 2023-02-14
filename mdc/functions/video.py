import cv2
from utilities.kmeans import Kmeans
import numpy as np 
import matplotlib.pyplot as plt

def video(args):
    centroids = _get_centroids(args)
    _get_palette(centroids)

def _get_centroids(args):
    video = args.video_name[0]
    kmeans = Kmeans()
    video = cv2.VideoCapture(video)
    fps = video.get(cv2.CAP_PROP_FPS)
    start_frame, end_frame = 0, video.get(cv2.CAP_PROP_FRAME_COUNT)
    if args.s or args.e:
        if args.s:
            start_frame = int(fps*args.s)
        if args.e:
            end_frame = int(fps*args.e)     
    c = 0 
    s = True
    f = 0
    centroids = []
    while s:
        s, img = video.read()

        if f >= start_frame and f<=end_frame:
            if c == 10 and s == 1:
                img = cv2.resize(img, (256,144))
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                img = img.reshape((img.shape[0] *img.shape[1],3))
                centroid, clusters = kmeans.kmeans(img, 1)
                centroids.append(centroid)
                c = 0
            c+=1
        f+=1
    centroids = np.array(centroids)
    return centroids

def _get_palette(centroids):
    start = 0
    size = centroids.shape[0] * 50
    
    pallete = np.zeros((6000,size,3), np.uint8)
    for centroid in centroids:
        end = start + 50
        r,g,b = int(centroid[0]), int(centroid[1]),int(centroid[2])
        cv2.rectangle(pallete, (start, 0), (int(end), 6000), (r,g,b), -1)
        start = end
    plt.figure()
    plt.axis("off")
    plt.title("test", fontdict={'fontweight': 'bold'})
    plt.imshow(pallete)
    plt.savefig("test.png")
    plt.show()
    



