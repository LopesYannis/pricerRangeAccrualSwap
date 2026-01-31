import numpy as np
import matplotlib.pyplot as plt

T=2.0
Nval=252
n_sim=1000
r0=0.015
gamma=0.5
eta=0.015
sigma=0.01

notionnel=1000000
fixed=0.02
struct=0.05
inf=0.02
sup=0.04

def simTauxMarcheVasicek(T,Nval,r0,gamma,eta,sigma):
    Tval=np.linspace(0,T,Nval)
    dt=Tval[1]-Tval[0]
    r=np.zeros(Nval)
    r[0]=r0
    
    for i in range(1,Nval):
        #Solution de l'EDS de Vasicek
        r[i]=r[i-1]*np.exp(-gamma*dt)+(eta/gamma)*(1-np.exp(-gamma*dt))+np.sqrt(((sigma**2)/2*gamma)*(1-np.exp(-2*gamma*dt)))*np.random.randn()
    return r

def pricerSwapAccrualVasicek(n_sim,T,Nval,r0,gamma,eta,sigma,notional,fixed_rate,struct_coupon,inf_r,sup_r):
    tauxSim = np.zeros((Nval, n_sim))
    for i in range(n_sim):
        tauxSim[:, i] = simTauxMarcheVasicek(T, Nval, r0, gamma, eta, sigma)
    sum_struct= 0.0
    sum_fixe= 0.0
    
    for i in range(n_sim):
        n_range= 0
        sum_taux_c= 0.0
        for t in range(Nval):
            r_t= tauxSim[t,i]
            if (r_t >= inf_r) and (r_t <= sup_r) :
                n_range = n_range+1
            sum_taux_c= sum_taux_c+r_t
            
        ratio_range= n_range/Nval
        taux_moy= sum_taux_c/Nval
        df= np.exp(-taux_moy*T)
        
        sum_struct=sum_struct+(notional*struct_coupon*ratio_range*T)*df
        sum_fixe= sum_fixe+(notional*fixed_rate*T)*df

    prix_moy_struct = sum_struct / n_sim
    prix_moy_fixe = sum_fixe / n_sim
    
    print("Payoff structuré moyen :",prix_moy_struct,"\n")
    print("Payoff fixe moyen :",prix_moy_fixe,"\n")
    print("Payoff Net Moyen :",prix_moy_struct - prix_moy_fixe,"\n")
    
    #graph
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    ax1.plot(tauxSim[:, :50], color='grey', alpha=0.4, linewidth=0.8)
    ax1.axhline(y=sup, color='red', linestyle='--', linewidth=2, label='Barrière Haute')
    ax1.axhline(y=inf, color='green', linestyle='--', linewidth=2, label='Barrière Basse')

    ax1.set_title("Simulation Monte Carlo : 50 Scénarios")
    ax1.set_xlabel("Temps")
    ax1.set_ylabel("Taux d'intérêt")
    ax1.grid(True, alpha=0.3)
    
    taux_fin = tauxSim[-1, :]
    ax2.hist(taux_fin, bins=50, color='skyblue', edgecolor='black', alpha=0.7)
    
    ax2.axvline(x=sup, color='red', linestyle='--', linewidth=2, label='Barrière Haute')
    ax2.axvline(x=inf, color='green', linestyle='--', linewidth=2, label='Barrière Basse')
    
    ax2.set_title(f"Distribution des taux finaux (t={T} an)")
    ax2.set_xlabel("Taux")
    ax2.set_ylabel("Nombre de simulations")
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()
    
    return prix_moy_struct,prix_moy_fixe,tauxSim


val_struct,val_fixe,tauxSim=pricerSwapAccrualVasicek(n_sim,T,Nval,r0,gamma,eta,sigma,notionnel,fixed,struct,inf,sup)

def Calibration(val_struct, val_fixe, taux_fixe):
    taux_fixe_cible=taux_fixe*(val_struct/val_fixe)  
    print("Pour que la valeur du swap soit à 0 à t=0, il faut un taux fixe à ",taux_fixe_cible,"pour les paramètres donnés")
    return taux_fixe_cible


Calibration(val_struct, val_fixe, fixed)
