import time
import math

boolean = True
while boolean == True:
    with open('info.txt', "r") as ins:
        array = []
        for line in ins:
            array.append(line)


    newArray = []
    for elem in array:
        """elem = elem.replace(',' , '', 6)
        elem = elem.replace(elem[20:26], '')"""
        if elem !='\n':
            newArray.append(elem.split(','))
        #newArray[newArray.index(elem)] = newArray[newArray.index(elem)].split(',')

    #del newArray[-1]
    
    gpslat = []
    gpslong = []
    """gpsdirection = []"""
    for elem in newArray:
        gpslat.append(elem[0])
        gpslong.append(elem[1])
    """for elem in newArray:
        gpsdirection.append(elem[2])"""


    for elem in gpslat:
        newEleminc = int(float(elem)/100)
        newElemnotc = float(elem) - (newEleminc)*100
        newElem = newEleminc + newElemnotc /60
        gpslat[gpslat.index(elem)] = newElem
        x = gpslat.index(newElem)
        """if gpsdirection[x] == 'N\n':
            gpslat[x] = -(newElem)"""

    for elem in gpslong:
        newEleminc = int(float(elem)/100)
        newElemnotc = float(elem) - (newEleminc)*100
        newElem = newEleminc + newElemnotc /60
        gpslong[gpslong.index(elem)] = newElem
        x = gpslong.index(newElem)
        """if gpsdirection[x] == 'N\n':
            gpslong[x] = -(newElem)"""
    
    with open("position.kml", "w") as pos:
        pos.write("""<Placemark>
      <name>LIVE GPS ULB</name>
      <description>Some Descriptive text.</description>
      <Point>
        <coordinates>%s,%s,0</coordinates>
      </Point>
      <gx:ViewerOptions>
    <gx:option name="streetview" enabled=boolean />   
      </gx:ViewerOptions>
    <lookAt>
    <longitude> gpslong[len(gpslong)-1 </longitude>
    <latitude> gpslat[len(gpslat)-1 </latitude>   
    </Placemark>""" %(gpslat[len(gpslat)-1],gpslong[len(gpslong)-1]))

    print(gpslat[len(gpslat)-1], gpslong[len(gpslong)-1]) 

    lat1, lon1 = gpslat[len(gpslat)-1], gpslong[len(gpslong)-1]
    lat2, lon2 = gpslat[len(gpslat)-2] ,gpslong[len(gpslong)-2]

    x = (lat1, lon1)
    y = (lat2, lon2)
    print(x,y)
    radius = 6371 # km

    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c
    print(d)

    time.sleep(2)
