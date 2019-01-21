#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import numpy as np


def secure_arccos(c):

    if c > 1.:
        return 0.
    if c < -1.:
        return np.pi
    
    return np.arccos(c)



class Poppy_leg:
    
    R = 1.
    L = 0.9
    D = 0.8
    
    def __init__(self):
        self.theta = 0.
        self.phi = 0.
        self.psi = 0.

    def MGD(self, theta, phi, psi):
        
        tmp = self.R + self.L * np.cos(phi) + self.D * np.cos(phi + psi)
        x = tmp * np.cos(theta)
        y = tmp * np.sin(theta)
        z = self.L * np.sin(phi) + self.D * np.sin(phi + psi)
        
        return [x, y, z]
    
    def get_position(self):
        return self.MGD(self.theta, self.phi, self.psi)


    def test_MGD(self, array_of_test):
        
        print("\nTesting MGD :")
        
        for (theta, phi, psi) in array_of_test:
            print '\t', (theta, phi, psi), " : ", self.MGD(theta, phi, psi)
        

    def MGI(self, x, y, z):
        
        theta = np.arctan2(y, x)
    
        Radius_xy = np.sqrt(x*x + y*y)
        delta_radius = Radius_xy - self.R
        K_squared = delta_radius**2 + z**2
        
        K = np.sqrt(K_squared)
        L_squared = self.L ** 2
        D_squared = self.D ** 2

        psi = - secure_arccos((K_squared - L_squared - D_squared) / (2. * L_squared * D_squared))

        if (K == 0.):
            return [theta, 0., psi]
        
        alpha = np.arctan2(z, delta_radius)
        beta = secure_arccos((K_squared + L_squared - D_squared)/(2. * K * self.L))
        phi = alpha + beta
        
        return [theta, phi, psi]
        
    
    
        
    def test_MGI(self, array_of_test):
        
        print("\nTesting MGI :")
        
        for (x,y,z) in array_of_test:
            theta, phi, psi = self.MGI(x, y, z)
            print '\t', (x,y,z), " : ", (theta, phi, psi) , " -> ", self.MGD(theta, phi, psi)
        
        
    def set_position(self, x, y, z):
        self.theta, self.phi, self.psi = self.MGI(x, y, z)

        
        
        
x = Poppy_leg()


test_MGD_array = [
        
    (0.,0.,0.),
    (0., 0., np.pi/2),        
    (0., 0., -np.pi/2),        
    (0., np.pi/2.,0.),
    (0., -np.pi/2.,0.),
    (np.pi/2,0.,0.),   
    (-np.pi/2,0.,0.)   
]

x.test_MGD(test_MGD_array)


expected_theta = 0.3
expected_theta_2 = -0.7

test_MGI_array = [
        
    (3.,0.,0.),
    (0.,3.,0.),
    (-3.,0.,0.),
    (0.,-3.,0.),
     (np.cos(expected_theta), np.sin(expected_theta), -2.),
    (np.cos(expected_theta), np.sin(expected_theta), -1.9),
     (np.cos(expected_theta), np.sin(expected_theta), -1.),
      (np.cos(expected_theta), np.sin(expected_theta), 0.),
       (np.cos(expected_theta), np.sin(expected_theta), 1.),
       (np.cos(expected_theta), np.sin(expected_theta), 1.9),
       (np.cos(expected_theta), np.sin(expected_theta), 2.),
       
     (np.cos(expected_theta_2), np.sin(expected_theta_2), -2.),
    (np.cos(expected_theta_2), np.sin(expected_theta_2), -1.9),
     (np.cos(expected_theta_2), np.sin(expected_theta_2), -1.),
      (np.cos(expected_theta_2), np.sin(expected_theta_2), 0.),
       (np.cos(expected_theta_2), np.sin(expected_theta_2), 1.),
       (np.cos(expected_theta_2), np.sin(expected_theta_2), 1.9),
       (np.cos(expected_theta_2), np.sin(expected_theta_2), 2.),
    
    
    (2.7 * np.cos(expected_theta_2), 2.7 * np.sin(expected_theta_2), 0.)
]


x.test_MGI(test_MGI_array)







