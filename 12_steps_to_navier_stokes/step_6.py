import handout as hd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from tqdm import tqdm
from matplotlib.animation import FuncAnimation

output_dir = '/var/www/html/handouts/12_steps_to_navier_stokers/step_6'
doc = hd.handout.Handout(output_dir, title='Step 6')
doc.show()

nx = ny = 101
nt = 100

xs = np.linspace(0., 2, nx)
ys = np.linspace(0., 2, ny)

dx = xs[1] - xs[0]
dy = ys[1] - ys[0]
c = 1.
sigma = .2

dt = sigma * dx
ts = np.linspace(0., (nt - 1) * dt, nt)
doc.show()

u = np.zeros([nx, ny, nt])
u[:, :, :] = 1.
u[int(.5 / dy):int(1. / dy + 1.), int(.5 / dx):int(1. / dx + 1), :] = 2.

v = np.zeros([nx, ny, nt])
v[:, :, :] = 1.
v[int(.5 / dy):int(1. / dy + 1.), int(.5 / dx):int(1. / dx + 1), :] = 2.
doc.show()

for t in range(nt - 1):
  u[1:, 1:, t+1] = (
      u[1:, 1:, t] -
      u[1:, 1:, t] * dt / dx * (u[1:, 1:, t] - u[:-1, 1:, t]) -
      v[1:, 1:, t] * dt / dy * (u[1:, 1:, t] - u[1:, :-1, t]))

  v[1:, 1:, t+1] = (
      v[1:, 1:, t] -
      u[1:, 1:, t] * dt / dx * (v[1:, 1:, t] - v[:-1, 1:, t]) -
      v[1:, 1:, t] * dt / dy * (v[1:, 1:, t] - v[1:, :-1, t]))

  u[:, 0, t+1] =  1.
  u[:, -1, t+1] =  1.
  u[0,  :, t+1] =  1.
  u[-1, :, t+1] =  1.

  v[:, 0, t+1] =  1.
  v[:, -1, t+1] =  1.
  v[0,  :, t+1] =  1.
  v[-1, :, t+1] =  1.

for i in [0, 10, -1]:
  fig, ax = plt.subplots(ncols=2, figsize=(20, 8))
  ax[0].imshow(
      u[:, :, i], cmap='viridis', interpolation='none',
      aspect=1.,
      extent=[0, 2, 2, 0])
  ax[1].imshow(
      v[:, :, i], cmap='viridis', interpolation='none',
      aspect=1.,
      extent=[0, 2, 2, 0])
  doc.add_figure(fig)
doc.show()

tq = tqdm(nt)
fig, ax = plt.subplots(ncols=2, figsize=(7, 4))
imu = ax[0].imshow(
    u[:, :, i], cmap='viridis', interpolation='none',
    aspect=1.,
    extent=[0, 2, 2, 0])
imv = ax[1].imshow(
    v[:, :, i], cmap='viridis', interpolation='none',
    aspect=1.,
    extent=[0, 2, 2, 0])
patches = [imu, imv]
def animate(i):
  tq.update()
  imu.set_array(u[:, :, i])
  imv.set_array(v[:, :, i])
  return patches
anim = FuncAnimation(fig, animate, frames=nt)
anim.save('/'.join([output_dir, 'animation.mp4']), fps=60)
tq.close()
doc.add_html('<video autoplay controls loop src="animation.mp4"/>')
doc.show()
