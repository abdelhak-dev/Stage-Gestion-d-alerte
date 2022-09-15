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
                                    SensorID     INT NOT NULL PRIMARY KEY,
                                    SensorRef VARCHAR(21) NOT NULL ,
                                    Type   VARCHAR(21) NOT NULL ,
                                    Stat   VARCHAR(21) NOT NULL ,
                                    Temperature REAL ,
                                    Humidity REAL ,
                                    Date   TEXT);''')

    c.execute('''CREATE TABLE Alerte(
        AlertSubject VARCHAR(21) NOT NULL,
        SensorID    INT,
        DangerType VARCHAR(21) NOT NULL,
        DestinationEmail VARCHAR(21) NOT NULL,
        Date   TEXT,
        FOREIGN KEY(SensorID) REFERENCES Capteurs(SensorID));''')
    conn.commit()
    conn.close()

#Table Capteurs
def addCapteur(SensorID:int,SensorRef:str,Type:str):
    if type(SensorID) != type(3): return {"code": 404, "error": "SensorID not correct"}
    if type(SensorRef) != type("str"):return {"code":404,"error": "SensorRef not correct"}
    if type(Type) != type("str"): return {"code": 404, "error": "Type not correct"}

    with connection_DBase() as conn:
        try:
            c = conn.cursor()
            rSQL = ''' DELETE FROM Capteurs WHERE SensorID = '{}', SensorRef = '{}', Type = '{}';'''
            c.execute(rSQL.format(SensorID,SensorRef,Type))
            conn.commit()
            return {"code": 200, "SensorID": Type,"AddingSensor": SensorRef , "AddingSensorType": Type}
        except:
            rSQL = ''' INSERT INTO Capteurs (SensorID,SensorRef, Type) VALUES ('{}','{}','{}');'''
            c.execute(rSQL.format(SensorID,SensorRef, Type))
            conn.commit()
            return {"code": 200, "SensorID": SensorID,"Sensor": SensorRef , "Type":Type}

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

def modifType(SensorID:int,SensorRef:str,Type:str):
    if type(SensorID) != type(3): return {"code": 404, "error": "SensorID not correct"}
    if type(SensorRef) != type("str"):return {"code":404,"error": "SensorRef not correct"}
    if type(Type) != type("str"): return {"code": 404, "error": "Type not correct"}

    with connection_DBase() as conn:
        c = conn.cursor()
        rSQL = ''' UPDATE Capteurs SET Type ='{}' 
                                    WHERE SensorRef = '{}' AND SensorID = '{}';'''
        c.execute(rSQL.format(Type,SensorRef,SensorID))
        conn.commit()
        return {"code": 200, "ModifiedType": Type}


def availableSensors():
    with connection_DBase() as conn:
        c = conn.cursor()
        try:
            rSQL = ''' SELECT * FROM Capteur ORDER BY SensorID DESC;'''
            c.execute(rSQL)
            element= c.fetchall()
            conn.commit()
            return {"code": 200, "Element Found": element[0][0]}
        except:
            return {"Code": 404, "Element":None}

#Les valeurs temp et humid seront remplacer par ce qui viendra de la communication HTTP
def TemperatureHumidity(SensorRef:str,SensorID:int,Temperature:float,Humidity:float):
    if type(SensorID) != int(): return {"code": 404, "error": " SensorID not correct"}
    if type(SensorRef) != str(): return {"code": 404, "error": " SensorRef not correct"}
    if type(Temperature) != float(): return {"code":404,"error": "Value Sensor not correct"}
    if type(Humidity)    != float(): return {"code": 404, "error": "Value Sensor not correct"}

    with connection_DBase() as conn:
        c = conn.cursor()
        try:
            rSQL = ''' UPDATE Capteurs SET Temperature ='{}', Humidity = '{}'
                                WHERE SensorRef ='{}' AND SensorID ='{}'; '''
            c.execute(rSQL.format(Temperature,Humidity,SensorRef,SensorID))
            conn.commit()
            #print(Temperature, Humidity, Sensor, SensorID)
            return {"code": 200}
        except:
            return {"Code": 404}



"""def getvalue1()
##fonction qui prend la valeur receptionnée par HTTP
###Et la mets dans value1 de tableau capteurs
    pass

def getvalue2()
##fonction qui prend la valeur receptionnée par HTTP
###Et la mets dans value2 de tableau capteurs
    pass"""

#c'était qu'une fonction de test pour tester l'ajout de la date
#dans la base de donnée
def ddate():
    with connection_DBase() as conn:
        date = datetime.now()
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


def ThresholdTemp():
    global compare
    #Comparaison les valeur de temperature dans une plage
    with connection_DBase() as conn:
        c = conn.cursor()
        try:
            rSQL='''SELECT Temperature FROM Capteurs ORDER BY Temperature ASC LIMIT 1'''
            c.execute(rSQL)
            conn.commit()
            compare = c.fetchone()
            return {"Temperature":compare[0][0]}
        except:
            return {"code":404,"error":"not recorded"}
    return compare

"""
def alertCondition():
    with connection_DBase() as conn:
        c = conn.cursor()
        rSQL = '''SELECT SensorID FROM Capteurs 
                    WHERE Sensor ID MAX(30) ; ''' #Je veux selectionner les SensorID selon une plage de temperature
        # 8°<Low<30, 30°<High<45, 50°<Fatal<60
        c.execute(rSQL)
        val = c.fetchall()
        while val != []:
            rSQL = ''' SELECT medicineID FROM HISTORICORDER where orderID = {} ;'''
            c.execute(rSQL.format(val[0][0]))
            val2 = c.fetchone()
        print(val)
"""




#Fonction d'ajout à la base de donnée pour Table Alerte

def Alert(AlertSubject:str,SensorID:int,DangerType:str,Destination):
    Date = datetime.now()
    with connection_DBase() as conn:
        c = conn.cursor()
        try:
            rSQL = '''INSERT INTO Alerte (AlertSubject,DangerType,DestinationEmail,Date) 
                                VALUES ('{}','{}','{}','{}')'''
            c.execute(rSQL.format(AlertSubject,DangerType,Destination,Date)) #SELECT SensorID FROM Capteurs
            conn.commit()

            rSQL = '''INSERT INTO Alerte (SensorID) 
                        SELECT SensorID FROM Capteurs; '''
            c.execute(rSQL)
            conn.commit()

            return {"code": 200}
        except:
            rSQL = '''UPDATE Alerte SET AlertSubject ='{}',DangerType='{}',DestinationEmail='{}',Date='{}';'''
            c.execute(rSQL.format(AlertSubject, DangerType, Destination, Date))
            conn.commit()
            conn.close()
            return {"code": 200}

#fonction pour modifier le type d'alete from fatal to High or High to Fatal en fct de la date du déclenchement
def AlertDangerModif(AlertSubject:str,DangerType:str,Date):
    with connection_DBase() as conn:
        c = conn.cursor()
        rSQL = '''UPDATE Alerte SET DangerType ='{}' 
                    WHERE AlertSubject ='{}' AND Date = '{}';'''
        c.execute(rSQL.format(DangerType,AlertSubject,Date))
        conn.commit()
        return {"code": 200}

def AlertModif(AlertSubject:str,DangerType:str,Date):
    with connection_DBase() as conn:
        c = conn.cursor()
        rSQL = '''UPDATE Alerte SET AlertSubject ='{}' 
                    WHERE DangerType ='{}' AND Date = '{}';'''
        c.execute(rSQL.format(AlertSubject,DangerType,Date))
        conn.commit()
        return {"code": 200}




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

#test de l'ajout sensor et type:
"""
addCapteur("HCR","Ultrasonic") #ça fonctionne
fillTemperature(25)
fillHumidity(25)
ddate() """

#addCapteur("ZEGBEE","Ultrasonic",4)
#ddate()
#TemperatureHumidity("ZEGBEE",1,10.00,10.00) #TemperatureHumidity(Sensor:str,SensorID:int,Temperature:float,Humidity:float):
#availableSensors()
#test de l'ajout d'un alerte
#Alert("Temperature",1,'Fatal',"Admin@gmail.com")
#AlertDangerModif("Temperature","LOW","2022-09-13 09:42:29.947286")
#AlertModif("mimi","LOW","2022-09-13 09:42:29.947286")
#alertCondition()
#ThresholdTemp()