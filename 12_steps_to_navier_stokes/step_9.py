import handout as hd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from tqdm import tqdm
from matplotlib.animation import FuncAnimation

output_dir = '/var/www/html/handouts/12_steps_to_navier_stokers/step_9'
doc = hd.handout.Handout(output_dir, title='Step 9')
doc.show()

nx = ny = 41
nt = 1000

xs = np.linspace(0., 2, nx)
ys = np.linspace(0., 1, ny)

dx = xs[1] - xs[0]
dy = ys[1] - ys[0]
c = 1.
sigma = .1
doc.show()


p = np.zeros([nx, ny, nt])
p[-1, :, :] += ys[..., np.newaxis]

# Iterate
for t in range(nt - 1):
  p[1:-1, 1:-1, t+1] = (
      dy ** 2 * (p[2:, 1:-1, t] + p[:-2, 1:-1, t])   +
      dy ** 2 * (p[1:-1, 2:, t] + p[1:-1, :-2, t])
      ) / (2. * (dx ** 2 + dy ** 2))
  p[0,  :, t+1] =  0.
  p[-1, :, t+1] =  ys
  p[:, 0, t+1] =  p[:, 1, t+1]
  p[:, -1, t+1] =  p[:, -2, t+1]

import datetime
tq = tqdm(nt)
fig, ax = plt.subplots(ncols=1, figsize=(8, 8))
ax.set_title('{}'.format(datetime.datetime.now()))
im = ax.imshow(
    p[:, :, 0],
    cmap='viridis',
    interpolation='none',
    aspect=2.,
    origin='lower',
    extent=[xs[0], xs[-1], ys[0], ys[-1]])
patches = [im,]
def animate(i):
  s = 5
  im.set_array(p[:, :, i])
  ax.set_title('{}'.format(datetime.datetime.now()))
  tq.update()
  return patches
anim = FuncAnimation(fig, animate, frames=nt, blit=False)
anim.save('/'.join([output_dir, 'animation.mp4']), fps=60)
tq.close()
doc.add_html('<video autoplay controls loop src="animation.mp4"/>')
doc.show()
