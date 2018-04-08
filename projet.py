#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  projet.py
#
#  Copyright 2018 EstebanLeo <administrateur@Solus>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the SUISSE
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#
##------- Importation des modules --------##
from tkinter import*
from random import*
from math import*


##------- Création des voitures ------#
class Voiture:
    def __init__(self, X, Y, longueur, sens, couleur, valeur):
        """ Fonction constructeur de l'objet, appelée à chaque création d'une nouvelle instance de cette classe """
        global memoire
        global liste_vehicules
        self.sens = sens    #On définit le sens de déplacement de la voiture (0 pour horizontal, 1 pour vertical)
        self.X = X  # Coordonnées de l'objet selon la grille
        self.Y = Y 
        self.longueur = longueur    # Longueur de l'objet en nombres de cases
        self.valeur = valeur    # 1 pour la voiture rouge, 2 ou 3 pour les autres

        x1 = X*100  # On convertit les coordonnées de la grille en coordonnées de pixels pour TKinter
        y1 = Y*100
        x2 = y2 = 0
        if sens == 0: # Si la voiture est horizontale sur la grille
            x2 = x1 +longueur*100  # x2 est défini selon la longueur de la voiture
            y2 = y1+100     # y2 est défini pour une case de large
            for i in range(longueur):       # On inscrit la présence de la voiture dans le tableau de mémoire
                memoire[Y][X+i] = valeur # 1 pour la voiture rouge, 2 ou 3 pour les autres
        else:   # Mêmes actions, mais la voiture est horizontale sur la grille
            x2 = x1+100
            y2 = y1+longueur*100
            for i in range(longueur):
                memoire[Y+i][X] = valeur
        self.rectangle = jeu.create_rectangle(x1, y1, x2, y2, fill=couleur) # On crée un rectangle sur le plateau de jeu, et on stocke son identifiant dans l'attribut "rectangle" de l'objet
        self.largeur = abs(x2-x1) # Largeur et hauteur de l'objet en pixels
        self.hauteur = abs(y2-y1)
        liste_vehicules.append(self)    # On stocke l'objet créé dans la liste des véhicules


    def get_coords(self):
        """ Fonction qui permet d'obtenir la position de la voiture en fonction du rectangle TKinter """
        xTK = int(jeu.coords(self.rectangle)[0])    # Coordonnées TKinter x1 et y1 du rectangle correspondant à la voiture
        yTK = int(jeu.coords(self.rectangle)[1])
        # On divise par la largeur d'une case et on renvoie les valeurs obtenues sous la forme d'un tuple
        X = xTK//100
        Y = yTK//100
        resultat = [X, Y]
        return resultat
    
    def set_coords(self, X, Y):
        """ Fonction qui met à jour les coordonnées de la voiture dans les attributs de l'objet et dans le tableau de mémoire """
        self.X = X  # Mise à jour des attributs de l'objets
        self.Y = Y
        sens = self.sens    # Récupération des attributs de l'objet
        valeur = self.valeur
        longueur = self.longueur
        if sens == 0:   # SI la voiture est horizontale
            for i in range(longueur):   # On remplit chaque case avec la valeur de mémoire de la voiture
                memoire[Y][X+i] = valeur
        else:   # SI la voiture est verticale, on fait de même
            for i in range(longueur):
                memoire[Y+i][X] = valeur
    
    def get_limits(self):
        """ Fonction qui détermine les limites de déplacement de la voiture """
        X = self.X  # Récupération des coordonnées sur la grille et du sens
        Y = self.Y
        sens = self.sens
        ligne = [] # On initialise ligne et index
        index = 0
        if sens == 0 :   # SI la voiture est horizontale
            ligne = memoire[Y]  # On récupère la ligne
            index = X   # On définit l'index de départ sur la position X
        else:   # SI la voiture est verticale, on fait de même
            for i in range(6):  # On récupère la colonne
                ligne.append(memoire[i][X])
            index = Y
        
        value = ligne[index] # on prend la valeur de la case de l'index de départ (habituellement 0)
        while index >= 0 and value == 0: # On teste la limite à gauche
            index -= 1
            value = ligne[index]

        index +=1
        limite_gauche = index*100
        value = ligne[index]
        while index < 5 and value == 0: # Puis la limite à droite
            index += 1
            value = ligne[index]
        if value == 0:  # Si on est sur la dernière case, on teste si elle est vide
            index +=1
        limite_droite = index*100
        limites = [limite_gauche, limite_droite] # On renvoie ces valeurs sous la forme d'un tuple
        return limites
    
    def start_move(self):
        """ Fonction qui prépare le mouvement de la voiture en effaçant sa présence du tableau mémoire """
        X = self.X  # On récupère les coordonnées de la voiture, son sens et sa longueur
        Y = self.Y
        sens = self.sens
        longueur = self.longueur

        if sens == 0:    # SI la voiture est horizontale
            for i in range(longueur):   # On efface sa présence
                memoire[Y][X+i] = 0
        else:   # SI la voiture est verticale, on fait de même
            for i in range(longueur):
                memoire[Y+i][X] = 0
        self.limites = self.get_limits()

            

                


