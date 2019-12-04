import random
import numpy as np
import os
import copy
import time
import dice_battle_seq as dice_seq
import dice_battle_sim as dice_sim
import print_dice


bold = '\x1b[;1m'
blue = '\x1b[34;6m'
green = '\x1b[32;6m'
red = '\x1b[31;6m'
reset = '\x1b[m'

def main_menu():
    os.system('clear')
    print(bold + red + " " + "  _____    _                   ____            _     _     _       " )
    print(" "+" |  __ \  (_)                 |  _ \          | |   | |   | |       ")
    print(" "+ " | |  | |  _    ___    ___    | |_) |   __ _  | |_  | |_  | |   ___  ")
    print(" "+ " | |  | | | |  / __|  / _ \   |  _ <   / _` | | __| | __| | |  / _ \ ")
    print(" "+ " | |__| | | | | (__  |  __/   | |_) | | (_| | | |_  | |_  | | |  __/ ")
    print(" "+ " |_____/  |_|  \___|  \___|   |____/   \__,_|  \__|  \__| |_|  \___| ")
    print(" "+"                                                                     ")

def main():
    while(True):
        main_menu()
        print(red + "(Seq) Pour jouer en variante séquentielle")
        print(red+ "(Sim) Pour jouer en variante simultanée")
        print(red + "(Q) Quit")
        choice=0
        while not choice:
            val = input("\nChoisissez une action parmi celles affichées ci-dessus\n")
            if(val != 'Seq') and (val != 'Sim') and (val != "Q"):
                print("Veuillez saisir une action valide");
                continue
            menu = 1
            break
        if val == 'Q':
            break
        if val == 'Seq':
            print(red + "(PvC) Play vs Computer")
            print(red + "(PvP) Play PvP")
            print(red + "(Q) Quit")
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
            print(red + "Veuillez saisir le nombre de points à atteindre. (100 par défaut)")
            Nr = input(red + "N = " + '')
            if (len(Nr) == 0):
                N = 100
            else:
                N = int(Nr)

            print(red + "Veuillez saisir le nombre de dés maximum. (10 par défaut)")
            Dr = input(red + "D = " + '')
            if (len(Dr) == 0):
                D = 10
            else:
                D = int(Dr)
            print(red + "Souhaitez vous afficher les faces de dés obtenues? (yes/no)")
            dr = input(red + "draw = " + '')
            if (dr == 'yes'):
                draw = True
            else:
                draw = False
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
                    strategy1  = dice_seq.blind_strategy
                    d_opt = None
                elif strat1 == 'random':
                    strategy1  = dice_seq.random_strategy
                    d_opt = None
                else:
                    strategy1  = dice_seq.optimal_strategy
                    P = dice_seq.probabilities(D)
                    d_opt  = dice_seq.optimal_strategy_iter(D,P,N)[1]
                strategy2 = dice_seq.set_dices
                dice_seq.play(strategy1,strategy2,d_opt,N,D,draw,verbose=True)
                print(red + "Souhaitez vous jouer une autre partie? (yes/no)")
                r = input(red + "r = " + '')
                if r == 'yes' :
                    continue
                else:
                    break
            if choice_game == 1:
                strategy1 = dice_seq.set_dices
                strategy2 = dice_seq.set_dices
                print("Lancé d'une piece non biaisée pour décider lequel des deux joueurs jouera en premier .. \n")
                d = np.random.choice([0,1], p =[0.5,0.5])
                if d == 1 :
                    print("C'est le joueur 1 qui entame .. \n")
                    dice_seq.play(strategy1,strategy2,None,N,D,draw,verbose=True)
                if d == 0 :
                    print("C'est le joueur 2 qui entame .. \n")
                    dice_seq.play(strategy2,strategy1,None,N,D,draw,verbose=True)
                print(red + "Souhaitez vous jouer une autre partie? (yes/no)")
                r = input(red + "r = " + '')
                if r == 'yes' :
                    continue
                else:
                    break
        else :
            print(red + "(PvC) Play vs Computer")
            print(red + "(PvP) Play PvP")
            print(red + "(Q) Quit")
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
            print(red + "Veuillez saisir le nombre de dés maximum. (10 par défaut)")
            Dr = input(red + "D = " + '')
            if (len(Dr) == 0):
                D = 10
            else:
                D = int(Dr)
            print(red + "Souhaitez vous afficher les faces de dés obtenues? (yes/no)")
            dr = input(red + "draw = " + '')
            if (dr == 'yes'):
                draw = True
            else:
                draw = False
            if choice_game == 0:
                choice_d = 0
                while not choice_d:
                    strat1 = input("\nChoisissez une stratégie pour l'ordinateur parmis les suivantes : \n 'random' pour la stratégie random '\n 'blind' pour la stratégie aveugle \n 'optimal' pour la stratégie optimale \n ")
                    if (strat1 != 'random') and (strat1 != 'blind') and (strat1 != 'optimal') :
                        print("Veuillez saisir une stratégie valide");
                        continue
                    choice_d = 1
                    break
                choice_d = 0
                if strat1 == 'blind':
                    strategy1  = dice_seq.blind_strategy
                    P = None
                elif strat1 == 'random':
                    strategy1  = dice_seq.random_strategy
                    P = None
                else:
                    P = dice.probabilities(D)
                    strategy1  = dice_sim.strategy_sim(D,P)
                strategy2 = dice_seq.set_dices
                dice_sim.play_one_turn(strategy1,strategy2,D,P,draw=draw,verbose=True)
                print(red + "Souhaitez vous jouer une autre partie? (yes/no)")
                r = input(red + "r = " + '')
                if r == 'yes' :
                    continue
                else:
                    break
            if choice_game == 1:
                strategy1 = dice_seq.set_dices
                strategy2 = dice_seq.set_dices
                dice_sim.play_one_turn(strategy1,strategy2,D,draw = draw,verbose=True)
                print(red + "Souhaitez vous jouer une autre partie? (yes/no)")
                r = input(red + "r = " + '')
                if r == 'yes' :
                    continue
                else:
                    break

main()
