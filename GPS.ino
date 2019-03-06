#define RX1PIN 35
#define TX1PIN 13

HardwareSerial GPSserial(1);

String gps_data[4];

void setup() {
Serial.begin(115200);
GPSserial.begin(9600,SERIAL_8N1,RX1PIN,TX1PIN);
}

boolean Get_gps(){
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
    return true;
  } else {
    return false;
  }
}

void loop() {
  if (GPSserial.available()){
    if (Get_gps()){
      Serial.println("Lattitude "+gps_data[1]);
      Serial.println("Longitude "+gps_data[2]);
      Serial.println("Speed "+gps_data[3]);
    } else {
      Serial.println("No valide Gps signal");
    }
    
  } else {
    Serial.println("Gps not available.");
  }
  delay(2000);   
} 
