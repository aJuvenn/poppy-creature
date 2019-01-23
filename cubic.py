#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 22 09:37:33 2019

@author: ajuvenn
"""

from scipy.interpolate import CubicSpline
import matplotlib.pyplot as plt
import numpy as np

x = 2.*3.1415*np.arange(11)/10.
y = np.sin(x)
cs = CubicSpline(x, y)
xs = np.arange(-0.5, 9.6, 0.1)
fig, ax = plt.subplots(figsize=(6.5, 4))
ax.plot(x, y, 'o', label='data')
ax.plot(xs, np.sin(xs), label='true')
ax.plot(xs, cs(xs), label="S")
ax.plot(xs, cs(xs, 1), label="S'")
ax.plot(xs, cs(xs, 2), label="S''")
ax.plot(xs, cs(xs, 3), label="S'''")
ax.set_xlim(-0.5, 2.*3.1415)
ax.legend(loc='lower left', ncol=2)
plt.show()




T = 1.

times = [0., 3.*T/4., 7.*T/8., T]

xy_forward = 2.
xy_backward = 1.
xy_points = [xy_forward, xy_backward, 0.5*(xy_forward + xy_backward), xy_forward]

z_up = 10.
z_down = 0.
z_points = [z_down, z_down, z_up, z_down]

cs_xy = CubicSpline(times, xy_points)
cs_z = CubicSpline(times, z_points)


ts = np.arange(0., T, 0.01)
xy = cs_xy(ts)


fig, ax = plt.subplots(figsize=(6.5, 4))
ax.plot(times, xy_points, 'o')
ax.plot(ts, xy)
ax.set_xlim(-0.5, 1.1*T)
plt.show()


z = cs_z(ts)

fig, ax = plt.subplots(figsize=(6.5, 4))
ax.plot(times, z_points, 'o')
ax.plot(ts, z)
ax.set_xlim(-0.5, 1.1*T)
plt.show()


fig, ax = plt.subplots(figsize=(6.5, 4))
ax.plot(xy_points, z_points,  'o', label='data')
ax.plot(xy, z, 'x')
ax.set_xlim(0.5, 2.5)
plt.show()

###



T = 1.

times = [0., 3.*T/4., 7.*T/8., T]

xy_forward = 2.
xy_backward = 1.
xy_points = [xy_forward, xy_backward, 0.5*(xy_forward + xy_backward), xy_forward]

z_up = 10.
z_down = 0.
z_points = [z_down, z_down, z_up, z_down]

cs_xy = CubicSpline(times, xy_points)
cs_z = CubicSpline(times, z_points)


ts = np.arange(0., T, 0.01)
xy = cs_xy(ts)


fig, ax = plt.subplots(figsize=(6.5, 4))
ax.plot(times, xy_points, 'o')
ax.plot(ts, xy)
ax.set_xlim(-0.5, 1.1*T)
plt.show()


z = cs_z(ts)

fig, ax = plt.subplots(figsize=(6.5, 4))
ax.plot(times, z_points, 'o')
ax.plot(ts, z)
ax.set_xlim(-0.5, 1.1*T)
plt.show()


fig, ax = plt.subplots(figsize=(6.5, 4))
ax.plot(xy_points, z_points,  'o', label='data')
ax.plot(xy, z, 'x')
ax.set_xlim(0.5, 2.5)
plt.show()



###




T = 1.

times = [0., T/4., T/2., 3.*T/4., T]

xy_forward = 10.
xy_backward = 0.
xy_points = [xy_forward,  0.5*(xy_forward + xy_backward), xy_backward, 0.5*(xy_forward + xy_backward), xy_forward]

z_up = 0.5
z_down = 0.
z_points = [z_down, z_down, z_down, z_up, z_down]

cs_xy = CubicSpline(times, xy_points)
cs_z = CubicSpline(times, z_points)


ts = np.arange(0., T, 0.01)
xy = cs_xy(ts)


fig, ax = plt.subplots(figsize=(6.5, 4))
ax.plot(times, xy_points, 'o')
ax.plot(ts, xy)
ax.set_xlim(-0.5, 1.1*T)
plt.show()


z = cs_z(ts)

fig, ax = plt.subplots(figsize=(6.5, 4))
ax.plot(times, z_points, 'o')
ax.plot(ts, z)
ax.set_xlim(-0.5, 1.1*T)
plt.show()


fig, ax = plt.subplots(figsize=(6.5, 4))
ax.plot(xy_points, z_points,  'o', label='data')
ax.plot(xy, z, 'x')
ax.set_xlim(-1., 12.)
plt.show()





class InterpolationFunction:
    
    @classmethod     
    def cubic(cls, t1, t2, x1, x2):
    
        A = np.matrix([[t1**3, t1**2, t1, 1],
                       [t2**3, t2**2, t2, 1],
                       [3.*(t1**2), 2.*t1, 1., 0.],
                       [3.*(t2**2), 2.*t2, 1., 0]])
       
        b = np.array([x1, x2, 0., 0.]).reshape(4,1)
        
        return np.array(((A**-1)*b).reshape(1,4))[0]
    

    def __init__(self, ts, xs):
    
        self.ts = ts
        self.xs = xs
        self.polynomials = []
        
        for i in range(len(ts) - 1):
            self.polynomials.append(InterpolationFunction.cubic(0., ts[i+1] - ts[i], xs[i], xs[i+1]))
            print(self.polynomials)

    def __call__(self, t):
        
        t_index = 0
        
        while t_index+1 < len(self.polynomials) and self.ts[t_index+1] < t:
            t_index += 1
        
        return np.polyval(self.polynomials[t_index], t - self.ts[t_index])
        





def position_order(front_coordinates, horizontal_amplitude, horizontal_angle, vertical_amplitude, period):
    
    times = [0., period/2., 3.*period/4., period]
    horizontal_points = [0., -horizontal_amplitude, -horizontal_amplitude/2., 0.]
    vertical_points = [0., 0., vertical_amplitude, 0.]
    
    horizontal_interpol = InterpolationFunction(times, horizontal_points)
    vertical_interpol = InterpolationFunction(times, vertical_points)
    

    
    
    
    
    
    
    
    
    
    
    



T = 1.

times = [0., T/2., 3.*T/4., T]

xy_forward = 10.
xy_backward = 0.
xy_points = [xy_forward, xy_backward, 0.5*(xy_forward + xy_backward), xy_forward]

z_up = 0.5
z_down = 0.
z_points = [z_down, z_down, z_up, z_down]

cs_xy = InterpolationFunction(times, xy_points)
cs_z = InterpolationFunction(times, z_points)


ts = np.arange(0., T, 0.01)
xy = [cs_xy(t) for t in ts]


fig, ax = plt.subplots(figsize=(6.5, 4))
ax.plot(times, xy_points, 'o')
ax.plot(ts, xy)
ax.set_xlim(-0.5, 1.1*T)
plt.show()


z = [cs_z(t) for t in ts]

fig, ax = plt.subplots(figsize=(6.5, 4))
ax.plot(times, z_points, 'o')
ax.plot(ts, z)
ax.set_xlim(-0.5, 1.1*T)
plt.show()


fig, ax = plt.subplots(figsize=(6.5, 4))
ax.plot(xy_points, z_points,  'o', label='data')
ax.plot(xy, z, 'x')
ax.set_xlim(-1., 12.)
plt.show() 
