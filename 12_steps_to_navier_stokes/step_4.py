import handout as hd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import multiprocessing
import numpy as np
import subprocess
import sympy
import tensorflow as tf
import tensorflow_probability as tfp
from tqdm import tqdm
from matplotlib.animation import FuncAnimation
sympy.init_printing(use_latex=True)

output_dir = '/var/www/html/handouts/12_steps_to_navier_stokers/step_4'
doc = hd.handout.Handout(output_dir, title='Step 4')
doc.show()

nx = 101
xs = np.linspace(0., 2 * np.pi, nx)
dx = xs[1] - xs[0]
sigma = .2

nt = 1000
dt = sigma * dx**2
ts = np.linspace(0., (nt - 1) * dt, nt)
viscosity = 1.

doc.show()

sx, sv, st = sympy.symbols('x nu t')
sphi = (
    sympy.exp(-(sx - 4 * st) ** 2 / (4 * sv * (st + 1))) +
    sympy.exp(-(sx - 4 * st - 2 * sympy.pi) ** 2 / (4 * sv * (st + 1))))
doc.add_text(sphi)
doc.show()

sdphidx = sphi.diff(sx)
doc.add_text(sdphidx)
doc.show()

su0 = -2 * sv * (sdphidx / sphi) + 4
doc.add_text(su0)
doc.show()

u0 = sympy.utilities.lambdify((st, sx, sv), su0)

u = np.zeros([nx, nt])
#u[xs < .5, :] = 1.
#u[xs > .5, :] = 1.5
#u[xs > 1., :] = 1.
u[:, 0] = u0(0., xs, viscosity)
doc.show()

for t in range(nt - 1):
  u[0, t+1] = (
      u[0, t] +
      -u[0, t] * dt / dx * (u[0, t] - u[-1, t]) +
      viscosity * dt / dx**2 * (u[1, t] - 2 * u[0, t] + u[-1, t]))

  u[1:-1, t+1] = (
      u[1:-1, t] +
      -u[1:-1, t] * dt / dx * (u[1:-1, t] - u[0:-2, t]) +
      viscosity * dt / dx**2 * (u[2:, t] - 2 * u[1:-1, t] + u[0:-2, t]))

  u[-1, t+1] = (
      u[-1, t] +
      -u[-1, t] * dt / dx * (u[-1, t] - u[-1, t]) +
      viscosity * dt / dx**2 * (u[0, t] - 2 * u[-1, t] + u[-2, t]))

fig = plt.figure(figsize=(20, 8))
plt.imshow(u, cmap='viridis', interpolation='none',
           aspect=2. * nx / nt,
           extent=[0, nt * dt, 2, 0])
doc.add_figure(fig)
doc.show()

tq = tqdm(nt)

fig, ax = plt.subplots(figsize=(7, 4))
line = ax.plot(xs, u[:, 0], lw=2)[0]
ax.set_ylim(2., 6.)
def animate(i):
  tq.update()
  line.set_ydata(u[:, i])
anim = FuncAnimation(fig, animate, frames=nt)
anim.save('/'.join([output_dir, 'animation.mp4']), fps=60)
tq.close()
doc.add_html('<video autoplay controls loop src="animation.mp4"/>')
doc.show()
