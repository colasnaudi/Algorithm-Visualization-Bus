# ~~~~~~~~ Import de la bibliothèque json pour traiter un fichier json ~~~~~~~ #
# ~~~~~~~~~~~~~~~ Import de sin, cos et acos de la bibliothèque ~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~ math pour la fonction distanceGPS ~~~~~~~~~~~~~~~~~~~~ #
import json
from math import sin, cos, acos

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
#   A : importer les donnees du fichier JSON dans un dictionnaire donneesbus   #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

with open('donneesbus.json') as json_file:
    donneesbus = json.load(json_file)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
#         B : Créer une liste noms_arrets contenants le noms des arrêts        #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

noms_arrets=list(donneesbus.keys())
    
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
#                            C : Créer les fonctions                           #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

def nom(ind):
    """Retourne le nom de l'arrêt à l'indice ind

    :param ind: indice de l'arrêt
    :type ind: int
    :return: un nom
    :rtype: str
    """
    return noms_arrets[ind]


def indice_som(nom_som):
    """Retourne l'indice de l'arrêt de nom nom_som

    :param nom_som: nom de l'arrêt
    :type nom_som: str
    :return: un indice
    :rtype: int
    """
    return noms_arrets.index(nom_som)

def latitude(nom_som):
    """Retourne la latitude de l'arrêt de nom nom_som

    :param nom_som: nom de l'arrêt
    :type nom_som: str
    :return: une latitude
    :rtype: float
    """
    return donneesbus[nom_som][0]

def longitude(nom_som):
    """Retourne la longitude de l'arrêt de nom nom_som

    :param nom_som: nom de l'arrêt
    :type nom_som: str
    :return: une longitude
    :rtype: float
    """
    return donneesbus[nom_som][1]

def voisin(nom_som):
    """Retourne la liste des voisins de l'arrêt de nom nom_som

    :param nom_som: nom de l'arrêt
    :type nom_som: str
    :return: une liste de noms d'arrêts
    :rtype: list
    """
    return donneesbus[nom_som][2]

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
#            D : Le réseau du bus peut être modélisé par des graphes           #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
#                              Par un dictionnaire                             #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

# ~~~~~~~~~~~~~~~~~~~~~~~ Création du dictionnaire vide ~~~~~~~~~~~~~~~~~~~~~~ #
dic_bus = {}
for arret in noms_arrets:
    # ~~~~~~~~~~~~~~~~~~~~ Pour chaque arret dans noms_arrets ~~~~~~~~~~~~~~~~~~~~ #
    # ~~~~~~~~~~ On crée une liste vide qui a pour clé le nom de l'arrêt ~~~~~~~~~ #
    dic_bus[arret] = []
    for arret2 in noms_arrets:
        # ~~~~~~~~~~~~~ Pour chaque arret2 dans noms_arrets ~~~~~~~~~~~~~~~~~~~~~ #
        if arret2 in voisin(arret):
            # ~~~~~~~~~~~~~~~ Si arret2 est dans la liste des voisins ~~~~~~~~~~~~~ #
            dic_bus[arret].append(arret2)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
#                            Par une liste de liste                            #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

# ~~~~~~~~~~~~~~~~~~~~~~~~~ Création d'une liste vide ~~~~~~~~~~~~~~~~~~~~~~~~ #
mat_bus = []
for arret in noms_arrets:
    # ~~~~~~~~~~~~~~~~~~~~ Pour chaque arret dans noms_arrets ~~~~~~~~~~~~~~~~~~~~ #
    # ~~~~~~~~~~~~~~~~~~~~~~~~~ On crée une liste vide ~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
    liste = []
    for arret2 in noms_arrets:
        # ~~~~~~~~~~~~~ Pour chaque arret2 dans noms_arrets ~~~~~~~~~~~~~~~~~~~~~ #
        if arret2 in voisin(arret):
            # ~~~~~~~~~~~~~~~ Si arret2 est dans la liste des voisins ~~~~~~~~~~~~~ #
            liste.append(1)
        else:
            # ~~~~~~~~~~~~~~~ Si arret2 n'est pas dans la liste des voisins ~~~~~~~~~~~~~~~ #
            liste.append(0)
    # ~~~~~~~~~~~~~~~~~ Ajouter la liste liste à la liste mat_bus ~~~~~~~~~~~~~~~~ #
    mat_bus.append(liste)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
#                                 E : Distance                                 #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

def distanceGPS(latA,latB,longA,longB): 
    # Conversions des latitudes en radians 
    ltA=latA/180*3.14
    ltB=latB/180*3.14
    loA=longA/180*3.14
    loB=longB/180*3.14
    # Rayon de la terre en mètres (sphère IAG-GRS80) 
    RT = 6378137 
    # angle en radians entre les 2 points  
    S = acos(round(sin(ltA)*sin(ltB) + cos(ltA)*cos(ltB)*cos(abs(loB-loA)),14)) 
    # distance entre les 2 points, comptée sur un arc de grand cercle 
    return S*RT

def distarrets(arret1, arret2):
    """Retourne la distance entre les arrêts arret1 et arret2

    :param arret1 : nom de l'arrêt 1
    :type : str
    :param arret2 : nom de l'arrêt 2
    :type : str
    :return: distance entre les deux arrêts
    :rtype: float
    """
    return(round(distanceGPS(latitude(arret1),latitude(arret2),longitude(arret1),longitude(arret2))))

def distarc(arret1, arret2):
    """Retourne la distance entre les arrêts arret1 et arret2 s'il existe sinon retourne 'inf'

    :param arret1 : nom de l'arrêt 1
    :type : str
    :param arret2 : nom de l'arrêt 2
    :type : str
    :return: distance entre les deux arrêts
    :rtype: float
    """
    if arret2 in voisin(arret1):
        return(distarrets(arret1, arret2))
    else:
        return float("inf")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
#                    F : Modélisation par un graphe pondéré                    #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

# ~~~~~~~~~ Matrice des poids (liste de listes), poids_bus prenant en ~~~~~~~~ #
# ~~~~~~~~~~~ compte à la fois l’existence des arcs et leur poids. ~~~~~~~~~~~ #

poids_bus = []
for arret in noms_arrets:
    # ~~ Pour chaque arret dans noms_arrets, on l'ajoute dans la liste poids_bus ~ #
    # ~~~~~~~~~~~~~~~~~~~~~~~~ Puis on crée une liste vide ~~~~~~~~~~~~~~~~~~~~~~~ #
    liste = []
    for arret2 in noms_arrets:
        # ~~~~~ On regarde si l'arret2 est dans la liste des voisins de l'arret1 ~~~~~ #
        if arret2 in voisin(arret):
            # ~~~~~ Si oui, on ajoute la distance entre les deux arrêts dans la liste ~~~~ #
            liste.append(distarc(arret, arret2))
        else:
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~ Sinon on ajoute 'inf' ~~~~~~~~~~~~~~~~~~~~~~~~~~ #
            liste.append(float("inf"))
    # ~~~~~~~~~~~~~~~~~~~~~~~~ On ajoute la liste à la liste poids_bus ~~~~~~~~~~~~~~~~~~ #
    poids_bus.append(liste)



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
#                                    ETAPE 2                                   #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
#                                   DJIKSTRA                                   #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

