import socket
import json
from _thread import start_new_thread
#from sense_hat import SenseHat
from optparse import OptionParser
import matplotlib.pyplot as plt
import time

parser = OptionParser()
parser.add_option('-i', '--ip', type='string', dest='ip', default='127.0.0.1')
parser.add_option('-p', '--port', type='int', dest='port', default=5005)
parser.add_option('-n', '--numNodes', type='int', dest='numNodes', default=15)
(options, args) = parser.parse_args()

#sense = SenseHat()
#sense.clear()

#  temp = sense.get_temperature()

def clientReceiver():
    # create server
    s = socket.socket()
    s.bind((options.ip, options.port))
    s.listen(options.numNodes)

    # keep main in here to accept connections    
    cnt = 0
    while True:
        con, adr = s.accept()
        start_new_thread(dataStream, (con, cnt))
        cnt += 1

visDatas = {} # store all data to visualize
for i in range(options.numNodes):
    visDatas[i] = {'mem_use':[], 'cpu_use':[]}

# continually stream in data in separate threads
def dataStream(con, uid):
    while True:
        data = con.recv(1024).decode('utf-8')
        if data == '':
            break

        mDict = json.loads(data)

        visDatas[uid]['mem_use'].append(mDict['mem_use'])
        visDatas[uid]['cpu_use'].append(mDict['cpu_use'])

        print(mDict)

start_new_thread(clientReceiver, ())


plt.ion() # for live update plot
# plotting stuff
fig = plt.figure()
axRam = plt.subplot(2,1,1)
axCpu = plt.subplot(2,1,2)

# colors of lines
cols = ['C'+str(i%10) for i in range(options.numNodes)]
# styles of lines
lins = ['-']*10 + ['--']*10 + ['-.']*10 # manually update if need more

maxX = 20
while True:
    axRam.cla()
    axCpu.cla()
    for uid in range(options.numNodes):
        l = len(visDatas[uid]['mem_use'])
        axRam.plot(visDatas[uid]['mem_use'][max(0, l-maxX):l], 
            color=cols[uid], linestyle=lins[uid])
        axRam.set_title('RAM Usage of Nodes')
        axRam.set_ylabel('RAM (GB)')

        axCpu.plot(visDatas[uid]['cpu_use'][max(0, l-maxX):l], 
            color=cols[uid], linestyle=lins[uid])
        axCpu.set_title('CPU Usage of Nodes')

    plt.draw()
    fig.canvas.start_event_loop(1)
    #plt.pause(1)
    
