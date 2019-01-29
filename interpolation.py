#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np


class InterpolationFunction:
    
    @classmethod     
    def cubic(cls, t1, t2, x1, x2):
        """
            Returns a list of coefficient corresponding
            to a polynomial P such as P(t1) = x1, P(t2) = x2
            and P'(t1) = P'(t2) = 0
        """
    
        A = np.matrix([[t1**3, t1**2, t1, 1],
                       [t2**3, t2**2, t2, 1],
                       [3.*(t1**2), 2.*t1, 1., 0.],
                       [3.*(t2**2), 2.*t2, 1., 0]])
       
        b = np.array([x1, x2, 0., 0.]).reshape(4,1)
        
        return np.array(((A**-1)*b).reshape(1,4))[0]

    @classmethod
    def linear(cls, t1, t2, x1, x2):
        
        A = np.matrix([[t1, 1],
                       [t2, 1]])
    
        b = np.array([x1, x2]).reshape(2,1)

        return np.array(((A**-1)*b).reshape(1,2))[0]


    def __init__(self, ts, xs, use_linear = False):
        """
            Creates a new interpolation function f such as f(ts[i]) = xs[i]
            and f'(ts[i]) = 0. 
            Requirements : 2 <= len(ts) <= len(xs) and ts is sorted
        """
        
        self.ts = ts
        self.xs = xs
        self.polynomials = []
        
        if use_linear:
            interp_func = InterpolationFunction.linear
        else:
            interp_func = InterpolationFunction.cubic
        
        for i in range(len(ts) - 1):
            self.polynomials.append(interp_func(0., ts[i+1] - ts[i], xs[i], xs[i+1]))


    def __call__(self, t):
        """
            Computes the value of interpolation function at value t
        """

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
