import socket
import os
import psutil
import json
from optparse import OptionParser

parser = OptionParser()
parser.add_option('-i', '--ip', type='string', dest='ip', default='127.0.0.1')
parser.add_option('-p', '--port', type='int', dest='port', default=5005)
(options, args) = parser.parse_args()

s = socket.socket()
s.connect((options.ip, options.port))
while True:
    data = {}
    data['mem_use'] = psutil.virtual_memory().used/1000000000
    data['cpu_use'] = psutil.cpu_percent(0.5)
    s.sendall(json.dumps(data).encode('utf-8'))
    
