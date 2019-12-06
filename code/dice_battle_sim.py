import random
import numpy as np
import argparse
import print_dice as dc
import dice_battle_seq as ds
from scipy.optimize import linprog

bold = '\x1b[;1m'
blue = '\x1b[34;6m'
green = '\x1b[32;6m'
red = '\x1b[31;6m'
reset = '\x1b[m'

def play_one_turn(strategy1, strategy2, number_dice, draw=False, verbose=False):
    """
    Méthode permettant de simuler un seul tour en simultanée (on ne lance qu'une fois les dés)
    ----------------------------------------------------
    Args:
        - strategy1 : stratégie du joueur 1
        - strategy2 : stratégie du joueur 2
        - number_dice : nombre maximum de dés
        - P : matrice des probabilités (utile pour la stratégie optimale)
        - draw : booléen permettant de controler l'affichage des dés
        - verbose : booléen permettant de controler l'affichage de l'état du jeu
    """

    d1 = strategy1(number_dice)
    print("Le joueur 1 choisit de lancer {} dés..".format(d1))
    d2 =strategy2(number_dice)
    print("Le joueur 2 choisit de lancer {} dés..".format(d2))
    score1 =ds.player_roll(d1,draw,player ='1')
    score2 = ds.player_roll(d2,draw,player ='2')
    if score1 > score2 :
        winner = 1
        if verbose:
            print(blue + "\n\n\n\n")
            print("°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°")
            print("WINNER ! Le joueur 1 remporte la partie avec un score total de : ",score1)
            print("LOSER ! Le joueur 2 perd la partie avec un score total de : ",score2)
            print("°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°")
    elif score2 > score1 :
        winner = -1
        if verbose:
            print(red + "\n\n\n\n")
            print("°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°")
            print("WINNER ! Le joueur 2 remporte la partie avec un score total de : ",score2)
            print("LOSER ! Le joueur 1 perd la partie avec un score total de : ",score1)
            print("°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°")
    else :
        winner = 0
        if verbose:
            print(red + "\n\n\n\n")
            print("°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°")
            print("EGALITE ! score obtenu par les deux joueurs : ",score2)
            print("°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°")
    return winner

def EG(d1,d2,P):
    """
    Méthode permettant de calculer l'esperance de gain du joueur 1 s'il lance d1 dés et
    que le joueur 2 lance d2 dés
    ----------------------------------------------------
    Args:
        - d1 : nombre de dés lancés par le joueur 1
        - d2 : nombre de dés lancés par le joueur 2
        - P : matrice de probabilités
    """

    s = 0
    L = np.arange(1,6*d2+1)
    for k in range(1,6*d1+1):
        s += np.sum(P[d1,k]*P[d2,L[L<k]]) - np.sum(P[d1,k]*P[d2,L[L>k]])
    return s

def matrice_gain(D):
    """
    Méthode permettant de calculer la matrice des gains
    ----------------------------------------------------
    Args:
        - D : nombre maximum de dés qu'un joueur peut lancer
    """

    P = ds.probabilities(D)
    return np.array([[EG(d1,d2,P) for d2 in range(1,D+1)] for d1 in range(1,D+1)])



def get_probas(G):
    """
    Méthode permettant de calculer le vecteur de probabilité du joueur 1 en
    resolvant le programme linéaire associée
    ----------------------------------------------------
    Args:
        - G : matrice des gains
    """
    c = list(np.zeros(G.shape[0]).astype(int))
    b = list(np.zeros(G.shape[0]).astype(int))
    G_ = G * -1
    G_u = np.transpose(G_).tolist()
    A_eq = list(np.ones([1,G.shape[0]]).astype(int))
    b_eq = [1]
    res = linprog(c,A_ub = G_u,b_ub = b, A_eq = A_eq,b_eq = b_eq)
    return res.x


def generate_d(vector,D):
    """
    Méthode permettant de génerer un nombre de dés à lancer selon une distribution de probabilités
    ----------------------------------------------------
    Args:
        - vector : vecteur de probabilités
        - D : nombre maximum de dés qu'un joueur peut lancer

    """
    return np.random.choice(np.arange(1,D+1),p=vector)

def strategy_sim(D):
    """
    Méthode permettant de renvoyer une stratégie optimal
    ----------------------------------------------------
    Args:
        - D : nombre maximum de dés qu'un joueur peut lancer
        - P : matrice de probabilités

    """
    G = matrice_gain(D)
    v = get_probas(G)
    vect=np.where(v<0,0,v)
    return generate_d(vect,D)



def expected_rewards_simult(strategy1,strategy2,nb_games, list_D):
    """
    Méthode permettant de calculer l'espérance de gain pour le joueur 1  en simulant plusieurs parties et en faisant varier le nombre de dés maximum (D)
    ----------------------------------------------------
    Args:
        - strategy1 : stratégie du joueur 1
        - strategy2 : stratégie du joueur 2
        - nb_games : nombre de parties à simuler
        - list_D : liste des valeurs de D considérées
    """
    rewards1 = np.zeros(len(list_D))
    for i in range(len(list_D)):
        P=ds.probabilities(list_D[i])
        rewards1[i]= np.sum([play_one_turn(strategy1,strategy2,list_D[i],P) for _ in range(nb_games)])/nb_games*1.
    return list_D,rewards1
