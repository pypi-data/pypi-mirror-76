from pylab import *
from numpy import *
from .base_cluster import Base

""" 
K-means-plus class for clustering by using k-means++ algorithm
Attributes:
k (int) representing the clusters number
data (list of points) a list of points coordinate extracted from the data file
"""
class K_means_plus(Base):

    def __init__(self, k=3):
        Base.__init__(self, k)

    """Function to find the nearest distance between a point to current cluster centers
       Args: 
           point(float, float): coordinate of a point
           cluster_centers(list of points): current cluster_centers
       Returns: nearest distance
    """
    def nearest(self, point, cluster_centers):
        min_dist = inf
        m = np.shape(cluster_centers)[0]  # the number of cluster centers already
        for i in range(m):
            d = self.distance(point, cluster_centers[i,])   # calculate the distance between the point and the cluster center
            # choose the shortest distance
            if min_dist > d:
                min_dist = d
        return min_dist

    """Function to find cluster centers
       Args: None
       Returns: cluster centers(list of coordinate of centers)
    """
    def get_centroids(self):
        m, n = np.shape(self.data)
        cluster_centers = np.zeros((self.k, n))
        index = np.random.randint(0, m)
        cluster_centers[0,] = self.data[index,]
        # initial a list of distances
        d = [0.0 for _ in range(m)]
        for i in range(1, self.k):
            sum_all = 0
            for j in range(m):
                # for a point, find the nearest cluster centre
                d[j] = self.nearest(self.data[j,], cluster_centers[0:i, ])
                # sum of the nearest distances
                sum_all += d[j]
            # randomized the sum of nearest distances
            sum_all *= random.rand()
            # choose the point with the longest distance as cluster centre
            for j, di in enumerate(d):
                sum_all = sum_all - di
                if sum_all > 0:
                    continue
                cluster_centers[i,] = self.data[j,]
                break
        return cluster_centers

    """Function to cluster samples by using K-means++ algorithm
               Args: None
               Returns: None
    """
    def k_means_puls_clustering(self):
        row_m=shape(self.data)[0]
        self.cluster_assign=zeros((row_m,2))
        self.cluster_center=self.get_centroids()
        change=True
        while change:
            change=False
            for i in range(row_m):
                mindist=inf
                min_index=-1
                for j in range(self.k):
                    distance1=self.distance(self.cluster_center[j,:],self.data[i,:])
                    if distance1<mindist:
                        mindist=distance1
                        min_index=j
                if self.cluster_assign[i,0] != min_index:
                    change=True
                self.cluster_assign[i,:]=min_index,mindist**2
            for cen in range(self.k):
                cluster_data=self.data[nonzero(self.cluster_assign[:,0]==cen)]
                self.cluster_center[cen,:]=mean(cluster_data,0)

    """Function to output the characteristics of the Kmeans++ instance
           Args: None
           Returns:
                string: characteristics of the cluster
    """
    def __repr__(self):
        return "k {},\ncluster centers \n{}\ncluster assigns \n{}".format(self.k, self.cluster_center,
                                                                          self.cluster_assign)
