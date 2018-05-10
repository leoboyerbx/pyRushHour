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
from tkinter import filedialog
from tkinter import*
from random import*
from math import*
from copy import deepcopy


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

def init_jeu():
    """ Fonction qui initialise le plateau de jeu """

    global jeu
    global memoire
    global liste_vehicules
    ##------- Tableau de mémoire -------##
    memoire = []
    for ligne in range(1,7):
        transit = []                  # Les cases de chaque ligne seront stockées dans "transit"
        for colonne in range(6):      # Conception des cases d'une ligne
            transit.append(0)
        memoire.append(transit)       # Ajout de la ligne à la liste principale

    # Vidage du plateau et des voitures
    jeu.delete("all")
    liste_vehicules = []
    ##------- Création du plateau -------##
    jeu.create_rectangle(1, 1, 600, 600)
    for k in range(5):
        n = k+1
        jeu.create_line(n*c, 0, n*c, 600)
        jeu.create_line(0, n*c, 600, n*c)
    menu_fichier.entryconfig("Fermer le niveau", state='disabled')


def ouvrir_niveau():
    """ Fonction qui ouvre un niveau et crée les voitures correspondantes """
    ##------- Lecture du Fichier -------##
    ##----- Ouverture du fichier en lecture seule -----##
    chemin_niveau = filedialog.askopenfilename(initialdir = "./niveaux/",title = "Choisir un fichier niveau",filetypes = (("Niveaux Rush Hour","*.rhl"),("Tous fichiers","*.*")))  # Dialogue qui ouvre un choix de fichier
    if chemin_niveau: #Si un fichier est choisi
        #On vide le plateau de jeu -> réinitialisation
        init_jeu()
        fichier_niveau = open(chemin_niveau, 'r')

        ##----- Lecture des voitures -----##
        numVoiture = 1 # le numéro de voiture est initialisé à 1 pour s'incrémenter à partir de 2
        for num_ligne, ligne in enumerate(fichier_niveau):    #--ON parcourt chaque ligne dans le fichier
            if ligne[0] != "#":         # Pour ne pas interpréter les lignes commentées
                if ligne[0:7] == "voiture":     # Pour chaque instruction voiture
                    voitureX = voitureY = voitureLongueur = s = 0 # On initialise les variables à 0
                    try: # Essai et exception pour éviter un erreur de formatage du fichier de niveau
                        indexX = ligne.index("x=")  # On récupère l'index de chaque argument puis sa valeur
                        indexY = ligne.index("y=")
                        indexLong = ligne.index("longueur=")
                        indexS = ligne.index("sens=")
                        voitureX = int(ligne[indexX+2])
                        voitureY = int(ligne[indexY+2])
                        voitureLongueur = int(ligne[indexLong+9])
                        s = ligne[indexS+5]
                    except: # Signelement des erreurs à l'utilisateur
                        print("Erreur de formatage du fichier sur la ligne {}. Impossible de générer la voiture.".format(num_ligne + 1))
                        print("{}  - Instruction erronnée".format(ligne))
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
                        numVoiture += 1
                        voitureValeur = numVoiture
                                            
                    # exec("{} = Voiture({}, {}, {}, {}, '{}', {})".format(nomVoiture, voitureX, voitureY, voitureLongueur, voitureSens, voitureCouleur, voitureValeur)) # Création de la voiture: on utlise 'exec' pour avoir nu nommage de variable dynamique
                    Voiture(voitureX, voitureY, voitureLongueur, voitureSens, voitureCouleur, voitureValeur)


        ##----- Fermeture du fichier précédendemment ouvert -----##
        fichier_niveau.close()
        menu_fichier.entryconfig("Fermer le niveau", state='normal')



def Clic(event):
    """Gestion de l'événement clic gauche"""
    global clic_objet   # Récupération des variables globales
    global liste_vehicules
    global target
    X = event.x     # Coordonnées du clic
    Y = event.y
    for vehicule in liste_vehicules:    # Permet de définir si on a cliqué ou non sur un véhicule
        """ Pour chaque véhicule on teste si les coordonnées du clic correspondent aux coordonnées du véhicule """
        [xmin, ymin, xmax, ymax] = jeu.coords(vehicule.rectangle)
        xmin = int(xmin)
        xmax = int(xmax)
        ymin = int(ymin)
        ymax = int(ymax)
        if xmin <= X <= xmax and ymin <= Y <= ymax: # Si le clic a lieu sur le véhicule sélectionné
            clic_objet = True   # On définit le drapeau sur true
            target = vehicule   # On place le véhicule en question comme cible
            target.start_move()  # On applique la méthode start_move()
            break
        else:
            clic_objet = False


