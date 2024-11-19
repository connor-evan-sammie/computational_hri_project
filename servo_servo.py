# servo_server.py
import socket
from gpiozero import AngularServo as Servo
from time import sleep

# Set up the GPIO pins for the servos
leftWing = Servo(14, min_angle= -30, max_angle= 150, min_pulse_width=0.0005, max_pulse_width=0.0024)
rightWing = Servo(15, min_angle= 150, max_angle= -30, min_pulse_width=0.0005, max_pulse_width=0.0024)
headPitch = Servo(2, min_angle = 125, max_angle = -95, min_pulse_width=0.0005, max_pulse_width=0.0024)
headYaw = Servo(3, min_angle = 80, max_angle = -100, min_pulse_width=0.0005, max_pulse_width=0.0024)

leftWing.angle = 0
rightWing.angle = 0
headPitch.angle = 0
headYaw.angle = 0

# Set up the server
HOST = '0.0.0.0'  # Listen on all available interfaces
PORT = 65432
BUFFER_SIZE = 1024

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f'Server listening on {HOST}:{PORT}')

    while True:
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(BUFFER_SIZE)
                if not data:
                    break

                # Assume the data is a comma-separated string of angles for the servos
                try:
                    angles = list(map(float, data.decode().split(',')))
                    print(angles)
                    if len(angles) == 4:
                        leftWing.angle = angles[0]
                        rightWing.angle = angles[1]
                        headPitch.angle = angles[2]
                        headYaw.angle = angles[3]

                        print(f'Set angles to: {angles}')
                    else:
                        print(f'Unexpected number of angles received: {angles}')
                except ValueError as e:
                    print(f'Error decoding angles: {e}')