import numpy as np 
import matplotlib.pyplot as plt 

data = np.loadtxt('galaxy_data.txt')
kappa = np.array([element[0] for element in data])
color = np.array([element[1] for element in data])
extension = np.array([element[2] for element in data])
flux = np.array([element[3] for element in data])
flag = np.array([element[4] for element in data])

data_array = np.array([np.array([element[i] for element in data]) for i in np.arange(5)])

np.savetxt('data_array.txt', data_array)

M = len(data)

for i in range(len(data_array)):
    mean = sum(data_array[i])/M
    std  = sum((data_array[i]-mean)**2)/M #or M-1?
    data_array[i] = (data_array[i]-mean)/std
features = data_array 
fig, ax = plt.subplots(2,2, figsize=(10,8))
ax[0,0].hist(features[0], bins=20)
ax[0,0].set(ylabel='N', xlabel=r'$\kappa_{CO}$')
ax[0,1].hist(features[1], bins=20)
ax[0,1].set(xlabel='Color')
ax[1,0].hist(features[2], bins=20)
ax[1,0].set(ylabel='N', xlabel='Extended')
ax[1,1].hist(features[3], bins=20)
ax[1,1].set(xlabel='Emission line flux')
plt.savefig("fig3a.png")
plt.close()