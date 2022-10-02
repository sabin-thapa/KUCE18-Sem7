import numpy as np
from scipy.cluster.hierarchy import dendrogram, linkage
from scipy.spatial.distance import squareform
import matplotlib.pyplot as plt
mat = np.array([[0,0.5,2.24,3.35,3], [0.5,0,2.5,3.61,3.04], [2.24,2.5,0,1.12,1.41], [3.35,3.61,1.12,0,1.5], [3,3.04,1.41,1.5,0], ])
dists = squareform(mat)
linkage_matrix = linkage(dists, "complete")
dendrogram(linkage_matrix, labels=["x1","x2","x3","x4","x5",])
plt.title("Complete Link")
plt.savefig('output.png')