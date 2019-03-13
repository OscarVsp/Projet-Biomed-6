import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import paho.mqtt.client as mqtt
import time
import smtplib

MQTT_TOPIC = "/ULB/BA2/BIOMED6/6" 
MQTT_SERVER = 'broker.hivemq.com'
MQTT_SERVERPORT = 1883

pas_prec = 0

# se connecter au serveur
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(MQTT_TOPIC)

# recevoir un message
def on_message(client, userdata, msg):
    global step
    donnee = msg.payload.decode("utf-8","ignore")
    donnee = donnee.split("\n") #P T G A S
    print(donnee)
    pulsometre(donnee[0])
    temperature(donnee[1])
    gps(donnee[2])
    accelerometre(donnee[3])
    print(donnee[4]) # nombre de pas
    print(frequence(float(donnee[4][4:]))) # fréquence
    if donnee[0] == "Possible chute":
        mail("le coureur est tombe")

def temperature(donnee):
    # récupère les mesures de la donnée reçue
    val = float(donnee[4:])
    print("temp = "+str(val))
    tps = time.time()-tstart
    # ajoute les mesures dans une liste pour les porter en graphique
    xdata1.append(tps)
    ydata1.append(val)
    # vérifie le paramètre du coureur et envoie un mail si nécessaire"
    urgence('T', val)
    # place les données dans un fichier pour les sauver
    file=open('DataTemperature.txt','a')
    file.write("t = "+str(tps)+" temp = "+str(val)+'\n')
    file.close()

def accelerometre(donnee):
    # récupère les mesures de la donnée reçue
    val = donnee[4:].split()
    print("acc = "+str(val))
    tps = time.time()-tstart
    # vérifie le paramètre du coureur et envoie un mail si nécessaire
    urgence('A', [float(val[0]), float(val[2])])
    # place les données dans un fichier pour les sauver
    file=open('DataAccelerometre.txt','a')
    file.write("t = "+str(tps)+" x = "+str(val[0])+" y = "+str(val[1])+" z = "+str(val[2])+'\n')
    file.close()

def frequence(pas_total):
    print('ok1')
    global pas_prec
    pas = pas_total - pas_prec
    pas_prec = pas_total
    freq = pas*6
    return freq

def pulsometre(donnee):
    v = str(donnee[4:]).split()
    val1 = float(v[0][:(len(v[0])-1)])
    val2 = float(v[1])
    val = (val1 + val2)/2
    print("puls = "+str(val))
    tps = time.time()-tstart
    # ajoute les mesures dans une liste pour les porter en graphique
    xdata2.append(tps)
    ydata2.append(val)
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
        if  valeur[0] >= 15000 or valeur[1] >= 15000: #valeurs à verifier
            print("Problème! La personne est tombée !")
            #mail("Probleme! La personne est tombee !")
    # si le paramètre est la pulsation
    elif parametre == 'P':
        if valeur > 200 or valeur < 50 : # en considérant une personne normale de 20 ans
            print("Problème! Pulsation cardiaque " + str(valeur))
            mail("Probleme! Pulsation cardiaque de " + str(valeur))

def mail(message):
    mail = smtplib.SMTP('smtp.gmail.com',587)
    mail.ehlo()
    mail.starttls()
    mail.login('biomedgroupe6@gmail.com','biomed6ba1')
    mail.sendmail('biomedgroupe6@gmail.com', 'louisedewouters@gmail.com', message)
    mail.close()
    print("mail envoyé")

# TRACER LE GRAPHIQUE

""" graphe 1  : temperature """

#Function to init the matplotlib plot
def init1():
    ax1.set_ylim(10, 40) # /!/ diminuer le maximum avec les vraies valeurs
    ax1.set_xlim(0, 180) 
    del xdata1[:]
    del ydata1[:]
    line1.set_data(xdata1, ydata1)
    return line1,        

#Function execute to animate the matplotlib plot/update data
def run1(data1):
    # update the data
    if xdata1:
        xmin, xmax = ax1.get_xlim()
        if xdata1[-1]>xmax: #move x axes limit by 1 minute 
            d=60  #move 1minute axes
            ax1.set_xlim(xmin+d,xmax+d)
            while xdata1[0]<xmin+d: #remove old data
                xdata1.pop(0)
                ydata1.pop(0)
        line1.set_data(xdata1, ydata1)    
    return line1,          

""" graphe 2 : pulsation """

#Function to init the matplotlib plot
def init2():
    ax2.set_ylim(0, 150) # /!/ diminuer le maximum avec les vraies valeurs
    ax2.set_xlim(0, 180) 
    del xdata2[:]
    del ydata2[:]
    line2.set_data(xdata2, ydata2)
    return line2,        

#Function execute to animate the matplotlib plot/update data
def run2(data2):
    # update the data
    if xdata2:
        xmin, xmax = ax2.get_xlim()
        if xdata2[-1]>xmax: #move x axes limit by 1 minute 
            d=60  #move 1minute axes
            ax2.set_xlim(xmin+d,xmax+d)
            while xdata2[0]<xmin+d: #remove old data
                xdata2.pop(0)
                ydata2.pop(0)
        line2.set_data(xdata2, ydata2)    
    return line2,      


tstart=time.time()  #application time start 
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_SERVER, MQTT_SERVERPORT, 60)

# graphe température
fig1, ax1 = plt.subplots() #créer une figure (fig) et des axes (ax)
line1, = ax1.plot([], [], lw=2)
ax1.grid()
xdata1 = []
ydata1 = []
plt.title('Température corporelle')
plt.xlabel('Temps (s)')
plt.ylabel(r'Temperature ($^\circ$ C)')
#matplotlib animation update every second (1000ms)
ani1 = animation.FuncAnimation(fig1, run1, interval=1000,
                              repeat=True, init_func=init1)


# graphe pulsation
fig2, ax2 = plt.subplots() #créer une figure (fig) et des axes (ax)
line2, = ax2.plot([], [], lw=2)
ax2.grid()
xdata2 = []
ydata2 = []
plt.title('Pulsation cardiaque')
plt.xlabel('Temps (s)')
plt.ylabel(r'Pulsation cardiaque (batt/min)')
#matplotlib animation update every second (1000ms)
ani2 = animation.FuncAnimation(fig2, run2, interval=1000,
                              repeat=True, init_func=init2)


client.loop_start()                              
plt.show()
