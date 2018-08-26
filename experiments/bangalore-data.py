# -*- coding: utf-8 -*-
"""
Created on Fri Aug 10 19:29:11 2018

@author: ankurs
"""

import pandas as pd
from time import time
import numpy as np
from pandas import ExcelWriter

start_time = time()

def date_splitter(dateToSplit):
    dateToSplit = dateToSplit.split('-', 1)
    year = dateToSplit[0]
    dateToSplit = dateToSplit[1].split('-', 1)
    month = dateToSplit[0]
    day = dateToSplit[1]
    return year, month, day

bdf = pd.read_excel('bangalore-cas-alerts.xlsx')

bdf = bdf.rename(columns = {'deviceCode_time_recordedTime_$date':'timestamp'})
bdf['timestamp'] = pd.to_datetime(bdf['timestamp'])
bdf['eventDate'] = pd.to_datetime(bdf['timestamp'])
bdf['eventDate'] = bdf['eventDate'].dt.strftime('%Y%m%d')
bdf['e_hour'] = pd.to_datetime(bdf['timestamp'], format = '%H:%M:%S').dt.hour
bdf['ehourCat'] = 0
bdf['ehourCat'] = np.where((bdf['e_hour'] >= 0) & (bdf['e_hour'] < 6), 1, bdf['ehourCat'])
bdf['ehourCat'] = np.where((bdf['e_hour'] >= 6) & (bdf['e_hour'] < 10), 2, bdf['ehourCat'])
bdf['ehourCat'] = np.where((bdf['e_hour'] >= 10) & (bdf['e_hour'] < 16), 3, bdf['ehourCat'])
bdf['ehourCat'] = np.where((bdf['e_hour'] >= 16) & (bdf['e_hour'] < 21), 4, bdf['ehourCat'])
bdf['ehourCat'] = np.where((bdf['e_hour'] >= 21) & (bdf['e_hour'] < 24), 5, bdf['ehourCat'])
bdf['weatherDate'] = bdf['eventDate']
bdf['weatherDate'] = bdf['weatherDate'].astype(str)

bwdf = pd.read_excel('bangalore-weather.xlsx')
bwdf['w_hour'] = pd.to_datetime(bwdf['time'], format= '%H:%M').dt.hour
bwdf['hourCat'] = 0
bwdf['hourCat'] = np.where((bwdf['w_hour'] >= 0) & (bwdf['w_hour'] < 6), 1, bwdf['hourCat'])
bwdf['hourCat'] = np.where((bwdf['w_hour'] >= 6) & (bwdf['w_hour'] < 10), 2, bwdf['hourCat'])
bwdf['hourCat'] = np.where((bwdf['w_hour'] >= 10) & (bwdf['w_hour'] < 16), 3, bwdf['hourCat'])
bwdf['hourCat'] = np.where((bwdf['w_hour'] >= 16) & (bwdf['w_hour'] < 21), 4, bwdf['hourCat'])
bwdf['hourCat'] = np.where((bwdf['w_hour'] >= 21) & (bwdf['w_hour'] < 24), 5, bwdf['hourCat'])
bwdf = bwdf.drop_duplicates(subset = ['weatherDate', 'hourCat'], keep = 'first')
bwdf['ehourCat'] = bwdf['hourCat']
bwdf['weatherDate'] = bwdf['weatherDate'].astype(str)

b1 = pd.merge(bdf, bwdf, on = ['weatherDate', 'ehourCat'], how = 'left')
b1 = b1.rename(columns = {'deviceCode_location_wardName':'Area'})
badf = pd.read_excel('bangalore-accident-zones.xlsx')

##################################################################################################
#
#                                               MAIN DATASET
#
##################################################################################################

b = pd.merge(b1, badf, on = ['Area'], how = 'left')
b = b.rename(columns = {'deviceCode_pyld_alarmType':'Alarm_Type'})
b = b.rename(columns = {'deviceCode_pyld_speed':'Plying_Speed'})
b['hasOversped'] = np.where(b.Plying_Speed > 60, 1, 0)
b['hasOversped'] = np.where(b.Alarm_Type == 'Overspeed', 1, b['hasOversped'])

for column in ['temperature', 'visibility', 'condition']:
    b[column].fillna(b[column].mode()[0], inplace=True)

b['visibility'] = np.where(b['visibility'] < 10, 0, 1)

