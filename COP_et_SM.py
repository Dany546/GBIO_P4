#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 16:10:31 2020

Code pour voir si le manipulandum glisse quand la marge de sécurité devient négative (GF<SF).
Le début des lignes en jaunes indique le pic d'accélération.
@author: alexandreloffet
"""

import numpy as np
import glm_data_processing as glm
import matplotlib.pyplot as plt
from scipy import signal
import math
import os


#%% Def utiles
def SlipForce(n,k,TF): #calcule la force à laquelle le manipulandum glisse
    SlipF= pow(TF/2*k,1/n)
    return SlipF



#%% Autre façon de prendre les n et k: mu plus petit index/pouce et avant/après (cfr DifferentsNetK.py)
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

ListeNom=["Alexandre","Florent","Victor","Walid"]
#%%Code Felicien pour prendre et filtrer les données
#%%

plt.close('all')
subjects = ["walid_bas_sans"]
#subjects = ["alex_haut_avec","alex_haut_sans","alex_bas_sans","alex_bas_avec",
 #           "florent_haut_avec","florent_haut_sans","florent_bas_sans","florent_bas_avec",
  #          "victor_haut_avec","victor_haut_sans","victor_bas_sans","victor_bas_avec",
   #         "walid_haut_avec","walid_haut_sans","walid_bas_sans","walid_bas_avec"] #Names of subjects
ntrials = 3 #Number of trials for each subject

# Double for-loop that runs thrgough all subjects and trials
for s in subjects:
    for trial in range(1,ntrials+1): 
        # Set data path
        glm_path = "%s_00%d.glm" % (s,trial)
        
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
        GF    = GF-np.nanmean(GF[baseline])
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
        pk = signal.find_peaks(abs(accX),  prominence=9,distance=800)
        ipk = pk[0]
        cycle_starts = ipk
        cycle_ends = ipk+50
        #%%    SF et SM
        #Calcule de la slip force en fonction des coefficients de chacun
        if s[0]=="a":
            SF=SlipForce(N_CoeffAlex,K_CoeffAlex,LF)
            
        elif s[0]=="f":
            SF=SlipForce(N_CoeffFlo,K_CoeffFlo,LF)
            
        elif s[0]=="v":
            SF=SlipForce(N_CoeffVictor,K_CoeffVictor,LF)
            
        elif s[0]=="w":
            SF=SlipForce(N_CoeffWalid,K_CoeffWalid,LF)
        
        SM=GF-SF
        #%%Pour le COP
        #%%Compute COP manually
        Fal = -np.array([glm_df.loc[:,'Fxal'],glm_df.loc[:,'Fyal'],glm_df.loc[:,'Fzal']])
        Far = -np.array([glm_df.loc[:,'Fxar'],glm_df.loc[:,'Fyar'],glm_df.loc[:,'Fzar']])
        Tal = -np.array([glm_df.loc[:,'Txal'],glm_df.loc[:,'Tyal'],glm_df.loc[:,'Tzal']])
        Tar = -np.array([glm_df.loc[:,'Txar'],glm_df.loc[:,'Tyar'],glm_df.loc[:,'Tzar']])
    
        baseline=range(0,400)
        Fal=np.subtract(Fal,np.nanmean(Fal[:,baseline],1).reshape((3,1)))
        Far=np.subtract(Far,np.nanmean(Far[:,baseline],1).reshape((3,1)))
        Tal=np.subtract(Tal,np.nanmean(Tal[:,baseline],1).reshape((3,1)))
        Tar=np.subtract(Tar,np.nanmean(Tar[:,baseline],1).reshape((3,1)))
    
        z0=0.00155;
        COPthumb = -np.array([(Tal[1,:] + Fal[0,:]*z0)/Fal[2,:], -(Tal[0,:] - Fal[1,:]*z0)/Fal[2,:]])
        COPindex = -np.array([(Tar[1,:] + Far[0,:]*z0)/Far[2,:], -(Tar[0,:] - Far[1,:]*z0)/Far[2,:]]) 
    
        COPthumb_g=-COPthumb[0,:]*math.sin(0.523599)-COPthumb[1,:]*math.cos(0.523599)
        COPindex_g=COPindex[0,:]*math.sin(0.523599)+COPindex[1,:]*math.cos(0.523599)
        
        #%% Affichage des figures
        
        fig = plt.figure(figsize = [15,7])
        ax  = fig.subplots(3,1)
        
        ax[0].set_title("Graphe pour la marge de sécurité et le glissement de l'expérience: %s %i " %(s,trial) , fontsize=14, fontweight="bold")
        ax[0].plot(time,SM, label="Security Marge")
        ax[0].legend(fontsize=12)
        ax[0].set_ylabel("Force [N]", fontsize=13)
        ax[0].set_xlim([0,55])
        # Putting grey patches for cycles
        for i in range(0,len(cycle_starts)):
            rect0=plt.Rectangle((time[cycle_starts[i]],ax[0].get_ylim()[0]),\
                               time[cycle_ends[i]-cycle_starts[i]],\
                               ax[0].get_ylim()[1]-ax[0].get_ylim()[0],color='y',alpha=0.3)
            ax[0].add_patch(rect0)
        
        ax[1].set_title("Index", fontsize=14, fontweight="bold")
        ax[1].plot(time, COPindex_g*1000)
        ax[1].set_ylabel("COP [mm]", fontsize=13)
        ax[1].set_ylim([-25,25])
        ax[1].set_xlim([0,55])
        for i in range(0,len(cycle_starts)):
            rect0=plt.Rectangle((time[cycle_starts[i]],ax[1].get_ylim()[0]),\
                               time[cycle_ends[i]-cycle_starts[i]],\
                               ax[1].get_ylim()[1]-ax[1].get_ylim()[0],color='y',alpha=0.3)
            ax[1].add_patch(rect0)
            
        
        ax[2].set_title("Thumb", fontsize=14, fontweight="bold")
        ax[2].plot(time, COPthumb_g*1000)
        ax[2].set_ylabel("COP [mm]", fontsize=13)
        ax[2].set_ylim([-25,25])
        ax[2].set_xlim([0,55])
        for i in range(0,len(cycle_starts)):
            rect0=plt.Rectangle((time[cycle_starts[i]],ax[2].get_ylim()[0]),\
                               time[cycle_ends[i]-cycle_starts[i]],\
                               ax[2].get_ylim()[1]-ax[2].get_ylim()[0],color='y',alpha=0.3)
            ax[2].add_patch(rect0)
    
        
        """
        #%% Enregistrement des plots
        if not os.path.exists('figures_SMetCOP'):
            os.makedirs('figures_SMetCOP')
        fig.savefig("figures_SMetCOP/%s_%d_SMetCOP.png" %(s,trial))
        #Si vous êtes pas sur mac faut changer le backslash en slash
        """
        #%%









