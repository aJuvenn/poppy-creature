from numpy import sum
from functools import partial

from pypot.creatures import AbstractPoppyCreature
from pypot.creatures.ik import IKChain

from .primitives.dance import Dance
from .primitives.truc import FunLed
from .primitives.face_tracking import FaceTracking
from .primitives.tracking_feedback import TrackingFeedback
from .primitives.postures import (DiploPosture, BasePosture, RestPosture,
                                  CuriousPosture, TetrisPosture,
                                  SafePowerUp)

from .primitives.DiploMoveForward import DiploMoveForward
from .primitives.DiploTurnLeft import DiploTurnLeft
from .primitives.DiploTurnRight import DiploTurnRight


class PoppyErgoJr(AbstractPoppyCreature):
    @classmethod
    def setup(cls, robot):
        robot._primitive_manager._filter = partial(sum, axis=0)


        
        robot.attach_primitive(DiploMoveForward(robot), "diplo_move_forward")
        robot.attach_primitive(DiploTurnLeft(robot), "diplo_turn_left")
        robot.attach_primitive(DiploTurnRight(robot), "diplo_turn_right")
        
        robot.attach_primitive(DiploPosture(robot, 1.), 'diplo_posture')
        

        if not robot.simulated and hasattr(robot, 'marker_detector'):
            robot.attach_primitive(TrackingFeedback(robot, 25.),
                                   'tracking_feedback')

        for m in robot.motors:
            m.pid = (4, 2, 0)
            m.torque_limit = 70.
            m.led = 'off'

        if not robot.simulated and hasattr(robot, 'face_tracking'):
            robot.attach_primitive(FaceTracking(robot, 10,
                                                robot.face_detector),
                                   'face_tracking')
