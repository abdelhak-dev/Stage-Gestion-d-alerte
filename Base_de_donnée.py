"Creation de la base de données"
import sqlite3
from sqlite3 import Error
from pathlib import Path
from datetime import datetime

databaseName = "Server_room.db"

def connection_DBase():
    try:
        conn = sqlite3.connect(databaseName)
        return conn
    except:
        return False

#Vérification des tableaux (BD)

def verifTable():
    try:
        conn = sqlite3.connect(databaseName)
    except Error as e:
        quit
    c = conn.cursor()

    try:
        c.execute("SELECT 1 FROM Capteurs;")
        c.execute("SELECT 1 FROM Alerte;")
    except Error as notable:
        conn.close()
        return False

    conn.close()
    return True

def baseExists():
    "Dans cette fonction on va verifier si la base de données existe"
    file = Path(databaseName)
    if file.exists() and connection_DBase():
        return True
    return False


def createBase():
    try:
        conn = sqlite3.connect(databaseName)
    except Error as e:
        quit

    c = conn.cursor()
    c.execute('''CREATE TABLE Capteurs(
                                    SensorID     INTEGER,
                                    SensorRef VARCHAR(21) NOT NULL ,
                                    Type   VARCHAR(21) NOT NULL ,
                                    State   VARCHAR(21),
                                    Temperature REAL ,
                                    Humidity REAL ,
                                    Presence   VARCHAR(21),
                                    Date   TEXT,
                                    PRIMARY KEY (SensorID,Temperature,Humidity));''')

    c.execute('''CREATE TABLE Alerte(
        AlertID INTEGER ,
        AlertSubject VARCHAR(21) NOT NULL,
        SensorID    INTEGER NOT NULL,
        DangerType VARCHAR(21) NOT NULL,
        DestinationEmail VARCHAR(21) NOT NULL,
        Date   TEXT,
        FOREIGN KEY(SensorID) REFERENCES Capteurs(SensorID));''')

    c.execute('''CREATE TABLE HistoryRoom ( 
                                     Presence VARCHAR(21) NOT NULL , 
                                     Dte  TEXT NOT NULL);''')

    c.execute('''CREATE TABLE DataHistory ( 
                                         SensorID     INTEGER,
                                         Temperature REAL ,
                                         Humidity REAL ,
                                         Date  TEXT,
                                         PRIMARY KEY (SensorID,Temperature,Humidity,Date));''')

    conn.commit()
    conn.close()


#
##
### Add Sensor & Edit Sensor
def addCapteur(SensorID:int,SensorRef:str,Type:str):
    if type(SensorID) != type(3): return {"code": 404, "error": "SensorID not correct"}
    if type(SensorRef) != type("str"):return {"code":404,"error": "SensorRef not correct"}
    if type(Type) != type("str"): return {"code": 404, "error": "Type not correct"}
    with connection_DBase() as conn:
        try:
            #Idverif(SensorID)
            c=conn.cursor()
            rSQL = ''' INSERT OR REPLACE INTO Capteurs (SensorID,SensorRef,Type,State) VALUES ('{}','{}','{}',"OFF"); '''
            c.execute(rSQL.format(SensorID, SensorRef, Type))
            conn.commit()
            return {"code": 200, "Creating SensorID": SensorID, "SensorReference": SensorRef, "Type": Type}

        except:
            rSQL = ''' UPDATE Capteurs SET SensorID = '{}', SensorRef='{}',Type='{}',State= "OFF"
                        WHERE SensorID= '{}';'''
            c.execute(rSQL.format(SensorID,SensorRef,Type,SensorID))
            conn.commit()
            return {"code": 200, "Updating with SensorID": SensorID, "New SensorReference": SensorRef, "New SensorType": Type}

def modifSensorRef(SensorID:int,SensorRef:str,Type:str):
    if type(SensorID) != type(3): return {"code": 404, "error": "SensorID not correct"}
    if type(SensorRef) != type("str"):return {"code":404,"error": "SensorRef not correct"}
    if type(Type) != type("str"): return {"code": 404, "error": "Type not correct"}
    with connection_DBase() as conn:
        c = conn.cursor()
        rSQL = ''' UPDATE Capteurs SET SensorRef ='{}' 
                                                WHERE Type = '{}' AND SensorID = '{}';'''
        c.execute(rSQL.format(SensorRef,Type,SensorID))
        conn.commit()
        return {"code": 200, "ModifiedSensor": SensorRef}

