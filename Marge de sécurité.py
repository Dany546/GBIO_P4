#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 10:31:55 2020

Pour le calcul et le plot de la marge de sécurité

@author: alexandreloffet
"""

import numpy as np
import glm_data_processing as glm
import matplotlib.pyplot as plt
import os


#%% Def utiles
def SlipForce(n,k,TF): #calcule la slip force
    SlipF= pow(TF/2*k,1/n)
    return SlipF

#Pour Append les coeffs
def Ap(A1,A2):
    for i in range(2):
        A1.append(A2[i])


"""
Acienne méthode pour calculer les coeff où je faisait une moyenne puis je prennais le mu maximum
#%%Coefficients de frictions calculé par la fonction de félicien
#N
N_IAlex=[0.5722961232012791,0.6684962526224016]
N_IAlex=np.nanmean(N_IAlex)
N_PAlex=[0.6432730566031946,0.6421595151481689]
N_PAlex=np.nanmean(N_PAlex)
N_CoeffAlex=np.maximum(N_IAlex,N_PAlex)
print(N_CoeffAlex)


N_IFlo=[0.903905376625217,0.7706344311088271]
N_PFlo=[0.8244907310543801,0.7402058639164167]
N_IVictor=[0.6974757794117483]
N_PVictor=[0.6208810163847297]
N_IWalid=[0.660240161129793,0.698352289086897]
N_PWalid=[0.6704288293980596,0.6333643033817357]

#K
K_IAlex=[1.7002547264532362,1.450168010182277]
K_IAlex=np.nanmean(K_IAlex)
K_PAlex=[1.873263099364286,1.8866959417752258]
K_PAlex=np.nanmean(K_PAlex)
K_CoeffAlex=np.maximum(K_IAlex,K_PAlex)
print(K_CoeffAlex)

K_IFlo=[1.4516428129439272,1.8347237562200995]
K_PFlo=[1.4548983522387278,1.6567930102080082]
K_IVictor=[1.4013834508779774]
K_PVictor=[1.4583906664027992]
K_IWalid=[1.5637172616270336,1.2748140202603586]
K_PWalid=[1.4195189570873041,1.3488218066303728]

#%% N et K moyen par persone
#ici on fait la moyenne avant/apres et pouce/index
#Je ne sais pas si on considère pouce et index séparément dans le doute je prend la moyenne
#Ap(N_IAlex,N_PAlex)
#N_CoeffAlex=np.mean(N_IAlex)

Ap(N_IFlo,N_PFlo)
N_CoeffFlo=np.mean(N_IFlo)

N_IVictor.append(N_PVictor[0])
N_CoeffVictor=np.mean(N_IVictor)

Ap(N_IWalid,N_PWalid)
N_CoeffWalid=np.mean(N_IWalid)

#Ap(K_IAlex,K_PAlex)
K_CoeffAlex=np.mean(K_IAlex)

Ap(K_IFlo,K_PFlo)
K_CoeffFlo=np.mean(K_IFlo)

K_IVictor.append(K_PVictor[0])
K_CoeffVictor=np.mean(K_IVictor)

Ap(K_IWalid,K_PWalid)
K_CoeffWalid=np.mean(K_IWalid)

# Tous les N et K dans un tableau 
Ntab=[N_CoeffAlex,N_CoeffFlo,N_CoeffVictor,N_CoeffWalid]
Ktab=[K_CoeffAlex,K_CoeffFlo,K_CoeffVictor,K_CoeffWalid]
"""
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

ListeNom=["Alexandre","Florent","Victor","Walid"]
#%%Code Felicien pour prendre et filtrer les données
#%%

#flux = open("marge_de_sec_moy.txt","w")
#flux.write("Feuille pour voir les différentes marges de sécurités"+"\n"+"\n")
moytab=[]

plt.close('all')
subjects = ["alex_haut_sans"]
#subjects = ["alex_haut_avec","alex_haut_sans","alex_bas_sans","alex_bas_avec",
 #           "florent_haut_avec","florent_haut_sans","florent_bas_sans","florent_bas_avec",
  #          "victor_haut_avec","victor_haut_sans","victor_bas_sans","victor_bas_avec",
   #         "walid_haut_avec","walid_haut_sans","walid_bas_sans","walid_bas_avec"] #Names of subjects
ntrials = 3 #Number of trials for each subject

# Double for-loop that runs thrgough all subjects and trials
i=0 #compteur
SFM=[]
for s in subjects:
    SFM.clear
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
        #%%Fin code Felicien
        #%%    SF et SM
        #Calcule de la slip force en fonction des coefficients de chacun
        if s[0]=="a":
            SF=SlipForce(N_CoeffAlex,K_CoeffAlex,LF)
            
        if s[0]=="f":
            SF=SlipForce(N_CoeffFlo,K_CoeffFlo,LF)
            
        if s[0]=="v":
            SF=SlipForce(N_CoeffVictor,K_CoeffVictor,LF)
            
        if s[0]=="w":
            SF=SlipForce(N_CoeffWalid,K_CoeffWalid,LF)
        
        SM=GF-SF
        SFM.append(SF)
        
        #%% Affichage des figures
        
        fig = plt.figure(figsize = [15,7])
        ax  = fig.subplots(3,1)
        ax[0].plot(time, accX)
        ax[0].set_ylabel("Acceleration [m/s^2]", fontsize=13)
        ax[0].set_title("Graphe pour la marge de sécurité de l'expérience: %s %i " %(s,trial) , fontsize=14, fontweight="bold")
        ax[0].set_xlim([0,55])
        
        ax[1].plot(time,SF, label="Slip Force")
        ax[1].plot(time,GF, label="GF")
        ax[1].legend(fontsize=12)
        ax[1].set_xlabel("Time [s]", fontsize=13)
        ax[1].set_ylabel("Forces [N]", fontsize=13)
        ax[1].set_xlim([0,55])
        
        ax[2].plot(time,SM, label="Security Marge")
        ax[2].legend(fontsize=12)
        ax[2].set_ylabel("Force [N]", fontsize=13)
        ax[2].set_xlim([0,55])
        """
        #%% Enregistrement des plots
        if not os.path.exists('figures_secmarge'):
            os.makedirs('figures_secmarge')
        fig.savefig("figures_secmarge/%s_%d_marge_securité.png" %(s,trial))
        """
        """
        #%% Pour calculer la moyenne de marge de sécurité =>faut changer les commentaires plus haut le flux.open et le flux.close
        moySM=np.nanmean(SM)
        moytab.append(moySM)
        compte=trial/3
    
        if compte.is_integer():
            SMparExp= np.nanmean(moytab)
            flux.write("La marge de sécurité pour %s est de %f"%(s,SMparExp)+'\n')
            moytab.clear()
        
        
        """
        #%%
    
    i=i+1 #augmente le compteur
    print(np.nanmean(SFM))
#flux.close()









