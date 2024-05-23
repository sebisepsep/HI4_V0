import numpy as np
import matplotlib.pyplot as plt

contrast = np.load("contrast.npy")

def reversal(x_array): 
    x_array = x_array.astype(complex)
    N = 16
    y_array = np.empty(N,dtype=complex)
    #first bit reversal
    for element in np.arange(N-1,-1,-1): #0000 and 1111 are already symmetric - maybe we can also exclude 9 and 6?
        val = bin(element)[2:].zfill(4) #works only until N=16
        reverse =  val[3] + val[2] + val[1] + val[0] # might be possible to just do two operations

        val_int = int(f"{val}",2)
        reverse_int = int(f"{reverse}",2)

        y_array[val_int], y_array[reverse_int] = x_array[reverse_int], x_array[val_int] #might be inefficient to use second array
        
    return y_array

def fft_array(x_array):
    N = 16
    x_array = reversal(x_array)
    x_array = x_array.astype(complex)
    
    #loopilooppppsss
    nj = 2 #start at 2 and increase later
    while nj <= N: #alternative ,2
        for n in range(0, N, nj):
            for k in range(nj//2):
                m = n+k
                exponent = np.exp(-2j*np.pi*k/nj)
                t = x_array[m]
                x_array[m] = t + exponent * x_array[int(m+nj/2)]
                x_array[int(m+nj/2)] = t - exponent * x_array[int(m+nj/2)]
        nj *= 2
    
    
    return x_array

def fft_array_inverse(x_array):
    N = 16
    x_array = reversal(x_array)
    x_array = x_array.astype(complex)
    
    #loopilooppppsss
    nj = 2 #start at 2 and increase later
    while nj <=N: #alternative ,2
        for n in range(0, N, nj):
            for k in range(nj//2):
                exponent = np.exp(+2j*np.pi*k/nj)
                m = n+k
                t = x_array[m]
                x_array[m] = t + exponent * x_array[int(m+nj/2)]
                x_array[int(m+nj/2)] = t - exponent * x_array[int(m+nj/2)]
        nj *= 2
    
    
    return x_array

def fft_3d(matrix, func):
    matrix = matrix.astype(complex)
    N = 16
    for j in range(N):
        for i in range(N):
            matrix[j][i] = func(matrix[j][i])
            

    matrix = np.transpose(matrix, axes=(0,2,1))
    for j in range(N):
        for i in range(N):
            matrix[j][i] = func(matrix[j][i])
            

    matrix = np.transpose(matrix, axes=(2,1,0))
    for j in range(N):
        for i in range(N):
            matrix[j][i] = func(matrix[j][i])
            

    #back to normal
    matrix = np.transpose(matrix, axes=(2,1,0))
    matrix = np.transpose(matrix, axes=(0,2,1))
    return matrix

matrix_array = fft_3d(contrast,fft_array)
#now dividing by k^2 - use grid points!
grid = np.arange(16) + 0.5
potential = matrix_array / grid**2
inverse = fft_3d(potential,fft_array_inverse)

#after inverse!!!
potential = np.real(potential)
inverse = np.real(inverse)

# Problem 2.b
potential = potential
fig, ax = plt.subplots(2,2, figsize=(10,8))
pcm = ax[0,0].pcolormesh(np.arange(0,16), np.arange(0,16), potential[4])
ax[0,0].set(ylabel='y', title='z = 4.5')
fig.colorbar(pcm, ax=ax[0,0], label='Potential')
pcm =ax[0,1].pcolormesh(np.arange(0,16), np.arange(0,16), potential[9])
ax[0,1].set(title='z = 9.5')
fig.colorbar(pcm, ax=ax[0,1], label='Potential')
pcm = ax[1,0].pcolormesh(np.arange(0,16), np.arange(0,16), potential[11])
ax[1,0].set(ylabel='y', xlabel='x', title='z = 11.5')
fig.colorbar(pcm, ax=ax[1,0], label='Potential')
pcm = ax[1,1].pcolormesh(np.arange(0,16), np.arange(0,16), potential[14])
ax[1,1].set(xlabel='x', title='z = 14.5')
fig.colorbar(pcm, ax=ax[1,1], label='Potential')
ax[0,0].set_aspect('equal', 'box')
ax[0,1].set_aspect('equal', 'box')
ax[1,0].set_aspect('equal', 'box')
ax[1,1].set_aspect('equal', 'box')
plt.savefig("fig2b_pot.png")
plt.close()

fourier_potential = inverse
fig, ax = plt.subplots(2,2, figsize=(10,8))
pcm = ax[0,0].pcolormesh(np.arange(0,16), np.arange(0,16), fourier_potential[4])
ax[0,0].set(ylabel='y', title='z = 4.5')
fig.colorbar(pcm, ax=ax[0,0], label=r'log10(|$\~\Phi$|)')
pcm =ax[0,1].pcolormesh(np.arange(0,16), np.arange(0,16), fourier_potential[9])
ax[0,1].set(title='z = 9.5')
fig.colorbar(pcm, ax=ax[0,1], label=r'log10(|$\~\Phi$|)')
pcm = ax[1,0].pcolormesh(np.arange(0,16), np.arange(0,16), fourier_potential[11])
ax[1,0].set(ylabel='y', xlabel='x', title='z = 11.5')
fig.colorbar(pcm, ax=ax[1,0], label=r'log10(|$\~\Phi$|)')
pcm = ax[1,1].pcolormesh(np.arange(0,16), np.arange(0,16), fourier_potential[14])
ax[1,1].set(xlabel='x', title='z = 14.5')
fig.colorbar(pcm, ax=ax[1,1], label=r'log10(|$\~\Phi$|)')
ax[0,0].set_aspect('equal', 'box')
ax[0,1].set_aspect('equal', 'box')
ax[1,0].set_aspect('equal', 'box')
ax[1,1].set_aspect('equal', 'box')
plt.savefig("fig2b_fourier.png")
plt.close()



