import numpy as np
import matplotlib.pyplot as plt

# Question 2: Calculating forces with the FFT

np.random.seed(121) # DO NOT CHANGE (so positions are the same for all students)

n_mesh = 16
n_part = 1024
positions = np.random.uniform(low=0, high=n_mesh, size=(3, n_part))

grid = np.arange(n_mesh) + 0.5
densities = np.zeros(shape=(n_mesh, n_mesh, n_mesh))
cellvol = 1.

for p in range(n_part):
    cellind = np.zeros(shape=(3, 2))
    dist = np.zeros(shape=(3, 2))

    for i in range(3):
        cellind[i] = np.where((abs(positions[i, p] - grid) < 1) |
                              (abs(positions[i, p] - grid - 16) < 1) | 
                              (abs(positions[i, p] - grid + 16) < 1))[0]
        dist[i] = abs(positions[i, p] - grid[cellind[i].astype(int)])

    cellind = cellind.astype(int)

    for (x, dx) in zip(cellind[0], dist[0]):    
        for (y, dy) in zip(cellind[1], dist[1]):
            for (z, dz) in zip(cellind[2], dist[2]):
                if dx > 15: dx = abs(dx - 16)
                if dy > 15: dy = abs(dy - 16)
                if dz > 15: dz = abs(dz - 16)

                densities[x, y, z] += (1 - dx)*(1 - dy)*(1 - dz) / cellvol


hat = 1024/16**3
contrast = (densities-hat)/hat

np.save("contrast.npy",contrast)

# Problem 2.a
densitycontrast = contrast
fig, ax = plt.subplots(2,2, figsize=(10,8))
pcm = ax[0,0].pcolormesh(np.arange(0,16), np.arange(0,16), densitycontrast[4])
ax[0,0].set(ylabel='y', title='z = 4.5')
fig.colorbar(pcm, ax=ax[0,0], label='Density')
pcm =ax[0,1].pcolormesh(np.arange(0,16), np.arange(0,16), densitycontrast[9])
ax[0,1].set(title='z = 9.5')
fig.colorbar(pcm, ax=ax[0,1], label='Density')
pcm = ax[1,0].pcolormesh(np.arange(0,16), np.arange(0,16), densitycontrast[11])
ax[1,0].set(ylabel='y', xlabel='x', title='z = 11.5')
fig.colorbar(pcm, ax=ax[1,0], label='Density')
pcm = ax[1,1].pcolormesh(np.arange(0,16), np.arange(0,16), densitycontrast[14])
ax[1,1].set(xlabel='x', title='z = 14.5')
fig.colorbar(pcm, ax=ax[1,1], label='Density')
ax[0,0].set_aspect('equal', 'box')
ax[0,1].set_aspect('equal', 'box')
ax[1,0].set_aspect('equal', 'box')
ax[1,1].set_aspect('equal', 'box')
plt.savefig("fig2a.png")
plt.close()