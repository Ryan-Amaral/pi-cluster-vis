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
parser.add_option('-u', '--update', type='float', dest='update', default=0.2)
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
    while True:
        con, _ = s.accept()
        start_new_thread(dataStream, (con,))

visDatas = {} # store all data to visualize

# continually stream in data in separate threads
def dataStream(con):
    while True:
        data = con.recv(1024).decode('utf-8')
        if data == '':
            break

        mDict = json.loads(data)
    
        uid = mDict['uid']
        if uid not in visDatas:
            visDatas[uid] = {'mem_use':[], 'cpu_use':[]}
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
    for i, uid in enumerate(list(visDatas.keys())):
        l = len(visDatas[uid]['mem_use'])
        axRam.plot(visDatas[uid]['mem_use'][max(0, l-maxX):l], 
            color=cols[i], linestyle=lins[i], label=uid)

        axCpu.plot(visDatas[uid]['cpu_use'][max(0, l-maxX):l], 
            color=cols[i], linestyle=lins[i], label=uid)
            
        if len(visDatas[uid]['mem_use']) > maxX:
            visDatas[uid]['mem_use'] = visDatas[uid]['mem_use'][len(visDatas[uid]['mem_use'])-20:]
        if len(visDatas[uid]['cpu_use']) > maxX:
            visDatas[uid]['cpu_use'] = visDatas[uid]['cpu_use'][len(visDatas[uid]['cpu_use'])-20:]
    
    axRam.set_title('RAM Usage of Nodes')
    axRam.set_ylabel('RAM (GB)')
    axRam.get_xaxis().set_visible(False)
    axRam.legend(loc='upper left')
    axRam.set_ylim(0,1)
    
    axCpu.set_title('CPU Usage of Nodes (4 Cores)')
    axCpu.set_ylabel('CPU %')
    axCpu.get_xaxis().set_visible(False)
    axCpu.legend(loc='upper left')
    axCpu.set_ylim(0,100)
    
    
    
    plt.draw()
    fig.canvas.start_event_loop(options.update)
    
