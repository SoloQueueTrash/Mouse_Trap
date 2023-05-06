from flask import Flask
from flask import jsonify, send_file, request
import io
from datetime import datetime
import picamera
import time
import serial

closed = True
picture_path = None

# Create Arduino connection
arduino = serial.Serial("/dev/ttyACM0", 9600, timeout = 1)

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


@app.route('/status')
def status():
    return jsonify({'status': 'closed' if closed else 'open'})

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

        write_logs(f'File: {filename} sent to {client_ip}')
        
        return send_file(io.BytesIO(image), mimetype='image/jpeg')
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

        # returns "Not a valid command" if the command is wrong
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)