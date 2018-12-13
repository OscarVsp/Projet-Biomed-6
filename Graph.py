"""
Code par le groupe n°6 dans le cadre du projet BIOMEDICAL de BA2-IRCI à l'ULB. Année 2018-2019
Référence pour la librarie "matplotlib" : https://matplotlib.org/index.html
Utilisé pour la création de graphes à partir de données contenues dans le document texte "DATA"
"""

import matplotlib.pyplot as plt                                                             #Gère la création des graphiques
import matplotlib.animation as animation                                                    #Gère l'actualisation en temps réel des graphiques

def stat(liste):                                                                     #Fonction qui renvoye la moyenne, le minimum et le maximun de la donnée (liste) sous forme de texte.
    texte = ''
    somme = 0
    for i in liste:
        somme += i
    moyenne=round(somme/len(liste),2)                                                       #Arrondit à 2 chiffres après la virgule.
    texte += '\n'+"Moyenne = "+str(moyenne)+'\n'+"Min = "+str(min(liste))+", Max = "+str(max(liste))
    return texte


def animate(i):                                                                     #Cette fonction crée la fenêtre avec les graphiques des diférents paramètres. 

    nombreDeDonnées = 2                                                                     #Nombre de données eploitées (ne peut pas être supérieur au nombre de données comptenus dans le fichier txt.
    data=import_data(nombreDeDonnées)                                                       #Récupèration via la fct "import_data" d'un matrice dont chaque ligne contient les données d'un paramètre (temp, bpm, ...).
    time = data[0]                                                                          #Créer une liste qui va représenté l'abscisse sur chacun des graph.
  
                                                                                    #Création du graphique de température
    temp=data[1]                                                                            #Stock les données du paramètre température dans la liste "temp".
    ax1.clear()                                                                             #Efface le graphique n°1 précédement tracé.
    ax1.plot(time, temp, 'r-')                                                              #(Re)crée un graphique avec en abscisse, le nombre de données, et en ordonnée la température.
    ax1.grid()                                                                              #Affiche la grille du graphique.
    ax1.axis([0,max(time)+1,min(temp)-1.5,max(temp)+1.5])                                   #Configure les bornes du graph : [(min en y), (max en y), (min en x), (max en x)]
    ax1.set_title('Température'+str(stat(temp)), fontsize=10)                               #Affiche la moyenne, le max et le min, calculé par la fonction "stat".
    ax1.set_ylabel('Température'+'\n'+'en °C', fontsize=10)                                 #Nomme l'ordonné
    ax1.set_xlabel('Temps seconde', fontsize=10)                                            #Nomme l'abscisse
    ax1.set_xticks([20*i for i in range(len(temp)//2)])

    #Ajouter les autres paramètres de la même manière

    plt.savefig('graph.png')                                                            #Enregistre le graphique sous forme d'image en format png

def import_data(nbr):                                                               #Cette fonction permet d'importer les paramètres depuis le fichier "Data.txt".

    données=[]                                                                          #Création de la matrice qui va contenir les données (chaque ligne correspond au données d'un paramètre)                            
    for i in range(nbr):
        données.append([])
        
    file = open('Data.txt','r')                                                         #Ouvre le fichier "Data.txt".
    liste=file.readlines()                                                              #Récupèration des données de "Data.txt" dans une liste dont chaque ligne contient une donnée de chaque paramètre (dans l'ordre).
    file.close()                                                                        #Ferme le fichier "Data.txt" pour éviter d'interférer avec le programme MQTT.


    for line in liste:                                                                  #Lecture de chaque ligne.
        elements=line.split()                                                           #Pour chaque ligne, on va séparer les différentes données.
        for i in range(nbr):                                                            #Lecture de chaque élements
            données[i].append(float(elements[i]))                                       #On stocke chaque donnée dans la ligne de la matrice correspondante (température : ligne 1, BPM : ligne 2, ...).

    return données                                                                      #Renvoie de la matrice ainsi crée.
            


fig = plt.figure("Données en temps réel")                                               #Création de la fenêtre qui va contenir tous les graphes.

ax1 = fig.add_subplot(2,3,1)                                                            #Crée le premier graphe et lui donne la position 1 dans une grille de 2 lignes et 3 colonnes.
#ax2 = fig.add_subplot(2,3,2)                                                            #crée le deuxième graphe et lui donne la position 2 dans une grille de 2 lignes et 3 colonnes.


ani = animation.FuncAnimation(fig,animate,interval=2000)                                #Paramètre l'actualisation de la fenêtre des graphes (contenu,fonction qui contient les différents graphes, interval d'actualisation en ms).

plt.show()                                                                              #Affiche la fenêtre des graphes
