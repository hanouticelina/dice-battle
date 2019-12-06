import random
import numpy as np
import argparse
import print_dice as dc
from itertools import *
from scipy.optimize import linprog

red = '\x1b[31;6m'
bold = '\x1b[;1m'
blue = '\x1b[34;6m'
green = '\x1b[32;6m'


def probabilities(D):
    """
    Retourne un tableau contenant l'ensemble des P(d,k) pour d inférieur ou égale à D
    ----------------------------------------------------
    Args:
        - D : nombre maximum de dés
    """
    Q = np.zeros((D + 1, 6 * D + 1))
    # cas d'initialisation de Q pour d=1
    Q[1,2:7] = 1/5
    for d in range(2, D+1):
            for k in range(2*d, 6*d+1):
                t = max(k-6,0)
                Q[d, k] = np.sum(Q[d-1, t: k-1]) * (1/5)
    values_D = np.arange(1,D+1)
    P = np.zeros((D+1,6*D+1))
    # cas ou k=1 (au moins un dé tombe sur 1)
    P[1:,1] = list(map(lambda d : 1 - (5/6)**d, values_D))
    for d in range(P.shape[0]):
        for k in range(2,P.shape[1]):
                P[d,k] = Q[d,k]*(5/6)**d

    return P



def player_roll(d,draw,player = None):
    """
    Retourne le nombre total de points obtenus en lançant d dés
    ----------------------------------------------------
    Args:
        - d : nombre de dés
        - draw : booléen permettant de controler l'affichage des dés
    """
    # on lance d dés
    dices = np.random.randint(1,7,d)
    #Si au moins un dé tombe sur 1
    if np.any(dices == 1):
        counter = 1
    else:
        counter = sum(dices)
    # permet de controler l'affichage des dés lancés
    if draw:
        if player:
            print(bold + red + "Faces obtenues du joueur "+player+" :")
        else:
            print(bold + red + "Faces obtenues :")
        dc.print_dice_rolls(dices.tolist())
    return counter

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


def optimal_strategy_iter(D,P,N):
    """
    Retourne le tableau contenant le nombre de dés optimal à lancer selon chaque état possible du jeu
    ----------------------------------------------------
    Args:
        - D : nombre maximum de dés
        - P : matrice de probabilités
        - N : nombre de points à atteindre
    """
    E = np.full((N+6*D,N+6*D), np.inf)
    # permet de stocker le nombre de dés optimal pour chaque état (i,j) (on s'interesse qu'aux états ou i<N et j<N)
    d_opt = np.zeros([N,N], dtype = int)
    # on remplit les cas de base : quand i >= N ou j >= N
    E[:N, N:] = -1
    E[N:, :N] =  1
    # on fait un parcours inverse de la matrice
    for i in range(N-1, -1, -1):
        for j in range(i, -1, -1):
            for x,y in list(permutations((i,j))):
                tmp_ = -P[1: , 1:].dot(E[y,(x+1):(x+6*D+1)])
                d_opt[x,y] = 1 + np.argmax(tmp_)
                E[x,y] = tmp_[d_opt[x,y]-1]
    return E, d_opt


def optimal_strategy(d_opt,i,j):
    """
    Retourne le nombre de dés optimal à lancer lorsqu'on est dans l'état (i,j)
    ----------------------------------------------------
    Args:
        - d_opt : tableau contenant le nombre de dés optimal à lancer selon chaque état possible du jeu
        - i : nombre de points cumulé par le joueur 1
        - j : nombre de points cumulé par le joueur 1
    """
    return d_opt[i,j]


def set_dices(D):
    """
    Permet à un joueur de choisir le nombre de dés à lancer à chaque tour
    ----------------------------------------------------
    Args:
        - D : nombre maximum de dés qu'un joueur peut lancer
    """
    while True:
        print(bold + red + " how many dices?\n")
        d = int(input("d = "))
        if d <= D:
            break
    return d

