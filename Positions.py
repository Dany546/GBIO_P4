# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 10:24:43 2020

@author: Walid 
"""

import gbio_example_script_collisions as gbio 
import scipy.integrate as sc
import numpy as np 
import matplotlib.pyplot as plt
from sympy import *

def position(Acc,Time,blocN) : 
    acceleration=[0]
    for i in range(1,len(Acc)):
        acceleration.append(acceleration[-1]+sc.trapz(Acc[i-1:i],Time[i-1:i]))
    vitesse=[0]
    for i in range(1,len(acceleration)):
        vitesse.append(vitesse[-1]+sc.trapz(acceleration[i-1:i],Time[i-1:i]))
    
   
    
    fig=plt.figure()
    plt.plot(Time,vitesse)
    plt.show()
   # fig.savefig("PositionT\Position",blocN)
    
    

    
    