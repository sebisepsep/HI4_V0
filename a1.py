# we need to import the time module from astropy
from astropy.time import Time
# import some coordinate things from astropy
from astropy.coordinates import solar_system_ephemeris
from astropy.coordinates import get_body_barycentric_posvel
from astropy import units as u
import numpy as np
import matplotlib.pyplot as plt
import jplephem #needed to add this 


# pick a time (please use either this or the current time)
t = Time("2024-06-23 00:00")

# initialize the planets; Mars is shown as an example
names = np.array(['Sun', 'Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune'])
info = np.array([])
info_position = np.array([])
info_velocity = np.array([])

for element in names:
    with solar_system_ephemeris.set('jpl'):
        var = get_body_barycentric_posvel(f'{element}', t)
        info = np.append(info, var)
        info_position = np.append(info_position,var[0])
        info_velocity = np.append(info_velocity,var[1])

# calculate the position in AU
info_position = np.array([[element.x.to_value(u.AU),element.y.to_value(u.AU),element.z.to_value(u.AU)] for element in info_position])

#calculating the velocity in AU/day
info_velocity = np.array([[element.x.to_value(u.AU/u.d),element.y.to_value(u.AU/u.d),element.z.to_value(u.AU/u.d)] for element in info_velocity])


# Problem 1.a
x, y, z = np.array([element[0] for element in info_position]),np.array([element[1] for element in info_position]),np.array([element[2] for element in info_position])
names = np.array(['Sun', 'Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune'])

fig, ax = plt.subplots(1,2, figsize=(12,5), constrained_layout=True)
fig.suptitle("Initial position for planets around the sun", fontsize = 15)

for i, obj in enumerate(names):
    ax[0].scatter(x[i], y[i], label=obj)
    ax[1].scatter(x[i], z[i], label=obj)
ax[0].set_aspect('equal', 'box')
ax[1].set_aspect('equal', 'box')
ax[0].set(xlabel='X [AU]', ylabel='Y [AU]', xlim=[-5, 32], ylim=[-5, 20])
ax[1].set(xlabel='X [AU]', ylabel='Z [AU]', xlim=[-5, 32], ylim=[-5, 20])
plt.legend(loc=(1.05,0))

plt.savefig("fig1a.png")
plt.close()
np.save("position.npy",info_position)
np.save("velocity.npy",info_velocity)