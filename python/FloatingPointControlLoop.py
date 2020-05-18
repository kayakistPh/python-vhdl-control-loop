# -*- coding: utf-8 -*-
"""
Created on Thu May 14 14:21:12 2020

@author: phayn
"""

import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal

#def controlLoop(input):

fs = 1e6

delay = 30
    
P = 1.5
I = 1
D = 1        


#Create sawtooth wave
inputSignal = np.arange(-1,1,0.01)
inputSignal = np.concatenate((inputSignal,inputSignal,inputSignal,inputSignal))

#Create a step wave
#inputSignal = np.concatenate((np.zeros(200),1*np.ones(200),-1*np.ones(200),np.zeros(200)))


timebase = np.arange(0,(1/fs*len(inputSignal)),(1/fs))


plantOut = np.zeros_like(inputSignal)
controllerError = np.zeros_like(inputSignal)
feedback = np.zeros_like(inputSignal)
integrator = 0
for i in range(delay,len(inputSignal)):
    controllerError[i] = inputSignal[i] - feedback[i-1]
    #The plant is a sine wave
    plantOut[i] = np.sin(controllerError[i])
    #PID
    feedback[i] = P * plantOut[i]
    integrator = integrator + feedback[i]
    feedback[i] = I * integrator# + D * plantOut[i]
    
plt.figure(0)
plt.plot(timebase,inputSignal, label="Input")
plt.plot(timebase,plantOut, label="Plant Out")
plt.plot(timebase,controllerError, label="Controller Error")
plt.plot(timebase,feedback, label="Feedback")
plt.legend()  
