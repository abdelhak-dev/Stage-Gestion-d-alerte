"Creation de la base de données"
import sqlite3
from sqlite3 import Error
from pathlib import Path
from datetime import datetime
from Email_Center import SendMail as mail
databaseName = "Server_room.db"
now = datetime.now()
date = now.strftime("%m-%d-%Y, %H:%M")
Destination = "wedigitalpro.php@gmail.com"
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
        c.execute("SELECT 1 FROM DataHistory;")
        c.execute("SELECT 1 FROM Alerte;")
        c.execute("SELECT 1 FROM HistoryRoom;")
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
        AlertID INTEGER NOT NULL,
        AlertSubject VARCHAR(21) NOT NULL,
        SensorID    INTEGER ,
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
                                         FOREIGN KEY(SensorID) REFERENCES Capteurs(SensorID));''')

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


def Alert(Destination):
    Temperature = TempNorm()
    Humidity = HumidNorm()
    SensorID1 = Temperature[0]
    SensorID2 = Humidity[0]
    DangerType1 = Temperature[2]
    DangerType2 = Temperature[2]
    AlertID = 1
    AlertTopic1 = "Temperature"
    AlertTopic2 = "Humidity"
    with connection_DBase() as conn:
        c = conn.cursor()
        if Temperature[2] == "MEDIUM HIGH" or Temperature == "HIGH":  #Temperature Only
            #Envoyer l'alert rsql
            rSQL = ''' INSERT INTO Alerte (AlertID,AlertSubject,SensorID,DangerType,DestinationEmail,Date) 
                                        VALUES ('{}','{}','{}','{}','{}','{}');'''
            c.execute(rSQL.format(AlertID,AlertTopic1, SensorID1, DangerType1, Destination, date))
            conn.commit()
            AlertID += 1
            return {"code": 200,"Message":mail(AlertTopic1, SensorID1, DangerType1,date,Destination) }

        elif Humidity[2] == "HIGH":  #HUMIDITY
            #Envoyer l'alert rsql
            rSQL = ''' INSERT INTO Alerte (AlertID,AlertSubject,SensorID,DangerType,DestinationEmail,Date) 
                                                    VALUES ('{}','Humidity','{}','{}','{}','{}');'''
            c.execute(rSQL.format(AlertID,AlertTopic2, SensorID2, DangerType2, Destination, date))
            conn.commit()
            AlertID += 1
            #return {"code": 200, "Message": f" Alert '{AlertTopic2}' Repported"}
            return {"code": 200, "Message": mail(AlertTopic2, SensorID2, DangerType2, date, Destination)}

        elif Temperature[2] == "MEDIUM HIGH" and Humidity == "HIGH":    #Temperature AND #HUMIDITY
            # Envoyer l'alert rsql
            rSQL = ''' INSERT INTO Alerte (AlertID,AlertSubject,SensorID,DangerType,DestinationEmail,Date) 
                                                    VALUES ('{}','{}','{}','{}','{}','{}');'''
            c.execute(rSQL.format(AlertID, AlertTopic1,SensorID1, DangerType1, Destination, date))
            AlertID += 1

            rSQL = ''' INSERT INTO Alerte (AlertID,AlertSubject,SensorID,DangerType,DestinationEmail,Date) 
                                                                VALUES ('{}','{}','{}','{}','{}','{}');'''
            c.execute(rSQL.format(AlertID,AlertTopic2 ,SensorID2, DangerType2, Destination, date))
            AlertID += 1
            conn.commit()
            return {"code": 200, "Message 1": mail(AlertTopic1, SensorID1, DangerType1, date, Destination),"Message2":mail(AlertTopic2, SensorID2, DangerType2, date, Destination)}

        elif Temperature[2] == "HIGH" and Humidity == "HIGH":
            # Envoyer l'alert rsql
            rSQL = ''' INSERT INTO Alerte (AlertID,AlertSubject,SensorID,DangerType,DestinationEmail,Date) 
                                                                VALUES ('{}','{}','{}','{}','{}','{}');'''
            c.execute(rSQL.format(AlertID, AlertTopic1,SensorID1, DangerType1, Destination, date))
            AlertID += 1

            rSQL = ''' INSERT INTO Alerte (AlertID,AlertSubject,SensorID,DangerType,DestinationEmail,Date) 
                                                                VALUES ('{}','{}','{}','{}','{}','{}');'''
            c.execute(rSQL.format(AlertID,AlertTopic2, SensorID2, DangerType2, Destination, date))
            AlertID += 1
            conn.commit()
            return {"code": 200, "Message 1": mail(AlertTopic1, SensorID1, DangerType1, date, Destination),"Message2":mail(AlertTopic2, SensorID2, DangerType2, date, Destination)}


def TempNorm():
    NormTemp = {0: [10, "LOW"],
                1: [15, "MEDIUM"],
                2: [25, "MEDIUM HIGH"],
                3: [32, "HIGH"]}
    global ScaleTemp
    with connection_DBase() as conn:
        c = conn.cursor()
        rSQL = ''' SELECT SensorId, Temperature From Capteurs '''
        c.execute(rSQL)
        catch = c.fetchone()
        ###RECCUPERATION DE TEMP HUMD SENSR ID
        SensorID = catch[0]  # SensorID
        Temperature = catch[1]  # Temperature
        Result1 = [SensorID, Temperature]
        if Temperature <= NormTemp[0][0]:
            ScaleTemp = NormTemp[0][1]
            print("ScaleTemp is:", ScaleTemp)

        elif Temperature >= NormTemp[0][0] and Temperature <= NormTemp[1][0] :
            ScaleTemp = NormTemp[1][1]
            print("ScaleTemp is:", ScaleTemp)

        elif Temperature >= NormTemp[2][0] :
            ScaleTemp = NormTemp[2][1]
            print("ScaleTemp is:", ScaleTemp)

        elif Temperature >= NormTemp[2][0] and Temperature <= NormTemp[3][0] :
            ScaleTemp = NormTemp[2][1]
            print("ScaleTemp is:", ScaleTemp)

        elif Temperature >= NormTemp[3][0] :
            ScaleTemp = NormTemp[3][1]
            print("ScaleTemp is:", ScaleTemp)
    Result1.append(ScaleTemp)
    return Result1


def HumidNorm():
    NormHumid = {0: [8, "LOW"],
                 1: [20, "LOW"],
                 2: [50, "MEDIUM HIGH"],
                 3: [70, "HIGH"],
                 4: [80, "HIGH"]}
    with connection_DBase() as conn:
        c = conn.cursor()
        rSQL = ''' SELECT SensorId, Humidity From Capteurs '''
        c.execute(rSQL)
        catch = c.fetchone()
        ###RECCUPERATION DE TEMP HUMD SENSR ID
        SensorID = catch[0]  # SensorID
        Humidity = catch[1]     #Humidity
        Result2 = [SensorID, Humidity]
        if Humidity <= NormHumid[0][0] : #<= 8
            ScaleHumid = NormHumid[0][1]
            print("ScaleHumidity is:", ScaleHumid)

        elif Humidity >= NormHumid[0][0] and Humidity <= NormHumid[1][0]:  ## 8<=H<= 20
            ScaleHumid = NormHumid[1][1]
            print("ScaleHumidity is:", ScaleHumid)

        elif Humidity >= NormHumid[1][0] and Humidity <= NormHumid[2][0]:  ## 20<=H<= 50
            ScaleHumid = NormHumid[2][1]
            print("ScaleHumidity is:", ScaleHumid)

        elif Humidity >= NormHumid[2][0] and Humidity <= NormHumid[3][0]:  ## 50<=H<= 70
            ScaleHumid = NormHumid[3][1]
            print("ScaleHumidity is:", ScaleHumid)

        elif Humidity >= NormHumid[3][0] and Humidity <= NormHumid[4][0]:  ## 70<=H<= 80
            ScaleHumid = NormHumid[4][1]
            print("ScaleHumidity is:", ScaleHumid)

        elif Humidity >= NormHumid[4][0]:  ## 70<=H<= 80
            ScaleHumid = NormHumid[4][1]
            print("ScaleHumidity is:", ScaleHumid)

    Result2.append(ScaleHumid)
    return Result2
##
### Fonction Gestion d'Alerte

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
                    WHERE SensorID = 1 LIMIT 1;'''
        c.execute(rSQL)
        conn.commit()
        print("Data Stored Successflly !")
        return {"code":200}



#StoringData()

#Room Presence
#RoomAcces()

def __test__():
    ''' unit tests of this module functions
    '''
    print("test de l'existence de la base")
    if not baseExists():
        print("..je crée la base")
        createBase()
    else:
        StoringData()
        RoomAcces()
        Alert(Destination)
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

#UpdateHumidity("DHT22",1,82.00)
#UpdateTemperature("DHT22",1,20)
#UpdatePresence("HC-SR501",2,"PresenceDetected")

#Test DataStoring Functions
#StoringData()

#Room Presence
#RoomAcces()
#Test de l'ajout d'un alerte

#compareT()
#compareHumid()

#Alert("admin@admin.com") #Si la table DataHistory est vide l'alerte ne peut pas se créer

#Alert("admin@admin.com")
#AlertDangerModif("Temperature","LOW")
#AlertDangerModif("Temperature","LOW","2022-09-13 09:42:29.947286")
#AlertSubjectModif("mimi","LOW","2022-09-13 09:42:29.947286")
#alertCondition()



# Remarque il faut stocker les données avant de lancer une alert