def modifType(SensorID:int,SensorRef:str,Type:str):
    if type(SensorID) != type(3): return {"code": 404, "error": "SensorID not correct"}
    if type(SensorRef) != type("str"):return {"code":404,"error": "SensorRef not correct"}
    if type(Type) != type("str"): return {"code": 404, "error": "Type not correct"}
    with connection_DBase() as conn:
        c = conn.cursor()
        rSQL = ''' UPDATE Capteurs SET Type ='{}' 
                                    WHERE SensorRef = '{}' AND SensorID = '{}' ;'''
        c.execute(rSQL.format(Type,SensorRef,SensorID))
        conn.commit()
        return {"code": 200, "ModifiedType": Type}

#Les valeurs temp et humid seront remplacer par ce qui viendra de la communication HTTP
def UpdateTemperature(SensorRef:str,SensorID:int,Temperature):
    if type(SensorID) != type(1): return {"code": 404, "error": " SensorID not correct"}
    if type(SensorRef) != type("RJK8-2N_3I"): return {"code": 404, "error": " SensorRef not correct"}
    #if type(Temperature) != type(10.60): return {"code":404,"error": "Value Sensor not correct"}
    now = datetime.now()
    date = now.strftime("%m-%d-%Y, %H:%M:%S")
    with connection_DBase() as conn:
        c = conn.cursor()
        try:
            rSQL = ''' UPDATE Capteurs SET Temperature ='{}',Date ='{}',State ='ON'
                                WHERE SensorRef ='{}' AND SensorID ='{}'; '''
            c.execute(rSQL.format(Temperature,date,SensorRef,SensorID))
            conn.commit()
            #print(Temperature, Humidity, Sensor, SensorID)
            return {"code": 200, "Temperature Updated is:":Temperature}
        except:
            return {"Code": 404}

def UpdateHumidity(SensorRef:str,SensorID:int,Humidity):
    if type(SensorID) != type(2): return {"code": 404, "error": " SensorID not correct"}
    if type(SensorRef) != type("RHK-3O0"): return {"code": 404, "error": " SensorRef not correct"}
    #if type(Humidity)  != type(20.90): return {"code": 404, "error": "Value Sensor not correct"}
    now = datetime.now()
    date = now.strftime("%m-%d-%Y, %H:%M:%S")
    with connection_DBase() as conn:
        c = conn.cursor()
        try:
            rSQL = ''' UPDATE Capteurs SET Humidity ='{}',Date ='{}', State ='ON'
                                WHERE SensorRef ='{}' AND SensorID ='{}'; '''
            c.execute(rSQL.format(Humidity,date,SensorRef,SensorID))
            conn.commit()
            #print(Temperature, Humidity, Sensor, SensorID)
            return {"code": 200, "Humidity Updated is":Humidity}
        except:
            return {"Code": 404}

def UpdatePresence(SensorRef:str,SensorID:int,Presence:str):
    if type(SensorRef) != type("str"):return {"code":404,"error": "SensorRef not correct"}
    if type(SensorID) != type(3): return {"code": 404, "error": "SensorID not correct"}
    if type(Presence) != type("str"): return {"code": 404, "error": "Presence not correct"}
    #date = datetime.now()
    now = datetime.now()
    date = now.strftime("%m-%d-%Y, %H:%M:%S")
    with connection_DBase()as conn:
        c = conn.cursor()
        rSQL= ''' UPDATE Capteurs SET Presence ='{}',State ='ON',Date='{}'
                    WHERE SensorID='{}' AND SensorRef='{}'; '''
        c.execute(rSQL.format(Presence,date,SensorID,SensorRef))
        conn.commit()
    return {"code": 200, "Presence": Presence, "AT":date}

