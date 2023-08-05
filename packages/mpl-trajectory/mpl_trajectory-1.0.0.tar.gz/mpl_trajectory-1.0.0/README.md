# mpl_trajectory

You can read the docs from this badge
[![Documentation Status](https://readthedocs.org/projects/mpl-trajectory/badge/?version=latest)](https://mpl-trajectory.readthedocs.io/en/latest/?badge=latest)
# Table of Contents
1. [What Is This](#What_Is_This)
2. [Examples](#Examples)
3. [Install](#Install)

# What Is This
mpl_trajectory helps to plot particle trajectories as animations in matplotlib.

It can show show 3D trajectories by using the third axis as colour.

It can output a static graph or animation of the trajectories.
 

# Examples
## Sine Motion
Here is an example of using the code to display two sine waves.
<pre><code>from mpl_trajectory import trajectory
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
%matplotlib qt

plt.style.use('dark_background')

x1 = np.linspace(0,40,1500)
y1 = -5*np.sin(x1)
dydx_1 = -5*np.cos(x1)

x2 = np.linspace(0,40,1500)
y2 = 5*np.sin(x1)
dydx_2 = 5*np.cos(x1)

Traj = trajectory()
Traj.plot3D(x1,y1, dydx_1)
Traj.plot3D(x2,y2, dydx_2)
</code></pre>

<pre><code>Traj.ShowAnimation(with_color = True, z_axis=[-5,5], link_data = [[1,2]])</code></pre>

![Alt Text](https://raw.githubusercontent.com/Hitthesurf/mpl_trajectory/master/Examples/GIF/Sine_Wave_example.gif?raw=true)

## Spiral
Here is an example of a spiral
<pre><code>from mpl_trajectory import trajectory
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
%matplotlib qt

plt.style.use('dark_background')
theta = np.linspace(0,18*np.pi,1500)
r = np.linspace(0,9,1500)

x = r*np.cos(theta)
y = r*np.sin(theta)

Traj_2 = trajectory()
Traj_2.plot3D(x,y)
</code></pre>
<pre><code>Traj_2.ShowAnimation(follow_mass = -3, size = 9)</code></pre>
![Alt Text](https://raw.githubusercontent.com/Hitthesurf/mpl_trajectory/master/Examples/GIF/Spiral_Motion_Example.gif?raw=true)
<pre><code>Traj_2.ShowStatic(with_color = True)</code></pre>
![Alt Text](https://raw.githubusercontent.com/Hitthesurf/mpl_trajectory/master/Examples/PNG/Static_Spiral_with_color.png?raw=true)
# Install

You can use pip to install
<pre><code>pip install mpl-trajectory</code></pre>

## Spyder
You must run
<pre><code>%matplotlib qt</code></pre>
The graph will pop up in a window

## Jupyter Notebook
You can run 
<pre><code>%matplotlib qt</code></pre>
The graph will pop up in a window

Or
<pre><code>%matplotlib notebook</code></pre>
This will make the animation or graph appear in the cell bellow.

## Saving
If you want to save animations you must have ffmpeg for your system.
