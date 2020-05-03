# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 10:24:43 2020

@author: Walid 
"""


import scipy.integrate as sc
import numpy as np 
import matplotlib.pyplot as plt
from sympy import *
import scipy.stats as st

#def position(Acc,Time) : 
    # r=0.99875
    # v= np.convolve(Acc,[1,4,1],'same')/(3*800)
    # V = [Acc[0]]
    # for a in v[1:]:
    #     V=np.append(V,V[-1]*r +a)
    # p= np.convolve(Acc,[1,8,18,8,1],'same')/(9*800**2)
    # P = [0]
    # for a in p[1:]:
    #     P=np.append(P,P[-1]*r +a)

    # # acceleration=[0]
    # # for i in range(1,len(Acc)):
    # #     acceleration.append(acceleration[-1]+np.convolve(Acc[i-1:i],[1,4,1],"same"))/(3*800)
    # # vitesse=[0]
    # # for i in range(1,len(acceleration)):
    # #     vitesse.append(vitesse[-1]+np.convolve(acceleration[i-1:i],[1,4,1],"same"))/(3*800)
    # Soluce=(-1/4)*np.cos(4*Time)+(-1/7)*np.cos(7*Time)+(-1/9)*np.cos(9*Time)
   
    
    # fig = plt.figure(figsize = [15,7])
    # ax  = fig.subplots(3,1)
    # ax[0].plot(Time,Acc)
    # ax[1].plot(Time,V)
    # ax[2].plot(Time,P)
    # ax[1].plot(Time,Soluce)
    # ax[0].set_xlim([0,51])
    # ax[1].set_xlim([0,51])
    # ax[2].set_xlim([0,51])
    # fig.show()
   # fig.savefig("PositionT\Position",blocN)
    
    # -*- coding: utf-8 -*-



"""



Created on Sat Apr  4 20:12:14 2020






@author: Dany



"""



# from scipy.interpolate import lagrange
# import glm_data_processing as glm
# import matplotlib.pyplot as plt
# from scipy import signal
# import numpy as np
# import gbio_example_script_collisions as gbio



#def integ(A,T): 
    # freq = np.fft.fftfreq(len(A))  
    # omega = 2*np.pi*freq*800 
    # transfo = np.fft.fft(A)   
    # #plt.plot(freq*800,transfo)
    # Int = np.array([transfo[0]])  
    # Int = np.append(Int,transfo[1:]/(1j*omega[1:]))
    # V = np.fft.ifft(Int) 
    # V=V-np.nanmean(V)
  

    # #V = glm.filter_signal(V, fs=800, fc=0.1, N=4, type='high')
    # #V = glm.filter_signal(V, fs=800, fc=0.05, N=4, type='high')
    # Int[1:] = Int[1:]/(1j*omega[1:]) 
    # D = np.fft.ifft(Int)    
    # D=D-D[0]
    # #D = glm.filter_signal(D, fs=800, fc=0.1, N=4, type='high') 
    # fig = plt.figure(figsize = [15,7])
    # ax  = fig.subplots(3,1)
    # ax[0].plot(T,A)
    # ax[1].plot(T,V) 
    # ax[2].plot(T,D) 
    # # ax[0].set_xlim([0,51])
    # # ax[1].set_xlim([0,51])
    # # ax[2].set_xlim([0,51]) 
    # fig.show()




#@author: Dany

""

from scipy.interpolate import lagrange

import glm_data_processing as glm

import matplotlib.pyplot as plt

from scipy import signal

import numpy as np



def integ(A,T): 

    freq = np.fft.fftfreq(len(A))  

    omega = 2*np.pi*freq*800

    #A = glm.filter_signal(a, fs=800, fc=0.15, N=4, type='high') 

    transfo = np.fft.fft(A)    

    Int = np.array([transfo[0]])  

    Int = np.append(Int,transfo[1:]/(1j*omega[1:]))

    V = np.fft.ifft(Int) 

    V = V - np.nanmean(V[0:320])

    #V = glm.filter_signal(V, fs=800, fc=1, N=4, type='high')

    #V = glm.filter_signal(V, fs=800, fc=20, N=4, type='low')

    #V = glm.filter_signal(V, fs=800, fc=0.05, N=4, type='high')

    Int[1:] = Int[1:]/(1j*omega[1:])  

    D = np.fft.ifft(Int)      

    D = D - np.nanmean(D[0:320]) 

    #D = glm.filter_signal(D, fs=800, fc=0.1, N=4, type='high')

            

#    fig = plt.figure(figsize = [14,7])

#    ax  = fig.subplots(3,1)

#    ax[0].plot(T,A)

#    ax[1].plot(T,V) 

#    ax[2].plot(T,D) 

#    ax[0].set_xlim([5,10])

#    ax[1].set_xlim([5,10])

#    ax[2].set_xlim([5,10])  

#    #ax[2].set_ylim([-0.1,0.1])  

#    fig.show()

    return np.real(V), np.real(D)*100
def Ttest(P1,P2):
    seuil=0.05
    (Thas,Phas)=st.ttest_ind(P1,P2)
    if seuil>Phas : 
        print("PA and P2 has a significative difference of", Phas)
    else : 
        print ("We can't reject H0 ,So they have the same average") 
        print(Phas)       
    
               
               
    
    