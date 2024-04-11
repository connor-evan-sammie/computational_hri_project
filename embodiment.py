from gpiozero import AngularServo as Servo
import time

class Embodiment:
    def __init__(self):
        self.leftWing = Servo(14, min_angle=-180, max_angle=180)
        self.rightWing = Servo(15, min_angle=-180, max_angle=180)
        self.headPitch = Servo(2, min_angle=-180, max_angle=180)
        self.headYaw = Servo(3, min_angle=-180, max_angle=180)
        self.toNeutral
    
    def toNeutral(self):
        self.setLeftWing(0)
        self.setRightWing(0)
        self.setHeadPitch(0)
        self.setHeadYaw(0)

    def setLeftWing(self, degrees):
        if not (-25 <= degrees <= 155):
            print("Invalid angle! Range limited to [-25, 155]")
            return
        self.leftWingDegrees = degrees
        self.leftWing.angle = (self.leftWingDegrees+25)

    def setRightWing(self, degrees): # down to -25, up to 155
        if not (-25 <= degrees <= 155):
            print("Invalid angle! Range limited to [-25, 155]")
            return
        self.rightWingDegrees = degrees
        self.rightWing.angle = (180 - (self.rightWingDegrees+25)) 

    def setHeadPitch(self, degrees):
        if not (-10 <= degrees <= 25):
            print("Invalid angle! Range limited to [-10, 25]")
            return
        self.headPitchDegrees = degrees
        self.headPitch.angle = (180 - self.headPitchDegrees - 90)

    def setHeadYaw(self, degrees):
        if not (-90 <= degrees <= 90):
            print("Invalid angle! Range limited to [-90, 90]")
            return
        self.headYawDegrees = degrees
        self.headYaw.angle = (180 - self.headYawDegrees - 90)

    def getLeftWing(self): return self.leftWingDegrees
    def getRightWing(self): return self.rightWingDegrees
    def getHeadPitch(self): return self.headPitchDegrees
    def getHeadYaw(self): return self.headYawDegrees

if __name__ == "__main__":
    duck = Embodiment()
    duck.toNeutral()
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
