import io
import json
import logging
import os
import sys
import threading
import time
from datetime import datetime

import dotenv
import picamera
import requests
import serial
from flask import Flask, abort
from flask import jsonify, send_file, request

current_status = 'cmd_open'

app = Flask(__name__)


@app.errorhandler(404)
def not_found(error):
    logging.error(f'Wrong Route: \'{request.path}\' requested from {request.remote_addr}')
    abort(404)


@app.route('/status')
def status():
    logging.info(f'Status: {current_status} requested from {request.remote_addr}')
    return jsonify({'status': current_status})


@app.route('/photo/<string:message>')
def photoHandler(message):
    logging.info(f'Command: \'{message}\' requested from {request.remote_addr}')

    if message == 'cmd_photo':
        stream = io.BytesIO()

        with picamera.PiCamera() as camera:
            camera.resolution = (640, 480)
            camera.capture(stream, format='jpeg')

        image = stream.getvalue()
        timestamp = datetime.now()
        filename = timestamp.isoformat()
        path = 'images/' + filename
        save_image(image, path)
        logging.info(f'File: {filename} saved')
        logging.info(f'File: {filename} sent to {request.remote_addr}')
        return send_file(io.BytesIO(image), mimetype='image/jpeg')
    elif message == 'cmd_recent':
        filename = get_newest_file("images/")
        if filename is None:
            logging.error(f'No images found')
            abort(404)
        else:
            file = open("images/" + filename, 'rb')
            image = file.read()
            logging.info(f'File: {filename} sent to {request.remote_addr}')
            return send_file(io.BytesIO(image), mimetype='image/jpeg')
    else:
        abort(400)


# Sends commands to Arduino
@app.route('/arduino/<string:message>')
def toArduino(message):
    client_ip = request.remote_addr
    logging.info(f'Command: \'{message}\' requested from {client_ip}')
    if message == "cmd_open" or message == "cmd_close":
        global current_status
        # Log the command
        current_status = message
        arduino.flush()
        time.sleep(0.1)

        if arduino.isOpen():
            arduino.write(message.encode())

        return jsonify({'status': current_status})
    else:
        abort(400)


def get_newest_file(folder_path):
    files = os.listdir(folder_path)
    if not files:
        return None

    files.sort(key=lambda x: os.path.getmtime(os.path.join(folder_path, x)))

    newest_file = files[-1]
    return newest_file


def save_image(image, path):
    file = open(path, 'wb')
    file.write(image)
    file.close()


def handle_detected():
    while True:
        while arduino.inWaiting() == 0: pass

        if arduino.inWaiting() > 0:
            command = arduino.readline()
            arduino.flushInput()  # remove data after reading

        command = command.decode().replace('\r', '').replace('\n', '')

        logging.info(f'Command \'{command}\' got from Arduino')

        if command == "cmd_detected":
            logging.info("Movement detected")
            send_notification('trap', 'Trap Movement', 'Movement detected in trap')
        if command == "cmd_autoclose":
            send_notification('trap', 'Trap Timeout', 'Trap closed due to timeout')
            logging.info("Automatic closing due to timeout")
            global status
            status = 'cmd_close'


def send_notification(topic, title, body):
    global token
    if token is None:
        logging.error('No token found')
        return

    data = {
        "message": {
            "topic": topic,
            "notification": {
                "title": title,
                "body": body,
            }
        }
    }
    data = json.dumps(data)

    response = requests.post('https://fcm.googleapis.com/v1/projects/msi-ses2223-g06/messages:send', headers={
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json',
    }, data=data)

    logging.info(f'Notification to {topic} with title: {title} and body: {body} with response: {response.status_code}')


def refresh_token():
    rt = os.getenv('FCM_REFRESH_TOKEN')
    headers = {
        'Content-Type': 'application/json',
    }
    data = {
        "token_uri": "https://oauth2.googleapis.com/token",
        "refresh_token": rt,
    }
    data = json.dumps(data)
    response = requests.post('https://developers.google.com/oauthplayground/refreshAccessToken', headers=headers, data=data)
    if response.status_code == 200:
        return response.json()['access_token']
    else:
        return None


if __name__ == '__main__':
    logging.basicConfig(filename='logs/accesses.log', level=logging.INFO)
    dotenv.load_dotenv()
    token = refresh_token()
    arduino = serial.Serial(sys.argv[1], 9600)
    thread = threading.Thread(target=handle_detected)
    thread.deamon = True
    thread.start()
    app.run(host='0.0.0.0', port=8000, debug=True)
