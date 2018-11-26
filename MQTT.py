"""
Code par Oscar Van Slijpe
22/11/2018
Référence pour la librarie "Paho.mqtt" : https://pypi.org/project/paho-mqtt/
"""

import paho.mqtt.client as mqtt                                     #inclure la librarie Paho.mqtt

open('Data.txt','w').close()                                        #Efface les données contenu dans le fichier "temp.txt".

def on_connect(client, obj, flags, rc):                             #Exectuté lors de la connection au serveur.
    print("rc: "+str(rc))                                           #RC est le résultat de la connection (=0 : connecté,!= 0 : non connecté)

def on_message(client, obj, msg):                                   #Executé lors de la réception d'un msg.
    donnée = msg.payload.decode("utf-8","ignore")                   #MSG contient les données liés au msg, dont le msg en lui même. Ce dernier est stocker dans "donnée". 
    print(msg.topic+" "+str(données))                               #Afficher le topic et le contenu du msg.
    file=open('Data.txt','a')                                       #Ajoute le msg dans le fichier "temp.txt".
    file.write(données[1:]+'\n')
    file.close()
    
def on_publish(client, obj, mid):                                   #Executé lors de la publication d'un msg.
    print("mid: "+str(mid))                                         #MID est l'ID du msg. Peut être utilisé pour avoir un suivit de celui-ci.

def on_subscribe(client, obj, mid, granted_qos):                    #Executé lors de l'abonnement à un Topic.
    print("Subscribed: "+str(granted_qos))                          #Granted_qos est un indicateur de la qualité du du service fournit par le serveur.

 
client = mqtt.Client()                                              #Renome la fonction "mqtt.Client()" en "client" pour plus de lisibilité.

client.on_connect = on_connect                                      #Lors de la connection au serveur, execute la fonction "on_connect()".
client.on_subscribe = on_subscribe                                  #Lors de l'abonnement à un topic, execute la fonction "on_subscribe()".
client.on_message = on_message                                      #Lors de la reception d'un msg, execute la fonction "on_message()".
client.on_publish = on_publish                                      #Lors de la publication d'un msg, execute la fonction "on_publish()".

client.connect("broker.hivemq.com")                                 #Se connect au serveur.
client.subscribe("/ULB/BA2/BIOMED6/6")                              #S'abonne au topic.

client.loop_forever()                                               #Reste en attente d'un msg pour toujours.