def Drag(event):
    """ Gestion de l'événement glisser """
    X = event.x # Récupération des coordonnées du clic
    Y = event.y
    global Largeur      # Récupération des variables globales
    global Hauteur
    global target

    if clic_objet == True:  # On n'agit que si on est en train de déplacer un objet
        [xmin, ymin, xmax, ymax] = jeu.coords(target.rectangle)     # On récupère les coordonnées de la voiture
        xmin = int(xmin)
        xmax = int(xmax)
        ymin = int(ymin)
        ymax = int(ymax)
        deltaX = target.largeur/2
        deltaY = target.hauteur/2
        [limite_gauche, limite_droite] = target.limites #On récupère les limites de déplacement de l'objet


        # Empêcher l'objet de sortir de ses limites
        if target.sens == 0: #Si horizontal
            if X<deltaX + limite_gauche:
                X=deltaX + limite_gauche
            if X>limite_droite-deltaX:
                X=limite_droite-deltaX
            # déplacement de l'objet
            jeu.coords(target.rectangle,X-deltaX,ymin,X+deltaX,ymax)
        else:   # Si vertical
            if Y<deltaY + limite_gauche:
                Y=deltaY + limite_gauche
            if Y>limite_droite-deltaY:
                Y=limite_droite-deltaY
            # déplacement de l'objet
            jeu.coords(target.rectangle,xmin,Y-deltaY,xmax,Y+deltaY)


def Drop(event):
    """ Gestion de l'événement déposer (drop) """
    if clic_objet: #Si on est en train de déplacer un objet
        global target   # On récupère l'objet cible et ses coordonnées
        [xmin, ymin, xmax, ymax] = jeu.coords(target.rectangle)
        if target.sens == 0: # Si l'objet est horizontal
            xG = round(xmin/c) # On arrondit au carré le plus proche
            jeu.coords(target.rectangle, xG*c, ymin, xG*c+target.largeur, ymax) # On déplace l'objet (drop)
        else: # Si l'objet est vertical, pareil mais sur Y
            yG = round(ymin/c)
            jeu.coords(target.rectangle, xmin, yG*c, xmax, yG*c+target.hauteur)

        
        [xmin, ymin, xmax, ymax] = jeu.coords(target.rectangle) # On récupère les nouvelles coordonnées et on les stocke dans memoire
        print("Nouvelles coordonnées de l'objet --> ", round(xmin/100), round(ymin/100))
        target.set_coords(round(xmin/100), round(ymin/100))
        verif_gagnant() # On regarde si on a gagné


def verif_gagnant():
    """ Fonction qui vérifie si le joueur a gagné """
    global memoire
    if memoire[2][4] == memoire[2][5] == 1: # Si la voiture rouge se trouve sur la case en face de la sortie, on crée unje fenêtre pour dire "c'est gagné"
        fen_victoire = Tk()
        fen_victoire.title('Bravo !')
        bravo = Label(fen_victoire, text="Félicitation, vous avez gagné !")
        bravo.pack()
        ok = Button(fen_victoire, text="OK", command = fen_victoire.quit)
        ok.pack()

def couleurAleat(): #Fonction qui génère une couleur aléatoire
    couleurs = ["#2980b9", "#f9ca24", "#f0932b", "#8e44ad", "#2c3e50", "#f368e0", "#48dbfb"] #Liste de couleurs
    return couleurs[randint(0, len(couleurs) - 1)]  #On retourne une couleur au hasard dans la liste

def debugger(): #Débogage
    for i in range (6):
        print(memoire[i])

def aide(): #Intelligence Artificielle
    global memoire
    global sens
    global longueur

    liste_vehicules_aide = []       #Copie de la liste des caractéristiques des véhicules
    for vehicule in liste_vehicules:
        liste_vehicules_aide.append([vehicule.X, vehicule.Y, vehicule.longueur, vehicule.valeur,vehicule.sens],)

    deplacements_aide = []          #Création d'une liste vide où l'on va stocker les différents déplacements à faire
    print(liste_vehicules_aide)

    #    grille = []                        #Création d'un tableau identique à mémoire que l'on peut modifier sans altérer le jeu
#    for case in memoire:    
#        grille.append(case,)
    grille = deepcopy(memoire)
    print(grille)
    print(memoire)

    #Initialisation d'une variable
    vehicule_devant = 0     #cette variable devra, plus tard, contenir le numéro du vehicule situé devant le véhicule en cours

    #-- Localisation de la voiture rouge --#
    voitureRx = liste_vehicules_aide[0].X + 1
    voitureRy = liste_vehicules_aide[0].Y 

    if voitureRx == 5:       #Cas où l'on a déjà gagné
        aide_texte.configure(fen, text='Vous avez déjà gagné :)')

    #--  Etude du véhicule gênant le véhicule à déplacer (en premier la voiture rouge, puis celle qui la gêne, etc...) --#
    else:
        vehicule_en_coursX = voitureRx
        vehicule_en_coursY = voitureRy
        numero_vehicule_en_cours = grille[2][voitureRx]
       # if grille[2][voitureRx+1] != 0:
            
    while grille[2][voitureRx] != 5:
        vehicule_en_coursX = liste_vehicules_aide[numero_vehicule_en_cours][0]
        vehicule_en_coursY = liste_vehicules_aide[numero_vehicule_en_cours][1]
                


