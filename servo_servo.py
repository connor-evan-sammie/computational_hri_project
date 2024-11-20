# servo_server.py
import socket
#from gpiozero import AngularServo as Servo
from time import sleep
import gesticulator
from embodiment import Embodiment

body = Embodiment()


# Set up the GPIO pins for the servos
#leftWing = Servo(14, min_angle= -30, max_angle= 150, min_pulse_width=0.0005, max_pulse_width=0.0024)
#rightWing = Servo(15, min_angle= 150, max_angle= -30, min_pulse_width=0.0005, max_pulse_width=0.0024)
#headPitch = Servo(2, min_angle = 85, max_angle = -95, min_pulse_width=0.0005, max_pulse_width=0.0024)
#headYaw = Servo(3, min_angle = 80, max_angle = -100, min_pulse_width=0.0005, max_pulse_width=0.0024)

#leftWing.angle = 0
#rightWing.angle = 0
#headPitch.angle = 0
#headYaw.angle = 0

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
                    action_func = getattr(gesticulator, data.decode("utf-8"))
                    action_func(body)
                    conn.sendall("done".encode()) # Tell the computer that it finished
                    
                except ValueError as e:
                    print(f'Error decoding angles: {e}')