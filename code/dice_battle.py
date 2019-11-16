import random
import numpy as np
import argparse
import print_dice as dc



def Q(d,k):
    if d == 1:
        return 1/5
    if k < 2*d or k > 6*d:
        return 0
    else:
        return 1/5*sum([Q(d-1,k-j) for j in range(2,7)])

def probabilities(D):
    K = np.arange(2,6*D+1)
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
    return random.randint(1,6)

def player_roll(d,draw):
    counter = 0
    dices = []
    dice_1 = False
    for i in range(d):
        dice = roll_dice()
        dices.append(dice)
        if dice == 1 :
            dice_1 = True
    print("Faces obtenues : \n")
    if draw:
        dc.print_dice_rolls(dices)
    if dice_1 is True:
        counter = 1
    else :
        counter = sum(dices)
    return counter

def random_strategy(D):
    return random.randint(1,D)

def blind_strategy(D):
    expected = np.array([(4*d-1)*((5/6)**d) + 1 for d in range(1,D+1)])
    return np.argmax(expected)

def optimal_strategy(state):
    pass


def play(strategy1, strategy2, win_score = 100, number_dice = 10, draw=False): #nécessite des modifications pour la variante simultanée
    score_player1 = 0
    score_player2 = 0
    nb_turns = 1
    while score_player1 < win_score or score_player2 < win_score :
        print("Turn : ", nb_turns)
        print("Player 1 score : ", score_player1)
        print("Player 2 score : ", score_player2)
        print()

        print("Player 1 rolls ..")
        d1 = strategy1(number_dice)
        score1 = player_roll(d1,draw)
        score_player1 += score1

        if score_player1 >= win_score:
            winner = 1
            print("\n\n\n\n")
            print("°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°")
            print("WINNER ! Le joueur 1 remporte la partie avec un score total de : ",score_player1)
            print("LOSER ! Le joueur 2 remporte la partie avec un score total de : ",score_player2)
            print("°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°")
            break

        print()

        print("Player 2 rolls ..")
        d2 = strategy2(number_dice)
        score2 = player_roll(d2,draw)
        score_player2 += score2

        if score_player2 >= win_score:
            winner = 2
            print("\n\n\n\n")
            print("°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°")
            print("WINNER ! Le joueur 2 remporte la partie avec un score total de : ",score_player2)
            print("LOSER ! Le joueur 1 remporte la partie avec un score total de : ",score_player1)
            print("°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°")
            break

        print()

        nb_turns += 1
    return winner

def expected_rewards(strategy1,strategy2, nb_games,N): #nécessite des modifications pour la variante simultanée
    rewards = np.zeros(N)
    for n in range(N):
        for i in range(nb_games):
            win = play(strategy1,strategy2,win_score = n+20)
            if win == 1:
                rewards[n] += 1
            else:
                rewards[n] += -1
        rewards[n] = rewards[n]/nb_games
    return np.arange(20,N+20), rewards



def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('number_dice', type=int, help='the number of dice to roll at each turn')
    ap.add_argument('target_score', type=int, help='the target score')
    ap.add_argument('-s1', '--strategy1', help='choose a strategy for the 1st player',choices=['random', 'blind'], default='random')
    ap.add_argument('-s2', '--strategy2', help='choose a strategy for the 2nd player',choices=['random', 'blind'], default='random')
    args = ap.parse_args()
    D = args.number_dice
    N =args.target_score
    """print(probabilities(D))"""
    if args.strategy1 == 'blind':
        strat1  = blind_strategy
    else:
        strat1  = random_strategy

    if args.strategy2 == 'blind':
        strat2  = blind_strategy
    else:
        strat2  = random_strategy
    winner = play(strat1, strat2,N,D)

main()
