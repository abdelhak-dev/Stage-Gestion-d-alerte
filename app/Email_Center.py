from datetime import datetime
import os
import smtplib
import imghdr
import ssl
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText



def SendMail(AlertTopic,SensorID,DangerType,Date,Destination):
    Sender = 'Abdelhak.mhidi@etud.iga.ac.ma'
    TokenApp = 'joxj whvs vdwu avks'
    Dateformat = Date
    #Dateformat = Date.strftime("%d-%m-%Y %H:%M")
    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Alert {} ServerRoom | {}".format(AlertTopic, Dateformat)
    msg['From'] = Sender
    msg['To'] = Destination

    text = "Alert Repported From ServerRoom AT  {}\nAn Intervention Needed in the Room.\nThank You. \nServerBot".format(AlertTopic, DangerType, Dateformat)
    html = """\
    <html>
      <head></head>
      <body>
        <p><h2>Alert Repported From ServerRoom AT  {}<br></h2><br>
                    <b>Alerting SensorID : {} </b><br>
                    <b>Alert Type : {} </b><br>
                    <b>Alert Level : {} </b><br><br>
           An Intervention Needed in the Room.<br>
           Thank You.<br>
           <h5><i>@ServerBot IGA2022</i></h5>
        </p>
      </body>
    </html>
    """


    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text.format(AlertTopic, DangerType, Dateformat), 'plain')
    part2 = MIMEText(html.format(Dateformat, SensorID, AlertTopic,DangerType), 'html')
    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)
    # Send the message via local SMTP server.
    mail = smtplib.SMTP('smtp.gmail.com', 587)

    mail.ehlo()
    mail.starttls()
    mail.login(Sender, TokenApp)
    mail.sendmail(Sender, Destination, msg.as_string())
    mail.quit()
    print("Email sent !!")
    return {"code":200, "Message": "Email sendt !"}

