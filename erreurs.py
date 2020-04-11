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
        bs[0] = [2,9] 
        ba[1] = [9]
        ha[1] = [6]
        hs[0] = [5]
    elif Name == 'walid': 
        ba[2] = [0,3,5] 
        bs[0] = [3]
        bs[1] = [9]
    elif Name == 'victor':
        ha[0] = [4]
        ha[1] = [7]
        hs[1] = [2]
        bs[0] = [0]
        bs[2] = [3]
        ba[0] = [1,7,8]
    elif Name == 'florent':     
        ba[0] = [1]
        ha[1] = [6]
        hs[1] = [7]
        hs[2] = [4]
    
    A = [ha,hs,ba,bs]
    return A