import datetime

def ddate():
    date = datetime.datetime.now().date()
    print(date)

def dtime():
    time = datetime.datetime.now().timetz()
    print(time)
print(dtime())