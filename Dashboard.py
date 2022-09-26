# importing the required module
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from Base_de_donnée import *


def printGraph():
    with connection_DBase() as conn:
        c = conn.cursor()
        rSQL = ''' SELECT Temperature FROM DataHistory'''
        c.execute(rSQL)
        temp = c.fetchone()
        rSQL = ''' SELECT Humidity FROM DataHistory'''
        c.execute(rSQL)
        hum = c.fetchone()
        rSQL = ''' SELECT Date FROM DataHistory'''
        c.execute(rSQL)
        mdates = c.fetchone()


        print(temp[0])
        print(hum[0])
        print(str(date[0]))
        y = [2, 4, 1]
        plt.plot(temp[0],y)
        # naming the x axis
        plt.xlabel('x - time')
        # naming the y axis
        plt.ylabel('y - Temperature')
        plt.title('Dashboard')
        # function to show the plot
        plt.show()

    return
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
printGraph()