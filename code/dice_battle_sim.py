import random
import numpy as np
import argparse
import print_dice as dc
import dice_battle_seq as ds
from scipy.optimize import linprog


def play_one_turn(strategy1, strategy2, number_dice, P, draw=False, verbose=False):
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

    if(strategy1==strategy_sim):
        d1 = strategy_sim(number_dice,P)
    else:
        d1 = strategy1(number_dice)
    score1 =ds.player_roll(d1,draw)
    if(strategy2==strategy_sim):
        d2 = strategy_sim(number_dice,P)
    else:
        d2 =strategy2(number_dice)
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
        winner = -1
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
    L = np.arange(1,6*d2+1)
    for k in range(1,6*d1+1):
        s += np.sum(P[d1,k]*P[d2,L[L<k]]) - np.sum(P[d1,k]*P[d2,L[L>k]])
    return s

def matrice_gain(D,P):
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

def strategy_sim(D,P):
    G = matrice_gain(D,P)
    v = get_probas(G)
    vect=np.where(v<0,0,v)
    return generate_d(vect,D)

def random_strategy(D):
    """
    Retourne un nombre entre 1 et D correspondant à une stratégie aléatoire utilisée comme baseline
    ----------------------------------------------------
    Args:
        - D : nombre maximum de dés
    """
    return random.randint(1,D)

def blind_strategy(D):
    """
    Retourne un nombre de dés d*(D) correspondant à la stratégie aveugle
    ----------------------------------------------------
    Args:
        - D : nombre maximum de dés
    """

    expected = np.array([(4*d-1)*((5/6)**d) + 1 for d in range(1,D+1)])
    return 1 + np.argmax(expected)

def expected_rewards_simult(strategy1,strategy2,nb_games, list_D):
    rewards1 = np.zeros(len(list_D))
    for i in range(len(list_D)):
        P=ds.probabilities(list_D[i])
        rewards1[i]= np.sum([play_one_turn(strategy1,strategy2,list_D[i],P) for _ in range(nb_games)])/nb_games*1.
    return list_D,rewards1