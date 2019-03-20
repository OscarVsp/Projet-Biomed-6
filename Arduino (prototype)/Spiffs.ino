#include <SPIFFS.h>

String fileTxt;

void setup() {

  Serial.begin(115200);
  Serial.println("start");

  //demarrage file system
  SPIFFS.begin();
  Serial.println("Demarrage file System");
 
  File f = SPIFFS.open("/test.txt", "r");   //Ouverture fichier pour le lire
  Serial.println("Lecture du fichier en cours:");
  
  //Affichage des données du fichier
  fileTxt = f.readString(); // on recupere le contenu entier du ficher
  Serial.println(fileTxt);
  f.close();
  
  Serial.println("Ficher fermée");
}

void loop() {
  // écrire dans fichier test.txt
  File f = SPIFFS.open("/test.txt", "w");
  f.println(fileTxt);  // on réécrit l'ancien contenu sauvegardé au préalable
  f.print("Ecriture nouvelle info dupuis sketch :"); // puis les nouvelles infos.
  f.println(millis());
  f.close();
  // on ferme le fichier une fois les enregistrements terminés

  // on ouvre de nouveau pour lecture
  f = SPIFFS.open("/test.txt", "r");
  fileTxt = f.readString();
  //Affichage des données du fichier
  Serial.println("affichage de la nouvelle chaine de caractére :");
  Serial.println(fileTxt);
  f.close();
  //pause de 80 secondes , afin d'éviter de remplir la mémoire trop vite.Pensez à débrancher votre ESP ou d'uploader un nouveau sketch avant de saturer votre mémoire.
  delay(80000);

}
