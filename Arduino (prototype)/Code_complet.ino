#include <WifiLora.h>
unsigned long lastsent = 0;
unsigned long interval = 5000;
unsigned long lastsentacc = 0;
unsigned long intervalacc = 100;
float previous_y = -20000;
float stp = 0;


// ACCELEROMETRE library
#include "I2Cdev.h"
#include "MPU6050.h"


// PULSATION library
#include <Wire.h>
#include <BH1790GLC.h>
#include <stdio.h>

// TEMPERATURE library
#include <OneWire.h>
#include <DallasTemperature.h>
#include <SSD1306.h>

// ACCELEROMETRE 
MPU6050 accelgyro;
int16_t ax, ay, az;
int16_t gx, gy, gz;
#define OUTPUT_READABLE_ACCELGYRO
#define LED_PIN 13

//SPIFFS
#include <SPIFFS.h>

// PULSATION
BH1790GLC bh1790glc;
char str[100];

// TEMPERATURE
#define ONE_WIRE_BUS 16 // à changer to 17
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);
String Temp;

//GPS
#define RX1PIN 35
#define TX1PIN 13
HardwareSerial GPSserial(1);
String gps_data[4] = {"A","000","000","000"};

// display
SSD1306 display(0x3c, 4, 15);

//Lora/mqtt message 
TxMsg prev; //previous message from the WifiLora lib

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
      display.drawString(0,20,String("T=")+Temp+String(" | P=")+str);
      display.drawString(0,30,String("A=")+stp+String(" | G=")+gps_data[1]+","+gps_data[2]+","+gps_data[3]);
      display.drawString(0,40,(prev.loramode?String("Sent by lora ")+(prev.state==4?String(" ack ")+String(prev.ackRSSI):String("not ack")):String("Sent by mqtt ("+String(prev.mqttnb))+String(")")));
      display.drawString(0,50,String("Lora stats: ")+String(prev.loranbok)+"/"+String(prev.loranb));
    }
    display.display();
}

void begin_display(){
    //Reset pin for display !
    pinMode(16,OUTPUT);
    digitalWrite(16, LOW);    // set GPIO16 low to reset OLED
    delay(50); 
    digitalWrite(16, HIGH); // while OLED is running, must set GPIO16 in high、 
    display.init();
    display.clear();
    display.flipScreenVertically(); 
    display.setTextAlignment(TEXT_ALIGN_CENTER); 
    display.setFont(ArialMT_Plain_16);
    display.drawString(64,0,String("Projet Biomed"));
    display.drawString(64,15,String("2018 - 2019"));
    display.drawString(64,30,String("Groupe n°6"));
    display.drawString(64,45,String("Prototype final"));
    display.display();
}

void setup() {

    begin_display();
    delay(1500);
    

    Serial.begin(115200);
    WifiLora.start();
    Serial.println("WifiLora Started");
  
    // ACCELEROMETRE setup 115200 
    Wire.begin(21,22);
    accelgyro.initialize();
    Serial.println(accelgyro.testConnection() ? "Acc ok" : "Acc pas ok");

    display.clear();
    display.setTextAlignment(TEXT_ALIGN_LEFT); 
    display.setFont(ArialMT_Plain_10);
    display.drawString(0,0,String("Projet biomed groupe 6"));
    display.drawString(0,20,String("Démarrage des capteurs..."));
    display.drawString(0,30,(accelgyro.testConnection()?String("Acc ok"):String("Acc pas ok")));
    display.display();

    // PULSOMETRE setup 921600
    byte rc; 
    while (!Serial);
    Wire.setClock(400000L);  
    rc = bh1790glc.init();
    if (rc != 0) {
      Serial.println("Puls pas ok");
      }   
    else {
      Serial.println("Puls ok");
      }

    display.clear();
    display.drawString(0,0,String("Projet biomed groupe 6"));
    display.drawString(0,20,String("Démarrage des capteurs..."));
    display.drawString(0,30,(accelgyro.testConnection()?String("Acc ok | "):String("Acc pas ok | "))+(rc==0?String("Puls ok"):String("Puls pas ok")));
    display.display();

    // TEMPERATURE
    sensors.begin();
  
    //GPS
    GPSserial.begin(9600,SERIAL_8N1,RX1PIN,TX1PIN);
  
    //SPIFFS
    SPIFFS.begin();
    File f = SPIFFS.open("/Accelerometre.txt","w");
    f.close();
    f = SPIFFS.open("/Pulsometre.txt","w");
    f.close();
    f = SPIFFS.open("/GPS.txt","w");
    f.close();
    f = SPIFFS.open("/Temperature.txt","w");
    f.close();

    display.clear();
    display.drawString(0,0,String("Projet biomed groupe 6"));
    display.drawString(0,20,String("Démarrage des capteurs..."));
    display.drawString(0,30,(accelgyro.testConnection()?String("Acc ok | "):String("Acc pas ok | "))+(rc==0?String("Puls ok"):String("Puls pas ok")));
    display.drawString(0,40,String("Temp ok | GPS ok"));
    display.display();
    delay(1000);

    display.clear();
    display.setTextAlignment(TEXT_ALIGN_CENTER); 
    display.setFont(ArialMT_Plain_16);
    display.drawString(64,15,String("Prototype prêt"));
    display.drawString(64,33,String("Bonne course !"));
    display.display();
    delay(2000);


    display.clear();
    display.setTextAlignment(TEXT_ALIGN_LEFT); 
    display.setFont(ArialMT_Plain_10);   
    update_display();
}

