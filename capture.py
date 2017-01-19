import sys
import time
import RPi.GPIO as GPIO
from picamera import PiCamera

HOST = '203.253.23.14'
PORT = 9000
camera = PiCamera()
GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.IN)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

try:
    server_socket.bind((HOST, PORT))
except:
    print("Fail to bind")
    sys.exit()

print("Start Server")
server_socket.listen(5)
conn, addr = server_socket.accept()
print("Connect to client")

try:
    while True:
        if GPIO.input(21) == 0:
            camera.capture('image.jpg')

except KeyboardInterrupt:
    GPIO.cleanup()

conn.close()
server_socket.close()
