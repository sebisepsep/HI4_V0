import numpy as np
import matplotlib.pyplot as plt
from astropy import units as u
from astropy import constants as c

info_position = np.load("position.npy") #in AU
info_velocity = np.load("velocity.npy") #in AU/d
info_position = info_position - info_position[0] #choosing frame from sun
info_velocity = info_velocity - info_velocity[0] #static case
names = np.array(["sun", "mercury", "venus", "earth", "mars", "jupiter", "saturn", "uranus", "neptune"])

G_val = c.G.to_value()
M_sun = c.M_sun.to_value()

"""take seconds, beacuse you need enough points per oribit period to get an accurate result!!"""

year = 200* 3600 * 24 * 365 #s
day = 3600 * 24 #s

times = np.arange(0, year+0.5*day, 0.5*day)
N = len(times)

def gravity(r):
    a = -(G_val * M_sun * r / np.sqrt(sum(r**2))**3)
    return a

def leap_frog(func,times,h,x0,v0):
    pos = np.zeros((len(times), 3))
    pos[0] = x0 #initial value
    vel = np.zeros((len(times), 3))
    vel[0] = v0#initial value

    for i in range(1,len(times)):
        #runge kutta for first step
        if i == 1:
            vel[i] = vel[i-1] + 0.5*func(pos[i-1])*h #acceleration
        
        #offset by half
        else:
            vel[i] = vel[i-1] + func(pos[i-1])*h #acceleration
        
        #full position
        pos[i] = pos[i-1] + vel[i]*h
        
    return pos

   


#track pos
xpos = np.array([],dtype=object)
ypos = np.array([],dtype=object)
zpos = np.array([],dtype=object)

for i in range(1,9):
    rad = np.array([info_position[i][j] for j in [0,1,2]])*1.5*10**11#m
    vel = np.array([info_velocity[i][j] for j in [0,1,2]])*1.5*10**11 /(86400) #m/s

    #Doing the leapfrog integration
    pos = leap_frog(gravity, times, 0.5*day, rad, vel)

    xpos = np.append(xpos,0)
    ypos = np.append(ypos,0)
    zpos = np.append(zpos,0)
    
    xpos[i-1] = (pos[:,0])/(1.5*10**11)#AU
    ypos[i-1] = (pos[:,1])/(1.5*10**11)
    zpos[i-1] = (pos[:,2])/(1.5*10**11)


# Problem 1.b
# For visibility, you may want to do two versions of this plot: 
# one with all planets, and another zoomed in on the four inner planets
names = np.array(["mercury", "venus", "earth", "mars", "jupiter", "saturn", "uranus", "neptune"])
#add sun

x, y, z = xpos,ypos,zpos
time = times
fig, ax = plt.subplots(1,2, figsize=(12,5), constrained_layout=True)

ax[0].plot(0, 0, "o", label= "sun")
for i, obj in enumerate(names):
    ax[0].plot(x[i], y[i], label=obj)
    ax[1].plot(time, z[i], label=obj)
ax[0].set_aspect('equal', 'box')
ax[0].set(xlabel='X [AU]', ylabel='Y [AU]')
ax[1].set(xlabel='Time [yr]', ylabel='Z [AU]')
plt.legend(loc=(1.05,0))
plt.savefig("fig1b.png")
plt.close()


names = np.array(["mercury", "venus", "earth", "mars"])
#add sun

x, y, z = xpos,ypos,zpos
time = times
fig, ax = plt.subplots(1,2, figsize=(12,5), constrained_layout=True)

ax[0].plot(0, 0, "o", label= "sun")
for i, obj in enumerate(names):
    ax[0].plot(x[i], y[i], label=obj)
    ax[1].plot(time[:1500], z[i][:1500], label=obj)
ax[0].set_aspect('equal', 'box')
ax[0].set(xlabel='X [AU]', ylabel='Y [AU]')
ax[1].set(xlabel='Time [yr]', ylabel='Z [AU]')
plt.legend(loc=(1.05,0))
plt.savefig("fig1bInnen.png")
plt.close()

