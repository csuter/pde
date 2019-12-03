import handout as hd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import tensorflow as tf
import tensorflow_probability as tfp
doc = hd.handout.Handout(
    '/var/www/html/handouts/12_steps_to_navier_stokers/step_3', title='Step 3')
doc.show()

nx = 100
xs = np.linspace(0., 2., nx)
dx = xs[1] - xs[0]
sigma = .2

nt = 3000
dt = sigma * dx**2
ts = np.linspace(0., (nt - 1) * dt, nt)
viscosity = 0.3

doc.show()

u = np.zeros([nx, nt])
u[xs < .5, :] = 1.
u[xs > .5, :] = 1.5
u[xs > 1., :] = 1.
doc.show()

for t in range(nt - 1):
  u[1:-1, t+1] = (u[1:-1, t] +
                  viscosity * dt / dx**2 *
                  (u[2:, t] - 2 * u[1:-1, t] + u[:-2, t]))

fig = plt.figure(figsize=(20, 8))
plt.imshow(u, cmap='viridis', interpolation='none',
           aspect=.05,
           extent=[0, nt * dt, 2, 0])
doc.add_figure(fig)
doc.show()

fig = plt.figure(figsize=(20, 8))
nplts = 20
for i in range(nplts):
  #plt.plot(xs, u[:, i])
  plt.plot(xs, u[:, int(i * (len(ts) / nplts))])
doc.add_figure(fig)
doc.show()
