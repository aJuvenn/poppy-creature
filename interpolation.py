#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np


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


    def __call__(self, t):
        
        t_index = 0
        
        while t_index+1 < len(self.polynomials) and self.ts[t_index+1] < t:
            t_index += 1
        
        return np.polyval(self.polynomials[t_index], t - self.ts[t_index])
        
    
    def plot(self, eps = 0.01):
        fig, ax = plt.subplots(figsize=(6.5, 4))
        ax.plot(self.ts, self.xs, 'o')
        min_t = min(self.ts)
        max_t = max(self.ts)
        all_ts = np.arange(min_t, max_t, eps)
        all_xs = [self(t) for t in all_ts]
        ax.plot(all_ts, all_xs)
        ax.set_xlim(min_t, max_t)
        plt.show()


if __name__ == "__main__":
    ts = np.arange(0., 2. * np.pi, 1.)
    interp = InterpolationFunction(ts, np.sin(ts))
    interp.plot()