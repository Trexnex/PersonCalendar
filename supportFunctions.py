import datetime
import tkinter as tk


def checkForLeap(year): #Returns if a years is a leap year or not.
    if (year%400 == 0 or year%4 == 0 and year % 100 != 0):
        return True
    else:
        return False

daysInMonths = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

print(datetime.date.fromisocalendar(2021, 52, 7))

def getMonthStartDay(year, month):
    return datetime.date(year, month, 1).weekday()

def generateCalendar(core):
    buttonList = []
    emptyImage = tk.PhotoImage(height=0, width=0)
    for i in range(6):
        coloumn = []
        for x in range(7):
            coloumn.append(tk.Button(core, text="Test", relief="flat", height = 50, width = 100, image=emptyImage, compound="center", borderwidth=0))
        buttonList.append(coloumn)
    return buttonList