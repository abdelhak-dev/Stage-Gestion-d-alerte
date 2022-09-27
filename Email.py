import os
import smtplib
import imghdr
import ssl
from email.message import EmailMessage
from Base_de_donnée import *
"""def SendMail(Destination:str,messa):
    message = '''
             ALERT ServerRoom\n
      '{}' Repported From Sensor'{}'       
             '''.format()

    Sender='Abdelhak.mhidi@etud.iga.ac.ma'
    TokenApp = 'joxj whvs vdwu avks'
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login(Sender,TokenApp)
    server.sendmail(Sender,Destination,message)
    return {"code":200, "Message": "Email sendt !"}"""



def Emaibox():
    with connection_DBase()as conn:
        c = conn.cursor()
        rSQL = '''SELECT AlertSubject FROM Alerte ORDER BY Date ASC LIMIT 1;'''
        c.execute(rSQL)
        catch = c.fetchall()
        print(catch)