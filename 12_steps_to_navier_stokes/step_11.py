import handout as hd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from tqdm import tqdm
from matplotlib.animation import FuncAnimation

output_dir = '/Users/cgs/code/airplane/pde/12_steps_to_navier_stokes/step_10'
doc = hd.handout.Handout(output_dir, title='Step 11')
doc.show()

nx = ny = 100
nt = 300

xs = np.linspace(0., 2, nx)
ys = np.linspace(0., 2, ny)
ts = np.linspace(0., 1., nt)

dx = xs[1] - xs[0]
dy = ys[1] - ys[0]
doc.show()

u = np.zeors([nx, ny, nt])
v = np.zeors([nx, ny, nt])
p = np.zeros([nx, ny, nt])

print(b)

for t in range(nt - 1):
  # 1. Update velocity field u, v
  u[1:-1, 1:-1, t + 1] = (
        u[1:-1, 1:-1, t] +
        -u[1:-1, 1:-1, t] * (dt / dx) * (u[1:-1, 1:-1, t] - u[:-2, 1:-1, t]) +
        -v[1:-1, 1:-1, t] * (dt / dy) * (u[1:-1, 1:-1, t] - u[:-2, 1:-1, t]) +
        -(dt / (2. * density * dx)) * (p[2:, 1:-1] - p[:-2, 1:-1]) +
        viscosity * dt * (1 / dx**2 + 1 / dy**2) *
            (u[2:, 1:-1, t] - 2 * u[1:-1, 1:-1, t] + u[:-2, 1:-1, t]))

  v[1:-1, 1:-1, t + 1] = (
        v[1:-1, 1:-1, t] +
        -(dt / dx) * u[1:-1, 1:-1, t] * (v[1:-1, 1:-1, t] - v[:-2, 1:-1, t]) +
        -(dt / dy) * v[1:-1, 1:-1, t] * (v[1:-1, 1:-1, t] - v[:-2, 1:-1, t]) +
        -(dt / (2. * density * dy)) * (p[2:, 1:-1] - p[:-2, 1:-1]) +
        viscosity * dt * (1 / dx**2 + 1 / dy**2) *
            (v[2:, 1:-1, t] - 2 * v[1:-1, 1:-1, t] + v[:-2, 1:-1, t]))


  # 2. Compute new pressure source term
  b = np.zeros([nx, ny])
  b[1:-1, 1:-1] = 

  # 3. Iteratively solve for pressure field



  p[1:-1, 1:-1, t+1] = (
      dy ** 2 * (p[2:, 1:-1, t] + p[:-2, 1:-1, t]) +
      dx ** 2 * (p[1:-1, 2:, t] + p[1:-1, :-2, t]) -
      dx ** 2 * dy ** 2 * b[1:-1, 1:-1]
      ) / (2. * (dx ** 2 + dy ** 2))
  p[0,  :, t+1] =  0.
  p[-1, :, t+1] =  0.
  p[:, 0, t+1] =  0.
  p[:, -1, t+1] =  0.

import datetime
tq = tqdm(nt)
fig = plt.figure(figsize=(12, 12))
ax = fig.gca(projection='3d')

def plot(i):
  return ax.plot_surface(
      *np.meshgrid(xs, ys),
      p[:, :, i],
      antialiased=False,
      cmap='viridis',
      linewidth=.1,
      rstride=1,
      cstride=1)

def animate_slice(slice_num, slice_len, p):
  ax.set_title('{}'.format(datetime.datetime.now()))
  ax.set_zlim(p.min(), p.max())
  #import sys; sys.exit()
  surf = plot(0)
  def animate(i, surf):
    #surf.set_array(p[:, :, i])
    #surf.remove()
    ax.clear()
    surf = plot(slice_num * slice_len + i)
    ax.set_title('{}'.format(datetime.datetime.now()))
    ax.set_zlim(p.min(), p.max())
    tq.update()
    return [surf,]
  anim = FuncAnimation(fig, animate, frames=slice_len, blit=False, fargs=(surf,))
  anim.save('/'.join([output_dir, 'animation_slice_{:02d}.mp4'.format(slice_num)]), fps=60)

import multiprocessing as mp
import subprocess
num_slices = 10
sl = nt // num_slices
processes = [mp.Process(target=animate_slice, args=(sn, sl, p)) for sn in range(nt // sl)]
for proc in processes:
  proc.start()
for proc in processes:
  proc.join()
print(processes)

sliceslist_txt = '/'.join([output_dir, 'sliceslist.txt'])
with open(sliceslist_txt, 'w') as f:
  f.writelines([
    'file \'' + '/'.join([output_dir, 'animation_slice_{:02}.mp4'.format(i)]) + '\'\n' for i in range(nt // sl)
  ])

subprocess.run([
  'ffmpeg',
  '-f',
  'concat',
  '-safe', '0',
  '-i', sliceslist_txt,
  '-c', 'copy',
  '/'.join([output_dir, 'animation.mp4'])
  ])

tq.close()
doc.add_html('<video autoplay controls loop src="animation.mp4"/>')
doc.show()
