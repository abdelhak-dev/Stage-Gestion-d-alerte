import os
import smtplib
import imghdr
import ssl
from email.message import EmailMessage

def SendMail(AlertTopic,SensorID,DangerType,Date,Destination):
    message = '''
             ALERT ServerRoom\n
      '{}' '{}' Repported AT '{}'From Sensor'{}'  
      An Intervention Needed in the Room.     
             '''.format(AlertTopic,DangerType,Date,SensorID)

    Sender='Abdelhak.mhidi@etud.iga.ac.ma'
    TokenApp = 'joxj whvs vdwu avks'
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login(Sender,TokenApp)
    server.sendmail(Sender,Destination,message)
    return {"code":200, "Message": "Email sendt !"}
