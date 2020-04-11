#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  4 12:24:55 2020

Demande des tuteurs pour voir si les capteurs ont bien fonctionné...
Comme F=ma ,si on plot F en fonction de a théoriquement on devrait obtenir une droite.
Manifestement ça ne fonctionne pas à la place ça nous sort des gros scrabouchas...
Peut-être du fait des chocs

@author: alexandreloffet
"""

#%% Importation des librairies necessaires
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import os

import glm_data_processing as glm

# Fermeture des figures ouvertes
plt.close('all')

subjects = ["alex_haut_avec"] #Names of subjects
#subjects = ["alex_haut_avec","alex_haut_sans","alex_bas_sans","alex_bas_avec",
 #           "florent_haut_avec","florent_haut_sans","florent_bas_sans","florent_bas_avec",
  #          "victor_haut_avec","victor_haut_sans","victor_bas_sans","victor_bas_avec",
   #         "walid_haut_avec","walid_haut_sans","walid_bas_sans","walid_bas_avec"] #Names of subjects

ntrials = 3 #Number of trials for each subject

# Double for-loop that runs thrgough all subjects and trials
subject_number=0;
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
        accY  = glm_df.loc[:,'LowAcc_Y'].to_numpy()*(-9.81)
        accZ  = glm_df.loc[:,'LowAcc_Z'].to_numpy()*(-9.81)
        accX  = accX-np.nanmean(accX[baseline])
        GF    = glm_df.loc[:,'GF'].to_numpy()
        GF    = GF-np.nanmean(GF[baseline])
        LFv   = TFx_thumb+TFx_index
        LFh   = TFz_thumb+TFz_index
        LF    = np.hypot(LFv,LFh)
        
        Acc= accX+accY+accZ
        ForceT=NF_thumb+TFx_thumb +TFz_thumb  
        ForceI=NF_index+TFx_index+TFz_index
        # %%Filter data
        freqAcq=800 #Frequence d'acquisition des donnees
        freqFiltAcc=20 #Frequence de coupure de l'acceleration
        freqFiltForces=20 #Frequence de coupure des forces

        #accX = glm.filter_signal(accX, fs = freqAcq, fc = freqFiltAcc)
        GF   = glm.filter_signal(GF,   fs = freqAcq, fc = freqFiltForces)
        LF   = glm.filter_signal(LF,   fs = freqAcq, fc = freqFiltForces)
        LFv   = glm.filter_signal(LFv,   fs = freqAcq, fc = freqFiltForces)
        LFh   = glm.filter_signal(LFh,   fs = freqAcq, fc = freqFiltForces)
        
        ACC_X=glm.filter_signal(accX, fs = freqAcq, fc = freqFiltAcc)
        ACC_Y=glm.filter_signal(accY, fs = freqAcq, fc = freqFiltAcc)
        ACC_Z=glm.filter_signal(accZ, fs = freqAcq, fc = freqFiltAcc)
        
        NFi=glm.filter_signal(NF_index, fs = freqAcq, fc = freqFiltAcc)
        TFxi=glm.filter_signal(TFx_index, fs = freqAcq, fc = freqFiltAcc)
        TFzi=glm.filter_signal(TFz_index, fs = freqAcq, fc = freqFiltAcc)
        
        NFp=glm.filter_signal(NF_thumb, fs = freqAcq, fc = freqFiltAcc)
        TFxp=glm.filter_signal(TFx_thumb, fs = freqAcq, fc = freqFiltAcc)
        TFzp=glm.filter_signal(TFz_thumb, fs = freqAcq, fc = freqFiltAcc)
        #%%
        #Pour avoir la force dans la direction y
        EnY=NF_thumb-NF_index
        
        #%% Basic plot of the data
        fig = plt.figure(figsize = [15,7])
        ax  = fig.subplots(3,1)
    
        ax[0].plot(accX,LFv)
        ax[0].set_ylabel("LFv", fontsize=13)
        ax[0].set_xlabel("ACC_X", fontsize=13)
        ax[0].set_title("Forces en fonction de l'accélération: %s %i " %(s,trial) , fontsize=14, fontweight="bold")
        ax[0].set_xlim([-35,50]) #A:ici j'ai mis 50 pour avoir tout
        
        
        ax[1].plot( accY,EnY)
        ax[1].set_xlabel("ACC_Y", fontsize=13)
        ax[1].set_ylabel("NFt-NFi", fontsize=13)
        ax[1].set_xlim([-35,50]) #A:ici j'ai mis 50 pour avoir tout
        
        ax[2].plot(accZ,LFh)
        ax[2].set_xlabel("ACC_Z", fontsize=13)
        ax[2].set_ylabel("LFh", fontsize=13)
        ax[2].set_xlim([-35,50])#A:ici j'ai mis 50 pour avoir tout
        
        """
        #%%
        #Save the figure as png file. Creates a folder "figures" first if it
        # doesn't exist
        if not os.path.exists('figures_F=ma'):
            os.makedirs('figures_F=ma')
        
        fig.savefig("figures_F=ma/%s_%d_test.png" %(s,trial))
        #Changer le backslash si vous êtes pas sur mac
        """
        