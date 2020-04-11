# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 11:59:09 2020

@author: Dany
"""
import gbio_example_script_collisions_dany as gbio
from scipy.signal import find_peaks as peaks
import matplotlib.pyplot as plt
import numpy as np 

name = None
to_cancel = None
accX = None
GF = None
LF = None
dGF = None
vit = None
dis = None

def delai(Name):
    global accX, GF, LF, dGF, name, to_cancel  
    
    name = Name 
    to_cancel = gbio.to_cancel 
    accX = gbio.donnees_accX
    GF = gbio.donnees_GF
    LF = gbio.donnees_LF
    dGF = gbio.donnees_dGF
    
    new_accX,new_GF,new_LF,new_dGF,new_vit,new_dis = Sum()
        
    new_delai = [[None,None,None],[None,None,None]] 
      
    for i in range(2):
        for j in range(3):
            new_delai[i][j] = decal(new_GF[i*2][j],new_GF[(i*2)+1][j])
    
    # écris tout dans un fichier texte   
    try:     
        new_file = open("decalage\%s" %(name),"w")
        blocs = ['haut','bas']  
        for i in range(2): 
            new_file.write(blocs[i]+':\n')
            for j in range(3): 
                new_file.write('\t décalage moyen masse %d:\t ' %(j+1))
                for dec in new_delai[i][j]:
                    new_file.write(str(dec)+'\t')
                new_file.write('\n')    
            new_file.write('\n') 
        new_file.close()                
    except Exception:
        raise                  
    finally:
        if new_file != None:
            new_file.close()
 
# calcule le decalage entre deux signaux en milisecondes
def decal(signal_1,signal_2):
    
    pk_1 = peaks(signal_1,prominence=9,distance=400) 
    pk_2 = peaks(signal_2,prominence=9,distance=400) 
    
    return abs(pk_1[0]-pk_2[0])*5/4   # 1000/800 = 5/4 
    
def superpose(Name):
    global accX, GF, LF, dGF, name, to_cancel, vit, dis
         
    name = Name  
    to_cancel = gbio.to_cancel 
    accX = gbio.donnees_accX
    GF = gbio.donnees_GF
    LF = gbio.donnees_LF
    dGF = gbio.donnees_dGF
    vit = gbio.vit
    dis = gbio.dis
    
    fig = plt.figure(figsize = [8,10])
    ax  = fig.subplots(4,2)
    
    fig.suptitle(name, fontsize=16)
    
    ax[0,0].set_title("Haut", fontsize=14)
    ax[0,1].set_title("Bas", fontsize=14)
    
    ax[0,0].set_ylabel("Acceleration [m/s^2]", fontsize=13)
    ax[1,0].set_ylabel("LF [N]", fontsize=13)
    ax[2,0].set_ylabel("GF [N]", fontsize=13)
    ax[3,0].set_ylabel("GF derivative [N/s]", fontsize=13)
    
    ax[3,0].set_xlabel("Time [ms]", fontsize=13)
    ax[3,1].set_xlabel("Time [ms]", fontsize=13)
    
    new_accX,new_GF,new_LF,new_dGF,new_vit,new_dis = Sum()
    time = np.arange(0,1200*5/4,5/4)
     
    colors = ['r','b','r','b']
    cols = [0,0,1,1]
    lines1 = [None,None,None,None]
    lines2 = [None,None,None]
    line_type = [':','--',''] 
    for i in range(4):
        col = cols[i]
        color = colors[i] 
        j = 0
        for item_accX,item_GF,item_LF,item_dGF in zip(new_accX[i],new_GF[i],new_LF[i],new_dGF[i]):
            Color = line_type[j]+color
            lines1[i] = ax[0,col].plot(time,item_accX,Color)
            lines2[j] = ax[1,col].plot(time,item_LF,Color)
            ax[2,col].plot(time,item_GF,Color)
            ax[3,col].plot(time,item_dGF,Color) 
            j+=1
    lines1 = (lines1[0][0],lines1[1][0])  
    lines2 = (lines2[0][0],lines2[1][0],lines2[2][0])  
    fig.legend(lines1, ('avec anticipation', 'sans anticipation'), loc='upper right') 
    fig.legend(lines2, ('masse 1', 'masse 2', 'masse 3'), loc='upper right', bbox_to_anchor=(1, 0.95))    
    fig.savefig("figures\Add\%s_acc_forces_dGF.png" %(name)) 
    
    fig = plt.figure(figsize = [8,10])
    ax  = fig.subplots(3,2)
    
    fig.suptitle(name, fontsize=16)
    
    ax[0,0].set_title("Haut", fontsize=14)
    ax[0,1].set_title("Bas", fontsize=14)
    
    ax[0,0].set_ylabel("Acceleration [m/s^2]", fontsize=13)
    ax[1,0].set_ylabel("Vitesse [m/s]", fontsize=13)
    ax[2,0].set_ylabel("Déplacement [cm]", fontsize=13) 
    
    ax[2,0].set_xlabel("Time [ms]", fontsize=13)
    ax[2,1].set_xlabel("Time [ms]", fontsize=13) 
    
    time = np.arange(0,1200*5/4,5/4)
       
    lines1 = [None,None,None,None]
    lines2 = [None,None,None]
    for i in range(4):
        col = cols[i]
        color = colors[i]  
        j = 0
        for item_accX,item_vit,item_dis in zip(new_accX[i], new_vit[i], new_dis[i]):
            Color = line_type[j]+color
            lines1[i] = ax[0,col].plot(time,item_accX[:1200],Color)
            lines2[j] = ax[1,col].plot(time,item_vit,Color)
            ax[2,col].plot(time,item_dis,Color) 
            j+=1
    lines1 = (lines1[0][0],lines1[1][0])  
    lines2 = (lines2[0][0],lines2[1][0],lines2[2][0])  
    fig.legend(lines1, ('avec anticipation', 'sans anticipation'), loc='upper right') 
    fig.legend(lines2, ('masse 1', 'masse 2', 'masse 3'), loc='upper right', bbox_to_anchor=(1, 0.95))    
    fig.savefig("figures\Add\%s_dist.png" %(name)) 
    fig.show()
    
def Sum():
    global accX, GF, LF, dGF, name, to_cancel, vit, dis
    
    new_donnees_accX = [[None,None,None] for i in range(4)] 
    new_donnees_GF = [[None,None,None] for i in range(4)]   
    new_donnees_LF = [[None,None,None] for i in range(4)]   
    new_donnees_dGF = [[None,None,None] for i in range(4)]  
    new_vit = [[None,None,None] for i in range(4)]    
    new_dis = [[None,None,None] for i in range(4)]   
    
    # somme sur chaque masse pour les 3 memes blocs
    ind,blocks_ind,choc_number = block_order() 
    for i in range(12): 
        ind_1,ind_2 = blocks_ind[str(i+1)]
        for j in range(3):
            if ind[str(i+1)][str(j+1)] != []:
                for k in ind[str(i+1)][str(j+1)]: 
                    L = 0 
                    for item_accX,item_GF,item_LF,item_dGF,item_vit,item_dis in zip(accX[ind_1][ind_2],GF[ind_1][ind_2],LF[ind_1][ind_2],dGF[ind_1][ind_2],vit[ind_1][ind_2],dis[ind_1][ind_2]):
                        if k == L: 
                            if np.all(new_donnees_accX[ind_1][j]) == None:
                                new_donnees_accX[ind_1][j] = item_accX
                                new_donnees_GF[ind_1][j] = item_GF
                                new_donnees_LF[ind_1][j] = item_LF 
                                new_donnees_dGF[ind_1][j] = item_dGF 
                                new_vit[ind_1][j] = item_vit 
                                new_dis[ind_1][j] = item_dis 
                            else:
                                new_donnees_accX[ind_1][j] += item_accX
                                new_donnees_GF[ind_1][j] += item_GF
                                new_donnees_LF[ind_1][j] += item_LF 
                                new_donnees_dGF[ind_1][j] += item_dGF 
                                new_vit[ind_1][j] += item_vit 
                                new_dis[ind_1][j] += item_dis 
                        L += 1        
    
    # termine le calcul de la moyenne en divisant par le nombre de chocs correspondant
    for i in range(4):
        for j in range(3): 
            new_donnees_accX[i][j] = new_donnees_accX[i][j] / choc_number[i][j]
            new_donnees_GF[i][j] = new_donnees_GF[i][j] / choc_number[i][j]
            new_donnees_LF[i][j] = new_donnees_LF[i][j] / choc_number[i][j]
            new_donnees_dGF[i][j] = new_donnees_dGF[i][j] / choc_number[i][j] 
            new_vit[i][j] = new_vit[i][j] / choc_number[i][j] 
            new_dis[i][j] = new_dis[i][j] / choc_number[i][j] 
                    
    return new_donnees_accX, new_donnees_GF, new_donnees_LF, new_donnees_dGF , new_vit, new_dis                       
                    
def block_order(): 
    global name, to_cancel
    
    first = 0 ; Next = 0
    if name == 'alex':
        first = 1
        Next = 0 
    elif name == 'walid':
        first = 3
        Next = 2 
    elif name == 'victor':  
        first = 1
        Next = 0 
    elif name == 'florent':
        first = 2
        Next = 3
    else: 
        print('WTF is going on with your filename ???') 
        
    blocks_ind = {}    
    for i in range(6):
        if i < 3:
            blocks_ind[str((i*2)+1)] = first,i
            blocks_ind[str((i*2)+2)] = Next,i
        else: 
            new_first = 0 ; new_next = 0
            if first < 2:
                new_first = first+2
                new_next = Next+2
            else:
                new_first = first-2
                new_next = Next-2
            blocks_ind[str((i*2)+1)] = new_first,i-3
            blocks_ind[str((i*2)+2)] = new_next,i-3
        
    try:  
        filename = 'masses\%s.txt' %(name)
        file = open(filename,'r')
        
        ind = {} ; choc_number = {} ; block = '' ; n = 0
        for num,line in enumerate(file.readlines()):
            if line[:4] == 'Bloc':
                block = line.split(' ')[1][:-1] 
                ind[block] = {'1':[],'2':[],'3':[]}
                choc_number[block] = {'1':0,'2':0,'3':0}
                n = 0    
            elif not line == "\n": 
                mass = line.split(' ')[4][0]
                ind[block][mass].append(n)
                choc_number[block][mass] += 1
                n = n+1
        file.close()      
    except Exception:
        raise
    finally:
        if file != None:
            file.close()
        
    for j in range(6):
        for k in ['1','2','3']:
            if j<3:
                for l in ind[str((j*2)+1)][k]:
                    if to_cancel[first][j] != []:
                        for h in to_cancel[first][j]:
                            if l == h:
                                choc_number[str((j*2)+1)][k] -= 1 
                                ind[str((j*2)+1)][k].remove(l)
                for l in ind[str((j*2)+2)][k]:
                    if to_cancel[Next][j] != []:
                        for h in to_cancel[Next][j]:
                            if l == h:
                                choc_number[str((j*2)+2)][k] -= 1 
                                ind[str((j*2)+2)][k].remove(l)   
            else:
                new_first = 0 ; new_next = 0
                if first < 2:
                    new_first = first+2
                    new_next = Next+2
                else:
                    new_first = first-2
                    new_next = Next-2
                for l in ind[str((j*2)+1)][k]:  
                    if to_cancel[new_first][j-3] != []:
                        for h in to_cancel[new_first][j-3]:
                            if l == h:
                                choc_number[str((j*2)+1)][k] -= 1 
                                ind[str((j*2)+1)][k].remove(l)
                for l in ind[str((j*2)+2)][k]:
                    if to_cancel[new_next][j-3] != []:
                        for h in to_cancel[new_next][j-3]:
                            if l == h:
                                choc_number[str((j*2)+2)][k] -= 1  
                                ind[str((j*2)+2)][k].remove(l)
    
    new_choc_number = [[0,0,0] for i in range(4)]
    for i in range(12):
        k,_ = blocks_ind[str(i+1)] 
        for j in range(3):
            new_choc_number[k][j] += choc_number[str(i+1)][str(j+1)] 
        
    return ind, blocks_ind, new_choc_number  