# /!\ au cas du haut/bas, là le vehicule de devant est forcément en haut
                   # """  for voiture in liste_vehicules_aide:    #repérage de la voiture située devant la voiture rouge (qui gêne donc son avancée)
                  #  if liste_vehicules_aide[voiture][1] + liste_vehicules_aide[voiture][2] - 1 == vehicule_en_coursX + 1 or liste_vehicules_aide[voiture][1] + liste_vehicules_aide[voiture][2] - 1 == 3:
                   #     vehicule_devant = liste_vehicules_aide[voiture][3] #enregistrement du numéro du véhicule situé devant la voiture rouge dans une variable
                    #    print(vehicule_devant)    """            
        if liste_vehicules_aide[numero_vehicule_en_cours][4] == 1:     #si c'est un véhicule vertical
            if liste_vehicules_aide[numero_vehicule_en_cours][1] > 0 : #s'il n'est pas collé en haut 
                if grille[vehicule_en_coursY-1][vehicule_en_coursX] == 0:            #test de la case au dessus
                    grille[vehicule_en_coursY-1][vehicule_en_coursX] = numero_vehicule_en_cours       #déplacement du véhicule dans la grille
                    grille[vehicule_en_coursY + liste_vehicules_aide[numero_vehicule_en_cours][2]][vehicule_en_coursX+2] = 0
                    liste_vehicules_aide[numero_vehicule_en_cours][3] = liste_vehicules_aide[numero_vehicule_en_cours][3]-1     #déplacement du véhicule dans liste_deplacement_aide
                    deplacements_aide.append(['le haut',1,liste_vehicules_aide[numero_vehicule_en_cours][3]])  #enregistrement du déplacement dans une liste

        elif liste_vehicules_aide[numero_vehicule_en_cours][1] + liste_vehicules_aide[numero_vehicule_en_cours][2] - 1 < 5 and liste_vehicules_aide[numero_vehicule_en_cours][4] == 1:    #s'il n'est pas collé en bas et qu'il est vertical
            if grille[liste_vehicules_aide[numero_vehicule_en_cours][1]+liste_vehicules_aide[numero_vehicule_en_cours][2] - 1][vehicule_en_coursX+2] == 0:       #test de la case en dessous
                grille[liste_vehicules_aide[numero_vehicule_en_cours][1]+liste_vehicules_aide[numero_vehicule_en_cours][2] - 1][vehicule_en_coursX+2] = liste_vehicules_aide[numero_vehicule_en_cours][3]    #déplacement du véhicule dans la grille
                grille[liste_vehicules_aide[numero_vehicule_en_cours][1]+2][vehicule_en_coursX+1] = 0
                deplacements_aide.append(['le bas',1,liste_vehicules_aide[numero_vehicule_en_cours][3]])  #enregistrement du déplacement dans une liste
   

        elif liste_vehicules_aide[numero_vehicule_en_cours][0] > 0 and liste_vehicules_aide[numero_vehicule_en_cours][4] == 0: #s'il n'est pas collé à gauche et que c'est un véhicule horizontal
            if grille[vehicule_en_coursY][liste_vehicules_aide[numero_vehicule_en_cours][0]] == 0:       #test de la case à gauche
                grille[liste_vehicules_aide[numero_vehicule_en_cours][1]][vehicule_en_coursX-1] = liste_vehicules_aide[numero_vehicule_en_cours][3]       #déplacement du véhicule dans la grille
                grille[liste_vehicules_aide[numero_vehicule_en_cours][1] + liste_vehicules_aide[numero_vehicule_en_cours][2]][vehicule_en_coursX+1] = 0
                deplacements_aide.append(['la gauche',1,liste_vehicules_aide[numero_vehicule_en_cours][3]])  #enregistrement du déplacement dans une liste
                       

        elif liste_vehicules_aide[numero_vehicule_en_cours][1] + liste_vehicules_aide[numero_vehicule_en_cours][2] - 1 < 5 and liste_vehicules_aide[numero_vehicule_en_cours][4] == 1:    #s'il n'est pas collé en bas et qu'il est vertical
            if grille[liste_vehicules_aide[numero_vehicule_en_cours][1]+liste_vehicules_aide[numero_vehicule_en_cours][2] - 1][vehicule_en_coursX+2] == 0:       #test de la case en dessous
                grille[liste_vehicules_aide[numero_vehicule_en_cours][1]+liste_vehicules_aide[numero_vehicule_en_cours][2] - 1][vehicule_en_coursX+2] = liste_vehicules_aide[numero_vehicule_en_cours][3]    #déplacement du véhicule dans la grille
                grille[liste_vehicules_aide[numero_vehicule_en_cours][1]+1][vehicule_en_coursX+2] = 0
                deplacements_aide.append(['la droite',1,liste_vehicules_aide[numero_vehicule_en_cours][3]])  #enregistrement du déplacement dans une liste
                
        if liste_vehicules_aide[numero_vehicule_en_cours][4] == 0:                 #cas du véhicule horizontal
            if liste_vehicules_aide[numero_vehicule_en_cours][2] == 2:
                vehicule_devant = grille[vehicule_en_coursY][vehicule_en_coursX+2]
            else:
                vehicule_devant = grille[vehicule_en_coursY][vehicule_en_coursX+3]
        else:                                                                       #cas du véhicule vertical   
            vehicule_devant = grille[vehicule_en_coursY+1][vehicule_en_coursX] 

        print(numero_vehicule_en_cours)
        print(vehicule_devant)
        print(deplacements_aide)
        print(grille)
    aide_texte.configure(fen, text='Pour gagner, il faut déplacer le véhicule grisé de {} cases vers {}, \n puis le véhicule noirci de {} cases vers {}'.format(deplacements_aide[0][1], deplacements_aide[0][0], deplacements_aide[1][1], deplacements_aide[1][0]))
            
                       

                           
