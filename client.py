import socket
import os
import psutil
import json
from optparse import OptionParser

parser = OptionParser()
parser.add_option('-i', '--ip', type='string', dest='ip', default='127.0.0.1')
parser.add_option('-p', '--port', type='int', dest='port', default=5005)
(options, args) = parser.parse_args()

while True:
    s = socket.socket()
    isCon = False # is there connection
    print('Attempting Connection...')
    while not isCon:
        try:
            s.connect((options.ip, options.port))
            isCon = True
            print('Connected!')
        except:
            pass
        
    while True:
        try:
            data = {}
            data['mem_use'] = psutil.virtual_memory().used/(1024**3)
            data['cpu_use'] = psutil.cpu_percent(0.2)
            data['uid']     = socket.gethostname()

            s.sendall(json.dumps(data).encode('utf-8'))
        except:
            break
    
