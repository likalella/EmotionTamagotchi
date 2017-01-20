import os
import sys
import socket
import json
import datetime
import RPi.GPIO as GPIO
import requests
from picamera import PiCamera

# inis camera
camera = PiCamera()
GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.IN)

# init socket
HOST = '203.253.23.52'
PORT = 9000
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# init api requests
endpoint = 'https://westus.api.cognitive.microsoft.com/emotion/v1.0/recognize'
api_key = 'api_key'
headers = {
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': api_key,
}


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
            photo_name = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+ '.jpg'
            camera.capture(photo_name)
            photo_name = os.path.join(os.getcwd(), photo_name)
            image_binary = open(photo_name, 'rb').read()
            max_emotion = ''
            response = requests.post(url=endpoint, data=image_binary, headers=headers)
            try:
                json_object = json.loads(response.text)[0]
                emotion_list = json_object['scores']
                max_emotion = max(json_object['scores'], key=json_object['scores'].get)
            except:
                pass

            emotion_number = 4
            if max_emotion == 'anger':
                emotion_number = 2
            elif max_emotion == 'contempt':
                emotion_number = 7
            elif max_emotion == 'disgust':
                emotion_number = 5
            elif max_emotion == 'fear':
                emotion_number = 6
            elif max_emotion == 'happiness':
                emotion_number = 0
            elif max_emotion == 'neutral':
                emotion_number = 4 
            elif max_emotion == 'sadness':
                emotion_number = 1
            elif max_emotion == 'surprise':
                emotion_number = 3
            print max_emotion
            conn.send(str(emotion_number))

except KeyboardInterrupt:
    GPIO.cleanup()

conn.close()
server_socket.close()
