#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 25 15:34:21 2019

@author: ajuvenn
"""

from Poppy_leg import PoppyLeg
from pypot.creatures import PoppyErgoJr
import time
import command

FRONT_LEFT = 0
BACK_LEFT = 1
BACK_RIGHT = 2
FRONT_RIGHT = 3


jr = PoppyErgoJr()

FL_motors = [jr.m7, jr.m8, jr.m9]
BL_motors = [jr.m10, jr.m11, jr.m12]
BR_motors = [jr.m13, jr.m14, jr.m15]
FR_motors = [jr.m16, jr.m17, jr.m18]


FL_leg = PoppyLeg(FL_motors)
BL_leg = PoppyLeg(BL_motors)
BR_leg = PoppyLeg(BR_motors)
FR_leg = PoppyLeg(FR_motors)


legs = [FL_leg, BL_leg, BR_leg, FR_leg]


command_freq = 20.
dt = 1. / command_freq


pattern = command.PositionPattern.position_pattern_v1(10., 2.)
command = command.PositionCommand(pattern, [0.,0.,0.], 0., 10.)

last_time = time.time()

while (1):
    
    while (time.time() - last_time < dt):
        continue
    
    last_time = time.time()
    x, y, z = command.next_command()
    FL_leg.set_position(x, y, z, duration = dt)    
    
    
    
    
    
jr.compliant = False


command_freq = 20.
dt = 1. / command_freq

horiz_amp = 7.
vert_amp = 2.5
x0 = 3.
z0 = -8
y0_front = 9.
y0_back = 2.
T = 1.


patternFL = PositionPattern.position_pattern_v1(horiz_amp, vert_amp)
commandFL = PositionCommand(patternFL, [x0, y0_front, z0], -np.pi/2., T)

patternBL = PositionPattern.position_pattern_v1(horiz_amp, vert_amp, cursor = 0.5)
commandBL = PositionCommand(patternBL, [x0, y0_back, z0], -np.pi/2., T)

patternBR = PositionPattern.position_pattern_v1(horiz_amp, vert_amp)
commandBR = PositionCommand(patternBR, [x0, y0_back, z0], -np.pi/2., T)

patternFR = PositionPattern.position_pattern_v1(horiz_amp, vert_amp, cursor = 0.5)
commandFR = PositionCommand(patternFR, [x0, y0_front, z0], -np.pi/2., T)


while (1):
    x, y, z = commandFL.next_command()
    FL_leg.set_position(x, y, z, duration = dt)
    
    x, y, z = commandBL.next_command()
    BL_leg.set_position(x, y, z, duration = dt)
    
    x, y, z = commandBR.next_command()
    BR_leg.set_position(x, y, z, duration = dt)
    
    x, y, z = commandFR.next_command()
    FR_leg.set_position(x, y, z, duration = dt)
    
    time.sleep(dt)
    





