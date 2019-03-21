import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import paho.mqtt.client as mqtt
import time
import math
import smtplib

MQTT_TOPIC, MQTT_SERVER, MQTT_SERVERPORT = "/ULB/BA2/BIOMED6/6", 'broker.hivemq.com', 1883

pas_prec, pas_init, i = 0, 0, 0

radius, lastLat, lastLong, distance = 6371, 0.00000, 00.00000000000000, 0

# se connecter au serveur
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(MQTT_TOPIC)

# recevoir un message
def on_message(client, userdata, msg):
    global step, i, pas_init
    donnee = msg.payload.decode("utf-8","ignore")
    donnee = donnee.split("\n") #P T G A S
    pulsometre(donnee[0])
    temperature(donnee[1])
    gps(donnee[2])
    accelerometre(donnee[3])

    # nombre de pas 
    if i == 0:
        pas_init = float(donnee[4][4:])
        i = 1
    nombre_de_pas = float(donnee[4][4:]) - pas_init
    print("Nombre de pas = " + str(nombre_de_pas))
    
    frequence(float(nombre_de_pas)) # fréquence de pas
    
    if donnee[0] == "Possible chute":
        mail("le coureur est tombe")
    print("\n")

def temperature(donnee):
    # récupère les mesures de la donnée reçue
    val = float(donnee[4:])
    print("Température corporelle = "+str(val) + " °C" )
    tps = time.time()-tstart
    # ajoute les mesures dans une liste pour les porter en graphique
    xdata1.append(tps)
    ydata1.append(val)
    # vérifie le paramètre du coureur et envoie un mail si nécessaire"
    """urgence('T', val)"""
    # place les données dans un fichier pour les sauver
    file=open('DataTemperature.txt','a')
    file.write("t = "+str(tps)+" temp = "+str(val)+'\n')
    file.close()

def accelerometre(donnee):
    # récupère les mesures de la donnée reçue
    val = donnee[4:].split()
    print("Accéléromètre = "+str(val))
    tps = time.time()-tstart
    # vérifie le paramètre du coureur et envoie un mail si nécessaire
    """urgence('A', [float(val[0]), float(val[2])])"""
    # place les données dans un fichier pour les sauver
    file=open('DataAccelerometre.txt','a')
    file.write("t = "+str(tps)+" x = "+str(val[0])+" y = "+str(val[1])+" z = "+str(val[2])+'\n')
    file.close()

def frequence(pas_total):
    global pas_prec
    pas = pas_total - pas_prec
    pas_prec = pas_total
    freq = pas*6
    print("Fréquence de pas = " + str(freq) + " pas/minute")
    tps = time.time() - tstart
    # ajoute les mesures dans une liste pour les porter en graphique
    xdata3.append(tps)
    ydata3.append(freq)
    # place les données dans un fichier pour les sauver
    file=open('DataFrequence.txt','a')
    file.write("t = "+str(tps)+"freq = "+str(freq)+'\n')
    file.close()

def gps(donnees):
    global radius,lastLat,lastLong,distance
    donnees= donnees.split()[2].split(',')
    lat = degMinToDeg(float(donnees[0]))
    long = degMinToDeg(float(donnees[1]))
    vit = float(donnees[2])*1.85
    tps = time.time()-tstart
    # ajoute les mesures dans une liste pour les porter en graphique
    xdata4.append(tps)
    ydata4.append(vit)

    pos=open("position.kml", "w")
    pos.write("""<Placemark>
      <name>LIVE GPS ULB</name>
      <description>Some Descriptive text.</description>
      <Point>
        <coordinates>%s,%s,0</coordinates>
      </Point>
    <longitude> long </longitude>
    <latitude> lat </latitude>   
    </Placemark>""" %(long,lat))

    if (lastLat != 0 and lastLong != 0):
        dist(lat,long)

    lastLat, lastLong = lat, long


    file=open("DataGPS.txt",'a')
    file.write("lat = "+str(lat)+" long = "+str(long)+" vit = "+str(vit)+"\n")
    file.close()

def degMinToDeg(coord):
    inc = int(coord/100)
    otc = coord - (inc)*100
    return(inc + otc/60)

def dist(lat,long):
    global distance
    lat1, lon1 = math.radians(lat), math.radians(long)
    lat2, lon2 = math.radians(lastLat), math.radians(lastLong)
    radius = 6371 # km
    ans = math.cos(lat1) * math.cos(lat2)*math.cos(lon1)*math.cos(lon2) +math.cos(lat1) * math.sin(lon1)\
    * math.cos(lat2) * math.sin(lon2) + math.sin(lat1)*math.sin(lat2)
    c = math.acos(ans)
    d = radius * c
    distance += d


