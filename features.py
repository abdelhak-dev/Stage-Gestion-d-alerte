from Base_de_donnée import *
import datetime
import requests



#ajout d'un capteur
def add_Sensor(SensorID:int,SensorRef:str,Type:str):
    return addCapteur(SensorID,SensorRef,Type)

#Modification nom ou type du capteur
def edit_SensorRef(SensorID:int,SensorRef:str,Type:str): #modifSensorRef(SensorID:int,SensorRef:str,Type:str)
    return modifSensorRef(SensorID,SensorRef,Type)

#Modification type du capteur
def edit_SensorType(SensorID:int,SensorRef:str,Type:str): #modifType(SensorID:int,SensorRef:str,Type:str)
    return modifType(SensorID,SensorRef,Type)

#Afficher le réseau de capteurs connecté

#Set threshold : mettre un seuil de déclenchemnt de l'alerte (sur Temperature ou Humidité)
def Update_TempHumid(SensorRef:str,SensorID:int,Temperature:float,Humidity:float):
    temp = UpdateTemperature(SensorRef,SensorID,Temperature)
    humid = UpdateHumidity(SensorRef,SensorID,Humidity)
    return temp,humid

#update la Presence dans la salle si il ya quelqun ou pas
def Update_Presence(SensorRef:str,SensorID:int,Presence:str):
    return UpdatePresence(SensorRef,SensorID,Presence)

#Record Date
def Record_Date():
    return ddate()

#
##
## Now we add Alert structure from database
#Ajouter une alerte avec son type de danger Dnger : high or Fatal or Low
def add_Alert(AlertSubject: str,SensorID:int, DangerType: str, Destination):
    return Alert(AlertSubject,SensorID, DangerType, Destination)

#Modifier le type d'alerte : high or Fatal or Low
def edit_AlertType(Alert:str,AlertDanger:str,Date):
    return AlertDangerModif(Alert,AlertDanger,Date)

#Modifier le sujet de l'alerte : Temperature par exemple
def edit_Alert(Alert:str,AlertDanger:str,Date):
    return AlertModif(Alert,AlertDanger,Date)


#
##
### RoomHistory function

def RoomHistory():
    return Roomtest()