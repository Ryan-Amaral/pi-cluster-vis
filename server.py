import socket
import json
from _thread import start_new_thread
from sense_hat import SenseHat
from optparse import OptionParser

parser = OptionParser()
parser.add_option('-i', '--ip', type='string', dest='ip', default='127.0.0.1')
parser.add_option('-p', '--port', type='int', dest='port', default=5005)
(options, args) = parser.parse_args()

sense = SenseHat()
sense.clear()

#  temp = sense.get_temperature()
 
ip = '127.0.0.1' # set as contant for analysis node later
port = 5005

s = socket.socket()
s.bind((ip, port))
s.listen(20)

visDatas = {} # store all data

def dataStream(con, adr):
    
    while True:
        data = con.recv(1024).decode('utf-8')
        if data == '':
            break
        mDict = json.loads(data)
        mDict['addr'] = adr[0]
        
        print(str(adr) + ' :  ' + str(data))
        print(jData['mem_use'])
    
    
while True:
    con, adr = s.accept()
    start_new_thread(dataStream, (con, adr))
    