def pulsometre(donnee):
    v = str(donnee[4:]).split()
    val1 = float(v[0][:(len(v[0])-1)])
    val2 = float(v[1])
    val = (val1 + val2)/2
    print("Pulsation = "+str(val) + " batt/min")
    tps = time.time()-tstart
    # ajoute les mesures dans une liste pour les porter en graphique
    xdata2.append(tps)
    ydata2.append(val)
    # vérifie le paramètre du coureur et envoie un mail si nécessaire
    """urgence('P',val)"""
    # place les données dans un fichier pour les sauver
    file=open('DataPuslometre.txt','a')
    file.write("t = "+str(tps)+" puls = "+str(val)+'\n')
    file.close()

def moy(liste):
    if (len(liste) == 0):
        return 0
    else:
        tot = 0
        for elem in liste:
            tot+=elem
        return (tot/len(liste))
        
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
            mail("Probleme! La personne est tombee !")
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
    ax1.set_title('Température corporelle'+'\n'+'Moyenne : '+str(round(moy(ydata1),1))+' °C')
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
    ax2.set_title('Pulsation cardiaque'+'\n'+'Moyenne : '+str(round(moy(ydata2)))+' BPM')
    ax2.set_ylim(0, 150) # /!/ diminuer le maximum avec les vraies valeurs
    ax2.set_xlim(0, 180) 
    del xdata2[:]
    del ydata2[:]
    line2.set_data(xdata2, ydata2)
    return line2,        

#Function execute to animate the matplotlib plot/update data
def run2(data2):
    # update the data
    ax2.set_title('Pulsation cardiaque'+'\n'+'Moyenne : '+str(round(moy(ydata2)))+' BPM')
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

""" graphe 3  : fréquence de pas """

#Function to init the matplotlib plot
def init3():
    ax3.set_title('Fréquence de pas'+'\n'+'Moyenne : '+str(round(moy(ydata3)))+' pas/s | nbr pas : '+str(pas_prec)+' pas')
    ax3.set_ylim(10, 40) # /!/ diminuer le maximum avec les vraies valeurs
    ax3.set_xlim(0, 180) 
    del xdata3[:]
    del ydata3[:]
    line3.set_data(xdata3, ydata3)
    return line3,        

#Function execute to animate the matplotlib plot/update data
def run3(data3):
    # update the data
    ax3.set_title('Fréquence de pas'+'\n'+'Moyenne : '+str(round(moy(ydata3)))+' pas/s | nbr pas : '+str(pas_prec)+' pas')
    if xdata3:
        xmin, xmax = ax3.get_xlim()
        if xdata3[-1]>xmax: #move x axes limit by 1 minute 
            d=60  #move 1minute axes
            ax3.set_xlim(xmin+d,xmax+d)
            while xdata3[0]<xmin+d: #remove old data
                xdata3.pop(0)
                ydata3.pop(0)
        line3.set_data(xdata3, ydata3)    
    return line3,

""" graphe 4 : gps """

#Function to init the matplotlib plot
def init4():
    ax4.set_title('Vitesse'+'\n'+'Vitesse moyenne : '+str(round(moy(ydata4),1))+'km/h | Distance totale : '+str(round(distance,2))+' km')
    ax4.set_ylim(0, 20) # /!/ diminuer le maximum avec les vraies valeurs
    ax4.set_xlim(0, 180)
    del xdata4[:]
    del ydata4[:]
    line4.set_data(xdata4, ydata4)
    return line4,        

#Function execute to animate the matplotlib plot/update data
def run4(data4):
    # update the data
    ax4.set_title('Vitesse'+'\n'+'Vitesse moyenne : '+str(round(moy(ydata4),1))+'km/h | Distance totale : '+str(round(distance,2))+' km')
    if xdata4:
        xmin, xmax = ax4.get_xlim()
        if xdata4[-1]>xmax: #move x axes limit by 1 minute 
            d=60  #move 1minute axes
            ax4.set_xlim(xmin+d,xmax+d)
            while xdata4[0]<xmin+d: #remove old data
                xdata4.pop(0)
                ydata4.pop(0)
        line4.set_data(xdata4, ydata4)    
    return line4,


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

# graphe fréquence de de pas
fig3, ax3 = plt.subplots() #créer une figure (fig) et des axes (ax)
line3, = ax3.plot([], [], lw=2)
ax3.grid()
xdata3 = []
ydata3 = []
plt.title('Fréquence de pas')
plt.xlabel('Temps (s)')
plt.ylabel('Fréquence de pas (nombre de pas/min)')
#matplotlib animation update every second (1000ms)
ani3 = animation.FuncAnimation(fig3, run3, interval=1000,
                              repeat=True, init_func=init3)

# graphe gps
fig4, ax4 = plt.subplots() #créer une figure (fig) et des axes (ax)
line4, = ax4.plot([], [], lw=2)
ax4.grid()
xdata4 = []
ydata4 = []
plt.title('Vitesse'+'\n'+'(Distance totale parcourue : 0 km)')
plt.xlabel('Temps (s)')
plt.ylabel(r'Vitesse (km/h)')
#matplotlib animation update every second (1000ms)
ani4 = animation.FuncAnimation(fig4, run4, interval=1000,
                              repeat=True, init_func=init4)

client.loop_start()                              
plt.show()
