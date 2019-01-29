#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
import time
from interpolation import InterpolationFunction

class PositionPattern:
    
    
    def __init__(self, cursor_values, horizontal_values, vertical_values, cursor = 0., use_linear = False):
        
        self.cursor_values = cursor_values
        self.horizontal_values = horizontal_values
        self.vertical_values = vertical_values

        self.horizontal_interpol = InterpolationFunction(cursor_values, horizontal_values, use_linear = use_linear)
        self.vertical_interpol = InterpolationFunction(cursor_values, vertical_values, use_linear = use_linear)
        
        self.cursor = cursor % 1.
  
    
    def set_cursor(self, cursor):
        self.cursor = cursor % 1.
        
        
    def increase_cursor(self, dcursor):
        self.cursor = (self.cursor + dcursor) % 1.
        
        
    def __call__(self):
        
        horizontal_value = self.horizontal_interpol(self.cursor)
        vertical_value = self.vertical_interpol(self.cursor)
       
        return [horizontal_value, vertical_value]


    def plot(self, eps = 0.01):
        
        ts = np.arange(0., 1., eps)
        horiz = [self.horizontal_interpol(t) for t in ts]
        vert = [self.vertical_interpol(t) for t in ts]
        
        fig, ax = plt.subplots(figsize=(6.5, 4))
        ax.plot(self.cursor_values, self.horizontal_values, 'o')
        ax.plot(ts, horiz)
        ax.set_xlim(-0.1, 1.1)
        plt.show()
        
        fig, ax = plt.subplots(figsize=(6.5, 4))
        ax.plot(self.cursor_values, self.vertical_values, 'o')
        ax.plot(ts, vert)
        ax.set_xlim(-0.1, 1.1)
        plt.show()
        
        fig, ax = plt.subplots(figsize=(6.5, 4))
        ax.plot(self.horizontal_values, self.vertical_values, 'o')
        ax.plot(horiz, vert, 'x')
        ax.set_xlim(min(horiz) - 1., max(horiz) + 1.)
        plt.show()

        


    @classmethod    
    def position_pattern_v1(cls, horizontal_amplitude, vertical_amplitude, cursor = 0., use_linear = False):
        
        cursor_values = [0., 1./2. , 3./4., 1.]
        horizontal_values = [0., horizontal_amplitude, horizontal_amplitude/2., 0.]
        vertical_values = [0., 0., vertical_amplitude, 0.]
        
        return PositionPattern(cursor_values, horizontal_values, vertical_values, cursor = cursor, use_linear = use_linear)
    




class PositionCommand:
    
    def __init__(self, pattern, coordinates, horizontal_angle, period):
        
        self.pattern = pattern
        self.coordinates = coordinates
        self.cos_horizontal_angle = np.cos(horizontal_angle)
        self.sin_horizontal_angle = np.sin(horizontal_angle)
        self.period = period
        self.last_call_time = time.time()


    def set_period(self, period):
        self.period = period
        
        
    def set_coordinates(self, coordinates):
        self.coordinates = coordinates
        
        
    def set_horizontal_angle(self, horizontal_angle):
        self.cos_horizontal_angle = np.cos(horizontal_angle)
        self.sin_horizontal_angle = np.sin(horizontal_angle)
        
        
    def reset_last_call_time(self):
        self.last_call_time = time.time()
        
        
    def next_command(self):
        
        current_time = time.time()
        dcursor = (current_time - self.last_call_time) / self.period
        self.last_call_time = current_time
        self.pattern.increase_cursor(dcursor)
        
        horizontal_command, vertical_command = self.pattern()
        
        x_command = self.coordinates[0] + horizontal_command * self.cos_horizontal_angle
        y_command = self.coordinates[1] + horizontal_command * self.sin_horizontal_angle
        z_command = self.coordinates[2] + vertical_command
        
        return [x_command, y_command, z_command]

