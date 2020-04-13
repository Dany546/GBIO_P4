# -*- coding: utf-8 -*-
"""
Example script for processing and plotting GLM data
The script uses the data of an oscillation task performed with the 
manipulandum (file TEST_DATA.glm)

Created on Wed Jan 29 11:16:06 2020

@author: opsomerl & fschiltz
"""
#%% Importation des librairies necessaires
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import os
from integ import integ as Positions
import glm_data_processing as glm
import derive as der
import Add 
import erreurs

# Fermeture des figures ouvertes
plt.close('all') 

donnees_accX = [[],[],[],[]] # haut avec, haut sans, bas avec, bas sans
donnees_GF = [[],[],[],[]] 
donnees_LF = [[],[],[],[]]  
donnees_dGF = [[],[],[],[]] 
donnees_SF = [[],[],[],[]] 
donnees_SM = [[],[],[],[]] 
to_cancel = None
delai = [[],[],[],[]]
vit = [[[],[],[]],[[],[],[]],[[],[],[]],[[],[],[]]]
dis = [[[],[],[]],[[],[],[]],[[],[],[]],[[],[],[]]] 
  
# Double for-loop that runs through all subjects and trials 
def make_plots(beginning,The_end,Name='alex',Delai=False,add=False,zoom=False,chock_number=1,Trial=0,Type='',noreturn=True):
    global donnees_accX, donnees_GF, donnees_LF, donnees_dGF, vit, dis, to_cancel, donnees_SF, donnees_SM  
    file=os.listdir("mesures") 
    subjects=[path.split('_')[0]+'_'+path.split('_')[1]+'_'+path.split('_')[2] for i,path in enumerate(file) if i%3 == 0] 
    donnees_accX = [[],[],[],[]] # haut avec, haut sans, bas avec, bas sans
    donnees_GF = [[],[],[],[]] 
    donnees_LF = [[],[],[],[]]  
    donnees_dGF = [[],[],[],[]]  
    donnees_SF = [[],[],[],[]] 
    donnees_SM = [[],[],[],[]] 
    delai = [[],[],[],[]]
    vit = [[[],[],[]],[[],[],[]],[[],[],[]],[[],[],[]]]
    dis = [[[],[],[]],[[],[],[]],[[],[],[]],[[],[],[]]] 
    subjects = subjects[beginning:The_end]
    to_cancel = erreurs.err(Name)
    if zoom and (not add) and (not Delai): 
        subjects = [subjects]         
    for s in subjects:
        name,hb,block = s.split('_')[:3] 
        for trial in range(1,4): 
            if trial==Trial or Trial==0:
                # Set data path
                glm_path = "mesures/%s_00%d.glm" % (s,trial)
                
                # Import data 
                glm_df = glm.import_data(glm_path)
                
                baseline = range(0,400)        
                # Normal Force exerted by the thumb
                NF_thumb = glm_df.loc[:,'Fygl']-np.nanmean(glm_df.loc[baseline,'Fygl'])
                # Vertical Tangential Force exerted by the thumb
                TFx_thumb  = glm_df.loc[:,'Fxgl']-np.nanmean(glm_df.loc[baseline,'Fxgl'])
                #Horizontal Tangential Force exerted by the thumb
                TFz_thumb  = glm_df.loc[:,'Fzgl']-np.nanmean(glm_df.loc[baseline,'Fzgl'])
         
                # Normal Force exerted by the index
                NF_index = -(glm_df.loc[:,'Fygr']-np.nanmean(glm_df.loc[baseline,'Fygr']))
                # Vertical Tangential Force exerted by the index
                TFx_index = glm_df.loc[:,'Fxgr']-np.nanmean(glm_df.loc[baseline,'Fxgr'])
                #Horizontal Tangential Force exerted by the index
                TFz_index = glm_df.loc[:,'Fzgr']-np.nanmean(glm_df.loc[baseline,'Fzgr'])
                 
                #%% Get acceleration, LF and GF
                time  = glm_df.loc[:,'time'].to_numpy()
                accX  = glm_df.loc[:,'LowAcc_X'].to_numpy()*(-9.81)
                accX  = accX-np.nanmean(accX[baseline])
                GF    = glm_df.loc[:,'GF'].to_numpy()
                
                if name=='victor' and hb=='bas' and  block=='sans' and trial==1:
                    GF = GF-np.nanmin(GF)
                else: 
                    GF = GF-np.nanmean(GF[baseline])
                    
                LFv   = TFx_thumb+TFx_index
                LFh   = TFz_thumb+TFz_index
                LF    = np.hypot(LFv,LFh)
                
                # %%Filter data
                freqAcq=800 #Frequence d'acquisition des donnees
                freqFiltAcc=20 #Frequence de coupure de l'acceleration
                freqFiltForces=20 #Frequence de coupure des forces
                  
                accX = glm.filter_signal(accX, fs = freqAcq, fc = freqFiltAcc)   
                GF   = glm.filter_signal(GF,   fs = freqAcq, fc = freqFiltForces)
                LF   = glm.filter_signal(LF,   fs = freqAcq, fc = freqFiltForces)
                LFv   = glm.filter_signal(LFv,   fs = freqAcq, fc = freqFiltForces)
                LFh   = glm.filter_signal(LFh,   fs = freqAcq, fc = freqFiltForces)
                
                #%% CUTTING THE TASK INTO SEGMENTS (your first task)
                pk = signal.find_peaks(abs(accX),prominence=4.5,distance=2000) # avant:prominence=9,distance=1000
                ipk = pk[0] 
                 
                if name=='victor' and hb=='haut' and block=='avec' and trial==1:
                    ip = [-1 if ii == 4 else ipk[ii] for ii in range(5)]
                    ipk = np.append(ip,ipk[4:])
                elif name=='victor' and hb=='bas' and block=='sans' and trial==1: 
                    ipk = np.append([-1],ipk) 
                elif name=='alex' and hb=='bas' and block=='sans' and trial==1:
                    ip = [-1 if ii == 2 else ipk[ii] for ii in range(3)]
                    ipk = np.append(ip,ipk[2:]) 
                elif name=='alex' and hb=='haut' and block=='avec' and trial==2:
                    ip = [-1 if ii == 6 else ipk[ii] for ii in range(7)]
                    ipk = np.append(ip,ipk[6:])  
                elif name=='florent' and hb=='bas' and block=='avec' and trial==1:
                    ip = [-1 if ii == 1 else ipk[ii] for ii in range(2)]
                    ipk = np.append(ip,ipk[1:])  
                elif name=='florent' and hb=='haut' and block=='avec' and trial==2:
                    ip = [-1 if ii == 6 else ipk[ii] for ii in range(7)]
                    ipk = np.append(ip,ipk[6:])  
                elif name=='florent' and hb=='bas' and block=='sans' and trial==1:
                    ip = [-1 if ii == 7 else ipk[ii] for ii in range(8)]
                    ipk = np.append(ip,ipk[7:])  
                elif name=='florent' and hb=='haut' and block=='sans' and trial==3:
                    ip = [-1 if ii == 4 else ipk[ii] for ii in range(5)]
                    ipk = np.append(ip,ipk[4:])  
                        
                if len(ipk)>10:
                    ipk = ipk[:10]  
                
                bk = np.zeros(1200)    
                         
                cycle_starts = ipk-400  # 1 seconde = 800 
                cycle_ends = ipk+800
                
                start = time[cycle_starts[chock_number-1]] 
                end = time[cycle_ends[chock_number-1]] 
                       
                #%% Compute derivative of LF
                dGF=der.derive(GF,800)
                dGF=glm.filter_signal(dGF, fs = freqAcq, fc = 10)
                
                if (not add) and (not zoom): 
                    accX = accX[0:ipk[-1]+3200]  
                    GF   = GF[0:ipk[-1]+3200]
                    LF   = LF[0:ipk[-1]+3200]
                    dGF  = dGF[0:ipk[-1]+3200] 
                    time  = time[0:ipk[-1]+3200] 
                    
                #%%   alexandre était ici :)  
                    
                #%% Autre façon de prendre les n et k: mu plus petit index/pouce et avant/après cfr DifferentsNetK.py
                N_PAlex=[0.6421595151481689]
                K_PAlex=[1.8866959417752258]
                N_CoeffAlex=N_PAlex[0]
                K_CoeffAlex=K_PAlex[0]
                
                K_PFlo=[1.6567930102080082]
                N_PFlo=[0.7402058639164167]
                N_CoeffFlo=N_PFlo[0]
                K_CoeffFlo=K_PFlo[0]
                
                N_PVictor=[0.6208810163847297]
                K_PVictor=[1.4583906664027992]
                N_CoeffVictor=N_PVictor[0]
                K_CoeffVictor=K_PVictor[0]
                
                N_PWalid=[0.6333643033817357]
                K_PWalid=[1.3488218066303728]
                N_CoeffWalid=N_PWalid[0]
                K_CoeffWalid=K_PWalid[0]
 
                #%%    SF et SM 
                #Calcule de la slip force en fonction des coefficients de chacun
                if s[0]=="a":
                    SF=pow(LF/2*K_CoeffAlex,1/N_CoeffAlex) 
                    
                if s[0]=="f":
                    SF=pow(LF/2*K_CoeffFlo,1/N_CoeffFlo) 
                
                if s[0]=="v":
                    SF=pow(LF/2*K_CoeffVictor,1/N_CoeffVictor) 
                
                if s[0]=="w":
                    SF=pow(LF/2*K_CoeffWalid,1/N_CoeffWalid) 
            
                SM=GF-SF
                
                #%% alexandre est parti :( 
                
                #%% Basic plot of the data  
                fig = None ; ax = None
                if zoom and (not add) and (not Delai) and (not Marge):
                    fig = plt.figure(figsize = [3,12]) 
                elif (not add) and (not Delai):
                    fig = plt.figure(figsize = [15,7])
                if add or Delai:  
                    if hb == 'haut': 
                        if block == 'avec':
                            donnees_accX[0].append([bk if st<0 else accX[st:e] for st,e in zip(cycle_starts,cycle_ends)]) 
                            donnees_GF[0].append([bk if st<0 else GF[st:e] for st,e in zip(cycle_starts,cycle_ends)]) 
                            donnees_LF[0].append([bk if st<0 else LF[st:e] for st,e in zip(cycle_starts,cycle_ends)]) 
                            donnees_dGF[0].append([bk if st<0 else dGF[st:e] for st,e in zip(cycle_starts,cycle_ends)])
                            donnees_SF[0].append([bk if st<0 else SF[st:e] for st,e in zip(cycle_starts,cycle_ends)])
                            donnees_SM[0].append([bk if st<0 else SM[st:e] for st,e in zip(cycle_starts,cycle_ends)])  
                            for st,e in zip(cycle_starts,cycle_ends):
                                if st<0: 
                                    vit[0][trial-1].append(bk) 
                                    dis[0][trial-1].append(bk) 
                                else: 
                                    v,d =Positions(accX[st:e],time[st:e])
                                    vit[0][trial-1].append(v) 
                                    dis[0][trial-1].append(d)  
                        elif block == 'sans':
                            donnees_accX[1].append([bk if st<0 else accX[st:e] for st,e in zip(cycle_starts,cycle_ends)]) 
                            donnees_GF[1].append([bk if st<0 else GF[st:e] for st,e in zip(cycle_starts,cycle_ends)]) 
                            donnees_LF[1].append([bk if st<0 else LF[st:e] for st,e in zip(cycle_starts,cycle_ends)]) 
                            donnees_dGF[1].append([bk if st<0 else dGF[st:e] for st,e in zip(cycle_starts,cycle_ends)]) 
                            donnees_SF[1].append([bk if st<0 else SF[st:e] for st,e in zip(cycle_starts,cycle_ends)])
                            donnees_SM[1].append([bk if st<0 else SM[st:e] for st,e in zip(cycle_starts,cycle_ends)])  
                            for st,e in zip(cycle_starts,cycle_ends):
                                if st<0: 
                                    vit[1][trial-1].append(bk) 
                                    dis[1][trial-1].append(bk) 
                                else: 
                                    v,d =Positions(accX[st:e],time[st:e])
                                    vit[1][trial-1].append(v) 
                                    dis[1][trial-1].append(d)  
                    elif hb == 'bas':
                        if block == 'avec':
                            donnees_accX[2].append([bk if st<0 else accX[st:e] for st,e in zip(cycle_starts,cycle_ends)]) 
                            donnees_GF[2].append([bk if st<0 else GF[st:e] for st,e in zip(cycle_starts,cycle_ends)]) 
                            donnees_LF[2].append([bk if st<0 else LF[st:e] for st,e in zip(cycle_starts,cycle_ends)]) 
                            donnees_dGF[2].append([bk if st<0 else dGF[st:e] for st,e in zip(cycle_starts,cycle_ends)]) 
                            donnees_SF[2].append([bk if st<0 else SF[st:e] for st,e in zip(cycle_starts,cycle_ends)])
                            donnees_SM[2].append([bk if st<0 else SM[st:e] for st,e in zip(cycle_starts,cycle_ends)]) 
                            for st,e in zip(cycle_starts,cycle_ends):
                                if st<0: 
                                    vit[2][trial-1].append(bk) 
                                    dis[2][trial-1].append(bk) 
                                else: 
                                    v,d =Positions(accX[st:e],time[st:e])
                                    vit[2][trial-1].append(v) 
                                    dis[2][trial-1].append(d)  
                        elif block == 'sans':
                            donnees_accX[3].append([bk if st<0 else accX[st:e] for st,e in zip(cycle_starts,cycle_ends)]) 
                            donnees_GF[3].append([bk if st<0 else GF[st:e] for st,e in zip(cycle_starts,cycle_ends)]) 
                            donnees_LF[3].append([bk if st<0 else LF[st:e] for st,e in zip(cycle_starts,cycle_ends)]) 
                            donnees_dGF[3].append([bk if st<0 else dGF[st:e] for st,e in zip(cycle_starts,cycle_ends)])  
                            donnees_SF[3].append([bk if st<0 else SF[st:e] for st,e in zip(cycle_starts,cycle_ends)])
                            donnees_SM[3].append([bk if st<0 else SM[st:e] for st,e in zip(cycle_starts,cycle_ends)]) 
                            for st,e in zip(cycle_starts,cycle_ends):
                                if st<0:  
                                    vit[3][trial-1].append(bk) 
                                    dis[3][trial-1].append(bk)  
                                else: 
                                    v,d =Positions(accX[st:e],time[st:e])
                                    vit[3][trial-1].append(v) 
                                    dis[3][trial-1].append(d)  
                else:    
                    ax  = fig.subplots(3,1) 
                    
                    ax[0].set_ylabel("Acceleration [m/s^2]", fontsize=13)
                    ax[0].set_title("Simple example of GLM data", fontsize=14, fontweight="bold")
                   
                    ax[1].set_xlabel("Time [s]", fontsize=13)
                    ax[1].set_ylabel("Forces [N]", fontsize=13)
                    
                    ax[2].set_xlabel("Time [s]", fontsize=13)
                    ax[2].set_ylabel("GF derivative [N/s]", fontsize=13)
                    
                    ax[0].plot(time, accX)
                    ax[0].plot(time[ipk],accX[ipk], linestyle='', marker='o', 
                           markerfacecolor='None', markeredgecolor='r')
                    ax[1].plot(time,LF, label="LF")
                    ax[1].plot(time,GF, label="GF")
                    ax[1].legend(fontsize=12)
                    ax[2].plot(time,dGF)
                    if zoom:
                        ax[0].set_xlim([start,end])
                        ax[1].set_xlim([start,end])
                        ax[2].set_xlim([start,end])
                        mini = accX[ipk[chock_number-1]]
                        ax[0].set_ylim([mini-2,-mini])  
                    
                if (not zoom) and (not add) and (not Delai):
                    # Putting grey patches for cycles
                    for i in range(0,len(cycle_starts)):
                        rect0=plt.Rectangle((time[cycle_starts[i]],ax[0].get_ylim()[0]),\
                                           time[cycle_ends[i]-cycle_starts[i]],\
                                           ax[0].get_ylim()[1]-ax[0].get_ylim()[0],color='k',alpha=0.3)
                        ax[0].add_patch(rect0)
                    
                #%% Save the figure as png file. Creates a folder "figures" first if it
                # doesn't exist
                if not fig==None:
                    if not os.path.exists('figures'):
                        os.makedirs('figures')
                    
                    fig.savefig("figures\%s_%d_acc_forces_dGF.png" %(s,trial)) 
                    
    if add and noreturn:
        Add.superpose(Name,Type)
    elif add:
        return donnees_accX, donnees_GF, donnees_LF, donnees_dGF, vit, dis, to_cancel, donnees_SF, donnees_SM      
    elif Delai:
        Add.delai(Name)                                        