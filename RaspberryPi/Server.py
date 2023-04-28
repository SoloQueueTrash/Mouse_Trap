import socket
import mysql.connector
import io
from datetime import datetime
import picamera
import config
import time
import serial

def removeChar(argument):
    argument = argument.replace('\r','')
    argument =  argument.replace('\n','')
    return argument

def stateToApp(argument, client_socket):
    if(argument == config.STATE_OPEN or argument == config.STATE_CLOSE):
        print(f"Sending {argument} to Android.")
        argument = argument + '\n'
        client_socket.send(argument.encode())
        return 1
    
    return -1

def handlerFromApp(argument, arduino, client_socket):
    if(argument == config.PHOTO):
        sendPhoto(client_socket)
        return 1

    if(argument == config.STATE or argument == config.CLOSE or argument == config.OPEN):
        response = sendToArduino(argument, arduino)
        print(f"Sending {argument} to Arduino.")

        response2 = "state_" + response.split('_')[1]
        stateToApp(response2, client_socket)
        return 1

    return -1

# Send the picture bytes to Android Server
def sendPhoto(client_socket):
    stream = io.BytesIO()
    print("Taking picture ...")

    with picamera.PiCamera() as camera:
        camera.resolution = (640, 480)
        camera.capture(stream, format='jpeg')

    byte_sequence = stream.getvalue()
    timestamp = datetime.now()
    
    #sql = "INSERT INTO images (image, timestamp) VALUES (%s, %s)"
    #val = (byte_sequence, timestamp)
    #cursor.execute(sql, val)

    #cnx.commit()

    client_socket.sendall(byte_sequence)
    print("Photo sent ...")


# Query specific photo by its id
def getPhoto(id):
    query = ("SELECT image, timestamp FROM images WHERE id = %s")
    cursor.execute(query, (id,))
    result = cursor.fetchone()

    if result is not None:
        return (result[0], result[1])

    raise Exception("Query error!")

def sendToArduino(message, arduino):
    arduino.flush() # flush any existing data in the input buffer
    time.sleep(0.1) #wait for serial to opens
    if arduino.isOpen():
        arduino.write(message.encode())
        #time.sleep(0.1) #wait for arduino to answer
        while arduino.inWaiting() == 0: pass
        if  arduino.inWaiting() > 0: 
            answer = arduino.readline()
            arduino.flushInput() #remove data after reading
    answer = removeChar(answer.decode())
    return answer

# Create Arduino connection
arduino = serial.Serial("/dev/ttyACM0", 9600, timeout = 1)

# Connect to the database
cnx = mysql.connector.connect(user = config.USER, password = config.PASSWORD, database = config.DATABASE)
cursor = cnx.cursor()

# Create a socket object to connect to Android App
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind((config.IP_ADDRESS, config.PORT))
server_socket.listen()

print(f"Server listening on {config.IP_ADDRESS}:{config.PORT}")

while True:
    client_socket, client_address = server_socket.accept()

    print(f"Java client connected from {client_address[0]}:{client_address[1]}")

    while True:
        data = removeChar(client_socket.recv(1024).decode())

        # break the loop if no data is received
        if not data:
            break
        
        print(f"Receiving {data} from Android.")

        if(data == "exit"):
            response = "Closing socket ..."
            client_socket.send(response.encode())
            print(response)
            break

        data = handlerFromApp(data, arduino, client_socket)
        print()

    client_socket.close()
