# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 18:05:52 2020

@author: Dany
""" 

ha = [[],[],[]]
hs = [[],[],[]]
ba = [[],[],[]]
bs = [[],[],[]]

def err(Name):
    global ha, hs, ba, bs
    
    if Name == 'alex':
        bs[0] = [3]
        ha[1] = [7]
    elif Name == 'walid':
        ha[0] = []
    elif Name == 'victor':
        ha[0] = [5]
    elif Name == 'florent':     
        ba[0] = [2]
        ha[1] = [7]
        hs[1] = [8]
        hs[2] = [5]
    
    A = [ha,hs,ba,bs]
    return A