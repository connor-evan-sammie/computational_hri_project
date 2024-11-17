# servo_server.py
import socket
from gpiozero import AngularServo
from time import sleep

# Set up the GPIO pins for the servos
servo1 = AngularServo(17, min_angle=-90, max_angle=90)
servo2 = AngularServo(18, min_angle=-90, max_angle=90)
servo3 = AngularServo(27, min_angle=-90, max_angle=90)
servo4 = AngularServo(22, min_angle=-90, max_angle=90)

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
                    if len(angles) == 4:
                        servo1.angle = angles[0]
                        servo2.angle = angles[1]
                        servo3.angle = angles[2]
                        servo4.angle = angles[3]

                        print(f'Set angles to: {angles}')
                    else:
                        print(f'Unexpected number of angles received: {angles}')
                except ValueError as e:
                    print(f'Error decoding angles: {e}')