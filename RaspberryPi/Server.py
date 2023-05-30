import io
import os
import sys
import threading
import time
from datetime import datetime

import picamera
import serial
from flask import Flask
from flask import jsonify, send_file, request

current_status = 'cmd_open'

app = Flask(__name__)


@app.errorhandler(404)
def not_found(error):
    path = request.path
    client_ip = request.remote_addr
    write_logs(f'Wrong Route: \'{path}\' requested from {client_ip}')
    return jsonify({'status': '404', 'message': 'Route Not Found'})


@app.route('/status')
def status():
    client_ip = request.remote_addr
    global current_status
    write_logs(f'Status: {current_status} requested from {client_ip}')
    return jsonify({'status': current_status})


@app.route('/photo/<string:message>')
def photoHandler(message):
    client_ip = request.remote_addr
    write_logs(f'Command: \'{message}\' requested from {client_ip}')

    if message == 'cmd_photo':
        stream = io.BytesIO()

        with picamera.PiCamera() as camera:
            camera.resolution = (640, 480)
            camera.capture(stream, format='jpeg')

        image = stream.getvalue()
        timestamp = datetime.now()
        filename = str(timestamp.day) + '-' + str(timestamp.month) + '-' + str(timestamp.year) + '_' + str(
            timestamp.hour) + ':' + str(timestamp.minute) + ':' + str(timestamp.second) + '.jpeg'
        path = 'images/' + filename

        save_image(image, path)
        write_logs(f'File: {filename} sent to {client_ip}')

        return send_file(io.BytesIO(image), mimetype='image/jpeg')
    elif message == 'cmd_recent':
        fileA = get_newest_file("images/")
        if fileA is None:
            return jsonify({'status': '404', 'message': 'Photo Not Found'})
        else:
            file = open("images/" + fileA, 'rb')
            imageB = file.read()
            return send_file(io.BytesIO(imageB), mimetype='image/jpeg')
    else:
        return jsonify({'status': '404', 'message': 'Invalid Command'})


# Sends commands to Arduino
@app.route('/arduino/<string:message>')
def toArduino(message):
    client_ip = request.remote_addr
    write_logs(f'Command: \'{message}\' requested from {client_ip}')
    if message == "cmd_open" or message == "cmd_close":
        global current_status
        current_status = message
        print("CURRET STATUS = " + current_status)
        arduino.flush()
        time.sleep(0.1)

        if arduino.isOpen():
            arduino.write(message.encode())

        return jsonify({'status': current_status})
    else:
        return jsonify({'status': '404', 'message': 'Invalid Command'})


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


def write_logs(message):
    file = open('logs/accesses.log', 'a')
    now = datetime.now()
    file.write('[' + str(now) + ']' + ': ' + message + '\n')
    file.close()


def handle_detected():
    while True:
        while arduino.inWaiting() == 0: pass

        if arduino.inWaiting() > 0:
            command = arduino.readline()
            arduino.flushInput()  # remove data after reading

        command = command.decode().replace('\r', '').replace('\n', '')

        write_logs(f'Command \'{command}\' got from Arduino')
        print("COMMAND = " + command)

        if command == "cmd_detected":
            print("DETECTED")
        if command == "cmd_autoclose":
            global status
            status = 'cmd_close'
            print("AUTOCLOSE")


arduino = serial.Serial(sys.argv[1], 9600)
thread = threading.Thread(target=handle_detected)
thread.deamon = True
thread.start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
