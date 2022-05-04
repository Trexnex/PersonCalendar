import datetime
import math
import tkinter as tk
from PIL import Image, ImageDraw, ImageFont, ImageTk
import sqlite3
from icalendar import Calendar, Event
from tkinter import simpledialog

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

def frameClick(event, counter, daysInto, month, year):
    event.widget['bg'] = "red"
    temp = str(event.widget)
    temp = temp.replace(".!frame", "")
    temp = temp.replace(".!label", "")
    temp = int(temp) - (counter * 42)
#   if temp == "":
#       print([0, 0])
#   else:
#       temp = int(temp)
#       print(temp-daysInto)
#       xCoord = math.floor((temp-1)/7)
#       yCoord = (temp-1)%7
#       print([xCoord, yCoord])
    temp = (temp - daysInto)
    datePlanPopup(temp, month, year)

def makeImage(nummer, busy):
    font = ImageFont.truetype("arial.ttf", 50)
    if busy:
        tempImg = Image.new(mode="RGB", size=(100, 50), color=(200, 200, 200))
    else:
        tempImg = Image.new(mode="RGB", size=(100, 50), color=(255, 255, 255))
    editImg = ImageDraw.Draw(tempImg)
    editImg.text((0, 0), str(nummer), ("black"), font = font)
    return tempImg

def createPicturelist():
    pictureList = []
    for i in range(45):
        pictureList.append(ImageTk.PhotoImage(makeImage(i + 1, False)))
    return pictureList

def createBusyPicturelist():
    pictureList = []
    for i in range(45):
        pictureList.append(ImageTk.PhotoImage(makeImage(i + 1, True)))
    return pictureList

def updateCalendar(core, frameList, pictureList, month, year, busypicturelist):
    busyList = getBusyDays(month, year)
    if checkForLeap(year) and month == 2:
        dayInTheMonth = 29
    else:
        dayInTheMonth = daysInMonths[month - 1]
    global counter
    counter += 1
    for i in frameList: #Clear the frame
        for x in i:
            x.destroy()
    for i in core.winfo_children(): #Clear the calendar
        if str(i).__contains__("frame"):
            i.destroy()
    frameList = generateCalendar(core) #Generate a new calendar
    y = 0
    y -= getMonthStartDay(year, month) - 1 #Get the start day of the month
    for i in range(6): #Place elements
        for x in range(7):
            if y > 0:
                if y <= dayInTheMonth:
                    frameList[i][x].place(y=i * 50, x=x * 100)
                    if y in busyList:
                        tempLabel = tk.Label(frameList[i][x], image=busypicturelist[y - 1])
                    else:
                        tempLabel = tk.Label(frameList[i][x], image=pictureList[y - 1])
                    tempLabel.bind("<Button-1>", lambda event, o = counter, daysInto = getMonthStartDay(year, month), month = month, year = year: frameClick(event, o, daysInto, month, year)) #Bind a command to left click when clicking on a day
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
    cs.execute("DELETE FROM people WHERE name = ?", (name,))
    db.commit()

def dbUpdate(db, cs, name, nickname, birthday, adress, socialmedia, email, phone, birthdayWishes, work, knowsFrom, notes): #Updates a person in the database
    cs.execute("UPDATE people SET nickname = ?, birthday = ?, adress = ?, socialmedia = ?, email = ?, phone = ?, birthdayWishes = ?, work = ?, knowsFrom = ?, notes = ? WHERE name = ?", (nickname, birthday, adress, socialmedia, email, phone, birthdayWishes, work, knowsFrom, notes, name))
    db.commit()

def getBusyDays(month, year): #Returns a list of busy days in a month
    list = []
    data = open('calendarFile.ics', 'rb')
    cal = Calendar.from_ical(data.read())
    if len(str(month)) == 1:
        month = "0" + str(month)
    else:
        month = str(month)
    for events in cal.walk():
        if events.name == "VEVENT":
            temp = (events.get('dtstart').dt)
            temp = str(temp).split("-")
            if temp[1] == month and temp[0] == str(year):
                list.append(int(temp[2]))
    data.close()
    return list

def getEvent(day, month, year): #Returns the event of a day
    data = open('calendarFile.ics', 'rb')
    cal = Calendar.from_ical(data.read())
    if len(str(month)) == 1:
        month = "0" + str(month)
    else:
        month = str(month)
    if len(str(day)) == 1:
        day = "0" + str(day)
    else:
        day = str(day)
    for events in cal.walk():
        if events.name == "VEVENT":
            temp = (events.get('dtstart').dt)
            temp = str(temp).split("-")
            if temp[1] == month and temp[0] == str(year) and temp[2] == day:
                return events.get('summary')
    data.close()