df = b.copy()
df['hasOversped'] = np.where(b.hasOversped == 1, 'Yes', 'No')
df['visibility'] = np.where(b.visibility == 0, 'Low', 'High')
df['ehourCat'] = b['ehourCat'].map({1: 'Early', 2: 'PeakM', 3: 'RegularM'})
b['Accident_Severity'] = b['Accident_Severity'].map({'High': 3, 'Medium': 2, 'Low': 1})
b['Pothole_Severity'] = b['Pothole_Severity'].map({'High': 3, 'Medium': 2, 'Low': 1})
b['Alarm_Type'] = b['Alarm_Type'].map({'PCW': 1, 'FCW': 2, 'Overspeed': 3, 'HMW': 4, 'UFCW': 5, 'LDWL': 6, 'LDWR': 7})
b['condition'] = b['condition'].map({'Clear': 1, 'Sunny': 2, 'Passing clouds': 3,
       'Broken clouds': 4, 'Scattered clouds': 5, 'Fog': 6, 'Haze': 7, 'Partly cloudy': 8,
       'Mild': 9, 'Drizzle. Broken clouds': 10})
b['Area'] = b['Area'].map({'Kadugodi': 1, 'Garudachar Playa': 2, 'Hudi': 3, 'Other': 4, 'Devasandra': 5,
       'Hagadur': 6, 'Bellanduru': 7, 'Marathahalli': 8, 'Dodda Nekkundi': 9, 'Varthuru': 10,
       'HAL Airport': 11, 'Vijnana Nagar': 12, 'Konena Agrahara': 13, 'A Narayanapura': 14,
       'C V Raman Nagar': 15, 'Jeevanbhima Nagar': 16, 'HSR Layout': 17, 'Domlur': 18, 'Jogupalya': 19,
       'Hoysala Nagar': 20, 'New Tippasandara': 21, 'Benniganahalli': 22, 'Singasandra': 23,
       'Basavanapura': 24, 'Halsoor': 25, 'Agaram': 26, 'Shantala Nagar': 27, 'Sampangiram Nagar': 28,
       'Sudham Nagara': 29, 'Dharmaraya Swamy Temple': 30, 'Chickpete': 31, 'Banasavadi': 32,
       'Horamavu': 33, 'Kacharkanahalli': 34, 'Kammanahalli': 35, 'Vijnanapura': 36, 'Ramamurthy Nagar': 37,
       'K R Puram': 38, 'BTM Layout': 39, 'Madivala': 40, 'Gurappanapalya': 41, 'J P Nagar': 42, 'Sarakki': 43,
       'Jaraganahalli': 44, 'Vasanthpura': 45, 'Hemmigepura': 46, 'Yelchenahalli': 47,
       'Jayanagar East': 48, 'Bharathi Nagar': 49, 'other': 4})

writer = ExcelWriter('bangalore-consolidated-data.xlsx')
b.to_excel(writer, index = False, sheet_name = 'Sheet1')
df.to_excel(writer, index = False, sheet_name = 'Sheet2')
writer.save()

del b['deviceCode_deviceCode'], b['deviceCode_location_latitude'], b['deviceCode_location_longitude']
del b['w_hour'], b['Mapped_Location'], b['timestamp'], b['e_hour'], b['weatherDate']
del b['hourCat'], b['time'], b['temperature'], b['eventDate'], b['Plying_Speed']

del df['deviceCode_deviceCode'], df['deviceCode_location_latitude'], df['deviceCode_location_longitude']
del df['w_hour'], df['Mapped_Location'], df['timestamp'], df['e_hour'], df['weatherDate']
del df['hourCat'], df['time'], df['temperature'], df['eventDate'], df['Plying_Speed']

del bwdf, b1, badf, bdf

##################################################################################################
#
#                                       CLUSTERING ALGORITHMS
#
##################################################################################################

##### NUMERICAL DATA INPUT #######

from sklearn.cluster import KMeans
X = b.values.astype(np.float)
kmeans = KMeans(n_clusters = 2, max_iter = 1000).fit(X)
kmlabels = kmeans.labels_
kmlabels = kmlabels.tolist()
print('Finished clustering using K-Means')

from sklearn.cluster import KMeans
X = b.values.astype(np.float)
kmeans = KMeans(n_clusters = 2, max_iter = 1000, algorithm = 'full').fit(X)
kmflabels = kmeans.labels_
kmflabels = kmflabels.tolist()
print('Finished clustering using K-Means')

from sklearn.cluster import KMeans
X = b.values.astype(np.float)
kmeans = KMeans(n_clusters = 2, max_iter = 2000, algorithm = 'full').fit(X)
kmf2labels = kmeans.labels_
kmf2labels = kmf2labels.tolist()
print('Finished clustering using K-Means')


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


"""
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
#newDf['Birch'] = birchlabels
newDf['Kmeans'] = kmlabels
newDf['EMKmeans'] = kmflabels
newDf['EM2Kmeans'] = kmf2labels
newDf['DKmeans'] = dkmlabels
newDf['DEMKmeans'] = dkmflabels
newDf['DEM2Kmeans'] = dkmf2labels

end_time = time()
time_taken = end_time - start_time

print("\nTotal time taken in seconds: ", time_taken)