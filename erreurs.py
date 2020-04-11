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
        bs[0] = [3,10] 
        ba[1] = [10]
        ha[1] = [7]
        hs[0] = [6]
    elif Name == 'walid': 
        ba[2] = [1,4,6] 
        bs[0] = [4]
        bs[1] = [10]
    elif Name == 'victor':
        ha[0] = [5]
        ha[1] = [8]
        hs[1] = [3]
        bs[0] = [1]
        bs[2] = [4]
        ba[0] = [2,8,9]
    elif Name == 'florent':     
        ba[0] = [2]
        ha[1] = [7]
        hs[1] = [8]
        hs[2] = [5]
    
    A = [ha,hs,ba,bs]
    return A