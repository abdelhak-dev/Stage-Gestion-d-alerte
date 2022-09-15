from Base_de_donnée import *
import datetime
import requests



#ajout d'un capteur
def add_Sensor(Sensor:str,Type:str,SensorID:int):
    return addCapteur(Sensor,Type,SensorID)

#Modification nom ou type du capteur
def edit_SensorName(Sensor:str,Type:str):
    return modifSensor(Sensor,Type)

#Modification type du capteur
def edit_SensorType(Sensor:str,Type:str):
    return modifType(Sensor,Type)

#Afficher le réseau de capteurs connecté

#Set threshold : mettre un seuil de déclenchemnt de l'alerte (sur Temperature ou Humidité)
def set_Threshold(SensorRef:str,SensorID:int,Temperature:float,Humidity:float):
    temp = SetTemperature(SensorRef,SensorID,Temperature)
    humid = SetHumidity(SensorRef,SensorID,Humidity)
    return temp,humid

#Record Date
def Record_Date():
    return ddate()

#
##
## Now we add Alert structure from database
#Ajouter une alerte avec son type de danger Dnger : high or Fatal or Low
def add_Alert(Alert: str, Danger: str, Destination):
    return Alert(Alert, Danger, Destination)

#Modifier le type d'alerte : high or Fatal or Low
def edit_AlertType(Alert:str,AlertDanger:str,Date):
    return AlertDangerModif(Alert,AlertDanger,Date)

#Modifier le sujet de l'alerte : Temperature par exemple
def edit_Alert(Alert:str,AlertDanger:str,Date):
    return AlertModif(Alert,AlertDanger,Date)