############## attention au for vehicule in machin, ça ne marche pas, il faut plutot creer un programme pour détecter la voiture de devant (deux cas, soit la voiture en question est verticale auquel cas on chercher une voiture horizontale, soit la voiture est horizontale auquel cas on cherche une voiture verticale)
############ il faut vérifier les valeurs dans les grilles parce que quand on déplace un véhicule, ça peut changer la valeur en question
    #    else:
     #       print(memoire)
    #        grille[2][voitureRx + 1] = 1    #déplacement du véhicule dans la grille
     #       grille[2][voitureRx - 1] = 0
    #        deplacements_aide.append(['la droite',1,1])  #enregistrement du déplacement dans une liste
    #        print(deplacements_aide)
    #        print(grille)
    #        print(memoire)
        #ici: griser le véhicule du deplcements_aide[0] et noircir le vehicule du deplacement_aide[1]

#  1- boucle:
    #on teste la voiture de devant en haut puis en bas
    #on teste le haut plus en détails si nécessaire et on déplace les véhicules en retournant en arrière dans les tests (sinon PB avec la voiture rouge)
    #pareil pour le bas
    #on affiche le coup à faire pour avancer



##------- Variables globales --------##


clic_objet = False  # "Drapeau" qui indique si on est en train d'agir sur une voiture
c = 100                          # Longueur d'un côté d'une case
n = 6                           # Nombre de cases par ligne et par colonne
Largeur = Hauteur = n*c

liste_vehicules = []    # Liste qui contient toutes les instances de la classe Voiture


##------- Création de la fenêtre -------##
fen = Tk()
fen.title('Rush Hour')                # ---> On donne un titre à la fenêtre
# ---> La fenêtre fait 400*400px, et est située à 200px de la gauche de l'écran, à 100px du haut
fen.geometry('800x700+200+100')

##-------- Création de la barre de menu ---------##
barre_menu = Menu(fen)
menu_fichier = Menu(barre_menu, tearoff=0)
menu_fichier.add_command(label="Ouvrir un niveau", command=ouvrir_niveau)
menu_fichier.add_command(label="Fermer le niveau", command=init_jeu, state='disabled')
menu_fichier.add_separator()
menu_fichier.add_command(label="Quitter", command=fen.quit)
barre_menu.add_cascade(label="Fichier", menu=menu_fichier)

fen.config(menu=barre_menu)

##-------- Création des zones de texte ---------##
bienvenue = Label(
    fen, text='Bienvenue sur RushHour, déplacez les véhicules pour faire sortir la voiture rouge !')
bienvenue.pack()
aide_texte = Label(fen, text='')    #Zone de texte pour l'aide
aide_texte.pack()

##------- Création du Canvas -------##
jeu = Canvas(fen, width=700, height=600, bg='#fff')
jeu.pack()

init_jeu()

##------- Création des boutons -------##
quitter = Button(fen, text='Quitter', command=fen.quit)
quitter.pack()
#debug = Button(fen, text='debug', command=debugger)
#debug.pack()
aide = Button(fen,text='Aide', command=aide)
aide.pack()

##------- Programme principal -------##

jeu.bind('<Button-1>', Clic)  # évévement clic gauche (press)
jeu.bind('<B1-Motion>', Drag)  # événement bouton gauche enfoncé (hold down)
jeu.bind('<ButtonRelease-1>', Drop)

fen.mainloop()
