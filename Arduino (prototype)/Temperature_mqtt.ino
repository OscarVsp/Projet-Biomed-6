// Partie du code "lecture du capteur de température" issue du site http://jakemakes.eu/esp32-arduino-ds18b20-temperature-sensor/ visité pour la dernière fois le 12/12/2018.
// Nécessite les library "OneWire" et "DallasTemperature" disponible via le lien ci-dessus.
// Partie du code pour l'envoie des données et l'affichage sur l'écran OLED directement tirées des exemples fournit avec la librairie "WifiLora".
// Utilisé pour tester le capteur de température en envoyant les données via MQTT (nécessite que le microcontrôleur soit connecté à internet).

#include <WifiLora.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#include <SSD1306.h>

#define ONE_WIRE_BUS 16

OneWire oneWire(ONE_WIRE_BUS);

DallasTemperature sensors(&oneWire);

SSD1306 display(0x3c, 4, 15);

//Lora/mqtt message 
TxMsg prev; //previous message from the WifiLora lib
unsigned long lastsent=0; //timestamp of the last message sent
unsigned long interval=10000; //interval period between messages (in ms)

//Update the OLED display
void update_display() {
    display.clear();
    display.drawString(0,0,String("Lora Node ")+String(WifiLora.getAddress()));  
    if (!WifiLora.isEnableWifi())
      display.drawString(0,10,String("Wifi is disabled "));
    else {
      if (WifiLora.isClientWifi()) {
        display.drawString(0,10,String("Wifi client: ")+IP2Str(WiFi.localIP()));
      }
      else {
        display.drawString(0,10,String("Wifi AP: ")+IP2Str(WiFi.softAPIP()));
      }
    }
    if (prev.state>2) {
      display.drawString(0,20,String("Msg: ")+prev.msg.substring(0,40));
      display.drawString(0,30,(prev.loramode?String("Sent by lora ")+(prev.state==4?String(" ack ")+String(prev.ackRSSI):String("not ack")):String("Sent by mqtt ("+String(prev.mqttnb))+String(")")));
      display.drawString(0,40,String("Lora stats: ")+String(prev.loranbok)+"/"+String(prev.loranb));
    }
    display.display();
}

//setup the different components
void setup() {
  // put your setup code here, to run once:
  
  Serial.begin(9600);
  Serial.println("Dallas Temperature IC Control Library Demo");
  sensors.begin();

  
  WifiLora.start();      
  //Reset pin for display !
  pinMode(16,OUTPUT);
  digitalWrite(16, LOW);    // set GPIO16 low to reset OLED
  delay(50); 
  digitalWrite(16, HIGH); // while OLED is running, must set GPIO16 in high、 
  display.init();
  display.clear();
  display.flipScreenVertically(); 
  display.setTextAlignment(TEXT_ALIGN_LEFT); 
  display.setFont(ArialMT_Plain_10);  
  update_display();     
}

//main loop
void loop() {  
  //Message to send
  if (millis()-lastsent>interval) { //read temperature every 10sec and send it 
    lastsent=millis();
    Serial.print("Requesting temperatures...");
    sensors.requestTemperatures();
    Serial.println("DONE");
    Serial.print("Temperature for the device 1 (index 0) is: ");
    String Temp = sensner.getTempCByIndex(0);
    Serial.println(Temp);
    String str = "T = "+Temp;
    lastsent=millis();
    prev=WifiLora.getTx(); //get informations about the previous message sent
    update_display();                    
    if (WifiLora.send(str)) Serial.println(String("Send message : ")+str);      
  }   
}
