import datetime
import math
import tkinter as tk
from PIL import Image, ImageDraw, ImageFont, ImageTk
import sqlite3

counter = -1

def getMonthAndYear():
    month = datetime.datetime.today().month
    year = datetime.datetime.today().year
    return month, year

def checkForLeap(year): #Returns if a years is a leap year or not.
    if (year%400 == 0 or year%4 == 0 and year % 100 != 0):
        return True
    else:
        return False

daysInMonths = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
monthNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]


def getMonthStartDay(year, month):
    return datetime.date(year, month, 1).weekday()

def generateCalendar(core):
    frameList = []
    for i in range(6):
        rows = []
        for x in range(7):
            temp = (tk.Frame(core, height = 50, width = 100))
            rows.append(temp)
        frameList.append(rows)
    return frameList

def frameClick(event, counter, daysInto):
    print(counter)
    event.widget['bg'] = "red"
    temp = str(event.widget)
    print(temp)
    temp = temp.replace(".!frame", "")
    temp = temp.replace(".!label", "")
    temp = int(temp) - (counter * 42)
    if temp == "":
        print([0, 0])
    else:
        temp = int(temp)
        print(temp-daysInto)
        xCoord = math.floor((temp-1)/7)
        yCoord = (temp-1)%7
        print([xCoord, yCoord])

def makeImage(nummer):
    font = ImageFont.truetype("arial.ttf", 50)
    tempImg = Image.new(mode="RGB", size=(100, 50), color=(255, 255, 255))
    editImg = ImageDraw.Draw(tempImg)
    editImg.text((0, 0), str(nummer), ("black"), font = font)
    return tempImg

def createPicturelist():
    pictureList = []
    for i in range(45):
        pictureList.append(ImageTk.PhotoImage(makeImage(i + 1)))
    return pictureList

def updateCalendar(core, frameList, pictureList, month, year):
    global counter
    counter += 1
    for i in frameList: #Clear the frame
        for x in i:
            x.destroy()
    print(core.winfo_children())
    for i in core.winfo_children(): #Clear the calendar
        if str(i).__contains__("frame"):
            i.destroy()
    frameList = generateCalendar(core) #Generate a new calendar
    y = 0
    y -= getMonthStartDay(year, month) - 1 #Get the start day of the month
    for i in range(6): #Place elements
        for x in range(7):
            if y > 0:
                if y < daysInMonths[month - 1] + 1:
                    frameList[i][x].place(y=i * 50, x=x * 100)
                    tempLabel = tk.Label(frameList[i][x], image=pictureList[y - 1])
                    tempLabel.bind("<Button-1>", lambda event, o = counter, daysInto = getMonthStartDay(year, month): frameClick(event, o, daysInto)) #Bind a command to left click when clicking on a day
                    tempLabel.pack()
            y += 1
def createDatabase(): #Creates a database
    db = sqlite3.connect("database.db")
    cs = db.cursor()
    cs.execute("CREATE TABLE IF NOT EXISTS people (name TEXT, nickname TEXT, birthday TEXT, adress TEXT, socialmedia TEXT, email TEXT, phone TEXT, birthdayWishes TEXT, work TEXT, knowsFrom TEXT, notes TEXT)")
    db.commit()
    return db, cs


def dbAdd(db, cs, name, nickname, birthday, adress, socialmedia, email, phone, birthdayWishes, work, knowsFrom, notes): #Adds a person to the database
    cs.execute("INSERT INTO people VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (name, nickname, birthday, adress, socialmedia, email, phone, birthdayWishes, work, knowsFrom, notes))
    db.commit()

def dbSearch(db, cs, name): #Searches for a person in the database
    cs.execute("SELECT * FROM people WHERE name LIKE ?", ("%"+name+"%",))
    return cs.fetchall()

def dbDelete(db, cs, name): #Deletes a person from the database
    cs.execute("DELETE FROM people WHERE name = ?", (name))
    db.commit()

def dbUpdate(db, cs, name, nickname, birthday, adress, socialmedia, email, phone, birthdayWishes, work, knowsFrom, notes): #Updates a person in the database
    cs.execute("UPDATE people SET nickname = ?, birthday = ?, address = ?, socialmedia = ?, email = ?, phone = ?, birthdayWishes = ?, work = ?, knowsFrom = ?, notes = ? WHERE name = ?", (nickname, birthday, adress, socialmedia, email, phone, birthdayWishes, work, knowsFrom, notes, name))
    db.commit()