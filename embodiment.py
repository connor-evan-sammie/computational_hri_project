from piservo import Servo

class Embodiment:
    def __init__(self):
        self.leftWing = Servo(0)
        self.rightWing = Servo(1)
        self.headPitch = Servo(2)
        self.headYaw = Servo(3)
    
    def toNeutral(self):
        self.setLeftWing(0)
        self.setRightWing(0)
        self.setHeadPitch(0)
        self.setHeadYaw(0)

    def setLeftWing(self, degrees):
        self.leftWing.write(180 - degrees)

    def setRightWing(self, degrees):
        self.rightWing.write(degrees)

    def setHeadPitch(self, degrees):
        self.headPitch.write(degrees + 90)

    def setHeadYaw(self, degrees):
        self.headYaw.write(degrees + 90)