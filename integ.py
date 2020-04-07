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

def integ(a,T): 
    freq = np.fft.fftfreq(len(a))  
    omega = 2*np.pi*freq*800
    #A = glm.filter_signal(a, fs=800, fc=0.15, N=4, type='high')
    A=a
    transfo = np.fft.fft(A)    
    Int = np.array([transfo[0]])  
    Int = np.append(Int,transfo[1:]/(1j*omega[1:]))
    V = np.fft.ifft(Int) 
    V = V - np.nanmean(V)
    #V = glm.filter_signal(V, fs=800, fc=1, N=4, type='high')
    #V = glm.filter_signal(V, fs=800, fc=20, N=4, type='low')
    #V = glm.filter_signal(V, fs=800, fc=0.05, N=4, type='high')
    Int[1:] = Int[1:]/(1j*omega[1:])  
    D = np.fft.ifft(Int)      
    #D = D - np.nanmean(D) 
    #D = glm.filter_signal(D, fs=800, fc=0.1, N=4, type='high')
            
    fig = plt.figure(figsize = [14,7])
    ax  = fig.subplots(3,1)
    ax[0].plot(T,a)
    ax[1].plot(T,V) 
    ax[2].plot(T,D) 
    ax[0].set_xlim([5,10])
    ax[1].set_xlim([5,10])
    ax[2].set_xlim([5,10])  
    #ax[2].set_ylim([-0.1,0.1])  
    fig.show()