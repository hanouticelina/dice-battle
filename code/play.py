import random
import numpy as np
import os
import copy
import time
import dice_battle as dice
import print_dice


bold = '\x1b[;1m'
blue = '\x1b[34;6m'
green = '\x1b[32;6m'
red = '\x1b[31;6m'
reset = '\x1b[m'

def main_menu():
    os.system('clear')
    print(bold + green + " " + "  _____    _                   ____            _     _     _       " )
    print(" "+" |  __ \  (_)                 |  _ \          | |   | |   | |       ")
    print(" "+ " | |  | |  _    ___    ___    | |_) |   __ _  | |_  | |_  | |   ___  ")
    print(" "+ " | |  | | | |  / __|  / _ \   |  _ <   / _` | | __| | __| | |  / _ \ ")
    print(" "+ " | |__| | | | | (__  |  __/   | |_) | | (_| | | |_  | |_  | | |  __/ ")
    print(" "+ " |_____/  |_|  \___|  \___|   |____/   \__,_|  \__|  \__| |_|  \___| ")
    print(" "+"                                                                     ")

def set_dices(D,player = 0):
    if player == 0 :
        c = blue
    else:
        c = red
    while True:
        print(c + " how many dices?\n")
        d = int(input("d = "))
        if d <= D:
            break
    return d
def main():
    while(True):
        main_menu()
        print(green + "(PvC) Play vs Computer")
        print(green + "(PvP) Play PvP")
        print(green + "(Q) Quit")
        choice=0
        while not choice:
            val = input("\nChoisissez une action parmi celles affichées ci-dessus\n")
            if(val != 'PvC') and (val != 'PvP') and (val != 'R') and (val != "Q"):
                print("Veuillez saisir une action valide");
                continue
            menu = 1
            break
        if val == 'Q':
            break
        if val == 'PvC':
            choice_game = 0
        else :
            choice_game = 1
        print(green + "Veuillez saisir le nombre de points à atteindre. (100 par défaut)")
        Nr = input(green + "N = " + '')
        if (len(Nr) == 0):
            N = 100
        else:
            N = int(Nr)

        print(green + "Veuillez saisir le nombre de dés maximum. (10 par défaut)")
        Dr = input(green + "D = " + '')
        if (len(Dr) == 0):
            D = 10
        else:
            D = int(Dr)
        print(green + "Souhaitez vous afficher les faces de dés obtenues? (yes/no)")
        dr = input(green + "draw = " + '')
        if (dr == 'yes'):
            draw = True
        else:
            draw = False
        print(choice_game)
        if choice_game == 0:
            choice_d = 0
            while not choice_d:
                strat1 = input("\nChoisissez une stratégie pour l'ordinateur parmis les suivantes : \n 'random' pour la stratégie random \n 'blind' pour la stratégie aveugle \n 'optimal' pour la stratégie optimale \n ")
                if(strat1 != 'random') and (strat1 != 'blind') and (strat1 != 'optimal') :
                    print("Veuillez saisir une stratégie valide");
                    continue
                choice_d = 1
                break
            choice_d = 0
            if strat1 == 'blind':
                strategy1  = dice.blind_strategy
            elif strat1 == 'random':
                strategy1  = dice.random_strategy
            else:
                strategy1  = dice.optimal_strategy
            strategy2 = dice.set_dices
            dice.play(strategy1,strategy2,N,D,draw)
            print(green + "Souhaitez vous jouer une autre partie? (yes/no)")
            r = input(green + "r = " + '')
            if r == 'yes' :
                continue
            else:
                break
        if choice_game == 1:
            strategy1 = dice.set_dices
            strategy2 = dice.set_dices
            print("Lancé d'une piece non biaisée pour décider lequel des deux joueurs jouera en premier .. \n")
            d = np.random.choice([0,1], p =[0.5,0.5])
            if d == 1 :
                print("C'est le joueur 1 qui entame .. \n")
                dice.play(strategy1,strategy2,N,D,draw)
            if d == 0 :
                print("C'est le joueur 2 qui entame .. \n")
                dice.play(strategy2,strategy1,N,D,draw)
            print(green + "Souhaitez vous jouer une autre partie? (yes/no)")
            r = input(green + "r = " + '')
            if r == 'yes' :
                continue
            else:
                break
main()
