from flask import Flask
from flask import jsonify
#import mysql.connector
import io
from datetime import datetime
#import picamera
import config
import time
import serial

closed = True
picture_path = None

# Create Arduino connection
#arduino = serial.Serial("/dev/ttyACM0", 9600, timeout = 1)

# Connect to the database
#cnx = mysql.connector.connect(user = config.USER, password = config.PASSWORD, database = config.DATABASE)
#cursor = cnx.cursor()

app = Flask(__name__)


@app.route('/toggle')
def toggle():
    global closed
    closed = not closed # Fazer coisas na rasp
    return jsonify({'status': 'ok'})


@app.route('/status')
def status():
    return jsonify({'status': 'closed' if closed else 'open'})


@app.route('/take_picture')
def sendPhoto():
    # stream = io.BytesIO()
    # print("Taking picture ...")

    # with picamera.PiCamera() as camera:
    #     camera.resolution = (640, 480)
    #     camera.capture(stream, format='jpeg')

    # byte_sequence = stream.getvalue()
    # timestamp = datetime.now()
    
    #sql = "INSERT INTO images (image, timestamp) VALUES (%s, %s)"
    #val = (byte_sequence, timestamp)
    #cursor.execute(sql, val)

    #cnx.commit()
    return jsonify({'status': 'ok', 'message': 'Photo taken'})


@app.route('/picture')
def picture():
    return jsonify({'picture_path': picture_path})

def removeChar(argument):
    argument = argument.replace('\r','')
    argument =  argument.replace('\n','')
    return argument

@app.route('/sendCommand/<string:message>')
def sendToArduino(message, arduino):
    # arduino.flush() # flush any existing data in the input buffer
    # time.sleep(0.1) #wait for serial to opens

    # if arduino.isOpen():
    #     arduino.write(message.encode())
    #     #time.sleep(0.1) #wait for arduino to answer
    #     while arduino.inWaiting() == 0: pass

    #     if  arduino.inWaiting() > 0: 
    #         answer = arduino.readline()
    #         arduino.flushInput() #remove data after reading

    # answer = removeChar(answer.decode())
    answer = "nigger"
    return jsonify({'status': 'ok', 'message': answer})

if __name__ == '__main__':
    app.run(host='localhost', port=8001, debug=True)