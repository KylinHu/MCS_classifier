#!/usr/local/bin/python

# An alternative script to assigning the regime, but to all eight regimes, the CD sub-regimes + 7 regimes. The satellite ID code is included in the output to allow analysis within each domain and track satellite changes. This script produces 3-hourly regimes by using the native 3-hour ISCCP resolution.

import numpy as np


datapath = '../Data/raw_3hr/'  # path where regime files are output to
cenpath = '../Data/cent/'            # path to the centroids file


import random
#prepare data
C = np.loadtxt('%shist_199901.asc' % datapath)
k=3
def kmeans(traindata, k):
    numSample,dim=traindata.shape
    changed = True
    center = np.array(random.sample(traindata, k))
    eucldist = np.zeros((numSample, k))
    # Loop until the center won't change
    while changed:
        for i in range(k):
            c= np.tile(center[i,:], (numSample,1))
            eucldist[:,i]=np.sqrt(np.sum((traindata-c)**2,axis=1))
        labels = np.argmin(eucldist, axis=1)
        newcenter = np.zeros((k,dim))
        for i in range(k):
            newcenter[i,:] =  np.average(traindata[labels==i,:], axis=0)
        changed = np.all(newcenter != center)
        center = newcenter
    # Calculate the number of each type
    num_of_each_type = np.array([traindata[labels == i,:].shape[0] for i in range(k)])
    # Calcultate the total distance
    totalDistance = 0
    for i in range(k):
        newCenter = np.tile(center[i,:], (sum(labels==i),1))
        #print "dist"+str(np.sum((x_train[labels==i,:]-newCenter)**2,axis=1))
        totalDistance += np.sum((np.sum((traindata[labels==i,:]-newCenter)**2,axis=1)))
    # return type labels and total distance and number of each type
    return labels,totalDistance,num_of_each_type
#loop to find the optimal center
n=10
labels = {}
num = {}
totalDist = np.zeros(n)
minDist = 10**4
minIndex = 0
for j in range(n):
    labels[j], totalDist[j], num[j] = kmeans(C, k)
    if totalDist[j] < minDist:
        minIndex = j
        minDist = totalDist[j]
# Print the classification results
filename = 'centroid0.txt' 
np.savetxt(cenpath + filename,center)

