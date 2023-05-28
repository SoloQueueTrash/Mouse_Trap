from flask import Flask
from flask import jsonify, send_file, request
import io
from datetime import datetime
import picamera
import time
import serial
import requests
import sys 

closed = True
picture_path = None
clients = []
recentPhoto = ""
 
api_key = 'AAAAMHMssHI:APA91bEW7enKmz6XH0FtAUPvce7ggJTLCF--QQiFnNw43lyIGAmXnBMfptSKqHxSoTGYkLB5ncQE36ko9WqWdbMQQ7iKtmNXh3lmms7V1_X6eGSHucMvaQai6ejD0_9NppPoddKeXUrd'


# Create Arduino connection
arduino = None #serial.Serial("/dev/ttyACM1", 9600)

app = Flask(__name__)

@app.errorhandler(404)
def not_found(error):
    path = request.path
    client_ip = request.remote_addr
    
    write_logs(f'Wrong Route: \'{path}\' requested from {client_ip}')

    return jsonify({'status': '404', 'message': 'Route Not Found'})

@app.route('/toggle')
def toggle():
    global closed
    closed = not closed # Fazer coisas na rasp
    return jsonify({'status': 'ok'})


@app.route('/hello')
def status():
    client_ip = request.remote_addr
    clients.append(client_ip)
    return jsonify({'status': 'ok' , 'message' : 'Hello'})

# Sends commands to Arduino
@app.route('/sendCommand/<string:message>')
def sendToArduino(message):
    client_ip = request.remote_addr
    write_logs(f'Command: \'{message}\' requested from {client_ip}')

    if(message == 'cmd_photo'):
        stream = io.BytesIO()

        with picamera.PiCamera() as camera:
            camera.resolution = (640, 480)
            camera.capture(stream, format='jpeg')

        image = stream.getvalue()
        timestamp = datetime.now()
        filename = str(timestamp.day) + '-' +  str(timestamp.month) + '-' + str(timestamp.year) + '_'+ str(timestamp.hour) + ':' + str(timestamp.minute) + ':' + str(timestamp.second) + '.jpeg'
        path = 'images/' + filename

        save_image(image, path)
        
        recentPhoto = path

        write_logs(f'File: {filename} sent to {client_ip}')
        
        return send_file(io.BytesIO(image), mimetype='image/jpeg')
    elif(message == 'cmd_recentPhoto'):
        if(recentPhoto == ''):
            return jsonify({'status': '404', 'message': 'Photo Not Found'})
        else:
            file = open(recentPhoto, 'rb')
            imageB = file.read()
            return send_file(io.BytesIO(imageB), mimetype='image/jpeg')
    else:
        arduino.flush() # flush any existing data in the input buffer
        time.sleep(0.1) #wait for serial to opens

        if arduino.isOpen():
            arduino.write(message.encode())
            #time.sleep(0.1) #wait for arduino to answer
            while arduino.inWaiting() == 0: pass

            if  arduino.inWaiting() > 0: 
                answer = arduino.readline()
                arduino.flushInput() #remove data after reading

        answer = answer.decode().replace('\r','').replace('\n','')

        write_logs(f'Command \'{answer}\' returned from Arduino')

        return jsonify({'status': 'ok', 'message': answer})


def save_image(image, path):
    file = open(path, 'wb')
    file.write(image)
    file.close()

def write_logs(message):
    file = open('logs/accesses.log', 'a')
    now = datetime.now()
    file.write('[' + str(now) + ']' +': '+ message + '\n')
    file.close()

def handle_detected():
    while(True):
        while arduino.inWaiting() == 0: pass

        if  arduino.inWaiting() > 0: 
            command = arduino.readline().decode().replace('\r','').replace('\n','')
            arduino.flushInput() #remove data after reading

            print("comand = " + command)
            if(command == "cmd_detected"):
                write_logs(f'Command \'{command}\' got from Arduino')
                print(jsonify({'status': 'ok', 'message': 'cmd_detect'}))
                requests.post(
                    'https://fcm.googleapis.com/v1/projects/myproject-b5ae1/messages:send',
                    headers={
                        'Content-Type': 'application/json',
                        'Authorization': f'Bearer {api_key}'
                    },
                    json={
                        "message": {
                            "topic": "foo-bar",
                            "notification": {
                                "body": "This is a Firebase Cloud Messaging Topic Message!",
                                "title": "FCM Message"
                            }
                        }
                    }
                )

import threading
if __name__ == '__main__':

    arduino = serial.Serial(sys.argv[1], 9600)

    thread = threading.Thread(target=handle_detected)
    thread.deamon =True
    thread.start()

    app.run(host='0.0.0.0', port=8308, debug=True)
