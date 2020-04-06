# -*- coding: utf-8 -*-
"""
Created on Sat Apr  4 20:12:14 2020

@author: Dany
"""
from scipy.interpolate import lagrange
import glm_data_processing as glm
import matplotlib.pyplot as plt
from scipy import signal
import numpy as np

def integ(A,T): 
    freq = np.fft.fftfreq(len(A))  
    omega = 2*np.pi*freq*800
    transfo = np.fft.fft(A)   
    plt.plot(freq*800,transfo)#
    Int = np.array([transfo[0]])  
    Int = np.append(Int,transfo[1:]/(1j*omega[1:]))
    V = np.fft.ifft(Int) 
    V = glm.filter_signal(V, fs=800, fc=0.1, N=4, type='high')
    #V = glm.filter_signal(V, fs=800, fc=0.05, N=4, type='high')
    Int[1:] = Int[1:]/(1j*omega[1:]) 
    D = np.fft.ifft(Int)    
    D = glm.filter_signal(D, fs=800, fc=0.1, N=4, type='high') 
            
    fig = plt.figure(figsize = [15,7])
    ax  = fig.subplots(3,1)
    ax[0].plot(T,A)
    ax[1].plot(T,V) 
    ax[2].plot(T,D) 
    ax[0].set_xlim([0,51])
    ax[1].set_xlim([0,51])
    ax[2].set_xlim([0,51]) 
    fig.show()