"""
Created on Fri Apr 24 19:31:31 2020

@author: Dany
"""
import gbio_example_script_collisions as gbio 
import matplotlib.pyplot as plt
import numpy as np 
import erreurs
import Add
import scipy.stats as sc
 
# =============================================================================
#     box plot de déplacement
# =============================================================================
def MoyDeplacement(dis,Name,Type) :
    Max= Add.Sum2(dis,lambda x:np.abs(np.min(x)),Name) 
              
    if Type=='all':
        names=['alex','walid','victor','florent']
    else :
        names=[Name]
  
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
               
            Dis = gbio.make_plots(start,end,Name=the_name,position=True,noreturn=False)
            
            for i in range(4):
                for j in range(3):
                    for item in Dis[i][j]: 
                        Max[i]=np.append(Max[i],[np.abs(np.min(item))])
    Alpha = 0.05                 
    if Type=="all":
        Name="general"
        
    Condition=["haut avec","haut sans","bas avec", "bas sans"]   
    for i in range (4): 
        _,Signif=sc.ttest_ind(Max[i][0],Max[i][1],equal_var=False)
        _,Signif1=sc.ttest_ind(Max[i][0],Max[i][2],equal_var=False)
        _,Signif2=sc.ttest_ind(Max[i][2],Max[i][1],equal_var=False)
        Masse=["100g","200g","300g"]
        
        if Alpha>Signif : 
            print("Significative difference of "+str(Signif)+" "+"for "+Condition[i]+": "+Masse[0]+" "+Masse[1])
        else : 
            print("No significative difference for "+Condition[i]+" between : "+Masse[0]+" "+Masse[1])
            print(str(Signif))
        if Alpha>Signif1 : 
            print("Significative difference of "+str(Signif1)+" "+"for "+Condition[i]+": "+Masse[0]+" "+Masse[2])
        else : 
            print("No significative difference for "+Condition[i]+" between : "+Masse[0]+" "+Masse[2])
            print(str(Signif1))
        if Alpha>Signif2 : 
            print("Significative difference of "+str(Signif2)+" "+"for "+Condition[i]+": "+Masse[1]+" "+Masse[2])
    
        else : 
            print("No significative difference for "+Condition[i]+" between : "+Masse[1]+" "+Masse[2])
            print(str(Signif2))
        fig=plt.figure(figsize=[6,6]) 
        plt.boxplot(Max[i])
        axe=plt.gca()
        axe.set_xticklabels(["100g","200g","300g"])
        axe.set_ylabel("déplacement [cm]")
        axe.set_title("Boxplot des déplacements maximum par masse pour "+Condition[i])
        fig.savefig("figures\Add\Position_%s_%s"%(Name,Condition[i]))   
    
    Max2=[None,None,None,None]
    Max2[0]=np.append(Max[0][0],np.append(Max[0][1],Max[0][2]))
    Max2[1]=np.append(Max[1][0],np.append(Max[1][1],Max[1][2]))
    Max2[2]=np.append(Max[2][0],np.append(Max[2][1],Max[2][2]))
    Max2[3]=np.append(Max[3][0],np.append(Max[3][1],Max[3][2]))
    fig=plt.figure(figsize=[6,6]) 
    plt.boxplot(Max2)
    axe=plt.gca()
    axe.set_xticklabels(Condition)
    axe.set_ylabel("déplacement [cm]")
    axe.set_title("Boxplot des déplacements maximum par masse pour "+Condition[i])
    #fig.savefig("figures\Add\Position_%s_%s"%(Name,Condition[i]))
    # for i in range(4):
    #     for j in range(i+1,4):
    #         _,Signif=sc.ttest_ind(Max2[i],Max2[j],equal_var=False)
     
    #         if Alpha>Signif : 
    #             print("Significative difference of"+str(Signif)+" "+"for "+Condition[i]+" and "+Condition[j])
    #         else : 
    #             print("No significative difference between : "+Condition[i]+" and "+Condition[j])
    #             print(str(Signif))
            

# =============================================================================
#     box plot de GF
# =============================================================================
def MoyForces(G,L,SF,SME,Name,Type):  
    global name, to_cancel
    
    name = Name
    to_cancel = erreurs.err(Name)
    
    Max_G=[np.array([]),np.array([]),np.array([]),np.array([])] 
    Max_L=[np.array([]),np.array([]),np.array([]),np.array([])]  
    Moy_SME=[np.array([]),np.array([]),np.array([]),np.array([])] 
    Max_SF=[np.array([]),np.array([]),np.array([]),np.array([])]   
    
    ind,blocks_ind,choc_number = Add.block_order() 
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
                
                ind,blocks_ind,choc_number = Add.block_order() 
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