def SensorState(SensorID:int,State:str):
    if type(SensorID) != type(1): return {"code": 404, "error": " SensorID not correct"}
    #if type(SensorRef) != str(): return {"code": 404, "error": " SensorRef not correct"}
    if type(State) != type("ON"):return {"code": 404, "error": " State not correct"}
    #if State != "ON" or "OFF" : return {"code": 404, "error": " State should be ONLY ON or OFF"}
    with connection_DBase() as conn:
        c = conn.cursor()
        rSQL = ''' UPDATE Capteurs SET State='{}' 
                        WHERE SensorID ='{}';'''
        c.execute(rSQL.format(State,SensorID))
        conn.commit()
        return {"code": 200, "State": State}
        #return "state changed to '{}'".format(State)


#
##
### List Available Devices "Sensors"
def availableSensors():
    with connection_DBase() as conn:
        c = conn.cursor()
        rSQL=''' SELECT * FROM Capteurs ORDER BY SensorRef;'''
        c.execute(rSQL)
        val = c.fetchall()
        for i in range(3):
            for j in range(2):
                return {"Sensors":val[i][j]}

#c'était qu'une fonction de test pour tester l'ajout de la date
#dans la base de donnée
def ddate():
    with connection_DBase() as conn:
        #date = datetime.now()
        now = datetime.now()
        date = now.strftime("%m-%d-%Y, %H:%M:%S")
        c = conn.cursor()
        try:
            rSQL =''' INSERT INTO Capteurs (Date) VALUES ('{}');'''
            c.execute(rSQL.format(date))
            conn.commit()
            return {"code": 200, "Date": date}
        except:
            rSQL = ''' UPDATE Capteurs SET Date ='{}';'''
            c.execute(rSQL.format(date))
            conn.commit()
            return {"code": 200}

def sort_Temperature():
    values = []
    with connection_DBase() as conn:
        c = conn.cursor()
        rSQL='''SELECT Temperature FROM Capteurs ORDER BY Temperature DESC'''
        c.execute(rSQL)
        itemlist = c.fetchall()
        for item in itemlist:
            values[item] = itemlist[item]
            item+=1
            return values

def Idverif(SensorID:int):
    with connection_DBase() as conn:
        c = conn.cursor()
        rSQL = ''' SELECT COUNT(*) FROM Capteurs WHERE SensorID ='{}' ;'''
        c.execute(rSQL.format(SensorID))
        catch = c.fetchall()
        if catch[0][0] == SensorID:
            #return{"error":"The SensorID already exist !"}
            print({"error":"The SensorID already exist !"})
        # 8°<Low<30, 30°<High<45, 50°<Fatal<60


#
##
### Compare to Declenche Alerte
def compareT():
 with connection_DBase() as conn:
     c = conn.cursor()
     NormTemp = [10,15,25,32]
     #try:
     rSQL = ''' SELECT Temperature From Capteurs '''
     c.execute(rSQL)
     Temp = c.fetchone()

     rSQL = ''' SELECT Humidity From Capteurs '''
     c.execute(rSQL)
     Humid = c.fetchone()
     if Temp[0] <= NormTemp[0]: #Temp[0] >= lst[0][0] and Temp <= lst[0][1]
         DangerType ="LOW"
         return DangerType
         #return {"code":200,"Temperature Mesured is:":Temp[0],"DangerType is":"LOW"}

         #print("Temperature selected is:", Temp[0]+ "LOW")
     elif Temp[0] >= NormTemp[0] and Temp[0] <= NormTemp[1]:
         DangerType = "AVERAGE"
         return DangerType
         #return {"code": 200, "Temperature Mesured is:": Temp[0], "DangerType is": "AVERAGE"}
         #print("Temperature selected is:", Temp[0]+"AVERAGE")
     elif Temp[0] >= NormTemp[1] and Temp[0] <= NormTemp[2]:
         DangerType = "AVERAGE HIGH"
         return DangerType
         #return {"code": 200, "Temperature Mesured is:": Temp[0], "DangerType is": "AVERAGE HIGH"}
         #print("Temperature selected is:", Temp[0] +"AVERAGE HIGH")
     elif Temp[0] <= NormTemp[2] and Temp[0] <= NormTemp[3]:
         DangerType ="FATAL"
         return DangerType
         #return {"code": 200, "Temperature Mesured is:": Temp[0], "DangerType is": "FATAL"}
         #print("Temperature selected is:", Temp[0] + "FATAL")
     elif Temp[0] >= NormTemp[3]:
         DangerType = "FATAL"
         return DangerType
         #return {"code": 200, "Temperature Mesured is:": Temp[0], "DangerType is": "FATAL"}