def addEvent(day, month, year, plan): #Adds an plan to the calendar
    data = open('calendarFile.ics', 'rb')
    cal = Calendar.from_ical(data.read())
    data.close()
    event = Event()
    event.add('summary', plan)
    event.add('dtstart', datetime.date(year, month, day))
    cal.add_component(event)
    data = open('calendarFile.ics', 'wb')
    data.write(cal.to_ical())
    data.close()


def deleteEvent(day, month, year): #Deletes an event from the calendar
    data = open('calendarFile.ics', 'rb')
    cal = Calendar.from_ical(data.read())
    data.close()
    if len(str(month)) == 1:
        month = "0" + str(month)
    else:
        month = str(month)
    if len(str(day)) == 1:
        day = "0" + str(day)
    else:
        day = str(day)
    for events in cal.walk():
        if events.name == "VEVENT":
            temp = (events.get('dtstart').dt)
            temp = str(temp).split("-")
            if temp[1] == month and temp[0] == str(year) and temp[2] == day:
                cal.subcomponents.remove(events)
    data = open('calendarFile.ics', 'wb')
    data.write(cal.to_ical())
    data.close()

def datePlanPopup(day, month, year): #Shows a popup with the plan of a day
    plan = getEvent(day, month, year)
    if plan == None:
        plan = ""
    popup = tk.Tk()
    popup.title("Plan")
    popup.geometry("300x125")
    textWidget = tk.Text(popup, height=6, width=34)
    textWidget.insert(tk.END, plan)
    textWidget.pack()
    closeButton = tk.Button(popup, text="Close", command=lambda popup = popup, textField = textWidget, day = day,
                                                                month = month, year = year: closePopup(popup, textField, day, month, year), height=1, width=6)
    closeButton.place(x=150, y=100)
    popup.mainloop()


def closePopup(popup, textField, day, month, year): #Closes a popup
    value = textField.get("1.0", tk.END)
    if value == "" or value == "\n":
        deleteEvent(day, month, year)
    else:
        deleteEvent(day, month, year)
        addEvent(day, month, year, value)
    popup.destroy()

def createPermanentWidgets(popupUI, index, databaseOutput, db, cs): #Creates permanent widgets
    nameBox = tk.Text(popupUI, height=1, width=34)
    nameBox.insert(tk.END, databaseOutput[index][0])
    nameBox.place(x=10, y=30)
    nicknameBox = tk.Text(popupUI, height=5, width=34)
    nicknameBox.insert(tk.END, databaseOutput[index][1])
    nicknameBox.place(x=350, y=30)
    birthdayBox = tk.Text(popupUI, height=1, width=34)
    birthdayBox.insert(tk.END, databaseOutput[index][2])
    birthdayBox.place(x=10, y=100)
    adressBox = tk.Text(popupUI, height=1, width=34)
    adressBox.insert(tk.END, databaseOutput[index][3])
    adressBox.place(x=350, y=170)
    socialMediaBox = tk.Text(popupUI, height=5, width=34)
    socialMediaBox.insert(tk.END, databaseOutput[index][4])
    socialMediaBox.place(x=10, y=170)
    emailBox = tk.Text(popupUI, height=1, width=34)
    emailBox.insert(tk.END, databaseOutput[index][5])
    emailBox.place(x=350, y=240)
    phoneBox = tk.Text(popupUI, height=1, width=34)
    phoneBox.insert(tk.END, databaseOutput[index][6])
    phoneBox.place(x=10, y=310)
    birthdayWishesBox = tk.Text(popupUI, height=3, width=34)
    birthdayWishesBox.insert(tk.END, databaseOutput[index][7])
    birthdayWishesBox.place(x=350, y=310)
    workBox = tk.Text(popupUI, height=1, width=34)
    workBox.insert(tk.END, databaseOutput[index][8])
    workBox.place(x=10, y=380)
    knowsFromBox = tk.Text(popupUI, height=1, width=34)
    knowsFromBox.insert(tk.END, databaseOutput[index][9])
    knowsFromBox.place(x=350, y=380)
    notesBox = tk.Text(popupUI, height=5, width=80)
    notesBox.insert(tk.END, databaseOutput[index][10])
    notesBox.place(x=10, y=450)

    nameLabel = tk.Label(popupUI, text="Name:")
    nameLabel.place(x=10, y=5)
    nicknameLabel = tk.Label(popupUI, text="Nickname:")
    nicknameLabel.place(x=350, y=5)
    birthdayLabel = tk.Label(popupUI, text="Birthday:")
    birthdayLabel.place(x=10, y=75)
    phoneLabel = tk.Label(popupUI, text="Phone:")
    phoneLabel.place(x=10, y=285)
    emailLabel = tk.Label(popupUI, text="Email:")
    emailLabel.place(x=350, y=215)
    addressLabel = tk.Label(popupUI, text="Address:")
    addressLabel.place(x=350, y=145)
    socialMediaLabel = tk.Label(popupUI, text="Social Media:")
    socialMediaLabel.place(x=10, y=145)
    birthdayWishesLabel = tk.Label(popupUI, text="Birthday Wishes:")
    birthdayWishesLabel.place(x=350, y=285)
    workLabel = tk.Label(popupUI, text="Work:")
    workLabel.place(x=10, y=365)
    knowsFromLabel = tk.Label(popupUI, text="Knows From:")
    knowsFromLabel.place(x=350, y=365)
    NotesLabel = tk.Label(popupUI, text="Notes:")
    NotesLabel.place(x=10, y=425)
    searchEntry = tk.Entry(popupUI, width=20)
    searchEntry.place(x=10, y=550)
    if index != len(databaseOutput)-1:
        nextIndexButton = tk.Button(popupUI, text="Next", command=lambda popupUI=popupUI, index=int(index) + 1,databaseOutput=databaseOutput, db = db, cs = cs: newData(popupUI,databaseOutput,index, db, cs),height=1, width=6)
        nextIndexButton.place(x=400, y=550)
    searchButton = tk.Button(popupUI, text="Search", command=lambda popupUI = popupUI, index = 0, searchTerm = searchEntry, db = db, cs = cs: newSearchData(popupUI, searchTerm, index, db, cs), height=1, width=6)
    searchButton.place(x=150, y=550)
    indexLabel = tk.Label(popupUI, text=str(index))
    indexLabel.place(x=350, y=550)
    if index != 0:
        previousIndexButton = tk.Button(popupUI, text="Previous", command=lambda popupUI=popupUI, index=int(index) - 1,databaseOutput=databaseOutput, db = db, cs = cs: newData(popupUI, databaseOutput, index, db, cs), height=1, width=6)
        previousIndexButton.place(x=300, y=550)
    deleteButton = tk.Button(popupUI, text="Delete", command=lambda popupUI = popupUI, index = index, databaseOutput = databaseOutput, db = db, cs = cs: deletePerson(popupUI, index, databaseOutput, db, cs), height=1, width=6)
    deleteButton.place(x=450, y=550)
    updateButton = tk.Button(popupUI, text="Update", command=lambda db = db, cs = cs, name = nameBox, nickname = nicknameBox, birthday = birthdayBox, address = adressBox, socialmedia = socialMediaBox, email = emailBox, phone = phoneBox, birthdaywishes = birthdayWishesBox, work = workBox, knowsfrom = knowsFromBox, notes= notesBox, index = index, databaseOutput = databaseOutput: updatePerson(db, cs, name, nickname, birthday, address, socialmedia, email, phone, birthdaywishes, work, knowsfrom, notes, index, databaseOutput), height=1, width=6)
    updateButton.place(x=500, y=550)
    addButton = tk.Button(popupUI, text="Add", command=lambda popupUI = popupUI, db = db, cs = cs: addPage(popupUI, db, cs), height=1, width=6)
    addButton.place(x=550, y=550)


