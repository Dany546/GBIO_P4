# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 11:59:09 2020

@author: Dany
"""
import gbio_example_script_collisions_dany as gbio
from scipy.signal import find_peaks as peaks
import matplotlib.pyplot as plt
import erreurs
import numpy as np 

name = None
to_cancel = None
accX = None
GF = None
LF = None
dGF = None
vit = None
dis = None
SF = None
SM = None  

def delai(Name,Type): 
    global accX, GF, LF, dGF, name, to_cancel, vit, dis, SF, SM
         
    name = Name  
    to_cancel = gbio.to_cancel 
    accX = gbio.donnees_accX
    GF = gbio.donnees_GF
    LF = gbio.donnees_LF
    dGF = gbio.donnees_dGF
    vit = gbio.vit
    dis = gbio.dis
    SF = gbio.donnees_SF
    SM = gbio.donnees_SM  
 
    _,new_GF,_,_,_,_,_,_ = Sum() 
    
    # pour utiliser les donnnées de tout les sujets
    if Type=='all': 
        
        new_GF = new_GF/4
        
        for the_name in ['alex','walid','victor','florent']:
            if not name==the_name:
                start = 0 ; end = 0
                if the_name == 'alex':
                    start = 0 ; end = 4
                elif the_name == 'florent': 
                    start = 4 ; end = 8 
                elif the_name == 'victor': 
                    start = 8 ; end = 12
                elif the_name == 'walid': 
                    start = 12 ; end = 16  
                _,B,_,_,_,_,G,_,_ = gbio.make_plots(start,end,Name=the_name,Delai=True,noreturn=False) 
                to_cancel = G 
                GF = B 
                name = the_name
                _,new_GF_2,_,_,_,_,_,_ = Sum()  
                for mmmh,item in enumerate(new_GF_2):
                    new_GF[mmmh][0] = new_GF[mmmh][0] + item[0]/4
                    new_GF[mmmh][1] = new_GF[mmmh][1] + item[1]/4
                    new_GF[mmmh][2] = new_GF[mmmh][2] + item[2]/4   
                    
        name = 'Moyenne générale' 
        
    new_delai = [[None,None,None],[None,None,None]] 
      
    for i in range(2):
        for j in range(3):
            new_delai[i][j] = decal(new_GF[i*2][j],new_GF[(i*2)+1][j])
    
    # écris tout dans un fichier texte   
    new_file = None
    try:     
        new_file = open("decalage\%s" %(name),"w")
        blocs = ['haut','bas']  
        for i in range(2): 
            new_file.write(blocs[i]+':\n')
            for j in range(3): 
                new_file.write('\t décalage moyen masse %d:\t ' %(j+1))
                for dec in new_delai[i][j]:
                    new_file.write(str(dec)+'\t [ms]')
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
    
    pk_1 = peaks(signal_1,prominence=10,distance=800) 
    pk_2 = peaks(signal_2,prominence=10,distance=800)  
    
    return abs(pk_1[0]-pk_2[0])*5/4   # 1000/800 = 5/4 
    
def superpose(Name,Type):
    global accX, GF, LF, dGF, name, to_cancel, vit, dis, SF, SM
         
    name = Name  
    to_cancel = gbio.to_cancel 
    accX = gbio.donnees_accX
    GF = gbio.donnees_GF
    LF = gbio.donnees_LF
#    dGF = gbio.donnees_dGF
    vit = gbio.vit
    dis = gbio.dis
    SF = gbio.donnees_SF
    SM = gbio.donnees_SM
    
    new_accX,new_GF,new_LF,new_dGF,new_vit,new_dis,new_SF,new_SM = Sum()
    
    if Type=='all': 
        for i in range(4):
            for j in range(3): 
                new_accX[i][j] = new_accX[i][j]/4
                new_GF[i][j] = new_GF[i][j]/4
                new_LF[i][j] = new_LF[i][j]/4                 
#                new_dGF[i][j] = new_dGF[i][j]/4
                new_vit[i][j] = new_vit[i][j]/4
                new_dis[i][j] = new_dis[i][j]/4
                new_SF[i][j] = new_SF[i][j]/4
                new_SM[i][j] = new_SM[i][j]/4
        for the_name in ['alex','walid','victor','florent']:
            if not name==the_name:
                start = 0 ; end = 0
                if the_name == 'alex':
                    start = 0 ; end = 4
                elif the_name == 'florent': 
                    start = 4 ; end = 8 
                elif the_name == 'victor': 
                    start = 8 ; end = 12
                elif the_name == 'walid': 
                    start = 12 ; end = 16  
                A,B,C,D,E,F,G,H,I = gbio.make_plots(start,end,Name=the_name,add=True,noreturn=False)
                to_cancel = G
                accX = A
                GF = B
                LF = C
#                dGF = D
                vit = E
                dis = F
                SF = H
                SM = I
                name = the_name
                new_accX_2,new_GF_2,new_LF_2,new_dGF_2,new_vit_2,new_dis_2,new_SF_2,new_SM_2 = Sum()
                for mmmh,item in enumerate(new_accX_2):
                    new_accX[mmmh][0] = new_accX[mmmh][0] + item[0]/4
                    new_accX[mmmh][1] = new_accX[mmmh][1] + item[1]/4
                    new_accX[mmmh][2] = new_accX[mmmh][2] + item[2]/4
                for mmmh,item in enumerate(new_GF_2):
                    new_GF[mmmh][0] = new_GF[mmmh][0] + item[0]/4
                    new_GF[mmmh][1] = new_GF[mmmh][1] + item[1]/4
                    new_GF[mmmh][2] = new_GF[mmmh][2] + item[2]/4
                for mmmh,item in enumerate(new_LF_2):
                    new_LF[mmmh][0] = new_LF[mmmh][0] + item[0]/4
                    new_LF[mmmh][1] = new_LF[mmmh][1] + item[1]/4
                    new_LF[mmmh][2] = new_LF[mmmh][2] + item[2]/4
#                for mmmh,item in enumerate(new_dGF_2):
#                    new_dGF[mmmh][0] = new_dGF[mmmh][0] + item[0]/4
#                    new_dGF[mmmh][1] = new_dGF[mmmh][1] + item[1]/4
#                    new_dGF[mmmh][2] = new_dGF[mmmh][2] + item[2]/4 
                for mmmh,item in enumerate(new_vit_2):
                    new_vit[mmmh][0] = new_vit[mmmh][0] + item[0]/4
                    new_vit[mmmh][1] = new_vit[mmmh][1] + item[1]/4
                    new_vit[mmmh][2] = new_vit[mmmh][2] + item[2]/4  
                for mmmh,item in enumerate(new_dis_2):
                    new_dis[mmmh][0] = new_dis[mmmh][0] + item[0]/4
                    new_dis[mmmh][1] = new_dis[mmmh][1] + item[1]/4
                    new_dis[mmmh][2] = new_dis[mmmh][2] + item[2]/4  
                for mmmh,item in enumerate(new_SF_2):
                    new_SF[mmmh][0] = new_SF[mmmh][0] + item[0]/4
                    new_SF[mmmh][1] = new_SF[mmmh][1] + item[1]/4
                    new_SF[mmmh][2] = new_SF[mmmh][2] + item[2]/4  
                for mmmh,item in enumerate(new_SM_2):
                    new_SM[mmmh][0] = new_SM[mmmh][0] + item[0]/4
                    new_SM[mmmh][1] = new_SM[mmmh][1] + item[1]/4
                    new_SM[mmmh][2] = new_SM[mmmh][2] + item[2]/4   
                    
        name = 'Moyenne générale'        
    
    time = np.arange(0,1200*5/4,5/4)
    
    fig = plt.figure(figsize = [8,10])
    ax  = fig.subplots(3,2)       # 4
    
    fig.suptitle(name, fontsize=16)
        
    ax[0,0].set_title("Haut", fontsize=14)
    ax[0,1].set_title("Bas", fontsize=14)
    
    ax[0,0].set_ylabel("Acceleration [m/s^2]", fontsize=13)
    ax[1,0].set_ylabel("LF [N]", fontsize=13)
    ax[2,0].set_ylabel("GF [N]", fontsize=13)
#    ax[3,0].set_ylabel("GF derivative [N/s]", fontsize=13)
    
    ax[2,0].set_xlabel("Time [ms]", fontsize=13)
    ax[2,1].set_xlabel("Time [ms]", fontsize=13)
    
    colors = ['r','b','r','b']
    cols = [0,0,1,1]
    lines1 = [None,None,None,None]
    lines2 = [None,None,None]
    line_type = [':','--',''] 
    for i in range(4):
        col = cols[i]
        color = colors[i] 
        j = 0
        for item_accX,item_GF,item_LF in zip(new_accX[i],new_GF[i],new_LF[i]):     #,item_dGF  ,new_dGF[i]
            Color = line_type[j]+color
            lines1[i] = ax[0,col].plot(time,item_accX,Color)
            lines2[j] = ax[1,col].plot(time,item_LF,Color)
            ax[2,col].plot(time,item_GF,Color)
#            ax[3,col].plot(time,item_dGF,Color) 
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
    
    fig = plt.figure(figsize = [8,10])
    ax  = fig.subplots(4,2)
    
    if Type=='all':
        fig.suptitle("Marge de sécurité moyenne", fontsize=16)
    else:
        fig.suptitle("Marge de sécurité moyenne pour %s " %(name) , fontsize=16)
    
    ax[0,0].set_title("Haut", fontsize=14)
    ax[0,1].set_title("Bas", fontsize=14)
    
    ax[0,0].set_ylabel("Acceleration [m/s^2]", fontsize=13)
    ax[1,0].set_ylabel("Grip force [N]", fontsize=13)
    ax[2,0].set_ylabel("Slip force [N]", fontsize=13) 
    ax[3,0].set_ylabel("Security Marge [N]", fontsize=13)
     
    ax[3,0].set_xlabel("Time [s]", fontsize=13)
    ax[3,1].set_xlabel("Time [s]", fontsize=13)
     
    lines1 = [None,None,None,None]
    lines2 = [None,None,None]
    line_type = [':','--',''] 
    for i in range(4):
        col = cols[i]
        color = colors[i] 
        j = 0
        for item_accX,item_GF,item_SF,item_SM in zip(new_accX[i],new_GF[i],new_SF[i],new_SM[i]):
            Color = line_type[j]+color
            lines1[i] = ax[0,col].plot(time,item_accX,Color)
            lines2[j] = ax[1,col].plot(time,item_GF,Color)
            ax[2,col].plot(time,item_SF,Color)
            ax[3,col].plot(time,item_SM,Color) 
            j+=1
    lines1 = (lines1[0][0],lines1[1][0])  
    lines2 = (lines2[0][0],lines2[1][0],lines2[2][0])  
    fig.legend(lines1, ('avec anticipation', 'sans anticipation'), loc='upper right') 
    fig.legend(lines2, ('masse 1', 'masse 2', 'masse 3'), loc='upper right', bbox_to_anchor=(1, 0.95))    
    fig.savefig("figures\Add\%s_marge_de_secu.png" %(name)) 
     
def Sum():
    global accX, GF, LF, dGF, to_cancel, vit, dis, name, SF, SM
    
    new_donnees_accX = np.array([np.array([None,None,None]) for i in range(4)]) 
    new_donnees_GF = np.array([np.array([None,None,None]) for i in range(4)])   
    new_donnees_LF = np.array([np.array([None,None,None]) for i in range(4)])
    new_donnees_dGF = np.array([np.array([None,None,None]) for i in range(4)])
    new_vit = np.array([np.array([None,None,None]) for i in range(4)])
    new_dis = np.array([np.array([None,None,None]) for i in range(4)])
    new_SF = np.array([np.array([None,None,None]) for i in range(4)])
    new_SM = np.array([np.array([None,None,None]) for i in range(4)])
    
    # somme sur chaque masse pour les 3 memes blocs
    ind,blocks_ind,choc_number = block_order() 
    for i in range(12): 
        ind_1,ind_2 = blocks_ind[str(i+1)]
        for j in range(3):
            if ind[str(i+1)][str(j+1)] != []:
                for k in ind[str(i+1)][str(j+1)]: 
                    L = 0 
                    for item_accX,item_GF,item_LF,item_vit,item_dis,item_SF,item_SM in zip(accX[ind_1][ind_2],GF[ind_1][ind_2],LF[ind_1][ind_2],vit[ind_1][ind_2],dis[ind_1][ind_2],SF[ind_1][ind_2],SM[ind_1][ind_2]): # ,item_dGF  ,dGF[ind_1][ind_2] 
                        if k == L: 
                            if np.all(new_donnees_accX[ind_1][j]) == None:
                                new_donnees_accX[ind_1][j] = item_accX
                                new_donnees_GF[ind_1][j] = item_GF
                                new_donnees_LF[ind_1][j] = item_LF 
#                                new_donnees_dGF[ind_1][j] = item_dGF 
                                new_vit[ind_1][j] = item_vit 
                                new_dis[ind_1][j] = item_dis 
                                new_SF[ind_1][j] = item_SF 
                                new_SM[ind_1][j] = item_SM 
                            else:
                                new_donnees_accX[ind_1][j] += item_accX
                                new_donnees_GF[ind_1][j] += item_GF
                                new_donnees_LF[ind_1][j] += item_LF 
#                                new_donnees_dGF[ind_1][j] += item_dGF 
                                new_vit[ind_1][j] += item_vit 
                                new_dis[ind_1][j] += item_dis 
                                new_SF[ind_1][j] += item_SF 
                                new_SM[ind_1][j] += item_SM 
                        L += 1        
    
    # termine le calcul de la moyenne en divisant par le nombre de chocs correspondant
    for i in range(4):
        for j in range(3): 
            new_donnees_accX[i][j] = new_donnees_accX[i][j] / choc_number[i][j]
            new_donnees_GF[i][j] = new_donnees_GF[i][j] / choc_number[i][j]
            new_donnees_LF[i][j] = new_donnees_LF[i][j] / choc_number[i][j]
#            new_donnees_dGF[i][j] = new_donnees_dGF[i][j] / choc_number[i][j] 
            new_vit[i][j] = new_vit[i][j] / choc_number[i][j] 
            new_dis[i][j] = new_dis[i][j] / choc_number[i][j] 
            new_SF[i][j] = new_SF[i][j] / choc_number[i][j] 
            new_SM[i][j] = new_SM[i][j] / choc_number[i][j] 
                    
    return new_donnees_accX, new_donnees_GF, new_donnees_LF, new_donnees_dGF , new_vit, new_dis, new_SF, new_SM                       
                    
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
    file = None    
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
 
def MoyDeplacement(dis,Name,Type) :
    Max=[np.array([]),np.array([]),np.array([]),np.array([])] 
    for i in range(4):
                for j in range(3):
                    for item in dis[i][j]: 
                        Max[i]=np.append(Max[i],[np.abs(np.min(item))])              
    if Type=='all':
        names=['alex','walid','victor','florent']
    else :
        names=[Name]
  
    for the_name in names:
        if not name==the_name:
            start = 0 ; end = 0
            if the_name == 'alex':
                start = 0 ; end = 4
            elif the_name == 'florent':
                start = 4 ; end = 8
            elif the_name == 'victor':
                start = 8 ; end = 12
            elif the_name == 'walid':
                start = 12 ; end = 16
               
            Dis = gbio.make_plots(start,end,Name=the_name,position=True,noreturn=False)
            
            for i in range(4):
                for j in range(3):
                    for item in Dis[i][j]: 
                        Max[i]=np.append(Max[i],[np.abs(np.min(item))])
    fig=plt.figure(figsize=[6,6])
  
    if Type=="all":
        Name="general"
    plt.boxplot(Max)
    axe=plt.gca()
    axe.set_xticklabels(["haut_avec","haut_sans","bas_avec","bas_sans"])
    axe.set_ylabel("déplacement [cm]")
    axe.set_title("Boxplot des déplacements maximum par conditions")
    fig.savefig("figures\Add\Position_%s"%(Name))   
    
def MoyForces(G,L,SF,SME,Name,Type):  
    global name, to_cancel
    
    name = Name
    to_cancel = erreurs.err(Name)
    
    Max_G=[np.array([]),np.array([]),np.array([]),np.array([])] 
    Max_L=[np.array([]),np.array([]),np.array([]),np.array([])]  
    Moy_SME=[np.array([]),np.array([]),np.array([]),np.array([])] 
    Max_SF=[np.array([]),np.array([]),np.array([]),np.array([])]   
#    for i in range(4):
#        for j in range(3):
#            for item_G,item_L,item_SF in zip(G[i][j],L[i][j],SF[i][j]): #,SM[i][j]): ,item_SM 
#                if np.nanmax(np.abs(item_G))>0: 
#                    Max_G[i]=np.append(Max_G[i],[np.nanmax(np.abs(item_G))])  
#                    Max_L[i]=np.append(Max_L[i],[np.nanmax(np.abs(item_L))]) 
               # Max_SM[i]=np.append(Max_SM[i],[np.max(np.abs(item_SM))])  
#                    Max_SF[i]=np.append(Max_SF[i],[np.nanmax(np.abs(item_SF))])  
#                for item_SME in SME[i][j]: 
#                    if np.nanmax(np.abs(G[i][j]))>0: 
                    
                    
    ind,blocks_ind,choc_number = block_order() 
    for i in range(12): 
        ind_1,ind_2 = blocks_ind[str(i+1)]
        for key,val in ind[str(i+1)].items(): 
            if val != []:
                for k in val:
                    if np.nanmax(np.abs(G[ind_1][ind_2][k]))>0: 
                        Max_G[ind_1]=np.append(Max_G[ind_1],[np.nanmax(np.abs(G[ind_1][ind_2][k]))])  
                        Max_L[ind_1]=np.append(Max_L[ind_1],[np.nanmax(np.abs(L[ind_1][ind_2][k]))]) 
                        Max_SF[ind_1]=np.append(Max_SF[ind_1],[np.nanmax(np.abs(SF[ind_1][ind_2][k]))]) 
                    if k<9:
                        Moy_SME[ind_1]=np.append(Moy_SME[ind_1],[np.nanmean(SME[ind_1][ind_2][k])]) 
                
    if Type=='all':
        names=['alex','walid','victor','florent'] 
        for the_name in names:
            if not Name==the_name:
                start = 0 ; end = 0
                if the_name == 'alex':
                    start = 0 ; end = 4
                elif the_name == 'florent':
                    start = 4 ; end = 8
                elif the_name == 'victor':
                    start = 8 ; end = 12
                elif the_name == 'walid':
                    start = 12 ; end = 16
                   
                new_G,new_L,new_SF,new_SME = gbio.make_plots(start,end,Name=the_name,Force=True,noreturn=False) #new_SM,
                
                name = the_name
                to_cancel = erreurs.err(the_name)
                
                ind,blocks_ind,choc_number = block_order() 
                for i in range(12): 
                    ind_1,ind_2 = blocks_ind[str(i+1)]
                    for key,val in ind[str(i+1)].items(): 
                        if val != []:
                            for k in val:
                                if np.nanmax(np.abs(new_G[ind_1][ind_2][k]))>0: 
                                    Max_G[ind_1]=np.append(Max_G[ind_1],[np.nanmax(np.abs(new_G[ind_1][ind_2][k]))])  
                                    Max_L[ind_1]=np.append(Max_L[ind_1],[np.nanmax(np.abs(new_L[ind_1][ind_2][k]))]) 
                                  # Max_SM[i]=np.append(Max_SM[i],[np.max(np.abs(item_SM))])  
                                    Max_SF[ind_1]=np.append(Max_SF[ind_1],[np.nanmax(np.abs(new_SF[ind_1][ind_2][k]))]) 
                                if k<9:
                                    Moy_SME[ind_1]=np.append(Moy_SME[ind_1],[np.nanmean(new_SME[ind_1][ind_2][k])]) 
                
#                for i in range(4):
#                    for j in range(3):
#                        for item_G,item_L,item_SF in zip(new_G[i][j],new_L[i][j],new_SF[i][j]): #,new_SM[i][j]): ,item_SM 
#                            if np.nanmax(np.abs(item_G))>0: 
#                                Max_G[i]=np.append(Max_G[i],[np.nanmax(np.abs(item_G))])  
#                                Max_L[i]=np.append(Max_L[i],[np.nanmax(np.abs(item_L))]) 
#                            #Max_SM[i]=np.append(Max_SM[i],[np.max(np.abs(item_SM))])  
#                            Max_SF[i]=np.append(Max_SF[i],[np.nanmax(np.abs(item_SF))])  
#                        for item_SME in new_SME[i][j]: 
#                            if np.nanmax(np.abs(G[i][j]))>0: 
#                                Moy_SME[i]=np.append(Moy_SME[i],[np.nanmean(item_SME)])  
        Name="general"
    
    # Grip Force                    
    fig=plt.figure(figsize=[6,6])  
    plt.boxplot(Max_G)
    axe=plt.gca()
    axe.set_xticklabels(["haut_avec","haut_sans","bas_avec","bas_sans"])
    axe.set_ylabel("Force [N]")
    axe.set_title("Boxplot des Grip Force maximum par conditions")
    fig.savefig("figures\Add\GF_%s"%(Name)) 
    
    # Load Force 
    fig=plt.figure(figsize=[6,6])  
    plt.boxplot(Max_L)
    axe=plt.gca()
    axe.set_xticklabels(["haut_avec","haut_sans","bas_avec","bas_sans"])
    axe.set_ylabel("Force [N]")
    axe.set_title("Boxplot des Load Force maximum par conditions")
    fig.savefig("figures\Add\LF_%s"%(Name))   
    
    # Slip Force 
    fig=plt.figure(figsize=[6,6])  
    plt.boxplot(Max_SF)
    axe=plt.gca()
    axe.set_xticklabels(["haut_avec","haut_sans","bas_avec","bas_sans"])
    axe.set_ylabel("Force [N]")
    axe.set_title("Boxplot des Slip Force maximum par conditions")
    fig.savefig("figures\Add\SF_%s"%(Name))  
    
    # Security marge entre
    fig=plt.figure(figsize=[6,6])  
    plt.boxplot(Moy_SME)
    axe=plt.gca()
    axe.set_xticklabels(["haut_avec","haut_sans","bas_avec","bas_sans"])
    axe.set_ylabel("Force [N]")
    axe.set_title("Boxplot des Security marge moyenne par conditions")
    fig.savefig("figures\Add\SM_entre_%s"%(Name))    