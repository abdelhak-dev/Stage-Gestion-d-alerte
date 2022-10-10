#include <Bridge.h>
#include <HttpClient.h>
#include <Process.h>
#include "DHT.h"
// DHT11 sensor pins
//#define DHTPIN 4 
//#define DHTTYPE DHT11
// PIR Pin
//#define PIR_Pin 2

String Presence;
int Sensitivity;

//Trame HTTP
String ServerName = "http://10.3.1.85:8000/";


// Process to get the measurement time
Process date;
//instance
//DHT dht(DHTPIN, DHTTYPE);
HttpClient client;

void setup() {
  //Initialisation de la communication
  Bridge.begin();
  Serial.begin(115200);
  while(!Serial);
  //DHT Initialisation
  //dht.begin();
  //PIR initialisation 
  pinMode(2, INPUT);
  //delay(4000);
}


void loop()
{
  
  // Measure the humidity & temperature in the Room Server
  SendTemperature(1,4,ServerName); //SendTemperature(int SensorID, pin)
  SendTemperature(3,5,ServerName); //SendTemperature(int SensorID, pin)
  SendTemperature(4,6,ServerName); //SendTemperature(int SensorID, pin)

//Presence in the Room 
  SendPresence(2,ServerName);

  /*
  Serial.flush();
  Serial.println("=======Serial_Dashboard=========");
  Serial.println("|                              |");
  Serial.print("Temp is: ");
  Serial.print(temperature);
  Serial.print(" Humidity is:");
  Serial.println(humidity);
  Serial.println("|                              |");
  Serial.println("|==Presence in the Room Server=|");
  Serial.print("              ");
  Serial.println(Presence);
  Serial.println("|       xxxxxxxxxxxxxxxx       |");
  */
  /*
  //Serial.flush();
  while (client.available()) {
    char c = client.read();
    Serial.println(c);
  }*/
  Serial.flush();
delay(3000);
}



void SendTemperature(int SensorID, int DHTPIN, String ServerName){
  DHT dht(DHTPIN, DHT11);
  dht.begin();
  HttpClient client;
  float humidity = dht.readHumidity();
  float temperature = dht.readTemperature();
  // Check if any reads failed and exit early (to try again).
    if (isnan(humidity) || isnan(temperature)){
      Serial.println(F("Failed to read from DHT sensor!"));
      return;
    }
    client.get(ServerName+"UpdateTempHumid/DHT11/" + SensorID + "/" + temperature + "/" + humidity);

  while (client.available()) {
    char c = client.read();
    Serial.print(c); //Affichage de la résponse API
  }
  //Serial.flush();
  }

  void SendPresence(int SensorID, String ServerName){
  HttpClient client;
  int Sensitivity = digitalRead(2);
  String Presence;
  if (Sensitivity == HIGH) {
    Presence = "PresenceDetected";
    }
  else {
    Presence = "PresenceNotDetected";
  }
  client.get(ServerName+"UpdatePresence/HC-SR501/"+SensorID+"/"+Presence);
  while (client.available()) {
    char c = client.read();
    Serial.print(c); //Affichage de la résponse API
  
  }
  //Serial.flush();
  }