def compareHumid():
    with connection_DBase() as conn:
        c = conn.cursor()
        NormHumid = [8,20,50,70,80]
        # try:
        rSQL = ''' SELECT Humidity From Capteurs  '''
        c.execute(rSQL)
        Humid = c.fetchone()
        print(Humid)
        if Humid[0]in range(NormHumid[0],NormHumid[1]):
            DangerType = "LOW"
            #return {"code":200,"Humidity Mesured is:":Humid[0],"DangerType is": DangerType}
            return DangerType
        elif Humid[0] in range(NormHumid[1],NormHumid[2]):
            DangerType = "MEDIUM"
            #return {"code":200,"Humidity Mesured is:": Humid[0], "DangerType is": DangerType}
            return DangerType
        elif Humid[0] in range(NormHumid[3],NormHumid[4]):
            #Creat Alert
            DangerType="HIGH"
            #return {"code":200,"Humidity Mesured is:": Humid[0], "DangerType is": DangerType}
            return DangerType
        else:
            #Creat Alert
            DangerType ="So HIGH"
            #return {"code":200,"Humidity Mesured is:": Humid[0], "DangerType is": DangerType}
            return DangerType


def CompareMixer():
    Temp_State = compareT()
    Humid_State = compareHumid()
    with connection_DBase() as conn:
        c = conn.cursor()
        if Temp_State == "HIGH" :
            AlerteTopic = "Temperature"
            return AlerteTopic
        elif Humid_State == "Humidity" :
            AlerteTopic = "Humidity"
            return AlerteTopic
        elif Temp_State == "HIGH" and Humid_State == "Humidity":
            AlerteTopic = 2
            return AlerteTopic
        else:
            AlerteTopic = 0
            return AlerteTopic



#
##
### Fonction Gestion d'Alerte

def CompareToAlert():

    return
def Alert(SensorID:int,Destination):
    now = datetime.now()
    Date = now.strftime("%m-%d-%Y, %H:%M:%S")
    DangerType = compareT()
    AlertSubject = CompareMixer()
    with connection_DBase() as conn:
        c = conn.cursor()
        if AlertSubject == 0:
            return {"code":200,"Message":"No Message Repported"}
        if AlertSubject == 2 :
            rSQL2 = ''' INSERT INTO Alerte (AlertSubject,SensorID,DangerType,DestinationEmail,Date) 
                            VALUES ('Temperature','{}','{}','{}','{}');'''
            c.execute(rSQL2)

            rSQL2 = ''' INSERT INTO Alerte (AlertSubject,SensorID,DangerType,DestinationEmail,Date) 
                                        VALUES ('Humidity','{}','{}','{}','{}');'''
            c.execute(rSQL2)
            conn.commit()
            return {"code":200,"Message":f" Alert '{AlertSubject}'Repported"}
        else:
            rSQL = '''INSERT INTO Alerte (AlertSubject,SensorID,DangerType,DestinationEmail,Date) 
                                VALUES ('{}','{}','{}','{}','{}');'''
            c.execute(rSQL.format(AlertSubject,SensorID,DangerType,Destination,Date)) #SELECT SensorID FROM Capteurs
            conn.commit()
            return {"code":200,"Message":f" Alert '{AlertSubject}'Repported"}.format()

        """except:
            rSQL = ''' UPDATE Alerte SET AlertSubject ='{}',DangerType='{}',DestinationEmail='{}',Date='{}'
                        WHERE SensorID = '{}' LIMIT 1;'''
            c.execute(rSQL.format(AlertSubject, DangerType, Destination, Date,SensorID))
            conn.commit()
            conn.close()
            return {"code": 200}"""

