#=======================================================#
#            PROGRAMME - ESCAPE GAME                    #
#=======================================================#

#================ Partie 0: Imports & prérequis

import turtle
import math as m


"""
Le fichier CONFIG.py n'est pas nécessaire, il a été copié ci-dessous:
Seul la catégorie "Lecture des fichiers" est à modifier et
merci de ne pas renommer les variables, seulement le chemin des fichiers.
    (Il faut mettre le fichier dans le dossier courant, ou bien mettre
        le chemin absolu du fichier à la place des strings)
Les inputs sont sensibles à la casse ("Texte" est différent de "texte")
Après la fermeture de la fenêtre, un message "turtle.Terminator" s'affiche
(parfois en rouge), mais cela est normal.
Pour le fichier du plan (du chateau par exemple), vérifiez qu'il y a bien
un espace entre chaque chiffre.

Images du jeu: https://i.imgur.com/5UFKKR9.png

    Bon jeu !
"""


ZONE_PLAN_MINI = (-240, -240)  # Coin inférieur gauche de la zone d'affichage du plan
ZONE_PLAN_MAXI = (50, 200)  # Coin supérieur droit de la zone d'affichage du plan
POINT_AFFICHAGE_ANNONCES = (-240, 240)  # Point d'origine de l'affichage des annonces
POINT_AFFICHAGE_INVENTAIRE = (70, 210)  # Point d'origine de l'affichage de l'inventaire

# Les valeurs ci-dessous définissent les couleurs des cases du plan
COULEUR_CASES = 'white'
COULEUR_COULOIR = 'white'
COULEUR_MUR = 'grey'
COULEUR_OBJECTIF = 'yellow'
COULEUR_PORTE = 'orange'
COULEUR_OBJET = 'green'
COULEUR_VUE = 'wheat'
COULEURS = [COULEUR_COULOIR, COULEUR_MUR, COULEUR_OBJECTIF, COULEUR_PORTE, \
            COULEUR_OBJET, COULEUR_VUE]
COULEUR_EXTERIEUR = 'white'

# Couleur et dimension du personnage
COULEUR_PERSONNAGE = 'red'
RATIO_PERSONNAGE = 0.9  # Rapport entre diamètre du personnage et dimension des cases
POSITION_DEPART = (0, 1)  # Porte d'entrée du château


# Lecture des fichiers
fichier_plan = 'plan_chateau.txt'
fichier_portes = 'dico_portes.txt'
fichier_objets = 'dico_objets.txt'

# Variables

HORIZ_PLAN = abs(ZONE_PLAN_MINI[0] - ZONE_PLAN_MAXI[0])
VERTIC_PLAN = abs(ZONE_PLAN_MINI[1] - ZONE_PLAN_MAXI[1])


#================ Partie 1: Plan du château

def lire_matrice(fichier):
  try:
    f = open(str(fichier),'r')
    s = f.readlines() # Récupération du fichier
    f.close()
  except:
    print("Erreur 1: Le fichier du plan entré n'est pas correct ou n'a pas été trouvé. \n Veuillez relancer le programme avec le fichier.")
    quit() # Tentative de fermer le programme pour éviter les appels de fonctions impossibles
  L = []
  for i in range(len(s)):
    l = []
    for j in range(0,len(s[0][:-1]),2): # On va jusqu'au "\n" 2 par 2
      l.append(int(s[i][j]))
    L.append(l)
  return L


def calculer_pas(matrice): # Matrice <=> liste de liste et pas un array
  vertic = len(matrice)
  horiz = len(matrice[0])
  return int(min( HORIZ_PLAN/horiz, VERTIC_PLAN/vertic)) # Arrondi par défaut


def coordonnees(case, pas):
    """
    Ici, la fonction ne prend en argument que case et le pas (et pas la matrice), donc impossible
    d'ancrer le labyrinth en bas à gauche si on ne connait pas la case maximale...
    Le labyrinthe sera toujours ancré en haut à gauche et il y a aura des bandes blanches
    en bas de la fenêtre.
    """
    return ( ZONE_PLAN_MINI[0] + case[1]*pas, ZONE_PLAN_MAXI[1] - (case[0]+1)*pas)




def tracer_carre(dimension): # Fonction pour tracer des carrés
  turtle.seth(90) # Direction nord, à supprimer pour optimiser le programme
  turtle.down()
  for i in range(4):
    turtle.forward(dimension)
    turtle.right(90)
  turtle.up()


def tracer_case(case, couleur, pas):
  turtle.up()
  turtle.goto(coordonnees(case,pas))
  turtle.color(COULEUR_CASES,couleur) # La première couleur désigne la couleur des contours
  turtle.begin_fill()
  tracer_carre(pas)
  turtle.end_fill()


