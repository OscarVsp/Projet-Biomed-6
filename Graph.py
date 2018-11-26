"""
Code par Oscar Van Slijpe
22/11/2018
Référence pour la librarie "matplotlib" : https://matplotlib.org/index.html
"""

import matplotlib.pyplot as plt                                             #Gère la création des graphiques
import matplotlib.animation as animation                                    #Gère l'actualisation en temps réel des graphiques


def animate(i):                                                             #Cette fonction crée la fenêtre avec les graphiques des diférents paramètres. 

    nombreDeDonnées = 2                                                     #Nombre de données eploitées (ne peut pas être supérieur au nombre de données comptenus dans le fichier txt.
    data=import_data(nombreDeDonnées)                                       #Récupèration via la fct "import_data" d'un matrice dont chaque ligne contient les données d'un paramètre (temp, bpm, ...).
    nbr = [i+1 for i in range(len(data[0]))]                                #Créer une liste qui va représenté l'abscisse sur chacun des graph.

                                                                            #Création du graphique de température
    temp=data[0]                                                                #Stock les données du paramètre température dans la liste "temp".
    ax1.clear()                                                                 #Efface le graphique n°1 précédement tracé.
    ax1.plot(nbr, temp)                                                         #(Re)crée un graphique avec en abscisse, le nombre de données, et en ordonnée la température.
    ax1.axis([1,int(len(temp))+1,min(temp)-2,max(temp)+2])                      #Configure les bornes du graph : [(min en y), (max en y), (min en x), (max en x)]
    ax1.set_title('Température'+'\n'+'Moyenne = '+str(moy(temp)))               #Affichage d'un titre et de la moyenne au dessus du graphique (moyenne obtenu grâce à la fonction "moy").
    ax1.set_ylabel('°C')                                                        #Nomme l'ordonné
    ax1.set_xlabel('Temps')                                                     #Nomme l'abscisse

    bpm=data[1]                                                             #Idem que précédement mais avec le paramètre BPM.
    ax2.clear()
    ax2.plot(nbr, bpm)
    ax2.axis([1,int(len(bpm))+1,min(bpm)-1,max(bpm)+1])
    ax2.set_title('BPM'+'\n'+'Moyenne = '+str(moy(bpm)))
    ax2.set_ylabel('/seconde')
    ax2.set_xlabel('Temps')

    #Ajouter les autres paramètres

def import_data(nbr):                                                       #Cette fonction permet d'importer les paramètres depuis le fichier "Data.txt".

    données=[]                                                                  #Création de la matrice qui va contenir les données (chaque ligne correspond au données d'un paramètre)                            
    for i in range(nbr):
        données.append([])
        
    file = open('Data.txt','r')                                                 #Ouvre le fichier "Data.txt".
    liste=file.readlines()                                                      #Récupèration des données de "Data.txt" dans une liste dont chaque ligne contient une donnée de chaque paramètre (dans l'ordre).
    file.close()                                                                #Ferme le fichier "Data.txt" pour éviter d'interférer avec le programme MQTT.

    for line in liste:                                                          #Lecture de chaque ligne.
        elements=line.split()                                                   #Pour chaque ligne, on va séparer les différentes données.
        for i in range(nbr):                                                    #Lecture de chaque élements
            données[i].append(float(elements[i]))                               #On stocke chaque donnée dans la ligne de la matrice correspondante (température : ligne 1, BPM : ligne 2, ...).

    return données                                                              #Renvoie de la matrice ainsi crée.
            

def moy(liste):                                                             #Fonction qui renvoye la moyenne des valeurs contenu dans la liste donnée.
    
    somme=0
    for i in liste:
        somme+=i
    moyenne=round(somme/len(liste),2)                                           #Arrondit à 2 chiffres après la virgule.
    
    return moyenne


fig = plt.figure("Données en temps réel")                                   #Création de la fenêtre qui va contenir tous les graphes.

ax1 = fig.add_subplot(2,3,1)                                                #Crée le premier graphe et lui donne la position 1 dans une grille de 2 lignes et 3 colonnes.
ax2 = fig.add_subplot(2,3,2)                                                #crée le deuxième graphe et lui donne la position 2 dans une grille de 2 lignes et 3 colonnes.
#ax3 = fig.add_subplot(2,3,3)
#ax4 = fig.add_subplot(2,3,4)
#ax5 = fig.add_subplot(2,3,5)

ani = animation.FuncAnimation(fig,animate,interval=2000)                    #Paramètre l'actualisation de la fenêtre des graphes (contenu,fonction qui contient les différents graphes, interval d'actualisation en ms).

plt.show()                                                                  #Affiche la fenêtre des graphes