def Djikstra(arret_dep, arret_arriv):
    """Calcule le plus court chemin entre deux points arret_dep et arret_ariv
    en utilisant l'algorithme de Djikstra
    :param arret_dep: arret de départ
    :type arret_dep: str
    :param arret_arriv: arret d'arrivée
    :type arret_arriv: str
    :return: une liste d'arrêts, la distance minimum
    :rtype: list, int
    """
    def extract_min(lst):
        minS = 100000
        valS = 100000
        for i in range (len(lst)):
            if (lst[i] < valS):
                minS = i
                valS = lst[i]
        return(minS)

    # ~~~~~~~~~~~~~~~~ Déclaration et initialisation des variables ~~~~~~~~~~~~~~~ #
    dist=[]
    pred=[]
    a_traiter=[]
    lst=[]
    som=indice_som(arret_dep)
    compteur = 0

    for i in range(len(poids_bus)):
        dist.append(float('inf'))
        lst.append(float('inf'))
        pred.append(float('inf'))
        a_traiter.append(i)
    
    a_traiter.remove(indice_som(arret_dep)) # On enlève l'arret de départ de la liste des arrets à traiter
    pred[som] = som # On met le prédécesseur de l'arret de départ à lui-même
    dist[som] = 0 # On met la distance de l'arret de départ à 0
    
    # ~~~~~~~~~~~~~~~~ Boucle tant qu'il y a des sommets à traiter ~~~~~~~~~~~~~~~ #
    while(len(a_traiter) != 0):
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~ Initialisation liste ~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
        for i in range(len(poids_bus)):
            lst[i] = (float('inf'))
    # ~~~~~~~~~~~~~~~~ Les poids de chaque arc commencant par som ~~~~~~~~~~~~~~~~ #
        for i in range(len(poids_bus)):
            if(i in a_traiter):
                lst[i] = (poids_bus[som][i])
    
    # ~~~~~~~~ Comparaison de la dist du sommet avec la nouvelle distance ~~~~~~~~ #
        for i in range(len(lst)):
            if(lst[i] < float('inf')):
                if(dist[i] > (dist[som]+lst[i])):
                    pred[i] = som
                    dist[i]
                    dist[i] = dist[som]+lst[i]
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Re initialisation ~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
        for i in range(len(poids_bus)):
            lst[i] = (float('inf'))
        # ~~~~~~~~~~~~~~~~~~ La distance des poids encore à traiter ~~~~~~~~~~~~~~~~~~ #
        for i in (a_traiter):
            lst[i] = dist[i]
        # ~~~~~~~~~~~~~~~~ Initialisation du nouveau sommet a traiter ~~~~~~~~~~~~~~~~ #
        som = extract_min(lst)
        a_traiter.remove(som)
        compteur = compteur+1
        
    # ~~~~~~~~ Liste des arrets du chemin (avec arret_dep et arret_arriv) ~~~~~~~~ #
    chemin = []
    som = indice_som(arret_arriv)
    while som != indice_som(arret_dep):
        chemin.append(nom(som))
        som = pred[som]
    chemin.append(arret_dep)
    chemin.reverse()
    
    # Affichage des résultats
    print("Le chemin permettant d'aller de", arret_dep, "jusqu'à",arret_arriv, "est :",str(chemin).replace("[","").replace("'","").replace(", "," -> ").replace("]",""),"\nLe trajet comptera", len(chemin), "arrets." ,"\nLa distance entre ces 2 arrets est de :", dist[indice_som(arret_arriv)],"m.")
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ APPEL ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
"""
arret_dep = input("Arret dep :")
arret_arriv = input("Arret fin :")
if(arret_dep not in noms_arrets):
    print("L'arret", arret_dep,"n'existe pas.")
    if(arret_arriv not in noms_arrets):
        print("L'arret", arret_arriv,"n'existe pas.")
else:
    Djikstra(arret_dep, arret_arriv)
"""

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
#                                   BELMANN                                    #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

def Belmann(arret_dep,arret_arriv):
    """Calcule le plus court chemin entre deux arrêts arret_dep et arret_arriv
    en utilisant l'algorithme de Bellman-Ford
    :param arret_dep: arret de départ
    :type arret_dep: str
    :param arret_arriv: arret d'arrivée
    :type arret_arriv: str
    :return: une liste d'arrêts, la distance minimum
    :rtype: list, int
    """
    #Création la liste des prédecesseurs
    pred = [None]*len(noms_arrets)
    #Création la liste des distances
    dist = [None]*len(noms_arrets)

    #Initialisation des listes
    for i in range(len(noms_arrets)):
        pred[i] = None
        dist[i] = float("inf")
    
    dist[indice_som(arret_dep)] = 0

    #Boucle de Bellman
    for i in range(len(noms_arrets)-1):
        for j in noms_arrets:
            for k in voisin(j):
                if dist[indice_som(j)] + poids_bus[indice_som(j)][indice_som(k)] < dist[indice_som(k)]:
                    dist[indice_som(k)] = dist[indice_som(j)] + poids_bus[indice_som(j)][indice_som(k)]
                    pred[indice_som(k)] = j
    
    #Création de la liste des arrêts parcourus
    arret_fin = arret_arriv
    chemin = []
    chemin.append(arret_fin)
    while pred[indice_som(arret_fin)] != None:
        chemin.append(pred[indice_som(arret_fin)])
        arret_fin = pred[indice_som(arret_fin)]
    chemin.reverse()
    
    print ("Le chemin permettant d'aller de", arret_dep, "jusqu'à",arret_arriv, "est :",str(chemin).replace("[","").replace("'","").replace(", "," -> ").replace("]",""),"\nLe trajet comptera", len(chemin), "arrets." ,"\nLa distance entre ces 2 arrets est de :", dist[indice_som(arret_arriv)],"m.")
"""
arret_dep = input("Arret dep :")
arret_arriv = input("Arret fin :")
if(arret_dep not in noms_arrets):
    print("L'arret", arret_dep,"n'existe pas.")
    if(arret_arriv not in noms_arrets):
        print("L'arret", arret_arriv,"n'existe pas.")
else:
    Belmann(arret_dep, arret_arriv)
"""

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
#                                FLOYD WARSHALL                                #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