##------- Définition des fonctions --------##


def Clic(event):
    """Gestion de l'événement clic gauche"""
    global clic_objet   # Récupération des variables globales
    global liste_vehicules
    global target
    X = event.x     # Coordonnées du clic
    Y = event.y
    for vehicule in liste_vehicules:    # Permet de définir si on a cliqué ou non sur un véhicule
        [xmin, ymin, xmax, ymax] = jeu.coords(vehicule.rectangle)
        xmin = int(xmin)
        xmax = int(xmax)
        ymin = int(ymin)
        ymax = int(ymax)
        if xmin <= X <= xmax and ymin <= Y <= ymax:
            clic_objet = True
            target = vehicule
            target.start_move()
            break
        else:
            clic_objet = False
            
    print("Clic sur un objet -> ", clic_objet)


def Drag(event):
    """ Gestion de l'événement glisser """
    X = event.x
    Y = event.y
    global Largeur
    global Hauteur
    global target

    if clic_objet == True:
        [xmin, ymin, xmax, ymax] = jeu.coords(target.rectangle)
        xmin = int(xmin)
        xmax = int(xmax)
        ymin = int(ymin)
        ymax = int(ymax)
        deltaX = target.largeur/2
        deltaY = target.hauteur/2
        [limite_gauche, limite_droite] = target.limites
        # limite de l'objet dans le canevas de jeu

        if target.sens == 0: #Si horizontal

            if X<deltaX + limite_gauche:
                X=deltaX + limite_gauche
            if X>limite_droite-deltaX:
                X=limite_droite-deltaX
            # déplacement de l'objet (drag)
            jeu.coords(target.rectangle,X-deltaX,ymin,X+deltaX,ymax)
        else:
            if Y<deltaY + limite_gauche:
                Y=deltaY + limite_gauche
            if Y>limite_droite-deltaY:
                Y=limite_droite-deltaY
            
            jeu.coords(target.rectangle,xmin,Y-deltaY,xmax,Y+deltaY)


def Drop(event):
    if clic_objet:
        global target
        [xmin, ymin, xmax, ymax] = jeu.coords(target.rectangle)
        if target.sens == 0:
            xG = round(xmin/c)
            jeu.coords(target.rectangle, xG*c, ymin, xG*c+target.largeur, ymax)
        else:
            yG = round(ymin/c)
            jeu.coords(target.rectangle, xmin, yG*c, xmax, yG*c+target.hauteur)

        
        [xmin, ymin, xmax, ymax] = jeu.coords(target.rectangle)
        print("Nouvelles coordonnées de l'objet --> ", round(xmin/100), round(ymin/100))
        target.set_coords(round(xmin/100), round(ymin/100))
        verif_gagnant()


def verif_gagnant():
    global memoire
    if memoire[2][4] == memoire[2][5] == 1:
        fen_victoire = Tk()
        fen_victoire.title('Bravo !')
        bravo = Label(fen_victoire, text="Félicitation, vous avez gagné !")
        bravo.pack()
        ok = Button(fen_victoire, text="OK", command = fen_victoire.quit)
        ok.pack()

def couleurAleat(): #Fonction qui génère une couleur aléatoire
    couleurs = ["#2980b9", "#f9ca24", "#f0932b", "#8e44ad", "#2c3e50", "#f368e0", "#48dbfb"] #Liste de couleurs
    return couleurs[randint(0, len(couleurs) - 1)]  #On retourne une couleur au hasard dans la liste