def personDatabaseUI(startIndex, db, cs):
    #sql categories
    #name, nickname, birthday, address, socialmeadia, email, phone, birthdayWishes, work, knowsFrom, notes

    index = startIndex
    popupUI = tk.Tk()
    popupUI.title("Person Database")
    popupUI.geometry("700x600")
    popupUI.resizable(False, False)
    databaseOutput = dbSearch(db, cs, "")
    createPermanentWidgets(popupUI, index, databaseOutput, db, cs)


def clearPopup(popupUI):
    for widget in popupUI.winfo_children():
        widget.destroy()

def newData(popupUI, databaseOutput, index, db, cs):
    clearPopup(popupUI)
    createPermanentWidgets(popupUI, index, databaseOutput, db, cs)

def newSearchData(popupUI, searchTerm, index, db, cs):
    databaseOutput = dbSearch(db, cs, searchTerm.get())
    print(databaseOutput)
    if databaseOutput != []:
        clearPopup(popupUI)
        createPermanentWidgets(popupUI, index, databaseOutput, db, cs)

def deletePerson(popupUI, index, databaseOutput, db, cs):
    print(type(databaseOutput[index][0]))
    dbDelete(db, cs, databaseOutput[index][0])

def updatePerson(db, cs, name, nickname, birthday, address, socialMedia, email, phone, birthdayWishes, work, knowsFrom, notes, index, databaseOutput):
    dbUpdate(db, cs, databaseOutput[index][0], nickname.get("1.0", tk.END), birthday.get("1.0", tk.END), address.get("1.0", tk.END), socialMedia.get("1.0", tk.END), email.get("1.0", tk.END), phone.get("1.0", tk.END), birthdayWishes.get("1.0", tk.END), work.get("1.0", tk.END), knowsFrom.get("1.0", tk.END), notes.get("1.0", tk.END))

def addPage(popupUI, db, cs):
    temp = tk.simpledialog.askstring("Add new person", "Enter name:", parent=popupUI)
    dbAdd(db, cs, temp, "", "", "", "", "", "", "", "", "", "")

