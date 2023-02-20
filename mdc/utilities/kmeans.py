import numpy as np


class Kmeans:
    def __init__(self, max_iterations=100, tolerance=1e-6) -> None:
        self.max_iterations = max_iterations
        self.tolerance = tolerance

    def kmeans(self, X, k):
        centroids = X[np.random.choice(X.shape[0], k, replace=False), :]
        for i in range(self.max_iterations):
            distances = np.array(
                [self._distance(X, centroid) for centroid in centroids]
            )
            clusters = np.argmin(distances, axis=0)
            new_centroids = np.array([X[clusters == j].mean(axis=0) for j in range(k)])
            if np.linalg.norm(new_centroids - centroids) < self.tolerance:
                break
            centroids = new_centroids

        return centroids, clusters

    def _distance(self, X, centroid):
        return np.linalg.norm(X - centroid, axis=1)
