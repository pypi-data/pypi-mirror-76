from pylab import *
from numpy import *
from .base_cluster import Base

""" 
K-means class for clustering by using k-means algorithm
Attributes:
k (int) representing the clusters number
data (list of points) a list of points coordinate extracted from the data file
"""
class K_means(Base):

    def __init__(self, k=3):
        Base.__init__(self, k)

    """Function to identify cluster centers randomly
       Args: 
           dataset(list of points): sample points
           k(int): number of clusters
       Returns (list of points): Initial centers
    """
    def rand_center(self, dataset, k):
        dim=shape(dataset)[1]
        init_cen=zeros((k,dim))
        for i in range(dim):
            min_i=min(dataset[:,i])
            range_i=float(max(dataset[:,i]) - min_i)
            init_cen[:,i]=min_i + range_i*random.rand(k)
        return init_cen

    """Function to cluster samples by using K-means algorithm
           Args: None
           Returns: None
    """
    def k_means_clustering(self):
        row_m=shape(self.data)[0]
        self.cluster_assign=zeros((row_m,2))
        self.cluster_center=self.rand_center(self.data,self.k)
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

    """Function to output the characteristics of the Kmeans instance
       Args: None
       Returns: string: characteristics of the cluster
    """
    def __repr__(self):
        return "k {},\ncluster centers \n{}\ncluster assigns \n{}".format(self.k, self.cluster_center, self.cluster_assign)