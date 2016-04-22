
import numpy as np


datapath = '../Data/raw_3hr/'  # path where regime files are output to
cenpath = '../Data/cent/'            # path to the centroids file


import random
#prepare data
x_train = np.loadtxt('%shist_199901.asc' % datapath)
num,dim = x_train.shape

# for different k (this case, we knew k=3)
k = 6
n = 0       # control iteration number
# sample,initial center

center = np.zeros([k,42])
center[:,:]= random.sample(x_train, k)
# judge to run
changed = True
while changed:
    # distance
    squaredist = np.zeros([num,k])
    for i in range(k):
        xcenter = np.tile(center[i],(num,1))
        diff = xcenter-x_train
        squarediff = diff**2
        squaredist[:,i] = np.sum(squarediff,axis=1)
        dist = np.sqrt(squaredist)    
    # sample labels
    labels = np.argmin(dist,axis=1)
    # new centers
    new_centers = np.zeros([k,42])
    # geometrical center  
    for i in range(k):
        new_centers[i,:] = np.mean(x_train[labels == i,:],axis=0)
        
        # judgement for cycle
    changed = np.all(new_centers != center)
    center = new_centers
    n = n+1

                             
# number of samples in each cluster
num_cluster = np.array([x_train[labels == i,:].shape[0] for i in range(k)])

filename = 'centroid1.txt' 
np.savetxt(cenpath + filename,center)