def FloydWarshall(arret_dep,arret_arriv):
    """Calcule le plus court chemin entre deux arrêts arret_dep et arret_arriv
    en utilisant l'algorithme de Floyd-Warshall
    :param arret_dep: arret de départ
    :type arret_dep: str
    :param arret_arriv: arret d'arrivée
    :type arret_arriv: str
    :return: une liste d'arrêts, la distance minimum
    :rtype: list, int
    """
    #Création de la matrice Mk
    Mk = []
    for i in range(len(noms_arrets)):
        Mk.append([])
        for j in range(len(noms_arrets)):
            if i == j:
                Mk[i].append(0)
            else:
                Mk[i].append(float("inf"))
    
    #Initialisation de la matrice Mk
    for i in range(len(noms_arrets)):
        for j in voisin(noms_arrets[i]):
            Mk[indice_som(noms_arrets[i])][indice_som(j)] = poids_bus[indice_som(noms_arrets[i])][indice_som(j)]

    #Création de la matrice Pk
    Pk = []
    for i in range(len(noms_arrets)):
        Pk.append([])
        for j in range(len(noms_arrets)):
            Pk[i].append(None)

    #Initialisation de la matrice Pk
    for i in range(len(noms_arrets)):
        for j in voisin(noms_arrets[i]):
            Pk[indice_som(j)][indice_som(noms_arrets[i])] = noms_arrets[i]
    
    #Boucle de Floyd-Warshall
    for k in range(len(noms_arrets)):
        #Création de la liste colonnes
        colonnes = []
        for i in range(len(noms_arrets)):
                if i != k and Mk[i][k] != float("inf"):
                    colonnes.append(i)          
        
        #Creation de la liste lignes
        lignes = []
        for i in range(len(noms_arrets)):
            if i != k and Mk[k][i] != float("inf"):
                lignes.append(i)
        
        #Boucle de calcul de Mk
        for i in colonnes:
            for j in lignes:
                if Mk[i][k] + Mk[k][j] < Mk[i][j]:
                    Mk[i][j] = Mk[i][k] + Mk[k][j]
                    Pk[i][j] = Pk[i][k]

    #Création de la liste des arrêts parcourus
    parcours = []
    arret_fin = arret_arriv
    parcours.append(arret_fin)
    while Pk[indice_som(arret_fin)][indice_som(arret_dep)] != None:
        parcours.append(Pk[indice_som(arret_fin)][indice_som(arret_dep)])
        arret_fin = Pk[indice_som(arret_fin)][indice_som(arret_dep)]
    parcours.reverse()
    print("Le chemin permettant d'aller de", arret_dep, "jusqu'à",arret_arriv, "est :",str(parcours).replace("[","").replace("'","").replace(", "," -> ").replace("]",""),"\nLe trajet comptera", len(parcours), "arrets." ,"\nLa distance entre ces 2 arrets est de :", Mk[indice_som(arret_arriv)][indice_som(arret_dep)],"m.")

"""
arret_dep = input("Arret dep :")
arret_arriv = input("Arret fin :")
if(arret_dep not in noms_arrets):
    print("L'arret", arret_dep,"n'existe pas.")
    if(arret_arriv not in noms_arrets):
        print("L'arret", arret_arriv,"n'existe pas.")
else:
    FloydWarshall(arret_dep, arret_arriv)
"""

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
#                                    A_STAR                                    #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

def A_star(arret_dep,arret_arriv):
    #A_star est une fonction qui prend en paramètre les deux arrêts de départ et d'arrivée.
    #Elle renvoie le plus court chemin, sous forme de la liste des arrêts parcourus ainsi, que la distance minimum.
    #Elle utilise la fonction heuristique ainsi que la fonction de recherche de plus court chemin.

    openList = [arret_dep]
    closedList = []
    pred = []
    dist = []

    #Initialisation de la liste des prédécesseurs
    for i in range(len(noms_arrets)):
        pred.append(None)
    #Initialisation de la liste des distances
    for i in range(len(noms_arrets)):
        if i == indice_som(arret_dep):
            dist.append(0)
        else:
            dist.append(float("inf"))
    #Initialisation de la liste des distances
    for i in range(len(noms_arrets)):
        dist[indice_som(noms_arrets[i])] = poids_bus[indice_som(noms_arrets[i])][indice_som(arret_dep)]
    
    #Boucle de A*
    #Si la file d'attente est vide, il n'y a aucun chemin du nœud initial au nœud d'arrivée, ce qui interrompt l'algorithme.
    while len(openList) != 0:

        #L'algorithme retire le premier nœud de la file d'attente prioritaire, le nœud courant.
        arret_courant = openList[0]

        #Si le nœud retenu est le nœud d'arrivée, A* reconstruit le chemin complet et s'arrête.
        if(arret_courant == arret_arriv):
            break
        
        #Si le nœud n'est pas le nœud d'arrivée, de nouveaux nœuds sont créés ;
        #Pour chaque nœud successif, A* calcule son coût et le stocke avec le nœud.
        #On cherche les nœuds qui sont accessibles par le nœud courant.
        for i in range(len(openList)):
            if dist[indice_som(openList[i])] < dist[indice_som(arret_courant)]:
                arret_courant = openList[i]
        #On le supprime de la liste des arrets à visiter
        openList.remove(arret_courant)
        #On l'ajoute à la liste des arrets visités
        closedList.append(arret_courant)
        #On récupère les voisins de l'arret courant
        voisins = voisin(arret_courant)
        #Boucle sur les voisins
        for i in voisins:
            #Si le voisin n'est pas dans la liste des arrets visités 
            #Si le voisin n'est pas dans la liste des arrets à visiter
            if i not in closedList and i not in openList:
                #On l'ajoute à la liste des arrets à visiter 
                openList.append(i)
            #On calcule la distance entre l'arret courant et le voisin
            dist_voisin = dist[indice_som(arret_courant)] + poids_bus[indice_som(arret_courant)][indice_som(i)]
            #Si la distance est inférieure à la distance actuelle
            if dist_voisin < dist[indice_som(i)]:
                #On met à jour la distance
                dist[indice_som(i)] = dist_voisin
                #On met à jour le prédécesseur
                pred[indice_som(i)] = arret_courant

    #Création de la liste des arrêts parcourus
    parcours = []
    arret_fin = arret_arriv

    parcours.append(arret_arriv)
    while pred[indice_som(arret_arriv)] != None:
        parcours.append(pred[indice_som(arret_arriv)])
        arret_arriv = pred[indice_som(arret_arriv)]
    parcours.append(arret_dep)
    parcours.reverse()

    print("A_Star : Le chemin permettant d'aller de", arret_dep, "jusqu'à",arret_fin, "est :",str(parcours).replace("[","").replace("'","").replace(", "," -> ").replace("]",""),"\nLe trajet comptera", len(parcours), "arrets." ,"\nLa distance entre ces 2 arrets est de :", dist[indice_som(arret_fin)],"m.")