#fonction pour modifier le type d'alete from fatal to High or High to Fatal en fct de la date du déclenchement
"""def AlertDangerModif(AlertSubject:str,DangerType:str,Date):
    with connection_DBase() as conn:
        c = conn.cursor()
        rSQL = '''UPDATE Alerte SET DangerType ='{}' 
                    WHERE AlertSubject ='{}' AND Date = '{}';'''
        c.execute(rSQL.format(DangerType,AlertSubject,Date))
        conn.commit()
        return {"code": 200}"""

def AlertDangerModif(AlertSubject:str,DangerType:str):
    with connection_DBase() as conn:
        c = conn.cursor()
        rSQL = ''' UPDATE Alerte SET DangerType ='{}' 
                    WHERE AlertSubject ='{}' ORDER by id DESC LIMIT 1;'''
        c.execute(rSQL.format(DangerType,AlertSubject))
        conn.commit()
        return {"code": 200}

def AlertSubjectModif(AlertSubject:str,DangerType:str,Date):
    with connection_DBase() as conn:
        c = conn.cursor()
        rSQL = ''' UPDATE Alerte SET AlertSubject ='{}' 
                    WHERE DangerType ='{}' AND Date = '{}';'''
        c.execute(rSQL.format(AlertSubject,DangerType,Date))
        conn.commit()
        return {"code": 200}

#
##
### Historique d'acces à la salle

def RoomAcces():
    with connection_DBase() as conn:
        #date = datetime.now()
        c = conn.cursor()
        rSQL = ''' INSERT OR IGNORE INTO HistoryRoom (Presence,Dte)
                    SELECT Presence,Date FROM Capteurs LIMIT 2 ;'''
        c.execute(rSQL)
        conn.commit()
        return {"code": 200, "Message": "Done"}

#
##
### Fonction Pour Affichage
def AfficheTemp():
    with connection_DBase()as conn:
        c = conn.cursor()
        rSQL = ''' SELECT Temperature FROM Capteurs;'''
        c.execute(rSQL)
        Temp = c.fetchone()
    return Temp[0]

def AfficheHumid():
    with connection_DBase()as conn:
        c = conn.cursor()
        rSQL = ''' SELECT Humidity FROM Capteurs ;'''
        c.execute(rSQL)
        Humid = c.fetchone()
    return Humid[0]


#
##
### Storage Functions

def StoringData():
    with connection_DBase()as conn:
        c = conn.cursor()
        rSQL = ''' INSERT OR IGNORE INTO DataHistory (SensorID,Temperature,Humidity,Date)
                    SELECT SensorID, Temperature,Humidity,Date
                    FROM Capteurs
                    WHERE SensorRef = "DHT11" LIMIT 1;'''
        c.execute(rSQL)
        conn.commit()
        print("Data Stored Successflly !")




def __test__():
    ''' unit tests of this module functions
    '''
    print("test de l'existence de la base")
    if not baseExists():
        print("..je crée la base")
        createBase()
    else:
        print("..", "la base existe")

if __name__=='__main__':  #'__Base_de_donnée__'
    __test__()


#
##
##Test de l'écriture à la base de données hors line:

### Ajout d'un capteur
#addCapteur(1,"DHT22","Temp&Humid")
#addCapteur(2,"HC-SR501","Mouvement")

#Test Arduino Yun Fonctions
#UpdateHumidity("DHT22",1,80.90)
#UpdateTemperature("DHT22",1,26)
#UpdatePresence("HC-SR501",2,"PresenceDetected")

#Test DataStoring Functions
StoringData()

#Room Presence
RoomAcces()
#Test de l'ajout d'un alerte

#Alert("Temperature",2,"Fatal","Admin@gmail.com")
#AlertDangerModif("Temperature","LOW")
#AlertDangerModif("Temperature","LOW","2022-09-13 09:42:29.947286")
#AlertSubjectModif("mimi","LOW","2022-09-13 09:42:29.947286")
#alertCondition()
#ThresholdTemp()


#compareT()
#compareHumid()