def debugger():
    for i in range (6):
        print(memoire[i])

##------- Variables globales --------##


clic_objet = False  # "Drapeau" qui indique si on est en train d'agir sur une voiture
c = 100                          # Longueur d'un côté d'une case
n = 6                           # Nombre de cases par ligne et par colonne
Largeur = Hauteur = n*c

liste_vehicules = []    # Liste qui contient toutes les instances de la classe Voiture

##------- Tableau de mémoire -------##
memoire = []
for ligne in range(1,7):
    transit = []                  # Les cases de chaque ligne seront stockées dans "transit"
    for colonne in range(6):      # Conception des cases d'une ligne
        transit.append(0)
    memoire.append(transit)       # Ajout de la ligne à la liste principale


##------- Création de la fenêtre -------##
fen = Tk()
fen.title('Rush Hour')                # ---> On donne un titre à la fenêtre
# ---> La fenêtre fait 400*400px, et est située à 200px de la gauche de l'écran, à 100px du haut
fen.geometry('800x700+200+100')

##-------- Création des zones de texte ---------##
bienvenue = Label(
    fen, text='Bienvenue sur RushHour, déplacez les véhicules pour faire sortir la voiture rouge !')
bienvenue.pack()

##------- Création du Canvas -------##
jeu = Canvas(fen, width=700, height=600, bg='#fff')
jeu.pack()

##------- Création du plateau -------##
jeu.create_rectangle(1, 1, 600, 600)
for k in range(5):
    n = k+1
    jeu.create_line(n*c, 0, n*c, 600)
    jeu.create_line(0, n*c, 600, n*c)

##------- Création des boutons -------##
quitter = Button(fen, text='Quitter', command=fen.quit)
quitter.pack()
debug = Button(fen, text='debug', command=debugger)
debug.pack()



##------- Lecture du Fichier -------##

##----- Ouverture du fichier en lecture seule -----##
fichier_niveau = open('niveaux/niv1.rhl', 'r')

##----- Lecture des voitures -----##
numVoiture = 0
for ligne in fichier_niveau:    #--ON parcourt chaque ligne dans le fichier
    if ligne[0] != "#":         # Pour ne pas interpréter les lignes commentées
        if ligne[0:7] == "voiture":     # Pour chaque instruction voiture
            index = ligne.index('(')    #On cherche le début de l'instruction, puis on parcourt les infos écrites dans le fichier
            voitureX = int(ligne[index+1])
            voitureY = int(ligne[index+3])
            voitureLongueur = int(ligne[index+5])
            s = ligne[index+7]
            if s == "h":    # On définit le sens
                voitureSens = 0
            else:
                voitureSens = 1

            voitureCouleur = "#000" #Couleur noire par défaut
            voitureValeur = 2 #Valeur de voiture par défaut
            if ligne[0:8] == "voitureR":    #Si on a affaire à la voiture Rouge, on lui donne une couleur, un nom et une valeur
                voitureCouleur = "#f00"
                nomVoiture = "VoitureR"
                voitureValeur = 1
            else: # Si c'est une autre voiture, on fait de même mais avec une autre valeur et une couleur aléatoire.
                voitureCouleur = couleurAleat()
                voitureValeur = 2
                numVoiture += 1
                nomVoiture = "Voiture"+str(numVoiture) # On crée un nom automatiquement pour la voiture
            
            exec("{} = Voiture({}, {}, {}, {}, '{}', {})".format(nomVoiture, voitureX, voitureY, voitureLongueur, voitureSens, voitureCouleur, voitureValeur)) # Création de la voiture: on utlise 'exec' pour avoir nu nommage de variable dynamique


##----- Fermeture du fichier précédendemment ouvert -----##
fichier_niveau.close()



##------- Création des camions -------##

##------- Programme principal -------##

jeu.bind('<Button-1>', Clic)  # évévement clic gauche (press)
jeu.bind('<B1-Motion>', Drag)  # événement bouton gauche enfoncé (hold down)
jeu.bind('<ButtonRelease-1>', Drop)

fen.mainloop()
