import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import paho.mqtt.client as mqtt
import time
import smtplib

MQTT_TOPIC = "/ULB/BA2/BIOMED6/6" 
MQTT_SERVER = 'broker.hivemq.com'
MQTT_SERVERPORT = 1883

# se connecter au serveur
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(MQTT_TOPIC)

# recevoir un message
def on_message(client, userdata, msg):
    donnee = msg.payload.decode("utf-8","ignore")
    if donnee[0] == 'T':
        temperature(donnee)
    elif donnee[0] == "A":
        accelerometre(donnee)
    elif donnee[0] == "P":
        pulsometre(donnee)

def temperature(donnee):
    # récupère les mesures de la donnée reçue
    val = float(donnee[4:])
    print("temp = "+str(val))
    tps = time.time()-tstart
    # ajoute les mesures dans une liste pour les porter en graphique
    xdata.append(tps)
    ydata.append(val)
    # vérifie le paramètre du coureur et envoie un mail si nécessaire"
    urgence('T', val)
    # place les données dans un fichier pour les sauver
    file=open('DataTemperature.txt','a')
    file.write("t = "+str(tps)+"temp = "+str(val)+'\n')
    file.close()

def accelerometre(donnee):
    # récupère les mesures de la donnée reçue
    valx = float(donnee[4:5])
    valy = float(donnee[6:7])
    valz = float(donnee[8:9])
    val = [valx,valy,valz]
    print("acc = "+str(val))
    tps = time.time()-tstart
    # vérifie le paramètre du coureur et envoie un mail si nécessaire
    urgence('A', val)
    # place les données dans un fichier pour les sauver
    file=open('DataAccelerometre.txt','a')
    file.write("t = "+str(tps)+" x = "+str(valx)+" y = "+str(valy)+" z = "+str(valz)+'\n')
    file.close()

def pulsometre(donnee):
    v = str(donnee[4:]).split()
    val1 = float(v[0][:(len(v[0])-1)])
    val2 = float(v[1])
    val = (val1 + val2)/2
    print("puls = "+str(val))
    tps = time.time()-tstart
    # ajoute les mesures dans une liste pour les porter en graphique
    xdata.append(tps)
    ydata.append(val)
    # vérifie le paramètre du coureur et envoie un mail si nécessaire
    urgence('P',val)
    # place les données dans un fichier pour les sauver
    file=open('DataPuslometre.txt','a')
    file.write("t = "+str(tps)+" puls = "+str(val)+'\n')
    file.close()
        
# MESSAGE D'URGENCE

def urgence(parametre, valeur):
    # si le paramètre est la température
    if parametre == 'T':
        if valeur >= 40 or valeur <= 35.5 : #valeurs à vérifier
            print("Problème! Température de " + str(valeur))
            mail("Probleme! Temperature de " + str(valeur))
    # si le paramètre est l'accélération
    elif parametre == 'A':
        if valeur[0] == 0 and valeur[1] == 0 and valeur[2] == 0: #valeurs à verifier
            print("Problème! Plus d'activité detectée !")
            #mail("Probleme! Plus d'activite detectee !")
    # si le paramètre est l'accélération
    elif parametre == 'P':
        if valeur > 200 or valeur < 20 : # en considérant une personne normale de 20 ans
            print("Problème! Pulsation cardiaque " + str(valeur))
            #mail("Probleme! Pulsation cardiaque de " + str(valeur))

def mail(message):
    mail = smtplib.SMTP('smtp.gmail.com',587)
    mail.ehlo()
    mail.starttls()
    mail.login('biomedgroupe6@gmail.com','biomed6ba1')
    mail.sendmail('biomedgroupe6@gmail.com', 'louisedewouters@gmail.com', message)
    mail.close()
    print("mail envoyé")

# TRACER LE GRAPHIQUE

#Function to init the matplotlib plot
def init():
    ax.set_ylim(0, 150) # /!/ diminuer le maximum avec les vraies valeurs
    ax.set_xlim(0, 180) 
    del xdata[:]
    del ydata[:]
    line.set_data(xdata, ydata)
    return line,        

#Function execute to animate the matplotlib plot/update data
def run(data):
    # update the data
    if xdata:
        xmin, xmax = ax.get_xlim()
        if xdata[-1]>xmax: #move x axes limit by 1 minute 
            d=60  #move 1minute axes
            ax.set_xlim(xmin+d,xmax+d)
            while xdata[0]<xmin+d: #remove old data
                xdata.pop(0)
                ydata.pop(0)
        line.set_data(xdata, ydata)    
    return line,          

tstart=time.time()  #application time start 
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_SERVER, MQTT_SERVERPORT, 60)

# graphe température
fig, ax = plt.subplots() #créer une figure (fig) et des axes (ax)
line, = ax.plot([], [], lw=2)
ax.grid()
xdata = []
ydata = []
plt.title('Température corporelle')
plt.xlabel('Temps (s)')
plt.ylabel(r'Temperature ($^\circ$ C)')
#matplotlib animation update every second (1000ms)
ani = animation.FuncAnimation(fig, run, interval=1000,
                              repeat=True, init_func=init)
"""

# graphe pulsation
fig, ax = plt.subplots() #créer une figure (fig) et des axes (ax)
line, = ax.plot([], [], lw=2)
ax.grid()
xdata = []
ydata = []
plt.title('Pulsation cardiaque')
plt.xlabel('Temps (s)')
plt.ylabel(r'Pulsation cardiaque (batt/min)')
#matplotlib animation update every second (1000ms)
ani = animation.FuncAnimation(fig, run, interval=1000,
                              repeat=True, init_func=init)

"""
client.loop_start()                              
plt.show()


