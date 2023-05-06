import mysql.connector
import io
from datetime import datetime
import picamera
import time

def updateDatabase(byte_sequence, timestamp):
    # Insert the data into the table
    sql = "INSERT INTO images (image, timestamp) VALUES (%s, %s)"
    val = (byte_sequence, timestamp)
    cursor.execute(sql, val)

    # Commit the changes and close the connection
    cnx.commit()

def getPhoto(id):
    # Execute a SELECT statement to retrieve the photo bytes
    query = ("SELECT image, timestamp FROM images WHERE id = %s")
    cursor.execute(query, (id,))

    result = cursor.fetchone()

    if result:
        return (result[0], result[1])

    raise Exception("No photo found for the given id:{}!".format(id))

# Connect to the database
cnx = mysql.connector.connect(user="se2223", password="1234", database='se2223')
cursor = cnx.cursor()

stream = io.BytesIO()

with picamera.PiCamera() as camera:
    camera.resolution = (640, 480)
    time.sleep(2)
    camera.capture(stream, format='jpeg')

byte_sequence = stream.getvalue()
timestamp = datetime.now()

updateDatabase(byte_sequence, timestamp)

try:
    bytes, times = getPhoto(3)

    with open(f'RaspberryPi/images/photo.jpg', 'wb') as f:
        f.write(bytes)

    print(times)
except Exception as e:
    print(e)

cursor.close()
cnx.close()