"""
arret_dep = input("Arret dep :")
arret_arriv = input("Arret fin :")
if(arret_dep not in noms_arrets):
    print("L'arret", arret_dep,"n'existe pas.")
    if(arret_arriv not in noms_arrets):
        print("L'arret", arret_arriv,"n'existe pas.")
else:
    A_star(arret_dep, arret_arriv)
"""

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
#                                    ETAPE 3                                   #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

# Pour lancer le programme -> Terminal
# ╰─ cd Desktop/GitHub/BUT-INFO/S2/S2.02-Exploration-algorithmique-d-un-problème
# ╰─ python3 Etape3_2.py

from graphics import *
from tkinter import ttk

# ~~ Création du tableau avec les coordonnées des arrêts calibrés sur la map ~ #
tab = []
for i in noms_arrets:
        tab.append([])
        # Le premier chiffre c'est pour se déplacer sur l'axe
        # Le deuxième chiffre c'est pour enlever la plus petite valeur
        # Le troisième chiffre c'est pour écarter/rétrécir l'espace entre les points
        long = 68+(longitude(i)+1.59)*4580
        lat = 805-(latitude(i)-43.430492)*6150
        tab[indice_som(i)].append(long)
        tab[indice_som(i)].append(lat)
    
# Fonction qui à partir d'une couleur retourne le suivante d'une liste de couleurs
def countX(liste, x):
    count = 0
    for ele in liste:
        if (ele == x):
            count = count + 1
    return count

def init(win):
    win.delete('all') # On efface tout
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Image de fond ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
    maps = Image(Point(450,420), "maps.png")
    maps.draw(win)
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Texte distance ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
    text1 = Text(Point(60,260), "Distance :")
    text1.setStyle('bold')
    text1.setTextColor('white')
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Texte Nb arrêts ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
    text2 = Text(Point(62,280), "Nb arrêts :")
    text2.setStyle('bold')
    text2.setTextColor('white')
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Dessiner les textes ~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
    text1.draw(win)
    text2.draw(win)

def dessiner_arrets(win, arret_dep, arret_arriv):
    for i in range(len(tab)):
        # Création du cercle
        c = Circle(Point(tab[i][0], tab[i][1]), 4)
        c.setFill("white")
        c.draw(win)
    # ~~~~~~~ Affichage du noms des deux arrêts en blanc au dessus du point ~~~~~~ #
    text1 = Text(Point(tab[indice_som(arret_dep)][0], tab[indice_som(arret_dep)][1]-10), arret_dep)
    text2 = Text(Point(tab[indice_som(arret_arriv)][0], tab[indice_som(arret_arriv)][1]-10), arret_arriv)
    text1.setStyle('bold')
    text2.setStyle('bold')
    text1.setTextColor('white')
    text2.setTextColor('white')
    text1.draw(win)
    text2.draw(win)
    # ~~~~~~~~~~~~~~~~~~~~~~~~~ L'arrêt de départ en vert ~~~~~~~~~~~~~~~~~~~~~~~~ #
    c = Circle(Point(tab[indice_som(arret_dep)][0], tab[indice_som(arret_dep)][1]), 4)
    c.setFill("green")
    c.draw(win)
    # ~~~~~~~~~~~~~~~~~~~~~~~~ L'arrêt d'arrivée en rouge ~~~~~~~~~~~~~~~~~~~~~~~~ #
    c = Circle(Point(tab[indice_som(arret_arriv)][0], tab[indice_som(arret_arriv)][1]), 4)
    c.setFill("red")
    c.draw(win)

