#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  4 11:45:28 2020

@author: alexandreloffet
"""




#%% Importation des librairies necessaires
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import os

import glm_data_processing as glm
import derive as der

# Fermeture des figures ouvertes
plt.close('all')

#subjects = ["victor_haut_avec","victor_bas_avec","victor_haut_sans","victor_bas_sans"] #Names of subjects
subjects = ["alex_haut_avec","alex_bas_avec","alex_haut_sans","alex_bas_sans",
            "florent_haut_avec","florent_bas_avec","florent_haut_sans","florent_bas_sans",
            "victor_haut_avec","victor_bas_avec","victor_haut_sans","victor_bas_sans",
            "walid_haut_avec","walid_bas_avec","walid_haut_sans","walid_bas_sans"] #Names of subjects

ntrials = 3 #Number of trials for each subject

# Double for-loop that runs thrgough all subjects and trials
subject_number=0;
i=0
for s in subjects:
    for trial in range(1,ntrials+1): 
        if s!="victor_bas_sans" or trial!=1: #Pour virer le premier victor_bas_sans_001
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
            NF_thumb=glm.filter_signal(NF_thumb,   fs = freqAcq, fc = freqFiltForces)
            NF_index=glm.filter_signal(NF_index,   fs = freqAcq, fc = freqFiltForces)
            #%%
            BasouHaut = (i+1)/2
            DiffIT = NF_thumb-NF_index
            NFT_Thumb = NF_thumb
            #Pour changer pouce et index de capteur quand on renverse le manipulandum
            #important de garder les sujets alternés
            if BasouHaut.is_integer():
                DiffIT = NF_index-NF_thumb
                NF_thumb = NF_index
                NF_index = NFT_Thumb
            
            
            
            
            
            
            #%% Basic plot of the data
            fig = plt.figure(figsize = [15,7])
            ax  = fig.subplots(3,1)
            
            ax[0].plot(time, accX)
            #ax[0].plot(time[ipk],accX[ipk], linestyle='', marker='o', 
            #          markerfacecolor='None', markeredgecolor='r')
            ax[0].set_ylabel("Acceleration [m/s^2]", fontsize=13)
            ax[0].set_title("Graphe FN_index-FN_pouce pour l'expérience: %s %i " %(s,trial) , fontsize=14, fontweight="bold")
            ax[0].set_xlim([0,55]) #A:ici j'ai mis 50 pour avoir tout
            
            # Putting grey patches for cycles
            #     for i in range(0,len(cycle_starts)):
            #    rect0=plt.Rectangle((time[cycle_starts[i]],ax[0].get_ylim()[0]),\
            #                      time[cycle_ends[i]-cycle_starts[i]],\
            #                     ax[0].get_ylim()[1]-ax[0].get_ylim()[0],color='k',alpha=0.3)
            # ax[0].add_patch(rect0)
            
            ax[1].plot(time,LF, label="LF")
            ax[1].plot(time,NF_thumb, label="NF thumb")
            ax[1].plot(time,NF_index, label="NF index",color="cyan")
            ax[1].legend(fontsize=12)
            ax[1].set_xlabel("Time [s]", fontsize=13)
            ax[1].set_ylabel("Forces [N]", fontsize=13)
            ax[1].set_xlim([0,55]) #A:ici j'ai mis 50 pour avoir tout
            
            ax[2].plot(time,DiffIT,label="NF thumb-NF_index")
            ax[2].set_xlabel("Time [s]", fontsize=13)
            ax[2].set_ylabel("Diff NFt-NFi [N]", fontsize=13)
            ax[2].set_xlim([0,55])#A:ici j'ai mis 50 pour avoir tout
            
            """
            #%%
            #Save the figure as png file. Creates a folder "figures" first if it
            # doesn't exist
            if not os.path.exists('figures_FNg-FNd'):
                os.makedirs('figures_FNg-FNd')
            
                
            #fig.savefig("\%s_%d_acc_forces_dGF.png" %(s,trial))
            fig.savefig("figures_FNg-FNd/%s_%d_FNg_FNd.png" %(s,trial))
           """
           
        
    i=i+1
        
        
        
        
        
        