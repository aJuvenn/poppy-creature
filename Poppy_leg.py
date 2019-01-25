#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import numpy as np



def secure_arccos(c):
    
    if c > 1.:
        print("Value too high !")
        return 0.
    if c < -1.:
        print("Value too low !")
        return np.pi
    
    return np.arccos(c)


def radian_to_degree(theta):
    return theta * 180. / np.pi


class PoppyLeg:
    
    R = 0.5
    L = 0.9
    D = 1.5
    L_squared = L * L
    D_squared = D * D
    
    def __init__(self, motors):
        self.theta = 0.
        self.phi = 0.
        self.psi = 0.
        self.motors = motors


    def MGD(self, theta, phi, psi):
        
        tmp = self.R + self.L * np.cos(phi) + self.D * np.cos(phi + psi)
        x = tmp * np.cos(theta)
        y = tmp * np.sin(theta)
        z = self.L * np.sin(phi) + self.D * np.sin(phi + psi)
        
        return [x, y, z]
    
    
    def MGI(self, x, y, z):
        
        theta = np.arctan2(y, x)
    
        Radius_xy = np.sqrt(x*x + y*y)
        delta_radius = Radius_xy - PoppyLeg.R
        K_squared = delta_radius**2 + z**2
        
        K = np.sqrt(K_squared)
        
        psi = - secure_arccos((K_squared - PoppyLeg.L_squared - PoppyLeg.D_squared) / (2. * PoppyLeg.L_squared * PoppyLeg.D_squared))

        if (K == 0.):
            return [theta, 0., psi]
        
        alpha = np.arctan2(z, delta_radius)
        beta = secure_arccos((K_squared + PoppyLeg.L_squared - PoppyLeg.D_squared)/(2. * K * PoppyLeg.L))
        phi = alpha + beta
        
        return [theta, phi, psi]
    
    
    def get_angles(self):
        return [self.theta, self.phi, self.psi]    
    
    
    def set_angles(self, theta, phi, psi, duration = 0):
        
        self.theta = theta
        self.phi = phi
        self.psi = psi
        
        self.motors[0].goto_position(radian_to_degree(theta), duration)
        self.motors[1].goto_position(radian_to_degree(phi), duration)
        self.motors[2].goto_position(radian_to_degree(psi), duration)


    def get_position(self):
        return self.MGD(self.theta, self.phi, self.psi)


    def set_position(self, x, y, z, duration = 0):
         theta, phi, psi = self.MGI(x, y, z)
         self.set_angles(theta, phi, psi, duration = duration)
        
    
    

    def test_MGD(self, array_of_test):
        
        print("\nTesting MGD :")
        
        for (theta, phi, psi) in array_of_test:
            print '\t', (theta, phi, psi), " : ", self.MGD(theta, phi, psi)
        

    
        
    def test_MGI(self, array_of_test):
        
        print("\nTesting MGI :")
        
        for (x,y,z) in array_of_test:
            theta, phi, psi = self.MGI(x, y, z)
            print '\t', (x,y,z), " : ", (theta, phi, psi) , " -> ", self.MGD(theta, phi, psi)        
    

        
        
if __name__ == "__main__":
    x = PoppyLeg([0,0,0])
    
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







