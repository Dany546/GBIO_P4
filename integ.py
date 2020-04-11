# -*- coding: utf-8 -*-
"""
Created on Sat Apr  4 20:12:14 2020

@author: Dany and walid
""" 
import numpy as np

def integ(a,T): 
    A = a - np.nanmean(a[:320])
    freq = np.fft.fftfreq(len(A))  
    omega = 2*np.pi*freq*800 
    transfo = np.fft.fft(A)    
    Int = np.array([transfo[0]])  
    Int = np.append(Int,transfo[1:]/(1j*omega[1:]))
    V = np.fft.ifft(Int)  
    V = V - np.nanmean(V[0:320])  
    Int[1:] = Int[1:]/(1j*omega[1:])  
    D = np.fft.ifft(Int)       
    D = D - np.nanmean(D[0:320])  
    
    return np.real(V), np.real(D)*100