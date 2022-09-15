from fastapi import FastAPI
from Base_de_donnée import *
from features import *
from fastapi import FastAPI, HTTPException
from sqlite3 import Error
from typing import Optional
import datetime
import json



tags_metadata = [
    {
        "name": "Welcome:",
        "description": "Welcome ! ENjoy our work 😉✌️  ",
    },
    {
        "name": "Set & Add Functions :",
        "description": "Add a patient or a medicine or a robot ID ",
    },

     {
        "name": "Set & Get Functions Robot_Side :",
        "description": "Main communication function's Robot/API or API/Robot ",
    },
    {
        "name": "Get & Responses :",
        "description": "get a response by the api, ex:getOrder/{room}.",
        "externalDocs": {
            "description": "The local API URL's ",
            "url": "http://127.0.0.1:8000/",
        },
    },
    {
        "name": "Statistic & Data Analysis Functions :",
        "description": "Statistic of recovery and History of robot's medicine delivery",
    },
]

app = FastAPI(title="Cluster's_Robot API",version="1.5.0",description="Happy to share with you the fruit of a hard worker team  ✌️" ,openapi_tags=tags_metadata)


'''
Le fichier app contient les URI API pour les différentes requetes utiles pour notre projet robot.
Ce fichier représente la partie apparant de l'ice-berg API, qui a pour racine le features et Base_de_données

'''


# message d'entée de l'api
@app.get("/", tags=['Welcome'])
async def root():
    return {"Project": " Hello cluster_robot !"}


### Add_functions tag:
##
#

# Créer une route dans l'api qui renvoi un  médicament avec son ID et son nom
# exemple: verbe/{argument1}/{arguemnt2}
@app.get('/setMedicine/{MedicineID}/{MedicineName}', tags=["Set & Add functions"])
async def add_medicine(MedicineID: int, MedicineName: str):
    return load_setMedicine(MedicineID, MedicineName)

#Add Capteur
@add.get('/add_Sensor/{Sensor}/{Type}',tags=["Set & Add functions"])
async def Add_Sensor(Sensor:str,Type:str):
    return add_Sensor(Sensor,Type)

#Modification nom ou type du capteur
@add.get('edit_ref/{Sensor}/{Type}',tags=["Set & Add functions"])
async def Edit_Sensor_Ref(Sensor:str,Type:str):
    return modifSensor(Sensor,Type)

#Modification type du capteur
@add.get('edit_sensor_type/{Sensor}/{Type}',tags=["Set & Add functions"])
async def Edit_Sensor_Type(Sensor:str,Type:str):
    return modifType(Sensor,Type)

#Set threshold : mettre un seuil de déclenchemnt de l'alerte (sur Temperature ou Humidité)
@dd.get('setTempHumid/{T}/{}',tags=["Set & Add functions"])
async def SetTempHumid(Sensor:str,Date:str,Temperature,Humidity):
    return set_Threshold(Sensor,Date,Temperature,Humidity)

#Record date



# Créer une route dans l'api qui ajoute un patient dans la base de données avec les paramètres d'entrées : room,ID,week
# exemple: verbe/{argument1}/{arguemnt2}
@app.get('/addPatient/{room}/{patientID}/{week}', tags=["Set & Add functions"])
async def add_patient(room: int, patientID: str, week: str):
    return load_addPatient(room, patientID, week)


# Créer une route dans l'api qui ajoute une chambre 'room' dans la base de données avec les paramètres d'entrées : ID,nom
# exemple: verbe/{argument1}/{arguemnt2}
@app.get('/setRoom/{room}/{name}', tags=["Set & Add functions"])
async def setRoom(room: int, name: str):
    return load_room(room, name)


# Créer une route dans l'api qui modifie l'état d'un patient dans la base de données selon son ID
# exemple: verbe/{argument1}/{arguemnt2}
@app.get('/setPatientCondition/{patientID}/{etat}', tags=["Set & Add functions"])
async def setPatientCondition(patientID: str, etat: str):
    return load_set_condition(patientID, etat)


