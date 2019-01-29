#!/usr/bin/env python2
# -*- coding: utf-8 -*-


from pypot.primitive import LoopPrimitive
from DiploLeg import DiploLeg
from command import PositionPattern, PositionCommand
import numpy as np


FRONT_LEFT = 0
BACK_LEFT = 1
BACK_RIGHT = 2
FRONT_RIGHT = 3



class DiploTurnLeft(LoopPrimitive):
    
    leg_names = ["front_left", "back_left", "back_right", "front_right"]
    is_front = [True, False, False, True]
        

    def __init__(self, robot, command_freq = 40):
        
        LoopPrimitive.__init__(self, robot, command_freq)
        
        self.legs = []
        self.all_leg_motors = []
        
        for i in range(4):
            leg_motors = getattr(self.robot, DiploTurnLeft.leg_names[i])
            self.legs.append(DiploLeg(leg_motors, DiploTurnLeft.is_front[i]))
            self.all_leg_motors.extend(leg_motors)
            
        self.command_freq = command_freq
        self.dt = 1. / command_freq
    

    def setup(self):

        for m in self.all_leg_motors:
            m.compliant = False
        
        move_period = 1.
        angle = np.arctan2(17.,15.)

        horiz_amp = 9.
        vert_amp = 1.3    
        offsets = [0., 0.5, 0., 0.5]
        patterns = [PositionPattern.position_pattern_v1(horiz_amp, vert_amp, cursor = offsets[i]) for i in range(4)]

        initial_front_position = DiploLeg.standard_front_position()
        intitial_back_position = DiploLeg.standard_back_position()
        initial_positions = [initial_front_position, intitial_back_position, intitial_back_position, initial_front_position]

        self.commands = []
        
        self.commands.append(PositionCommand(patterns[FRONT_LEFT], initial_positions[FRONT_LEFT], angle + np.pi/2., move_period))
        self.commands.append(PositionCommand(patterns[BACK_LEFT], initial_positions[BACK_LEFT], -angle + np.pi/2., move_period))
        self.commands.append(PositionCommand(patterns[BACK_RIGHT], initial_positions[BACK_RIGHT], -angle - np.pi/2., move_period))
        self.commands.append(PositionCommand(patterns[FRONT_RIGHT], initial_positions[FRONT_RIGHT], angle - np.pi/2., move_period))
        
        
    def update(self):
        
        for i in range(4):
            x, y, z = self.commands[i].next_command()
            self.legs[i].set_position(x, y, z, duration = self.dt) 

