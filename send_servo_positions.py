# send_servo_positions.py
import socket

# Replace with the IP address of your Raspberry Pi
HOST = '67.194.42.62'
PORT = 65432

def send_servo_positions(gesture):
    #data = ','.join(map(str, positions))

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        #s.sendall(data.encode())
        s.sendall(gesture.encode())
        data = s.recv(1024)
        #print(f'Sent servo gesture: {gesture}')

if __name__ == "__main__":
    # Example servo positions to send
    servo_positions = "horizontal_nod"
    send_servo_positions(servo_positions)
    send_servo_positions("neutral")
    send_servo_positions(servo_positions)
    send_servo_positions("neutral")
    send_servo_positions(servo_positions)
    send_servo_positions("neutral")
    send_servo_positions(servo_positions)
    send_servo_positions("neutral")
    send_servo_positions(servo_positions)
    send_servo_positions("neutral")
    send_servo_positions(servo_positions)
    send_servo_positions("neutral")