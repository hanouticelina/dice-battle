import random
import numpy as np
import argparse
import print_dice as dc
import dice_battle_seq as ds
from scipy.optimize import linprog


def play_one_turn(strategy1, strategy2, number_dice = 10, draw=False, verbose=True):
    """
    Méthode permettant de simuler un tour (on ne lance qu'une fois les dés)
    ----------------------------------------------------
    Args:
        - strategy1 : stratégie du joueur 1
        - strategy2 : stratégie du joueur 2
        - number_dice : nombre maximum de dés
        - draw : booléen permettant de controler l'affichage des dés
        - printing : booléen permettant de controler l'affichage de l'état du jeu
    """

    d1 = strategy1(number_dice)
    score1 = ds.player_roll(d1,draw)
    d2 = strategy2(number_dice)
    score2 = ds.player_roll(d2,draw)
    if score1 > score2 :
        winner = 1
        if verbose:
            print(blue + "\n\n\n\n")
            print("°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°")
            print("WINNER ! Le joueur 1 remporte la partie avec un score total de : ",score1)
            print("LOSER ! Le joueur 2 remporte la partie avec un score total de : ",score2)
            print("°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°")
    elif score2 > score1 :
        winner = 2
        if verbose:
            print(red + "\n\n\n\n")
            print("°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°")
            print("WINNER ! Le joueur 2 remporte la partie avec un score total de : ",score2)
            print("LOSER ! Le joueur 1 remporte la partie avec un score total de : ",score1)
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
    for k in range(1,6*d1+1):
        for l in range(1,6*d2+1):
            if k > l :
                s += P[d1][k] * P[d2][l]
            elif k < l :
                s -= P[d1][k] * P[d2][l]
    return s

def matrice_gain(D):
    """
    Méthode permettant de calculer la matrice des gains
    ----------------------------------------------------
    Args:
        - D : nombre maximum de dés qu'un joueur peut lancer
    """

    P = ds.probabilities(D)
    G = np.zeros([D,D])
    for d1 in range(1, D+1):
        for d2 in range(1, D+1):
            G[d1-1][d2-1] = EG(d1,d2,P)
    return G

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
    """G_ = G * -1
    G_u = np.transpose(G_).tolist()"""
    A_eq = list(np.ones([1,G.shape[0]]).astype(int))
    b_eq = [1]
    bnds = [(0,None) for _ in range(G.shape[0])]
    res = linprog(c,A_ub = G,b_ub = b,bounds=tuple(bnds), A_eq = A_eq,b_eq = b_eq)
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
    G = matrice_gain(D)
    v = get_probas(G)
    return generate_d(v,D)