def afficher_plan(matrice):
    p = len(matrice[0])
    pas = calculer_pas(matrice)
    for i in range(len(matrice)):
        for j in range(p):
            if matrice[i][j] == 1:
                tracer_case((i,j), COULEUR_MUR, pas)
            elif matrice[i][j] == 2:
                tracer_case((i,j), COULEUR_OBJECTIF, pas)
            elif matrice[i][j] == 3:
                tracer_case((i,j), COULEUR_PORTE, pas)
            elif matrice[i][j] == 4:
                tracer_case((i,j), COULEUR_OBJET, pas)
    global inventaire       # Création de l'inventaire avec une variable qui doit
    inventaire = []         # survivre après l'exécution de la fonction
    affichage_inventaire(inventaire)    # Affiche l'inventaire, encore vide


#================ Partie 2: Déplacement

def tracer_character(position, pas):
    turtle.up()
    global POS      # Modification de la variable donnant la position du joueur
    POS = position
    position = coordonnees(position,pas)
    turtle.goto(position[0]+pas/2, position[1]+pas/2)   # Se décalle légèrement pour tracer un dot
    turtle.down()
    turtle.dot(RATIO_PERSONNAGE*pas, COULEUR_PERSONNAGE)
    turtle.up()



def deplacer(matrice, position, mouvement, inventaire):
    pas = calculer_pas(matrice)
    horiz = len(matrice[0])
    vertic = len(matrice)
    if position[0] + mouvement[0] >= vertic or position[0] + mouvement[0] < 0 or position[1] + mouvement[1] >= horiz or position[1] + mouvement[1] < 0: # Tests, savoir si on sort des murs
        pass
    elif matrice[position[0] + mouvement[0]][position[1] + mouvement[1]] == 1:
        pass
    elif matrice[position[0] + mouvement[0]][position[1] + mouvement[1]] == 2:
        if len(inventaire) != len(dictio):  # Ici, le joueur est forcé à prendre tous les objets
            pen_annonce.clear()
            pen_annonce.write(f"Il vous manque {len(dictio) - len(inventaire)} objets !", False, align = "left", font = ("Arial", 11, "normal"))
        else:
            matrice[position[0] + mouvement[0]][position[1] + mouvement[1]] = 0
            pen_annonce.clear()
            pen_annonce.write("Bravo! Vous avez terminé l\'épreuve ! Merci d'avoir joué !", False, align = "left", font = ("Arial", 11, "normal"))
            tracer_case(position, COULEUR_VUE, pas)
            tracer_character((position[0] + mouvement[0], position[1] + mouvement[1]), pas)
            POS = (position[0] + mouvement[0], position[1] + mouvement[1])
    elif matrice[position[0] + mouvement[0]][position[1] + mouvement[1]] == 3:
        poser_question(matrice, position, mouvement)
    elif matrice[position[0] + mouvement[0]][position[1] + mouvement[1]] == 4:
        matrice[position[0] + mouvement[0]][position[1] + mouvement[1]] = 0  # Modifie la case pour ne pas la réactiver
        POS = (position[0] + mouvement[0], position[1] + mouvement[1])
        tracer_case(position, COULEUR_VUE, pas)
        tracer_case(POS, COULEUR_CASES, pas)
        tracer_character((position[0] + mouvement[0], position[1] + mouvement[1]), pas)
        ramasser_objet((position[0] + mouvement[0], position[1] + mouvement[1]), pas, dictio, inventaire)

    else:
        tracer_case(position, COULEUR_VUE, pas)
        POS = (position[0] + mouvement[0], position[1] + mouvement[1])
        tracer_character(POS, pas)

def deplacer_gauche():
    turtle.onkeypress(None, "Left")   # Désactive la touche Left
    deplacer(M, POS, (0,-1), inventaire)
    turtle.onkeypress(deplacer_gauche, "Left")   # Réassocie la touche Left à la fonction deplacer_gauche

def deplacer_droite():
    turtle.onkeypress(None, "Right")   # Désactive la touche Right
    deplacer(M, POS, (0,1), inventaire)
    turtle.onkeypress(deplacer_droite, "Right")   # Réassocie la touche Left à la fonction deplacer_droite

def deplacer_haut():
    turtle.onkeypress(None, "Up")   # Désactive la touche Left
    deplacer(M, POS, (-1,0), inventaire)
    turtle.onkeypress(deplacer_haut, "Up")   # Réassocie la touche Left à la fonction deplacer_gauche

def deplacer_bas():
    turtle.onkeypress(None, "Down")   # Désactive la touche Left
    deplacer(M, POS, (1,0), inventaire)
    turtle.onkeypress(deplacer_bas, "Down")   # Réassocie la touche Left à la fonction deplacer_gauche





#================ Partie 3: Objets

