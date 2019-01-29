#!/usr/bin/env python2
# -*- coding: utf-8 -*-


from pypot.primitive import Primitive
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




class DiploLeg(Primitive):
  
    # Lengths of the leg
    
    R = 4.7 #cm
    L = 5.6 #cm
    D = 11.1 #cm
    L_squared = L * L
    D_squared = D * D
    
    # Standard position
    
    x0 = 3.
    z0 = -6.8
    y0_front = 9.
    y0_back = -3.
    

    @classmethod    
    def MGD(cls, theta, phi, psi):
        
        tmp = DiploLeg.R + DiploLeg.L * np.cos(phi) + DiploLeg.D * np.cos(phi + psi)
        x = tmp * np.cos(theta)
        y = tmp * np.sin(theta)
        z = DiploLeg.L * np.sin(phi) + DiploLeg.D * np.sin(phi + psi)
        
        return [x, y, z]
    
    @classmethod
    def MGI(cls, x, y, z):
        
        theta = np.arctan2(y, x)
    
        Radius_xy = np.sqrt(x*x + y*y)
        delta_radius = Radius_xy - DiploLeg.R
        K_squared = delta_radius**2 + z**2
        
        K = np.sqrt(K_squared)
        
        psi = - secure_arccos((K_squared - DiploLeg.L_squared - DiploLeg.D_squared) / (2. * DiploLeg.L * DiploLeg.D))

        if (K == 0.):
            return [theta, 0., psi]
        
        alpha = np.arctan2(z, delta_radius)
        beta = secure_arccos((K_squared + DiploLeg.L_squared - DiploLeg.D_squared)/(2. * K * DiploLeg.L))
        phi = alpha + beta
        
        return [theta, phi, psi]
    
    
    @classmethod
    def standard_front_position(cls):
        return [DiploLeg.x0, DiploLeg.y0_front, DiploLeg.z0]
    
    
    @classmethod
    def standard_back_position(cls):
        return [DiploLeg.x0, DiploLeg.y0_back, DiploLeg.z0]
    

    def __init__(self, robot, leg_name, refesh_freq = 40):
        
        Primitive.__init__(self, robot)
        self.motors = getattr(self.robot, leg_name)
        self.leg_name = leg_name
    
    
    def setup(self):
        self.theta = 0.
        self.phi = 0.
        self.psi = 0.            
    
    
    
    def __repr__(self):
        return ('<Primitive name={self.name}>').format(self=self)
    
    
    @property
    def get_angles(self):
        return [self.theta, self.phi, self.psi]    
    
    
    def set_angles(self, theta, phi, psi, duration = 0):
        
        self.theta = theta
        self.phi = phi
        self.psi = psi
        
        self.motors[0].goto_position(radian_to_degree(theta), duration)
        self.motors[1].goto_position(radian_to_degree(phi), duration)
        self.motors[2].goto_position(radian_to_degree(psi), duration)


    @property
    def get_position(self):
        return self.MGD(self.theta, self.phi, self.psi)


    def set_position(self, x, y, z, duration = 0.):
         theta, phi, psi = self.MGI(x, y, z)
         self.set_angles(theta, phi, psi, duration = duration)
    
    
    def set_standard_position(self, duration = 0.):
        
        if self.name == 'front_left' or self.name == 'front_right':
            x, y, z =  DiploLeg.standard_front_position()
            self.set_position(x, y, z, duration = duration)   
            
        elif self.name == 'back_left' or self.name == 'back_right':
            x, y, z =  DiploLeg.standard_back_position()
            self.set_position(x, y, z, duration = duration)
    
  
    
    
       
        
    
        
        
        
        
        
        
    