void loop() {

  // on envoie les données de l'accéléromètre séparemment du reste
  
  if (millis()-lastsentacc > intervalacc) {
    lastsentacc= millis();
    accelerometre();
    stepcalculator();
    chute();
  }

  if (millis()-lastsent > interval) {
    
    lastsent= millis();

    Spiffs("/Accelerometre", "A = "+String(stp));
    
    pulsometre();
    Spiffs("/Pulsometre", "P = "+String(str));
    
    temperature();
    Spiffs("/Temperature", "T = "+String(Temp));
    
    gps();
    Spiffs("/GPS", "G = "+ gps_data[1]+","+gps_data[2]+","+gps_data[3]);

    String msg = ("P = " + String(str)+"T = "+String(Temp)+"\n"+"G = "
    + gps_data[1]+","+gps_data[2]+","+gps_data[3] + "\n" + "A = "+String(ax)+ " "+String(ay)+ " "+String(az)+ "\n" + "S = " + String(stp));
    
    prev=WifiLora.getTx(); //get informations about the previous message sent
    update_display();       
    if (WifiLora.send(msg)) Serial.println(String("Send message : ")+msg);
  }
}

void accelerometre(){

   accelgyro.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);
   
    #ifdef OUTPUT_BINARY_ACCELGYRO
        Serial.write((uint8_t)(ax >> 8)); Serial.write((uint8_t)(ax & 0xFF));
        Serial.write((uint8_t)(ay >> 8)); Serial.write((uint8_t)(ay & 0xFF));
        Serial.write((uint8_t)(az >> 8)); Serial.write((uint8_t)(az & 0xFF));
        Serial.write((uint8_t)(gx >> 8)); Serial.write((uint8_t)(gx & 0xFF));
        Serial.write((uint8_t)(gy >> 8)); Serial.write((uint8_t)(gy & 0xFF));
        Serial.write((uint8_t)(gz >> 8)); Serial.write((uint8_t)(gz & 0xFF));
    #endif
}

void pulsometre(){

    byte rc;
    unsigned short val[2];
    rc = bh1790glc.get_val(val);
    if (rc == 0) {
      sprintf(str, "%d, %d\n", val[1], val[0]);
  }
}

void temperature(){
  
    sensors.requestTemperatures();
    Temp = String(sensors.getTempCByIndex(0));    
}

void gps(){
  
  String GPS_txt;
  byte byteGps;
  do {
    GPS_txt = "";
    for (int i=0;i<6;i++){
      GPS_txt += char(GPSserial.read());
    }
  } while (GPS_txt != "$GPRMC");
  GPS_txt = "";  
  byteGps = GPSserial.read();
  do {
    byteGps = GPSserial.read();
  } while (char(byteGps != ','));
  byteGps = GPSserial.read();
  gps_data[0] = String(char(byteGps));

  if (char(byteGps) == 'A'){

    byteGps = GPSserial.read();
  
    byteGps = GPSserial.read();
    while (char(byteGps != ',')){
      GPS_txt += char(byteGps);
      byteGps = GPSserial.read();
    }
    gps_data[1] = GPS_txt;
    GPS_txt = "";
  
    byteGps = GPSserial.read();
    byteGps = GPSserial.read();
    byteGps = GPSserial.read();
    while (char(byteGps != ',')){
      GPS_txt += char(byteGps);
      byteGps = GPSserial.read();
    }
    gps_data[2] = GPS_txt;
    GPS_txt = "";
  
    byteGps = GPSserial.read();
    byteGps = GPSserial.read();
    byteGps = GPSserial.read();
    while (char(byteGps != ',')){
      GPS_txt += char(byteGps);
      byteGps = GPSserial.read();
    }
    gps_data[3] = GPS_txt;
  }
}

void stepcalculator(){
  if (ay >= -14000 and previous_y < -14000){
    stp = stp + 1;
  }
  previous_y = ay;
}

void chute(){
  if (abs(az) > 20000){
    WifiLora.send("Possible chute");
    Serial.println("chute");
  }
}

void Spiffs(String nameFile, String Data){
  String save;
  File f = SPIFFS.open(nameFile+".txt","r");
  save = f.readString();
  f.close();
  f = SPIFFS.open(nameFile+".txt", "w");
  f.println(save+Data+"\n");
  f.close();  
}