def A_star_Etape3(arret_dep,arret_arriv, win):
    #A_star est une fonction qui prend en paramètre les deux arrêts de départ et d'arrivée.
    #Elle renvoie le plus court chemin, sous forme de la liste des arrêts parcourus ainsi, que la distance minimum.
    #Elle utilise la fonction heuristique ainsi que la fonction de recherche de plus court chemin.
    dejaVisite = []
    openList = [arret_dep]
    closedList = []
    pred = []
    dist = []
    
    dessiner_arrets(win, arret_dep, arret_arriv)

    #Initialisation de la liste des prédécesseurs
    for i in range(len(noms_arrets)):
        pred.append(None)
    #Initialisation de la liste des distances
    for i in range(len(noms_arrets)):
        if i == indice_som(arret_dep):
            dist.append(0)
        else:
            dist.append(float("inf"))
    #Initialisation de la liste des distances
    for i in range(len(noms_arrets)):
        dist[indice_som(noms_arrets[i])] = poids_bus[indice_som(noms_arrets[i])][indice_som(arret_dep)]
    
    #Boucle de A*
    #Si la file d'attente est vide, il n'y a aucun chemin du nœud initial au nœud d'arrivée, ce qui interrompt l'algorithme.
    while len(openList) != 0:

        #L'algorithme retire le premier nœud de la file d'attente prioritaire, le nœud courant.
        arret_courant = openList[0]

        #Si le nœud retenu est le nœud d'arrivée, A* reconstruit le chemin complet et s'arrête.
        if(arret_courant == arret_arriv):
            break
        
        #Si le nœud n'est pas le nœud d'arrivée, de nouveaux nœuds sont créés ;
        #Pour chaque nœud successif, A* calcule son coût et le stocke avec le nœud.
        #On cherche les nœuds qui sont accessibles par le nœud courant.
        for i in range(len(openList)):
            if dist[indice_som(openList[i])] < dist[indice_som(arret_courant)]:
                arret_courant = openList[i]
        #On le supprime de la liste des arrets à visiter
        openList.remove(arret_courant)
        #On l'ajoute à la liste des arrets visités
        closedList.append(arret_courant)
        #On récupère les voisins de l'arret courant
        voisins = voisin(arret_courant)
        #Boucle sur les voisins
        for i in voisins:
            update(1000) # Optimisation de l'exécution
            #Si le voisin n'est pas dans la liste des arrets visités 
            #Si le voisin n'est pas dans la liste des arrets à visiter
            if i not in closedList and i not in openList:
                #On l'ajoute à la liste des arrets à visiter 
                openList.append(i)
            #On calcule la distance entre l'arret courant et le voisin
            dist_voisin = dist[indice_som(arret_courant)] + poids_bus[indice_som(arret_courant)][indice_som(i)]
            #Si la distance est inférieure à la distance actuelle
            if dist_voisin < dist[indice_som(i)]:
                #On met à jour la distance
                dist[indice_som(i)] = dist_voisin
                #On met à jour le prédécesseur
                pred[indice_som(i)] = arret_courant
                
                # ~~~~~~~~~~~~~~~~~~~~~ Affichage de la ligne du parcours ~~~~~~~~~~~~~~~~~~~~ #
                dejaVisite.append(arret_courant)
                Ligne = Line(Point(tab[indice_som(arret_courant)][0], tab[indice_som(arret_courant)][1]), Point(tab[indice_som(i)][0], tab[indice_som(i)][1]))
                # ~~~~~~~~~~~~~~ Couleur plus sombre selon le nombre de passage ~~~~~~~~~~~~~~ #
                if(countX(dejaVisite, arret_courant)==1):
                    Ligne.setFill("light green")
                if(countX(dejaVisite, arret_courant)==2):
                    Ligne.setFill("green")
                if(countX(dejaVisite, arret_courant)==3):
                    Ligne.setFill("dark green")
                if(countX(dejaVisite, arret_courant)==4):
                    Ligne.setFill("green")
                if(countX(dejaVisite, arret_courant)==5):
                    Ligne.setFill("black")
                Ligne.draw(win)
                # ~~~~~~~~~~~~~~~~~~~~~~~~ Affichage du point courant ~~~~~~~~~~~~~~~~~~~~~~~~ #
                c = Circle(Point(tab[indice_som(i)][0], tab[indice_som(i)][1]), 4)
                c.setFill("white")
                c.draw(win)
                # ~~~~~~~~~~~~~~~~~~~~~ Affichage du nom du point courant ~~~~~~~~~~~~~~~~~~~~ #
                text1 = Text(Point(tab[indice_som(i)][0], tab[indice_som(i)][1]-10), i)
                text1.setStyle('bold')
                text1.setTextColor('white')
                text1.draw(win)
                update(1000) # Optimisation de l'exécution
                # ~~~~~~~~~~~~~ On efface le point et le texte de l'arret courant ~~~~~~~~~~~~ #
                c.undraw()
                text1.undraw()
            if i == arret_arriv:
                break
        if i == arret_arriv:
                break

    #Création de la liste des arrêts parcourus
    parcours = []
    arret_fin = arret_arriv

    parcours.append(arret_arriv)
    while pred[indice_som(arret_arriv)] != None:
        parcours.append(pred[indice_som(arret_arriv)])
        arret_arriv = pred[indice_som(arret_arriv)]
    parcours.append(arret_dep)
    parcours.reverse()
    
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~ Commandes graphiques ~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
    # ~~~~~~~~~~~~~~~~~~~~~~~~~ Affichage de la distance ~~~~~~~~~~~~~~~~~~~~~~~~~ #
    text1 = Text(Point(120,260), str(dist[indice_som(arret_fin)]) + " m")
    text1.setStyle('normal')
    text1.setTextColor('white')
    # ~~~~~~~~~~~~~~~~~~~~~~~ Affichage du nombre d'arrêts ~~~~~~~~~~~~~~~~~~~~~~~ #
    text2 = Text(Point(110,280), len(parcours))
    text2.setStyle('normal')
    text2.setTextColor('white')
    text1.draw(win)
    text2.draw(win)
    # ~~~~~~~~~~~~~~~~~~~~~~~~~ Affichage du chemin final ~~~~~~~~~~~~~~~~~~~~~~~~ #
    for i in parcours:
        # ~~~~~~~~~~~~~ Affichage du texte de l'arrêt courant de parcours ~~~~~~~~~~~~ #
        text1 = Text(Point(tab[indice_som(i)][0], tab[indice_som(i)][1]-10), i)
        text1.setStyle('bold')
        text1.setTextColor('white')
        text1.draw(win)
        
        if i != arret_dep:
            # ~~~~~~~~~~~~~~~~~~~ Affichage des lignes entre les arrêts ~~~~~~~~~~~~~~~~~~ #
            Ligne = Line(Point(tab[indice_som(i)][0], tab[indice_som(i)][1]), Point(tab[indice_som(parcours[parcours.index(i)-1])][0], tab[indice_som(parcours[parcours.index(i)-1])][1]))
            Ligne.setFill("red")
            Ligne.draw(win)

        if i != arret_dep and i != arret_fin:
            # ~~~~~~~~~~~~~~~~~~~ Affichage du point de l'arrêt courant ~~~~~~~~~~~~~~~~~~ #
            c = Circle(Point(tab[indice_som(i)][0], tab[indice_som(i)][1]), 4)
            c.setFill("white")
            c.draw(win)


