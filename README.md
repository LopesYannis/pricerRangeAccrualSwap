Range Accrual Swap Pricer (Modèle de Vasicek)
Ce projet implémente un moteur de pricing pour un Range Accrual Swap en utilisant le modèle de taux stochastique de Vasicek.
L'objectif est de valoriser un produit structuré où le coupon n'est payé que pour les jours où le taux de référence se situe à l'intérieur d'un tunnel (Range).

Fonctions implémentées :
Simulation de Taux : Génération de trajectoires de taux d'intérêt via la solution exacte de l'EDS de Vasicek.
Pricing Monte Carlo : Calcul de la Valeur Actuelle Nette des deux jambes du swap (Fixe et Structurée) sur la base des simulations de Monte Carlo.
Calibration : Calcul du "Fair Rate", le taux fixe qui équilibre la valeur estimée des deux jambes du Swap à t=0.
Visualisation : Affichage des trajectoires de taux et de la distribution des taux finaux avec Matplotlib.

Modèle de Vasicek  taux court : $$dr_t =  (\eta - \gamma r_t)dt + \sigma dW_t$$

<img width="1072" height="425" alt="simPricerRangeAccrualSwapVasicek" src="https://github.com/user-attachments/assets/bbb9096d-b0b5-4402-b226-4601602fb5f9" />
