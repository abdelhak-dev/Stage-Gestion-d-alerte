# importing the required module
import matplotlib.pyplot as plt
import sqlite3
from sqlite3 import Error
from pathlib import Path
from datetime import datetime

def printGraph():
    with connection_DBase()as conn:
        c = conn.cursor
        rSQL = '''SELECT Temperature FROM DataHistory'''
        c.excute(rSQL)
        Temperature = conn.fe
    return
# x axis values
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