def creer_dictionnaire_des_objets(fichier_des_objets):
  try:
    f = open(str(fichier_des_objets),'r', encoding="utf-8") # UTF-8 pour avoir les accents
    s = f.readlines() # Récupération du fichier
    f.close()
  except:
    print("Erreur 2: Le fichier des objets n'est pas correct ou n'a pas été trouvé. \n Veuillez relancer le programme avec le fichier.")
    quit()
  global dictio
  dictio = {}
  for i in range(len(s)):
    (a,b) = eval(s[i])
    dictio[a] = b
  return dictio



def affichage_inventaire(inventaire):
    pen_inventaire.clear()
    pen_inventaire.goto((POINT_AFFICHAGE_INVENTAIRE[0] + 5, POINT_AFFICHAGE_INVENTAIRE[1] - 40))
    pen_inventaire.write("Inventaire", False, align = "left", font = ("Arial", 14, "underline"))
    for i in range(len(inventaire)):
        pen_inventaire.goto((POINT_AFFICHAGE_INVENTAIRE[0], POINT_AFFICHAGE_INVENTAIRE[1] - 70 - i*16))
        pen_inventaire.write(inventaire[i], False, align = "left", font = ("Arial", 8, "normal"))


def ramasser_objet(case, pas, dictio, inventaire):
    objet = dictio[case]
    pen_annonce.goto((POINT_AFFICHAGE_ANNONCES[0] + 5, POINT_AFFICHAGE_ANNONCES[1] - 30))
    pen_annonce.clear()
    pen_annonce.write(f"Vous avez obtenu: {objet} !", False, align = "left", font = ("Arial", 11, "normal"))
    inventaire.append(objet)
    affichage_inventaire(inventaire)


""" Les tailles de police et emplacements d'écriture sont forcés par le CONFIG.py..."""




#================ Partie 4: Portes

def creer_dictionnaire_des_portes(fichier_des_portes):
  try:
    f = open(str(fichier_des_portes),'r', encoding="utf-8") # UTF-8 pour avoir les accents
    s = f.readlines() # Récupération du fichier
    f.close()
  except:
    print("Erreur 3: Le fichier des portes n'est pas correct ou n'a pas été trouvé. \n Veuillez relancer le programme avec le fichier.")
    quit()
  global dictip
  dictip = {}
  for i in range(len(s)):
    (a,b) = eval(s[i])
    dictip[a] = b
  return dictip



def poser_question(matrice, case, mouvement):
    pen_annonce.goto((POINT_AFFICHAGE_ANNONCES[0] + 5, POINT_AFFICHAGE_ANNONCES[1] - 30))
    pen_annonce.clear()
    pen_annonce.write("Cette porte est fermée.", False, align = "left", font = ("Arial", 11, "normal"))
    tentative = turtle.textinput("Question", dictip[(case[0] + mouvement[0], case[1] + mouvement[1])][0])
    turtle.listen()
    if tentative != None and tentative == dictip[(case[0] + mouvement[0], case[1] + mouvement[1])][1]:
        pen_annonce.clear()
        pen_annonce.write("La porte a été déverrouillée !", False, align = "left", font = ("Arial", 11, "normal"))
        tracer_case((case[0] + mouvement[0], case[1] + mouvement[1]), COULEUR_CASES, pas)
        matrice[case[0] + mouvement[0]][case[1] + mouvement[1]] = 0
        tracer_case(case, COULEUR_VUE, pas)
        tracer_character((case[0] + mouvement[0], case[1] + mouvement[1]), pas)
        POS = (case[0] + mouvement[0], case[1] + mouvement[1])
    else:
        pen_annonce.clear()
        pen_annonce.write("Mauvaise réponse ! La porte reste verrouillée.", False, align = "left", font = ("Arial", 11, "normal"))






#================ Partie 5: Lancement du programme



turtle.setup(480,480)
turtle.hideturtle()
turtle.speed(0)
turtle.tracer(0,0) # Permet d'afficher instantanément

pen_inventaire = turtle.Pen()  # pen_inventaire: permet d'avoir l'affichage de l'inventaire indépendamment de turtle
pen_inventaire.color("Black")
pen_inventaire.speed(0)
pen_inventaire.up()
pen_inventaire.hideturtle()

pen_annonce = pen_inventaire.clone() # Clone (et pas simple = ) pour copier ses propriétés mais être indépendant


M = lire_matrice(fichier_plan)
dictio = creer_dictionnaire_des_objets(fichier_objets)
dictip = creer_dictionnaire_des_portes(fichier_portes)
pas = calculer_pas(M)

afficher_plan(M)


tracer_character(POSITION_DEPART,calculer_pas(M))
turtle.listen()    # Déclenche l’écoute du clavier
turtle.onkeypress(deplacer_gauche, "Left")   # Associe à la touche Left une fonction appelée deplacer_gauche
turtle.onkeypress(deplacer_droite, "Right")
turtle.onkeypress(deplacer_haut, "Up")
turtle.onkeypress(deplacer_bas, "Down")
turtle.mainloop()    # Place le programme en position d’attente d’une action du joueur
turtle.done()   # Termine le programme après la fermeture