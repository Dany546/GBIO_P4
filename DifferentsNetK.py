#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 10:26:16 2020

Pour déterminer quels N et K on prend pour chacun.
On va prendre le mu le plus petit par personne (Pouce/index et avant/après) pour calculer la marge de sécurité.


@author: alexandreloffet
"""


def SlipForce(n,k,TF): #calcule la slip force
    SlipF= pow(TF/2*k,1/n)
    return SlipF

flux = open("différents_coeff.txt","w")
flux.write("Différents N et K"+"\n"+"\n")
flux.write("Voici les données que nous renvoie la fonction better_example_friction.py :"+"\n")
    
flux.write("N_IAlex=[0.5722961232012791,0.6684962526224016]"+"\n"
           "N_PAlex=[0.6432730566031946,0.6421595151481689]"+"\n"
           "K_IAlex=[1.7002547264532362,1.450168010182277]"+"\n"
           "K_PAlex=[1.873263099364286,1.8866959417752258]"+"\n"+"\n"
           "N_IFlo=[0.903905376625217,0.7706344311088271]"+"\n"
           "N_PFlo=[0.8244907310543801,0.7402058639164167]"+"\n"
           "K_IFlo=[1.4516428129439272,1.8347237562200995]"+"\n"
           "K_PFlo=[1.4548983522387278,1.6567930102080082]"+"\n"+"\n"
           "N_IVictor=[0.6974757794117483]"+"\n"
           "N_PVictor=[0.6208810163847297]"+"\n"
           "K_IVictor=[1.4013834508779774]"+"\n"
           "K_PVictor=[1.4583906664027992]"+"\n"+"\n"
           "N_IWalid=[0.660240161129793,0.698352289086897]"+"\n"
           "N_PWalid=[0.6704288293980596,0.6333643033817357]"+"\n"
           "K_IWalid=[1.5637172616270336,1.2748140202603586]"+"\n"
           "K_PWalid=[1.4195189570873041,1.3488218066303728]"+"\n"+"\n")

flux.write("Sur base de ces données on calcule la slip force avec la formule: SlipF= pow(TF/2*k,1/n)"+"\n")
flux.write("Ci-dessous on peut observer les forces de glissement calculées pour les différents N et K.""\n")
flux.write("J'ai posé une LF de 10N. La LF et la SF sont liées par: LF= mu*SF "+"\n"+"\n")

N_IAlex=[0.5722961232012791,0.6684962526224016]
N_PAlex=[0.6432730566031946,0.6421595151481689]
K_IAlex=[1.7002547264532362,1.450168010182277]
K_PAlex=[1.873263099364286,1.8866959417752258]


TF=10
flux.write("Alexandre"+"\n")
flux.write("Index avant:  "+str(SlipForce(N_IAlex[0],K_IAlex[0],TF))+"\n")
flux.write("Mu vaut: LF/SF = "+str(TF/SlipForce(N_IAlex[0],K_IAlex[0],TF))+"\n")
flux.write("Soucis: lâché pendant friction"+"\n"+"\n")

flux.write("Pouce avant:  "+str(SlipForce(N_PAlex[0],K_PAlex[0],TF))+"\n")
flux.write("Mu vaut: LF/SF = "+str(TF/SlipForce(N_PAlex[0],K_PAlex[0],TF))+"\n")
flux.write("Soucis: lâché pendant friction"+"\n"+"\n")

flux.write("Index après: "+str(SlipForce(N_IAlex[1],K_IAlex[1],TF))+"\n")
flux.write("Mu vaut: LF/SF = "+str(TF/SlipForce(N_IAlex[1],K_IAlex[1],TF))+"\n"+"\n")

flux.write("Pouce après:  "+str(SlipForce(N_PAlex[1],K_PAlex[1],TF))+"\n")
flux.write("Mu vaut: LF/SF = "+str(TF/SlipForce(N_PAlex[1],K_PAlex[1],TF))+"\n")
flux.write("On va donc prendre celui-ci pour le calcul de la marge de sécurité pour Alexandre "+"\n"+"\n"+"\n")


flux.write("Florent"+"\n")
N_IFlo=[0.903905376625217,0.7706344311088271]
N_PFlo=[0.8244907310543801,0.7402058639164167]
K_IFlo=[1.4516428129439272,1.8347237562200995]
K_PFlo=[1.4548983522387278,1.6567930102080082]
flux.write("Index avant:  "+str(SlipForce(N_IFlo[0],K_IFlo[0],TF))+"\n")
flux.write("Mu vaut: LF/SF = "+str(TF/SlipForce(N_IFlo[0],K_IFlo[0],TF))+"\n")
flux.write("Soucis: Plot index moche"+"\n"+"\n")

flux.write("Pouce avant:  "+str(SlipForce(N_PFlo[0],K_PFlo[0],TF))+"\n")
flux.write("Mu vaut: LF/SF = "+str(TF/SlipForce(N_PFlo[0],K_PFlo[0],TF))+"\n"+"\n")

flux.write("Index après: "+str(SlipForce(N_IFlo[1],K_IFlo[1],TF))+"\n")
flux.write("Mu vaut: LF/SF = "+str(TF/SlipForce(N_IFlo[1],K_IFlo[1],TF))+"\n")
flux.write("Soucis: +-= à 1 sur le plot"+"\n"+"\n")

flux.write("Pouce après: "+str(SlipForce(N_PFlo[1],K_PFlo[1],TF))+"\n")
flux.write("Mu vaut: LF/SF = "+str(TF/SlipForce(N_PFlo[1],K_PFlo[1],TF))+"\n")
flux.write("On va donc prendre celui-ci pour le calcul de la marge de sécurité pour Florent"+"\n"+"\n"+"\n")

flux.write("Victor"+"\n")
N_IVictor=[0.6974757794117483]
N_PVictor=[0.6208810163847297]
K_IVictor=[1.4013834508779774]
K_PVictor=[1.4583906664027992]
flux.write("Index avant:"+str(SlipForce(N_IVictor[0],K_IVictor[0],TF))+"\n")
flux.write("Mu vaut: LF/SF = "+str(TF/SlipForce(N_IVictor[0],K_IVictor[0],TF))+"\n"+"\n")

flux.write("Pouce avant:"+str(SlipForce(N_PVictor[0],K_PVictor[0],TF))+"\n")
flux.write("Mu vaut: LF/SF = "+str(TF/SlipForce(N_PVictor[0],K_PVictor[0],TF))+"\n")
flux.write("On va donc prendre celui-ci pour le calcul de la marge de sécurité pour Victor "+"\n"+"\n")

flux.write("Pas de données exploitables pour Victor après"+"\n"+"\n"+"\n")



flux.write("Walid"+"\n")
N_IWalid=[0.660240161129793,0.698352289086897]
N_PWalid=[0.6704288293980596,0.6333643033817357]
K_IWalid=[1.5637172616270336,1.2748140202603586]
K_PWalid=[1.4195189570873041,1.3488218066303728]
flux.write("Index avant: "+str(SlipForce(N_IWalid[0],K_IWalid[0],TF))+"\n")
flux.write("Mu vaut: LF/SF = "+str(TF/SlipForce(N_IWalid[0],K_IWalid[0],TF))+"\n")
flux.write("Soucis: Plot mu index plus grand que pouce sur le graphe"+"\n"+"\n")

flux.write("Pouce avant: "+str(SlipForce(N_PWalid[0],K_PWalid[0],TF))+"\n")
flux.write("Mu vaut: LF/SF = "+str(TF/SlipForce(N_PWalid[0],K_PWalid[0],TF))+"\n"+"\n")

flux.write("Index après: "+str(SlipForce(N_IWalid[1],K_IWalid[1],TF))+"\n")
flux.write("Mu vaut: LF/SF = "+str(TF/SlipForce(N_IWalid[1],K_IWalid[1],TF))+"\n"+"\n")

flux.write("Pouce après: "+str(SlipForce(N_PWalid[1],K_PWalid[1],TF))+"\n")
flux.write("Mu vaut: LF/SF = "+str(TF/SlipForce(N_PWalid[1],K_PWalid[1],TF))+"\n")
flux.write("On va donc prendre celui-ci pour le calcul de la marge de sécurité pour Walid "+"\n"+"\n"+"\n")

flux.close()











