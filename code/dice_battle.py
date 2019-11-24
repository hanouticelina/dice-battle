import random
import numpy as np
import argparse
import print_dice as dc
from scipy.optimize import linprog

red = '\x1b[31;6m'
bold = '\x1b[;1m'
blue = '\x1b[34;6m'


def Q(d,k):
    """
    Calcule et retourne la probabilité d'obtenir k points en jetant d dés
    ----------------------------------------------------
    Args:
        - d : le nombre de dés
        - k : le nombre de points
    """
    if d == 1:
        return 1/5
    if k < 2*d or k > 6*d:
        return 0
    else:
        return 1/5*sum([Q(d-1,k-j) for j in range(2,7)])

def probabilities(D):
    """
    Retourne un tableau contenant l'ensemble des P(d,k) pour d inférieur ou égale à D
    ----------------------------------------------------
    Args:
        - D : nombre maximum de dés
    """
    values_D = np.arange(1,D+1)
    P = np.zeros([D,6*D])
    P[:,0] = list(map(lambda d : 1 - (5/6)**d, values_D))
    for d in range(P.shape[0]):
        for k in range(1,P.shape[1]):
            if k+1 > 6*(d+1) or (k+1 >= 2 and k+1 <= 2*(d+1)-1):
                P[d,k] = 0
            else:
                P[d,k] = Q(d+1,k+1)*(5/6)**(d+1)
    return P

def roll_dice():
    """
    Retourne un nombre entre 1 et 6 qui correspond à un jet de dés
    ----------------------------------------------------
    Args:
    """
    return random.randint(1,6)

def player_roll(d,draw):
    """
    Retourne le nombre total de points obtenus en lançant d dés
    ----------------------------------------------------
    Args:
        - d : nombre de dés
        - draw : booléen permettant de controler l'affichage des dés
    """
    counter = 0
    dices = []
    dice_1 = False
    for i in range(d):
        dice = roll_dice()
        dices.append(dice)
        if dice == 1 :
            dice_1 = True

    if draw:
        print(blue + "Faces obtenues : \n")
        dc.print_dice_rolls(dices)
    if dice_1 is True:
        counter = 1
    else :
        counter = sum(dices)
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
    E = np.ones([N+6*D,N+6*D])
    d_opt = np.zeros([N,N])
    E[0:N,N:N+6*D] = -1
    for i in range(N-1, -1, -1):
        for j in range(i, -1, -1):
            tmp = np.array([-P[d-1,0]*(E[j,i+1]) \
                    - np.sum([P[d-1,r-1]*(E[j,i+r]) for r in range(2*d,6*d+1)]) for d in range(1,D+1)])
            E[i,j] = np.max(tmp)
            E[j,i] = - E[i,j]
            d_opt[i,j] = 1 + np.argmax(tmp)
            d_opt[j,i] = 1 + np.argmin(tmp)
    d_opt = d_opt.astype(int)
    return E, d_opt


# ne fonctionne pas : pile de recursion déborde très rapidement
def optimal_strategy_rec(i,j,D,P,N,memo,d_opt):
    if i >= N and j < N :
        return 1
    if j >= N and i < N :
        return 0
    else:
        if memo[i,j] == np.inf:
            E = np.array([P[d-1,0]*(1-optimal_strategy_rec(j,i+1,D,P,N,memo,d_opt)) \
                    + np.sum([P[d-1,r-1]*(1 - optimal_strategy_rec(j,i+r,D,P,N,memo,d_opt)) \
                              for r in range(2*d,6*d+1)]) for d in range(1,D+1)])
            memo[i,j] = np.max(E)
            memo[j,i] = - memo[i,j]
            if(i >= 0 and i <= N-1 and j >= 0 and j <= N-1):
                    d_opt[i,j] = 1 + np.argmax(E)
        return memo[i,j]


