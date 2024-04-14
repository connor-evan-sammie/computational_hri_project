from gpiozero import AngularServo as Servo
import os
import time

DEBUG = True

class Embodiment:
    def __init__(self):
        os.environ["GPIOZERO_PIN_FACTORY"] = "pigpio"
        self.leftWing = Servo(14, min_angle=-30, max_angle=150, min_pulse_width=0.0005, max_pulse_width=0.0024)
        self.rightWing = Servo(15, min_angle=150, max_angle=-30, min_pulse_width=0.0005, max_pulse_width=0.0024)
        self.headPitch = Servo(2, min_angle = 90, max_angle = -90, min_pulse_width=0.0005, max_pulse_width=0.0024)
        self.headYaw = Servo(3, min_angle = 90, max_angle = -90, min_pulse_width=0.0005, max_pulse_width=0.0024)
        self.toNeutral()
    
    def toNeutral(self):
        self.setLeftWing(0)
        self.setRightWing(0)
        self.setHeadPitch(0)
        self.setHeadYaw(0)

    def setLeftWing(self, degrees):
        #if not (-25 <= degrees <= 155) and not DEBUG:
        #    print("Invalid angle! Range limited to [-25, 155]")
        #    return
        self.leftWingDegrees = degrees
        #self.leftWing.angle = (self.leftWingDegrees+25)
        self.leftWing.angle = (self.leftWingDegrees)

    def setRightWing(self, degrees): # down to -25, up to 155
        #if not (-25 <= degrees <= 155) and not DEBUG:
        #    print("Invalid angle! Range limited to [-25, 155]")
        #    return
        self.rightWingDegrees = degrees
        self.rightWing.angle = (self.rightWingDegrees) 
        #self.rightWing.angle = (180 - (self.rightWingDegrees+25)) 

    def setHeadPitch(self, degrees):
        if not (-30 <= degrees <= 40) and not DEBUG:
            print("Invalid angle! Range limited to [-30, 40]")
            return
        self.headPitchDegrees = degrees
        self.headPitch.angle = (self.headPitchDegrees)

    def setHeadYaw(self, degrees):
        #if not (-90 <= degrees <= 90) and not DEBUG:
        #    print("Invalid angle! Range limited to [-90, 90]")
        #    return
        self.headYawDegrees = degrees
        self.headYaw.angle = (self.headYawDegrees)

    def setPose(self, pose):
        self.setLeftWing(pose[0])
        self.setRightWing(pose[1])
        self.setHeadYaw(pose[2])
        self.setHeadPitch(pose[3])

    def getLeftWing(self): return self.leftWingDegrees
    def getRightWing(self): return self.rightWingDegrees
    def getHeadPitch(self): return self.headPitchDegrees
    def getHeadYaw(self): return self.headYawDegrees

    def getPose(self): return [self.getLeftWing(), self.getRightWing(), self.getHeadYaw(), self.getHeadPitch()]

if __name__ == "__main__":
    duck = Embodiment()
    #duck.toNeutral()
    cmd = ""
    while cmd != "q":
        if cmd != "":
            args = cmd.split()
            if len(args) == 2:
                args[1] = int(args[1])
                if args[0] == "l":
                    duck.setLeftWing(args[1])
                elif args[0] == "r":
                    duck.setRightWing(args[1])
                elif args[0] == "p":
                    duck.setHeadPitch(args[1])
                elif args[0] == "y":
                    duck.setHeadYaw(args[1])
                else:
                    print(f"Invalid command: {cmd}")
            else:
                print(f"Invalid command: {cmd}")
        print(f"l: {duck.getLeftWing()}, r: {duck.getRightWing()}, p: {duck.getHeadPitch()}, y: {duck.getHeadYaw()}")
        cmd = input()
