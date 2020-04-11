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

import glm_data_processing as glm
import derive as der

# Fermeture des figures ouvertes
plt.close('all')

subjects = ["alex","florent","victor","walid"] #Names of subjects
ntrials = 3 #Number of trials for each subject
essai_type = ["bas_avec", "bas_sans", "haut_avec", "haut_sans"] #type essai
# Double for-loop that runs thrgough all subjects and trials
tableau_final=[]

for e in essai_type:   
    moyenne_essai=np.array([])
    for s in subjects:
        moyenne_sujet=np.array([])
        for trial in range(1,ntrials+1): 
            # Set data path
            glm_path = r"C:\Users\victo\Desktop\Projet P4 mesures\Pythin\mesures\%s_%s_00%d.glm" %(s,e,trial) 
            
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
            pk = signal.find_peaks(abs(accX),  prominence=9,distance=400)
            ipk = pk[0]
            
            cycle_starts = ipk
            cycle_ends = ipk
            
            
            
            
            
            #Calcul de la moyenne
            moyenne = np.zeros(len(cycle_starts)-2)
            for i in range(1,len(cycle_starts)-1):
                
                debut=cycle_ends[i-1]-1000
                fin=cycle_starts[i]
                moyenne[i-1]=np.mean(GF[debut:fin+1])
            if(e=="bas_sans" and s=="victor" and trial==1 ):
                moyenne=np.absolute(moyenne)    
            print("La moyenne de l'essai %d de %s :\n" %(trial,s) ,moyenne,"\n")
            
            moyenne_sujet=np.concatenate((moyenne_sujet,moyenne))
            
            
            #fig2, ax2 = plt.subplots()
            #ax2.set_title('Notched boxes')
            #ax2.boxplot(moyenne, notch=False)
           
            #%% Save the figure as png file. Creates a folder "figures" first if it
            # doesn't exist
            #if not os.path.exists('figures'):
             #   os.makedirs('figures')
            
            #fig.savefig("figures\%s_%d_acc_forces_dGF.png" %(s,trial))
            
            #%% Pour calculer la moyenne 
        print("La moyenne totale de %s :\n" %s, moyenne_sujet,"\n")
            
        moyenne_essai=np.concatenate((moyenne_essai, moyenne_sujet))
    print("La moyenne totale pour %s:\n" %e,moyenne_essai)    
    fig2, ax2 = plt.subplots()
    ax2.set_title('%s'%e)
    red_square = dict(markerfacecolor='r', marker='s')
    ax2.boxplot(moyenne_essai, flierprops=red_square)
    moyenne_essai=np.ndarray.tolist(moyenne_essai)
    tableau_final = tableau_final + [moyenne_essai]
    
    
fig3, ax3 = plt.subplots()
ax3.set_title("Comparaison des moyennes dans les différents cas")
red_square = dict(markerfacecolor='r', marker='s')
ax3.boxplot(tableau_final, flierprops=red_square)
