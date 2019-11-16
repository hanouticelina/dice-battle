import sys
import ctypes
import os
import time
import dice_battle as dice
import print_dice

class ContinueMainLoop(Exception):
    pass

if __name__=="__main__":

    while(True):
        try:
            print("----------------------DICE BATTLE-------------------------")
            print("\n\n")
            print_dice.print_dice_rolls([1,2,3,4,5,6])
            print("\n\n")
            menu=0
            while not menu:
                print("----------------------MENU---------------------------- \n")
                val = input("\nChoisissez une action parmi : \n(play) Entamer une partie \n(test) Afficher une stratégie optimale selon N et D \n(quit) Quitter le jeu\n")
                if(val != 'play') and (val != 'quit') and (val != 'test'):
                    print("Veuillez saisir une action valide");
                    continue
                menu = 1
                break
            if val == 'play':
                choice = 0
                while not choice:
                    val = input("\nChoisissez le nombre de dès maximum\n")
                    try:
                        D = int(val)
                        choice = 1
                        break
                    except ValueError:
                        print("Veuillez saisir un entier.")
                choice = 0
                while not choice:
                    val2 = input("\nChoisissez le nombre de points à atteindre\n")
                    try:
                        N = int(val2)
                        choice = 1
                        break
                    except ValueError:
                        print("Veuillez saisir un entier.")
                choice = 0
                while not choice:
                    strat1 = input("\nChoisissez une stratégie pour le joueur 1 parmis les suivantes : \n 'random' pour la stratégie random \n 'blind' pour la stratégie aveugle \n ")
                    if(strat1 != 'random') and (strat1 != 'blind'):
                        print("Veuillez saisir une stratégie valide");
                        continue
                    choice = 1
                    break
                choice = 0
                while not choice:
                    strat2 = input("\nChoisissez une stratégie pour le joueur 2 parmis les suivantes : \n 'random' pour la stratégie random \n 'blind' pour la stratégie aveugle \n ")
                    if(strat2 != 'random') and (strat2 != 'blind'):
                        print("Veuillez saisir une stratégie valide");
                        continue
                    choice = 1
                    break
                choice = 0
                while not choice:
                    d = input("\nVoulez-vous afficher les faces des dès obtenues? : (yes,no) \n ")
                    if(d != 'yes') and (d != 'no'):
                        print("Veuillez répondre par oui ou par non");
                        continue
                    if (d == 'yes'):
                        draw = True
                    else:
                        draw = False
                    choice = 1
                    break
                choice = 0
                if strat1 == 'blind':
                    strategy1  = dice.blind_strategy
                else:
                    strategy1  = dice.random_strategy

                if strat2 == 'blind':
                    strategy2  = dice.blind_strategy
                else:
                    strategy2  = dice.random_strategy
                dice.play(strategy1,strategy2,N,D,draw)
                while not choice:
                    d = input("\nSaisir une action : \n(menu) Retourner au menu principale\n(quit) quitter le jeu\n")
                    if(d != 'menu') and (d != 'quit'):
                        print("Veuillez répondre par 'menu' ou par 'quit'");
                        continue
                    if (d == 'menu'):
                        choice = 1
                        break
                    else:
                        raise ContinueMainLoop()


            elif val == "test" :
                print("pas encore implémenter\n")

            else :
                raise ContinueMainLoop()

        except ContinueMainLoop:
            break