def FloydWarshall_Etape3(arret_dep,arret_arriv, win):
    """Calcule le plus court chemin entre deux arrêts arret_dep et arret_arriv
    en utilisant l'algorithme de Floyd-Warshall
    :param arret_dep: arret de départ
    :type arret_dep: str
    :param arret_arriv: arret d'arrivée
    :type arret_arriv: str
    :return: une liste d'arrêts, la distance minimum
    :rtype: list, int
    """
    dessiner_arrets(win, arret_dep, arret_arriv)
    #Création de la matrice Mk
    Mk = []
    for i in range(len(noms_arrets)):
        Mk.append([])
        for j in range(len(noms_arrets)):
            if i == j:
                Mk[i].append(0)
            else:
                Mk[i].append(float("inf"))
    
    #Initialisation de la matrice Mk
    for i in range(len(noms_arrets)):
        for j in voisin(noms_arrets[i]):
            Mk[indice_som(noms_arrets[i])][indice_som(j)] = poids_bus[indice_som(noms_arrets[i])][indice_som(j)]

    #Création de la matrice Pk
    Pk = []
    for i in range(len(noms_arrets)):
        Pk.append([])
        for j in range(len(noms_arrets)):
            Pk[i].append(None)

    #Initialisation de la matrice Pk
    for i in range(len(noms_arrets)):
        for j in voisin(noms_arrets[i]):
            Pk[indice_som(j)][indice_som(noms_arrets[i])] = noms_arrets[i]
    
    #Boucle de Floyd-Warshall
    for k in range(len(noms_arrets)):
        update(2000) # Optimisation de la vitesse
        #Création de la liste colonnes
        colonnes = []
        for i in range(len(noms_arrets)):
                if i != k and Mk[i][k] != float("inf"):
                    colonnes.append(i)          
        
        #Creation de la liste lignes
        lignes = []
        for i in range(len(noms_arrets)):
            if i != k and Mk[k][i] != float("inf"):
                lignes.append(i)
        
        #Boucle de calcul de Mk
        dejaVisite = []
        for i in colonnes:
            for j in lignes:
                if Mk[i][k] + Mk[k][j] < Mk[i][j]:
                    # time.sleep(0.01)        
                    aLine = Line(Point(tab[i][0],tab[i][1]), Point(tab[j][0],tab[j][1]))
                    dejaVisite.append(i)
                    # ~~~~~~~~~~~~~~ Couleur plus sombre selon le nombre de passage ~~~~~~~~~~~~~~ #
                    if(countX(dejaVisite,i)==1):
                        aLine.setFill("light green")
                    if(countX(dejaVisite,i)==2):
                        aLine.setFill("green")
                    if(countX(dejaVisite,i)==3):
                        aLine.setFill("dark green")
                    if(countX(dejaVisite ,i)==4):
                        aLine.setFill("green")
                    if(countX(dejaVisite ,i)==5):
                        aLine.setFill("black") 
                    aLine.draw(win)
                    Mk[i][j] = Mk[i][k] + Mk[k][j]
                    Pk[i][j] = Pk[i][k]    
        print(k)
    #Création de la liste des arrêts parcourus
    parcours = []
    arret_fin = arret_arriv
    parcours.append(arret_fin)
    while Pk[indice_som(arret_fin)][indice_som(arret_dep)] != None:
        parcours.append(Pk[indice_som(arret_fin)][indice_som(arret_dep)])
        arret_fin = Pk[indice_som(arret_fin)][indice_som(arret_dep)]
    parcours.reverse()

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~ Commandes graphiques ~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
    # ~~~~~~~~~~~~~~~~~~~~~~~~~ Affichage de la distance ~~~~~~~~~~~~~~~~~~~~~~~~~ #
    text1 = Text(Point(120,260), str(Mk[indice_som(arret_arriv)][indice_som(arret_dep)]) + " m")
    text1.setStyle('normal')
    text1.setTextColor('white')
    # ~~~~~~~~~~~~~~~~~~~~~~~~ Affichage du nombre d'arrêt ~~~~~~~~~~~~~~~~~~~~~~~ #
    text2 = Text(Point(110,280), len(parcours))
    text2.setStyle('normal')
    text2.setTextColor('white')
    text1.draw(win)
    text2.draw(win)
    # ~~~~~~~ Affichage à nouveau du nom de l'arrêt de départ et d'arrivée ~~~~~~~ #
    text1 = Text(Point(tab[indice_som(arret_dep)][0], tab[indice_som(arret_dep)][1]-10), arret_dep)
    text2 = Text(Point(tab[indice_som(arret_arriv)][0], tab[indice_som(arret_arriv)][1]-10), arret_arriv)
    text1.setStyle('bold')
    text2.setStyle('bold')
    text1.setTextColor('white')
    text2.setTextColor('white')
    text1.draw(win)
    text2.draw(win)
    # ~~~~~~~~~~~~~~~~~~~ Affichage du point de départ en vert ~~~~~~~~~~~~~~~~~~~ #
    c = Circle(Point(tab[indice_som(arret_dep)][0], tab[indice_som(arret_dep)][1]), 4)
    c.setFill("green")
    c.draw(win)
    # ~~~~~~~~~~~~~~~~~~~ Affichage du point d'arrivée en rouge ~~~~~~~~~~~~~~~~~~ #
    c = Circle(Point(tab[indice_som(arret_arriv)][0], tab[indice_som(arret_arriv)][1]), 4)
    c.setFill("red")
    c.draw(win)

    for i in parcours:
        # ~~~~~~~~~~~~~~~ Affichage du nom de l'arrêt courant de chemin ~~~~~~~~~~~~~~ #
        text1 = Text(Point(tab[indice_som(i)][0], tab[indice_som(i)][1]-10), i)
        text1.setStyle('bold')
        text1.setTextColor('white')
        text1.draw(win)
        if i != arret_dep:
            # ~~~~~~~~~~~~~~~~~~~ Affichage des lignes entre les arrêts ~~~~~~~~~~~~~~~~~~ #
            Ligne = Line(Point(tab[indice_som(i)][0], tab[indice_som(i)][1]), Point(tab[indice_som(parcours[parcours.index(i)-1])][0], tab[indice_som(parcours[parcours.index(i)-1])][1]))
            Ligne.setFill("red")
            Ligne.draw(win)

        if i != arret_dep and i != arret_arriv:
            # ~~~~~~~~~~~~~~~~~~~ Affichage du point de l'arrêt courant ~~~~~~~~~~~~~~~~~~ #
            c = Circle(Point(tab[indice_som(i)][0], tab[indice_som(i)][1]), 4)
            c.setFill("white")
            c.draw(win)

def Belmann_Etape3(arret_dep,arret_arriv, win):
    """Calcule le plus court chemin entre deux arrêts arret_dep et arret_arriv
    en utilisant l'algorithme de Bellman-Ford
    :param arret_dep: arret de départ
    :type arret_dep: str
    :param arret_arriv: arret d'arrivée
    :type arret_arriv: str
    :return: une liste d'arrêts, la distance minimum
    :rtype: list, int
    """
    dessiner_arrets(win, arret_dep, arret_arriv)
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Initialisation ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
    dejaVisite = []
    #Création la liste des prédecesseurs
    pred = [None]*len(noms_arrets)
    #Création la liste des distances
    dist = [None]*len(noms_arrets)

    #Initialisation des listes
    for i in range(len(noms_arrets)):
        pred[i] = None
        dist[i] = float("inf")
    
    dist[indice_som(arret_dep)] = 0

    #Boucle de Bellman
    for i in range(len(noms_arrets)-1):
        update(1000) # Optimisation de l'affichage
        for j in noms_arrets:
            for k in voisin(j):
                if dist[indice_som(j)] + poids_bus[indice_som(j)][indice_som(k)] < dist[indice_som(k)]:
                    dist[indice_som(k)] = dist[indice_som(j)] + poids_bus[indice_som(j)][indice_som(k)]
                    pred[indice_som(k)] = j
                    dejaVisite.append(k)
                    Ligne = Line(Point(tab[indice_som(j)][0], tab[indice_som(j)][1]), Point(tab[indice_som(k)][0], tab[indice_som(k)][1]))
                    if(countX(dejaVisite, k)==1):
                        Ligne.setFill("light green")
                    if(countX(dejaVisite, k)==2):
                        Ligne.setFill("green")
                    if(countX(dejaVisite, k)==3):
                        Ligne.setFill("dark green")
                    if(countX(dejaVisite, k)==4):
                        Ligne.setFill("green")
                    if(countX(dejaVisite, k)==5):
                        Ligne.setFill("black")
                    Ligne.draw(win)

    #Création de la liste des arrêts parcourus
    arret_fin = arret_arriv
    chemin = []
    chemin.append(arret_fin)
    while pred[indice_som(arret_fin)] != None:
        chemin.append(pred[indice_som(arret_fin)])
        arret_fin = pred[indice_som(arret_fin)]
    chemin.reverse()

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~ Commandes graphiques ~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
    # ~~~~~~~~~~~~~~~~~~~~~~~~~ Affichage de la distance ~~~~~~~~~~~~~~~~~~~~~~~~~ #
    text1 = Text(Point(120,260), str(dist[indice_som(arret_arriv)]) + " m")
    text1.setStyle('normal')
    text1.setTextColor('white')
    # ~~~~~~~~~~~~~~~~~~~~~~~~ Affichage du nombre d'arrêt ~~~~~~~~~~~~~~~~~~~~~~~ #
    text2 = Text(Point(110,280), len(chemin))
    text2.setStyle('normal')
    text2.setTextColor('white')
    text1.draw(win)
    text2.draw(win)
    for i in chemin:
        update(1000) # Optimisation de l'affichage
        # ~~~~~~~~~~~~~~~ Affichage du nom de l'arrêt courant de chemin ~~~~~~~~~~~~~~ #
        text1 = Text(Point(tab[indice_som(i)][0], tab[indice_som(i)][1]-10), i)
        text1.setStyle('bold')
        text1.setTextColor('white')
        text1.draw(win)
        
        if i != arret_dep:
            # ~~~~~~~~~~~~~~~~~~~ Affichage des lignes entre les arrêts ~~~~~~~~~~~~~~~~~~ #
            Ligne = Line(Point(tab[indice_som(i)][0], tab[indice_som(i)][1]), Point(tab[indice_som(chemin[chemin.index(i)-1])][0], tab[indice_som(chemin[chemin.index(i)-1])][1]))
            Ligne.setFill("red")
            Ligne.draw(win)

        if i != arret_dep and i != arret_arriv:
            # ~~~~~~~~~~~~~~~~~~~ Affichage du point de l'arrêt courant ~~~~~~~~~~~~~~~~~~ #
            c = Circle(Point(tab[indice_som(i)][0], tab[indice_som(i)][1]), 4)
            c.setFill("white")
            c.draw(win)


