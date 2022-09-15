from Base_de_donnée import *
import datetime
import requests



#ajout d'un capteur
def add_Sensor(Sensor:str,Type:str):
    return addCapteur(Sensor,Type)

#Modification nom ou type du capteur
def edit_SensorName(Sensor:str,Type:str):
    return modifSensor(Sensor,Type)

#Modification type du capteur
def edit_SensorType(Sensor:str,Type:str):
    return modifType(Sensor,Type)

#Set threshold : mettre un seuil de déclenchemnt de l'alerte (sur Temperature ou Humidité)
def set_Threshold(Sensor:str,Date:str,Temperature,Humidity):
    return TemperatureHumidity(Sensor,Date,Temperature,Humidity)

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


