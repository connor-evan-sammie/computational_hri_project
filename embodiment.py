import os
import platform
import time

# send_servo_positions.py
import socket

# Replace with the IP address of your Raspberry Pi
HOST = '67.194.42.62'
PORT = 65432

class Embodiment:
    def __init__(self):
        os.environ["GPIOZERO_PIN_FACTORY"] = "pigpio"
        #self.leftWing = Servo(14, min_angle= -30, max_angle= 150, min_pulse_width=0.0005, max_pulse_width=0.0024)
        #self.rightWing = Servo(15, min_angle= 150, max_angle= -30, min_pulse_width=0.0005, max_pulse_width=0.0024)
        #self.headPitch = Servo(2, min_angle = 105, max_angle = -75, min_pulse_width=0.0005, max_pulse_width=0.0024)
        #self.headYaw = Servo(3, min_angle = 80, max_angle = -100, min_pulse_width=0.0005, max_pulse_width=0.0024)
        
        self.toNeutral()
    
    def toNeutral(self):
        self.setPose([0, 0, 0, 0])

    def setLeftWing(self, degrees):
        if degrees > 150:
            degrees = 150
        if degrees < -30:
            degrees = -30
        self.leftWingDegrees = degrees

    def setRightWing(self, degrees):
        if degrees > 150:
            degrees = 150
        if degrees < -30:
            degrees = -30
        self.rightWingDegrees = degrees

    def setHeadPitch(self, degrees):
        if degrees > 40:
            degrees = 40
        if degrees < -20:
            degrees = -20
        self.headPitchDegrees = degrees

    def setHeadYaw(self, degrees):
        if degrees > 80:
            degrees = 80
        if degrees < -100:
            degrees = -100
        self.headYawDegrees = degrees

    def setPose(self, pose):
        self.setLeftWing(pose[0])
        self.setRightWing(pose[1])
        self.setHeadYaw(pose[2])
        self.setHeadPitch(pose[3])
        self.send_servo_positions()

    def send_servo_positions(self):
        positions = self.getPose()
        data = ','.join(map(str, positions))

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((HOST, PORT))
                s.sendall(data.encode())
                #print(f'Sent servo positions: {positions}')
        except ConnectionRefusedError:
            print("Could not connect to the duck")

    def getLeftWing(self): return self.leftWingDegrees
    def getRightWing(self): return self.rightWingDegrees
    def getHeadPitch(self): return self.headPitchDegrees
    def getHeadYaw(self): return self.headYawDegrees

    def getPose(self): return [self.getLeftWing(), self.getRightWing(), self.getHeadYaw(), self.getHeadPitch()]

if __name__ == "__main__":
    duck = Embodiment()
    duck.setPose([0, 0, 0, 0])
    time.sleep(1)
    duck.setPose([90, 0, 0, 0])
    time.sleep(1)
    duck.setPose([0, 90, 0, 0])
    time.sleep(1)
    duck.setPose([0, 0, 0, 0])
    #while cmd != "q":
    #    if cmd != "":
    #        args = cmd.split()
    #        if len(args) == 2:
    #            args[1] = int(args[1])
    #            if args[0] == "l":
    #                duck.setLeftWing(args[1])
    #            elif args[0] == "r":
    #                duck.setRightWing(args[1])
    #            elif args[0] == "p":
    #                duck.setHeadPitch(args[1])
    #            elif args[0] == "y":
    #                duck.setHeadYaw(args[1])
    #            else:
    #                print(f"Invalid command: {cmd}")
    #        else:
    #            print(f"Invalid command: {cmd}")
    #    print(f"l: {duck.getLeftWing()}, r: {duck.getRightWing()}, y: {duck.getHeadYaw()}, p: {duck.getHeadPitch()}")
    #    cmd = input()
