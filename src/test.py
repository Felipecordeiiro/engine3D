import numpy as np
import matplotlib.pyplot as plt

def create_sphere(cx, cy, cz, r, resolution=360):
    '''
    create sphere with center (cx, cy, cz) and radius r
    '''
    phi = np.linspace(0, 2*np.pi, 2*resolution)
    theta = np.linspace(0, np.pi, resolution)

    theta, phi = np.meshgrid(theta, phi)

    r_xy = r*np.sin(theta)
    x = cx + np.cos(phi) * r_xy
    y = cy + np.sin(phi) * r_xy
    z = cz + r * np.cos(theta)

    return x, y, z

fig = plt.figure(facecolor="black")
ax = plt.axes(projection="3d")

x, y, z = create_sphere(10, 10, 10, 10)
ax.plot_surface(x,y,z, rstride=5, cstride=5)
plt.show()