def play(strategy1, strategy2, d_opt = None, win_score = 100, number_dice = 10, draw=False, verbose=True):
    """
    Méthode permettant de simuler une partie entre deux joueurs
    ----------------------------------------------------
    Args:
        - strategy1 : stratégie du joueur 1
        - strategy2 : stratégie du joueur 2
        - d_opt : tableau contenant le nombre de dés optimal a lancer selon l'état du jeu (utile uniquement pour la stratégie optimale)
        - win_score : Nombre de points à atteindre
        - number_dice : nombre maximum de dés
        - draw : booléen permettant de controler l'affichage des dés
        - verbose : booléen permettant de controler l'affichage de l'état du jeu
    """
    score_player1 = 0
    score_player2 = 0
    nb_turns = 1
    while score_player1 < win_score or score_player2 < win_score :
        if verbose:
            print()
            print(blue + "Player 1 rolls ..")
        if strategy1 == optimal_strategy :
            d1 = strategy1(d_opt,score_player1,score_player2)
        else:
            d1 = strategy1(number_dice)
        score1 = player_roll(d1,draw)
        score_player1 += score1

        if score_player1 >= win_score:
            winner = 1
            if verbose:
                print(blue + "\n\n\n\n")
                print("°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°")
                print("WINNER ! Le joueur 1 remporte la partie avec un score total de : ",score_player1)
                print("LOSER ! Le joueur 2 perd la partie avec un score total de : ",score_player2)
                print("Nombre de tour : ",nb_turns)
                print("°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°")
            break

        if verbose:
            print(bold + red + "Player 1 score : ", score_player1)
            print("Player 2 score : ", score_player2)
            print()
            print()
            print(green + "Player 2 rolls ..")

        if strategy2 == optimal_strategy:
            d2 = strategy2(d_opt,score_player2,score_player1)
        else:
            d2 = strategy2(number_dice)
        score2 = player_roll(d2,draw)
        score_player2 += score2

        if score_player2 >= win_score:
            winner = -1
            if verbose:
                print(green + "\n\n\n\n")
                print("°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°")
                print("WINNER ! Le joueur 2 remporte la partie avec un score total de : ",score_player2)
                print("LOSER ! Le joueur 1 perd la partie avec un score total de : ",score_player1)
                print("Nombre de tour : ",nb_turns)
                print("°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°")
                print()
            break

        if verbose:
            print(bold + red + "Turn : ", nb_turns)
            print("Player 1 score : ", score_player1)
            print("Player 2 score : ", score_player2)

        nb_turns += 1
    return winner

def expected_rewards(strategy1, strategy2, nb_games, list_N, D, P,reverse=False):
    """
    Méthode permettant de calculer l'espérance de gain pour le joueur 1 ou le joueur 2 en simulant plusieurs parties et en faisant varier N
    ----------------------------------------------------
    Args:
        - strategy1 : stratégie du joueur 1
        - strategy2 : stratégie du joueur 2
        - nb_games : nombre de parties à simuler
        - list_N : liste des valeurs de N considérées
        - D : nombre maximum de dés
        - P : Tableau de probabilités
        - reverse : booléen permettant de controler pour lequel des deux joueurs on souhaite calculer l'espérance de gain
    """
    rewards = np.zeros(len(list_N))
    opt = False
    d_opt = None
    if(strategy1 == optimal_strategy or strategy2 == optimal_strategy):
        opt = True
    for i in range(len(list_N)):
        if opt:
            d_opt = optimal_strategy_iter(D,P,list_N[i])[1]
        if reverse:
            rewards[i] = np.sum([-play(strategy1,strategy2,d_opt,win_score = list_N[i],number_dice = D,verbose=False) for _ in range(nb_games)])/nb_games*1.0
        else:
            rewards[i] = np.sum([play(strategy1,strategy2,d_opt,win_score = list_N[i],number_dice = D,verbose=False) for _ in range(nb_games)])/nb_games*1.0
    return list_N, rewards

def expected_rewards_D(strategy1, strategy2, nb_games, N, list_D,reverse=False):
    """
    Méthode permettant de calculer l'espérance de gain pour le joueur 1 ou le joueur 2 en simulant plusieurs parties et en faisant varier D
    ----------------------------------------------------
    Args:
        - strategy1 : stratégie du joueur 1
        - strategy2 : stratégie du joueur 2
        - nb_games : nombre de parties à simuler
        - D : nombre de points à atteindre pour gagner la partie
        - list_D : liste des valeurs de D considérées
        - reverse : booléen permettant de controler pour lequel des deux joueurs on souhaite calculer l'espérance de gain
    """
    rewards = np.zeros(len(list_D))
    opt = False
    d_opt = None
    if(strategy1 == optimal_strategy or strategy2 == optimal_strategy):
        opt = True
    for i in range(len(list_D)):
        P = probabilities(list_D[i])
        if opt:
            d_opt = optimal_strategy_iter(list_D[i],P,N)[1]
        if reverse:
            rewards[i] = np.sum([-play(strategy1,strategy2,d_opt,win_score = N,number_dice = list_D[i],verbose=False) for _ in range(nb_games)])/nb_games*1.0
        else:
            rewards[i] = np.sum([play(strategy1,strategy2,d_opt,win_score = N,number_dice = list_D[i],verbose=False) for _ in range(nb_games)])/nb_games*1.0
    return list_D, rewards