# Créer une route dans l'api qui ajoute un médicament pour la chambre 'room'
# exemple: verbe/{argument1}/{arguemnt2}
@app.get('/setRoomMedicine/{room}/{medicine}', tags=["Set & Add functions"])
async def setRoomMedicine(room: int, medicine: int):
    return load_setRoomMedicine(room, medicine)


## Créer une route dans l'api qui ajoute un trajet pour la chambre en paramètre 'room' , le path est de la forme 'A2XX'
# avec A: le déplacement à faire  et 2 le numéro de la node arrivée
# exemple: verbe/{argument1}/{arguemnt2}
@app.get('/setPath/{room}/{path}', tags=["Set & Add functions"])
async def setPath(room: int, path: str):
    return load_setPath(room, path)


# Créer une route dans l'api qui ajoute un ordre à executer par le robot
# exemple: verbe/{argument1}/{arguemnt2}
@app.get('/addOrder/{room}/{medicine}', tags=["Set & Add functions"])
async def addOrder(room: int,medicine:int):
    return load_addOrder(room,medicine)

#ajouter un robot en lui attribuant un ID_Robot:
@app.get('/addRobot/{robotID}',tags=["Set & Get Functions Robot_Side"])
async def addrobotID(robotID:int):
    return load_addRobotID(robotID)

#Signaler la position du robot
@app.get('/setPosition/{robotID}/{node}',tags=["Set & Get Functions Robot_Side"])
async def setPosition_robot(robotID:int,node:int):
    return load_position_robot(robotID,node)


#Afficher la position du robot
@app.get('/getPosition/{robot}',tags=["Set & Get Functions Robot_Side"])
async def getPosition(robot:int):
    return load_getPosition(robot)

### Get functions tag:
##
#
#
#
## Créer une route dans l'api qui affiche la condition d'un patient selon son ID
### exemple: verbe/{argument1}/{arguemnt2}

@app.get('/getPatientCondition/{patientID}', tags=["Get & Responses"])
async def getPatientCondition(patientID: str):
    return load_patientCondition(patientID)
    # {'condition': '{}'.format(load_patientCondition(patientID))}


# Créer une route dans l'api qui permets de savoir le médicament donnée dans la chambre 'room'
# exemple: verbe/{argument1}/{arguemnt2}
@app.get('/getRoomMedicine/{room}', tags=["Get & Responses"])
async def getRoomMedicine(room: int):
    return load_getRoommedicine(room)


# Créer une route dans l'api qui affiche le trajet défini pour la chambre en question
# exemple: verbe/{argument1}/{arguemnt2}
@app.get('/getPath/{room}',tags=["Set & Get Functions Robot_Side"])
async def getPath(room: int):
    return load_getPath(room)


#astatus : done or delivered
@app.get('/setOrder/{order}/{status}',tags=["Set & Get Functions Robot_Side"])
async def setOrder(order :int,status:str):
    try:
        load_setOrder(order,status)
        return {"code":200}
    except:
        return {"code":404, "error":"Order not recorded"}

# C'est la requete utilisé en boucle par le robot, il permet d'afficher l'ordre à traiter
@app.get('/getOrder/{robot}',tags=["Set & Get Functions Robot_Side"])
async def getOrder(robot:int):
    return load_getOrder(robot)

#setNode c'est la fonction modifier par l'arduino
@app.get('/setNode/{node}/{booked}',tags=["Set & Get Functions Robot_Side"])
async def setNode(node:int,booked:str):
    return load_setNode(node,booked)

#getnode permet de savoir si une node est réservé ou pas
@app.get('/getNode/{node}',tags=["Set & Get Functions Robot_Side"])
async def getNode(node:int):
    return load_getNode(node)

# Cette fonction permets de d'avoir l'état du patient comme réponse
@app.get('/getStats/{room}',tags=["Statistic & Data Analysis Functions"])
async def getStats(room: int):
    return load_getStats(room)



#transmettre l'historique à l'interface
@app.get('/getHistory/',tags=["Statistic & Data Analysis Functions"])
async def getHistory(robot:int =0):
    return load_getHistory(robot)

