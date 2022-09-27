# importing the required module
import datetime

import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates
from Base_de_donnée import *

def printGraph():
    with connection_DBase() as conn:
        c = conn.cursor()
        Temp_First = ''' SELECT Temperature FROM DataHistory ORDER BY Temperature ASC LIMIT 1;'''
        c.execute(Temp_First)
        TempFirst = c.fetchall()

        Humid_First = ''' SELECT Humidity FROM DataHistory ORDER BY Humidity ASC LIMIT 1;'''
        c.execute(Humid_First)
        HumidFirst = c.fetchone()

        Temp_Last = ''' SELECT * FROM DataHistory ORDER BY Temperature DESC LIMIT 1;'''
        c.execute(Temp_Last)
        TempLast = c.fetchone()

        Himd_Last = ''' SELECT * FROM DataHistory ORDER BY Humidity DESC LIMIT 1 ;'''
        c.execute(Himd_Last)
        HimdLast = c.fetchone()

        Date_First = ''' SELECT Date FROM DataHistory ORDER BY Date ASC LIMIT 1;'''
        #Date_First = ''' SELECT STRFTIME ('%d-%m-%Y, %H:%M',Date) FROM DataHistory ;'''
        c.execute(Date_First)
        DateFirst = c.fetchone()

        Date_cursor = ''' SELECT * FROM DataHistory ORDER BY Date ASC LIMIT 1;'''
        c.execute(Date_First)
        Datecursor = c.fetchall()

        Date_Last = ''' SELECT * FROM DataHistory ORDER BY Date  DESC LIMIT 1;'''
        c.execute(Date_Last)
        DateLast = c.fetchone()

        #print("Temp first",TempFirst[0])
        #print("Temp last",TempLast[1])
        #print("Humidity first",HumidFirst[0])
        #print("Humidity Last",HimdLast[2])
        print("Date first:",DateFirst[0])
        print("Date Last:",DateLast[3])

        Start = datetime.datetime.strptime('{}',"%d-%m-%Y %H:%M:%S").format(datetime(DateFirst))
        end = datetime.datetime.strptime('{}',"%d-%m-%Y %H:%M:%S").format(DateLast)
        date_generated = [Start+ datetime.timedelta(days=i) for i in range(0,(end-Start).days)]

        for dte in date_generated:
            print(dte.strptime("%d-%m-%Y"))
    return

printGraph()
"""# x axis values
x = [1, 2, 3]
# corresponding y axis values
y = [2, 4, 1]

# plotting the points
plt.plot(x, y)

# naming the x axis
plt.xlabel('x - axis')
# naming the y axis
plt.ylabel('y - axis')

# giving a title to my graph
plt.title('Dashboard')

# function to show the plot
plt.show()
"""