# Pr(i,j): la probabilité de gagner lorsqu'on est dans l'état (i,j)
def optimal_strategy_iter1(D,P,N):
    Pr = np.ones([N+6*D,N+6*D])
    d = np.zeros([N,N])
    Pr[0:N,N:N+6*D] = 0
    for i in range(N-1, -1, -1):
        for j in range(i, -1, -1):
            tmp = np.array([P[d-1,0]*(1- Pr[j,i+1]) \
                    + np.sum([P[d-1,r-1]*(1 - Pr[j,i+r]) for r in range(2*d,6*d+1)]) for d in range(1,D+1)])
            Pr[i,j] = np.max(tmp)
            Pr[j,i] = 1 - Pr[i,j]
            d[i,j] = 1 + np.argmax(tmp)
            d[j,i] = 1 + np.argmin(tmp)
    d = d.astype(int)
    return Pr, d

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
        - D : nombre maximum de dés qu'un joeur peut lancer
    """
    while True:
        print(bold + red + " how many dices?\n")
        d = int(input("d = "))
        if d <= D:
            break
    return d


def play(strategy1, strategy2, d_opt = None, win_score = 100, number_dice = 10, draw=False, printing=True):
    """
    Méthode permettant de simuler une partie entre deux joueurs
    ----------------------------------------------------
    Args:
        - strategy1 : stratégie du joueur 1
        - strategy2 : stratégie du joueur 2
        - d_opt : tableau contenant le nombre de dés optimal a lancer selon l'état du jeu (stratégie optimale)
        - win_score : Nombre de points à atteindre
        - number_dice : nombre maximum de dés
        - draw : booléen permettant de controler l'affichage des dés
        - printing : booléen permettant de controler l'affichage de l'état du jeu
    """
    score_player1 = 0
    score_player2 = 0
    nb_turns = 1
    while score_player1 < win_score or score_player2 < win_score :
        if printing:
            print(blue + "Turn : ", nb_turns)
            print("Player 1 score : ", score_player1)
            print("Player 2 score : ", score_player2)
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
            if printing:
                print(blue + "\n\n\n\n")
                print("°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°")
                print("WINNER ! Le joueur 1 remporte la partie avec un score total de : ",score_player1)
                print("LOSER ! Le joueur 2 remporte la partie avec un score total de : ",score_player2)
                print("Nombre de tour : ",nb_turns+1)
                print("°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°")
            break

        if printing:
            print("Player 1 score : ", score_player1)
            print("Player 2 score : ", score_player2)
            print()
            print()
            print("Player 2 rolls ..")

        if strategy2 == optimal_strategy :
            d2 = strategy2(d_opt,score_player1,score_player2)
        else:
            d2 = strategy2(number_dice)
        score2 = player_roll(d2,draw)
        score_player2 += score2

        if score_player2 >= win_score:
            winner = 2
            if printing:
                print(red + "\n\n\n\n")
                print("°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°")
                print("WINNER ! Le joueur 2 remporte la partie avec un score total de : ",score_player2)
                print("LOSER ! Le joueur 1 remporte la partie avec un score total de : ",score_player1)
                print("Nombre de tour : ",nb_turns+1)
                print("°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°")
                print()
            break

        nb_turns += 1
    return winner

def expected_rewards(strategy1, strategy2, nb_games, list_N, D, P): # TODO: ajouter la possibilité de faire varier D
    """
    Méthode permettant de calculer l'esperance de gain pour le joueur 1 en simulant plusieurs parties
    ----------------------------------------------------
    Args:
        - strategy1 : stratégie du joueur 1
        - strategy2 : stratégie du joueur 2
        - nb_games : nombre de parties à simuler
        - list_N : liste des valeurs de N considérées
        - D : nombre maximum de dés
        - P : Tableau de probabilités
    """
    rewards = np.zeros(len(list_N))
    opt = False
    d_opt = None
    if(strategy1 == optimal_strategy or strategy2 == optimal_strategy):
        opt = True
    for i in range(len(list_N)):
        if opt:
            d_opt = optimal_strategy_iter(D,P,list_N[i])[1]
        for _ in range(nb_games):
            win = play(strategy1,strategy2,d_opt,win_score = list_N[i],number_dice = D,printing=False)
            if win == 1:
                rewards[i] += 1
            else:
                rewards[i] += -1
        rewards[i] = rewards[i]/nb_games
    return list_N, rewards

# ------------------------- Variante simultanée -------------------------------------------

def play_turn(strategy1, strategy2, number_dice = 10, draw=False, printing=True):
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

    d1 = strategy1(D)
    score1 = player_roll(d1,draw)
    d2 = strategy2(D)
    score2 = player_roll(d2,draw)
    if score1 > score2 :
        winner = 1
        if printing:
            print(blue + "\n\n\n\n")
            print("°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°")
            print("WINNER ! Le joueur 1 remporte la partie avec un score total de : ",score1)
            print("LOSER ! Le joueur 2 remporte la partie avec un score total de : ",score2)
            print("°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°")
    if score2 > score1 :
        winner = 2
        if printing:
            print(red + "\n\n\n\n")
            print("°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°")
            print("WINNER ! Le joueur 2 remporte la partie avec un score total de : ",score2)
            print("LOSER ! Le joueur 1 remporte la partie avec un score total de : ",score1)
            print("°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°")
    else :
        winner = 0
        if printing:
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
                s += P[d1-1][k-1] * P[d2-1][l-1]
            elif k < l :
                s -= P[d1-1][k-1] * P[d2-1][l-1]
    return s

def matrice_gain(D):
    """
    Méthode permettant de calculer la matrice des gains
    ----------------------------------------------------
    Args:
        - D : nombre maximum de dés qu'un joueur peut lancer
    """

    P = probabilities(D)
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



"""def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('number_dice', type=int, help='the number of dice to roll at each turn')
    ap.add_argument('target_score', type=int, help='the target score')
    ap.add_argument('-s1', '--strategy1', help='choose a strategy for the 1st player',choices=['random', 'blind'], default='random')
    ap.add_argument('-s2', '--strategy2', help='choose a strategy for the 2nd player',choices=['random', 'blind'], default='random')
    args = ap.parse_args()
    D = args.number_dice
    N =args.target_score
    print(probabilities(D))
    if args.strategy1 == 'blind':
        strat1  = blind_strategy
    else:
        strat1  = random_strategy

    if args.strategy2 == 'blind':
        strat2  = blind_strategy
    else:
        strat2  = random_strategy
    winner = play(strat1, strat2,N,D)

main()"""
