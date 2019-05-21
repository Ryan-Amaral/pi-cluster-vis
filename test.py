import matplotlib.pyplot as plt
import numpy as np
import random

amt = 100
y = np.random.rand(amt)

maxX = 20

axRam = plt.subplot(2,1,1)
axCpu = plt.subplot(2,1,2)

plt.ion() # for live update plot
for i in range(amt):
    axRam.cla()
    axRam.plot(y[max(0, i-maxX):i], color='C0')

    axCpu.cla()
    axCpu.plot(y[max(0, i-maxX):i], color='C1')
    
    
    plt.draw()
    plt.pause(0.5) # for debug stuff
    
plt.show(block=True)