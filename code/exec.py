import sys
import ctypes
import os
import time


class ContinueMainLoop(Exception):
    pass

if __name__=="__main__":

    while(True):
        try:
            b1=True
            choice=0
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
                strat1 = input("\nChoisissez une stratégie pour le joueur 1 parmis les suivantes : \n 'rand' pour la stratégie random \n 'blind' pour la stratégie aveugle \n ")
                if(strat1 != 'rand') or (strat1 != 'blind'):
                    print("Veuillez saisir une stratégie valide");
                    continue
                choice = 1
                break
            choice = 0
            while not choice:
                strat2 = input("\nChoisissez une stratégie pour le joueur 2 parmis les suivantes : \n 'rand' pour la stratégie random \n 'blind' pour la stratégie aveugle \n ")
                if(strat2 != 'rand') or (strat2 != 'blind'):
                    print("Veuillez saisir une stratégie valide");
                    continue
                choice = 1
                break
            choice = 0
            
            raise ContinueMainLoop()
        except ContinueMainLoop:
            continue
