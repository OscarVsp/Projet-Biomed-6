#include <TinyGPS.h>
#include <SSD1306.h>

#define RX1PIN 35
#define TX1PIN 13

SSD1306 display(0x3c, 4, 15);

HardwareSerial GPSserial(1);

float lat = 00.000,lon = 00.000; // create variable for latitude and longitude object  

TinyGPS gps; // create gps object 
int n = 0;

//Update the OLED display
void update_display() {
    display.clear();
    display.drawString(0,0,String("Test Tiny GPS."));
    if (lat==00.000 && lon==00.000){
      display.drawString(0,10,String("Aucun signal GPS..."));
    } else {
      display.drawString(0,10,String("Lattitude : ")+String(lat));
      display.drawString(0,20,String("Longitude : ")+String(lon));
      display.drawString(0,30,String(n));
    }
    display.display();
}

void setup(){ 
  Serial.begin(115200); // connect serial  
  GPSserial.begin(4800,SERIAL_8N1,RX1PIN,TX1PIN); // connect gps sensor 
  Serial.println("Start"); 

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
void loop(){
  Serial.println(String("mesure ..."));
  if (!GPSserial.available()){
    Serial.println(String("GPS invalid"));
  } else {
    Serial.println(String("Décodage..."));
  }
  while(GPSserial.available()){
    if (gps.encode(GPSserial.read())){
      Serial.println(String("encode ok"));
      gps.f_get_position(&lat,&lon);
      String latitude = String(lat,6); 
      String longitude = String(lon,6); 
      Serial.println(latitude+" ; "+longitude);//+" ; "+vitesse);
      n++;
      update_display();
      }
    }
} 