def Djikstra_Etape3(arret_dep, arret_arriv, win):
    """Calcule le plus court chemin entre deux points arret_dep et arret_ariv
    en utilisant l'algorithme de Djikstra
    :param arret_dep: arret de départ
    :type arret_dep: str
    :param arret_arriv: arret d'arrivée
    :type arret_arriv: str
    :return: une liste d'arrêts, la distance minimum
    :rtype: list, int
    """
    def extract_min(lst):
        minS = 100000
        valS = 100000
        for i in range (len(lst)):
            if (lst[i] < valS):
                minS = i
                valS = lst[i]
        return(minS)

    # ~~~~~~~~~~~~~~~~ Déclaration et initialisation des variables ~~~~~~~~~~~~~~~ #
    dist=[]
    pred=[]
    a_traiter=[]
    lst=[]
    som=indice_som(arret_dep)
    compteur = 0
    dejaVisite = []

    dessiner_arrets(win, arret_dep, arret_arriv)

    for i in range(len(poids_bus)):
        dist.append(float('inf'))
        lst.append(float('inf'))
        pred.append(float('inf'))
        a_traiter.append(i)
    
    a_traiter.remove(indice_som(arret_dep)) # On enlève l'arret de départ de la liste des arrets à traiter
    pred[som] = som # On met le prédécesseur de l'arret de départ à lui-même
    dist[som] = 0 # On met la distance de l'arret de départ à 0
    
    # ~~~~~~~~~~~~~~~~ Boucle tant qu'il y a des sommets à traiter ~~~~~~~~~~~~~~~ #
    while(len(a_traiter) != 0):
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~ Initialisation liste ~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
        for i in range(len(poids_bus)):
            lst[i] = (float('inf'))
    # ~~~~~~~~~~~~~~~~ Les poids de chaque arc commencant par som ~~~~~~~~~~~~~~~~ #
        for i in range(len(poids_bus)):
            if(i in a_traiter):
                lst[i] = (poids_bus[som][i])
    
    # ~~~~~~~~ Comparaison de la dist du sommet avec la nouvelle distance ~~~~~~~~ #
        update(1000)
        for i in range(len(lst)):
            if(lst[i] < float('inf')):
                if(dist[i] > (dist[som]+lst[i])):
                    pred[i] = som
                    dist[i]
                    dist[i] = dist[som]+lst[i]
                    # ~~~~~~~~~~~~~~~~ Affichage du fonctionnement de l'algorithme ~~~~~~~~~~~~~~~ #
                    Ligne = Line(Point(tab[som][0], tab[som][1]), Point(tab[i][0], tab[i][1]))
                    dejaVisite.append(som)
                    if(countX(dejaVisite, som)==1):
                        Ligne.setFill("light green")
                    if(countX(dejaVisite, som)==2):
                        Ligne.setFill("green")
                    if(countX(dejaVisite, som)==3):
                        Ligne.setFill("dark green")
                    if(countX(dejaVisite, som)==4):
                        Ligne.setFill("green")
                    if(countX(dejaVisite, som)==5):
                        Ligne.setFill("black")
                    Ligne.draw(win)
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Re initialisation ~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
        for i in range(len(poids_bus)):
            lst[i] = (float('inf'))
        # ~~~~~~~~~~~~~~~~~~ La distance des poids encore à traiter ~~~~~~~~~~~~~~~~~~ #
        for i in (a_traiter):
            lst[i] = dist[i]
        # ~~~~~~~~~~~~~~~~ Initialisation du nouveau sommet a traiter ~~~~~~~~~~~~~~~~ #
        som = extract_min(lst)
        a_traiter.remove(som)
        compteur = compteur+1
        
    # ~~~~~~~~ Liste des arrets du chemin (avec arret_dep et arret_arriv) ~~~~~~~~ #
    chemin = []
    som = indice_som(arret_arriv)
    while som != indice_som(arret_dep):
        chemin.append(nom(som))
        som = pred[som]
    chemin.append(arret_dep)
    chemin.reverse()

    # ~~~~~~~~~~~~~~~~~~~~~~~ Commandes graphiques ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
    # ~~~~~~~~~~~~~~~~~~~~~~~~~ Affichage de la distance ~~~~~~~~~~~~~~~~~~~~~~~~~ #
    text1 = Text(Point(120,260), str(dist[indice_som(arret_arriv)]) + " m")
    text1.setStyle('normal')
    text1.setTextColor('white')
    # ~~~~~~~~~~~~~~~~~~~~~~~~ Affichage du nombre d'arrêt ~~~~~~~~~~~~~~~~~~~~~~~ #
    text2 = Text(Point(110,280), len(chemin))
    text2.setStyle('normal')
    text2.setTextColor('white')
    text1.draw(win)
    text2.draw(win)
    for i in chemin:
        # ~~~~~~~~~~~~~~ Affichage du nom de l'arrêt courant dans chemin ~~~~~~~~~~~~~ #
        text1 = Text(Point(tab[indice_som(i)][0], tab[indice_som(i)][1]-10), i)
        text1.setStyle('bold')
        text1.setTextColor('white')
        text1.draw(win)
        
        if i != arret_dep:
            # ~~~~~~~~~~~~~~~~~~~~ Affichage du trait entre les arrets ~~~~~~~~~~~~~~~~~~~ #
            Ligne = Line(Point(tab[indice_som(i)][0], tab[indice_som(i)][1]), Point(tab[indice_som(chemin[chemin.index(i)-1])][0], tab[indice_som(chemin[chemin.index(i)-1])][1]))
            Ligne.setFill("red")
            Ligne.draw(win)

        if i != arret_dep and i != arret_arriv:
            # ~~~~~~~~~~~~~~~~~ Affichage des points des arrêts en blanc ~~~~~~~~~~~~~~~~~ #
            c = Circle(Point(tab[indice_som(i)][0], tab[indice_som(i)][1]), 4)
            c.setFill("white")
            c.draw(win)

