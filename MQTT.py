"""
Code par le groupe n°6 dans le cadre du projet BIOMEDICAL de BA2-IRCI à l'ULB. Année 2018-2019
Référence pour la librarie "Paho.mqtt" : https://pypi.org/project/paho-mqtt/
Utilisé pour la réccupèration de données via un serveur MQTT
"""

import paho.mqtt.client as mqtt                                     #Inclure la librarie Paho.mqtt

open('Data.txt','w').close()                                        #Efface les données contenu dans le fichier "DATA.txt".

def on_connect(client, obj, flags, rc):                             #Exectutée lors de la connection au serveur.
    print("rc: "+str(rc))                                           #RC est le résultat de la connection (=0 : connecté,!= 0 : non connecté)

def on_message(client, obj, msg):                                   #Executée lors de la réception d'un msg.
    donnée = msg.payload.decode("utf-8","ignore")                   #MSG contient les données liés au msg, dont le msg en lui même. Ce dernier est stocker dans "donnée". 
    print(msg.topic+" "+str(données))                               #Afficher le sujet et le contenu du msg.
    file=open('Data.txt','a')                                       #Ajoute le msg dans le fichier "temp.txt".
    file.write(données[1:]+'\n')
    file.close()

def on_subscribe(client, obj, mid, granted_qos):                    #Executée lors de l'abonnement à un Topic.
    print("Subscribed: "+str(granted_qos))                          #Indique la QoS définie pour l'abonnement.

 
client = mqtt.Client()                                              #Renome la fonction "mqtt.Client()" en "client" pour plus de lisibilité.

client.on_connect = on_connect                                      #Lors de la connection au serveur, execute la fonction "on_connect()".
client.on_subscribe = on_subscribe                                  #Lors de l'abonnement à un topic, execute la fonction "on_subscribe()".
client.on_message = on_message                                      #Lors de la reception d'un msg, execute la fonction "on_message()".

client.connect("broker.hivemq.com")                                 #Se connect au serveur.
client.subscribe("/ULB/BA2/BIOMED6/6",qos=1)                        #S'abonne au sujet.

client.loop_forever()                                               #Reste en attente d'un msg pour toujours.
