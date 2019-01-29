#!/usr/bin/env python2
# -*- coding: utf-8 -*-


from pypot.primitive import LoopPrimitive
from DipoLeg import DiploLeg
from command import PositionPattern, PositionCommand
import numpy as np


class DiploMoveForward(LoopPrimitive):
    

    def __init__(self, robot, command_freq = 40):
        
        LoopPrimitive.__init__(self, robot, command_freq)    
        leg_names = ["front_left", "back_left", "back_right", "front_right"]
        self.legs = [DiploLeg(robot, leg_name) for leg_name in leg_names] 
        self.command_freq = command_freq
        self.dt = 1. / command_freq
    
    
    def setup(self):
    
        T = 1.
        angle = -np.pi/2.

        horiz_amp = 9.
        vert_amp = 1.3        
        offsets = [0., 0.5, 0., 0.5]
        patterns = [PositionPattern.position_pattern_v1(horiz_amp, vert_amp, cursor = offsets[i]) for i in range(4)]

        initial_front_position = DiploLeg.standard_front_position()
        intitial_back_position = DiploLeg.standard_back_position()
        initial_positions = [initial_front_position, intitial_back_position, intitial_back_position, initial_front_position]

        self.commands = [PositionCommand(patterns[i], initial_positions[i], angle, T) for i in range(4)]


    def update(self):
        
        for i in range(4):
            x, y, z = self.commands[i].next_command()
            self.legs[i].set_position(x, y, z, duration = self.dt) 
            
            
    def teardown(self):
        
        for leg in self.legs:
            leg.set_standard_position(duration = 0.5)