def saisie_arret(win):
        def show_entry_fields():
                win.delete('all') # On efface tout
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Image de fond ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
                maps = Image(Point(450,420), "maps.png")
                maps.draw(win)
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Texte distance ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
                text1 = Text(Point(60,260), "Distance :")
                text1.setStyle('bold')
                text1.setTextColor('white')
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Texte Nb arrêts ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
                text2 = Text(Point(62,280), "Nb arrêts :")
                text2.setStyle('bold')
                text2.setTextColor('white')
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Dessiner les textes ~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
                text1.draw(win)
                text2.draw(win)

        def test() -> bool:
            """Fonction qui vérifie si le nom de l'arret est correct ou si les saisies sont identiques
            :return : bool
            """
            if saisie_arret.get() not in noms_arrets:
                print("L'arret", saisie_arret.get(), "n'existe pas.")
                return False
            elif saisie_arret_2.get() not in noms_arrets:
                print("L'arret", saisie_arret_2.get(), "n'existe pas.")
                return False
            elif saisie_arret.get() == saisie_arret_2.get():
                print("Les deux arrets sont identiques.")
                return False
            else:
                return True

        def AStar():
            """Fonction qui lance l'algorithme A*
            """
            if test():
                show_entry_fields()
                init(win)
                A_star_Etape3(saisie_arret.get(), saisie_arret_2.get(), win)

        def Warshall():
            """Fonction qui lance l'algorithme de Warshall
            """
            if test():
                show_entry_fields()
                init(win)
                FloydWarshall_Etape3(saisie_arret.get(), saisie_arret_2.get(), win)
        
        def Belmann():
            """Fonction qui lance l'algorithme de Belmann
            """
            if test():
                show_entry_fields()
                init(win)
                Belmann_Etape3(saisie_arret.get(), saisie_arret_2.get(), win)
        
        def Djikstra():
            """Fonction qui lance l'algorithme de Djikstra
            """
            if test():
                show_entry_fields() 
                init(win)
                Djikstra_Etape3(saisie_arret.get(), saisie_arret_2.get(), win)

        def quit():
            win.close()

        # ~~~~~~~~~~~~~~~~~~~~~~ Création d'un fenêtre de saisie ~~~~~~~~~~~~~~~~~~~~~ #
        master = tk.Tk()
        master.title("Saisie des arrêts")
        # ~~~~~~~~~~~~~~~~~~~~~~ Textes de la fenêtre secondaire ~~~~~~~~~~~~~~~~~~~~~ #
        tk.Label(master, 
                text="Arrêt Départ").grid(row=0)
        tk.Label(master, 
                text="Arrêt Arrivée").grid(row=1)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
        #                         Création des champs de saisie                        #
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
        # ~~~~~~~~~~~~~~~~~~~~~ Liste déroulante arrêt de départ ~~~~~~~~~~~~~~~~~~~~~ #
        n = tk.StringVar() 
        saisie_arret = ttk.Combobox(master, width = 15, textvariable = n) 
        arrets = sorted(noms_arrets,reverse=False)
        saisie_arret['values'] = arrets
        saisie_arret.grid(column = 1, row = 0) 
        saisie_arret.current() 

        # ~~~~~~~~~~~~~~~~~~~~~ Liste déroulante arrêt d'arrivée ~~~~~~~~~~~~~~~~~~~~~ #
        n = tk.StringVar() 
        saisie_arret_2 = ttk.Combobox(master, width = 15, textvariable = n) 
        saisie_arret_2['values'] = arrets
        saisie_arret_2.grid(column = 1, row = 1) 
        saisie_arret_2.current() 
        
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Bouton A* ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
        tk.Button(master, 
                text='A*', command=AStar, width=8).grid(row=3, column=0, sticky=tk.W, pady=4)
        
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Bouton Djikstra ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
        tk.Button(master, 
                text='Djikstra', command=Djikstra, width=8).grid(row=3, column=1, sticky=tk.W, pady=4)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Bouton Warshall ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
        tk.Button(master, 
                text='Warshall', command=Warshall, width=8).grid(row=4, column=0, sticky=tk.W, pady=4)
        
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Bouton Belmann ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
        tk.Button(master, 
                text='Belmann', command=Belmann, width=8).grid(row=4, column=1, sticky=tk.W, pady=4)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Bouton Quitter ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
        tk.Button(master, 
                text='Quitter', 
                command=quit).grid(row=5, 
                                        column=0, 
                                        sticky=tk.W, 
                                        pady=4)

def main():
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~ Création de la fenêtre ~~~~~~~~~~~~~~~~~~~~~~~~~~ #
    win = GraphWin("Plan Chronoplus", 900, 900, autoflush=False)
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Image de fond ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
    maps = Image(Point(450,420), "maps.png")
    # ~~~~~~~~~~~~~~~~~~~~~~~ Affichage de l'image de fond ~~~~~~~~~~~~~~~~~~~~~~~ #
    maps.draw(win)
    # ~~~~~~~~~~~~~~~~~~~~~~~~~ Appel fonction principale ~~~~~~~~~~~~~~~~~~~~~~~~ #
    saisie_arret(win)
    # ~~~~~~~~~~~~~~~~ Attente clic souris sur écran pour quitter ~~~~~~~~~~~~~~~~ #
    win.getMouse()
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~ Fermeture de la fenêtre ~~~~~~~~~~~~~~~~~~~~~~~~~ #
    win.close()

main()