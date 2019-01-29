from pypot.primitive import LoopPrimitive


class FunLed(LoopPrimitive):
    
    
    def setup(self):
        for m in self.robot.motors:
            m.compliant = True
    
    def update(self):
            for m in self.robot.motors:
                if(m.led == 'green'):
                    m.led="blue"
                else:
                    m.led="green"