# -*- coding: utf-8 -*-
"""
Created on Mon Aug 20 10:32:58 2018

@author: ankurs
"""

import pandas as pd
from time import time
import numpy as np

start_time = time()

b = pd.read_excel('bangalore-consolidated-data.xlsx', sheet_name = 'Sheet1')
df = pd.read_excel('bangalore-consolidated-data.xlsx', sheet_name = 'Sheet2')

del b['deviceCode_deviceCode'], b['deviceCode_location_latitude'], b['deviceCode_location_longitude']
del b['w_hour'], b['Mapped_Location'], b['timestamp'], b['e_hour'], b['weatherDate']
del b['hourCat'], b['time'], b['temperature'], b['eventDate'], b['Plying_Speed']

del df['deviceCode_deviceCode'], df['deviceCode_location_latitude'], df['deviceCode_location_longitude']
del df['w_hour'], df['Mapped_Location'], df['timestamp'], df['e_hour'], df['weatherDate']
del df['hourCat'], df['time'], df['temperature'], df['eventDate'], df['Plying_Speed']

##################################################################################################
#
#                                       CLUSTERING ALGORITHMS
#
##################################################################################################

##### NUMERICAL DATA INPUT #######

from sklearn.cluster import MiniBatchKMeans as KMeans
X = b.values.astype(np.float)
kmeans = KMeans(n_clusters = 2, max_iter = 1000).fit(X)
kmlabels = kmeans.labels_
kmlabels = kmlabels.tolist()
print('Finished clustering using K-Means')

from sklearn.cluster import MiniBatchKMeans as KMeans
X = b.values.astype(np.float)
kmeans = KMeans(n_clusters = 2, max_iter = 1000).fit(X)
kmflabels = kmeans.labels_
kmflabels = kmflabels.tolist()
print('Finished clustering using K-Means')

from sklearn.cluster import MiniBatchKMeans as KMeans
X = b.values.astype(np.float)
kmeans = KMeans(n_clusters = 2, max_iter = 2000).fit(X)
kmf2labels = kmeans.labels_
kmf2labels = kmf2labels.tolist()
print('Finished clustering using K-Means')

from sklearn.cluster import MiniBatchKMeans as KMeans
X = b.values.astype(np.float)
kmeans = KMeans(n_clusters = 2, max_iter = 3000).fit(X)
kmf3labels = kmeans.labels_
kmf3labels = kmf3labels.tolist()
print('Finished clustering using K-Means')

from sklearn.cluster import MiniBatchKMeans as KMeans
X = b.values.astype(np.float)
kmeans = KMeans(n_clusters = 2, max_iter = 3000).fit(X)
ekmf3labels = kmeans.labels_
ekmf3labels = ekmf3labels.tolist()
print('Finished clustering using K-Means')

"""
################# GAUSSIAN MIXTURE ############################

from sklearn.mixture import GaussianMixture
X = b.values.astype(np.float)
gm = GaussianMixture(n_components = 2, covariance_type='full', max_iter = 1000)


#############################################################################################

###### BINARY NUMERICAL DATA INPUT ##########

x = pd.get_dummies(data = df, columns = df.columns.values.tolist())

from sklearn.cluster import KMeans
X = x.values.astype(np.float)
kmeans = KMeans(n_clusters = 2, max_iter = 1000).fit(X)
dkmlabels = kmeans.labels_
dkmlabels = dkmlabels.tolist()
print('Finished clustering using K-Means')

from sklearn.cluster import KMeans
X = x.values.astype(np.float)
kmeans = KMeans(n_clusters = 2, max_iter = 1000, algorithm = 'full').fit(X)
dkmflabels = kmeans.labels_
dkmflabels = dkmflabels.tolist()
print('Finished clustering using K-Means')


from sklearn.cluster import KMeans
X = x.values.astype(np.float)
kmeans = KMeans(n_clusters = 2, max_iter = 2000, algorithm = 'full').fit(X)
dkmf2labels = kmeans.labels_
dkmf2labels = dkmf2labels.tolist()
print('Finished clustering using K-Means')



from sklearn.cluster import DBSCAN
db = DBSCAN(eps = 2.5, min_samples = 2, algorithm = 'auto').fit(X)
dblabels = db.labels_
dblabels = dblabels.tolist()
print('Finished clustering using DBSCAN')

from sklearn.cluster import SpectralClustering
sc = SpectralClustering(n_clusters = 2).fit(X)
sclabels = sc.labels_
sclabels = sclabels.tolist()
print('Finished clustering using Spectral Clustering')
"""
"""
from sklearn.cluster import Birch
birch = Birch(threshold = 0.5, branching_factor = 50, n_clusters = 2).fit(X)
birchlabels = birch.labels_
birchlabels = birchlabels.tolist()
print('Finished clustering using Birch')
"""
"""
from sklearn.cluster import FeatureAgglomeration
fa = FeatureAgglomeration(n_clusters = 2, affinity='euclidean').fit(X)
falabels = fa.labels_
falabels = falabels.tolist()
print('Finished clustering using Feature Agglomeration')

from sklearn.cluster import AgglomerativeClustering
ac = AgglomerativeClustering(n_clusters = 2, affinity = 'euclidean').fit(X)
aclabels = ac.labels_
aclabels = aclabels.tolist()
print('Finished clustering using Agglomerative Clustering').fit(X)
"""

newDf = pd.DataFrame()
newDf['Kmeans'] = kmlabels
newDf['EMKmeans'] = kmflabels
newDf['EM2Kmeans'] = kmf2labels
newDf['EM3Kmeans'] = kmf3labels
newDf['ElM3Kmeans'] = ekmf3labels
#newDf['DKmeans'] = dkmlabels
#newDf['DEMKmeans'] = dkmflabels
#newDf['DEM2Kmeans'] = dkmf2labels

b['labels'] = kmf2labels
df['labels'] = kmf2labels
df['labels'] = df['labels'].map({0: 'Low', 1: 'High'})

end_time = time()
time_taken = end_time - start_time

print("\nTotal time taken in seconds: ", time_taken)