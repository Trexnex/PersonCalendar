#Import of libraries
import datetime
import math
import tkinter as tk
from PIL import Image, ImageDraw, ImageFont, ImageTk
import sqlite3
from icalendar import Calendar, Event
from tkinter import simpledialog

#initialize the variables
counter = -1
daysInMonths = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
monthNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

def getMonthAndYear(): #Returns the current month and year
    month = datetime.datetime.today().month
    year = datetime.datetime.today().year
    return month, year

def checkForLeap(year): #Returns if a year is a leap year or not.
    if (year%400 == 0 or year%4 == 0 and year % 100 != 0):
        return True
    else:
        return False

def getMonthStartDay(year, month): #Returns the day of the week the month starts on
    return datetime.date(year, month, 1).weekday()

def generateCalendar(core): #Generates the calendar
    frameList = []
    for i in range(6):#Makes a 2d list of frames
        rows = []
        for x in range(7):
            temp = (tk.Frame(core, height = 50, width = 100))
            rows.append(temp)
        frameList.append(rows)
    return frameList

def frameClick(event, counter, daysInto, month, year): #When a frame is clicked run this function and open plans for the day
    temp = str(event.widget)
    temp = temp.replace(".!frame", "")
    temp = temp.replace(".!label", "")
    temp = int(temp) - (counter * 42) #removes all text and only leaves the number. From the number the amount of times the calendar has been updated is removed.
#   if temp == "":
#       print([0, 0])
#   else:
#       temp = int(temp)
#       print(temp-daysInto)
#       xCoord = math.floor((temp-1)/7)
#       yCoord = (temp-1)%7
#       print([xCoord, yCoord])
    temp = (temp - daysInto)
    datePlanPopup(temp, month, year) #Opens the popup for the day

def makeImage(nummer, busy): #Makes an image for the calendar
    font = ImageFont.truetype("arial.ttf", 50)
    if busy: #If the day is busy make it gray
        tempImg = Image.new(mode="RGB", size=(100, 50), color=(200, 200, 200))
    else:
        tempImg = Image.new(mode="RGB", size=(100, 50), color=(255, 255, 255))
    editImg = ImageDraw.Draw(tempImg)
    editImg.text((0, 0), str(nummer), ("black"), font = font) #Draws the number on the image
    return tempImg

def createPicturelist(): #Creates a list of pictures
    pictureList = []
    for i in range(45):
        pictureList.append(ImageTk.PhotoImage(makeImage(i + 1, False)))
    return pictureList

def createBusyPicturelist(): #Creates a list of pictures for the busy days
    pictureList = []
    for i in range(45):
        pictureList.append(ImageTk.PhotoImage(makeImage(i + 1, True)))
    return pictureList

def updateCalendar(core, frameList, pictureList, month, year, busypicturelist): #Updates the calendar
    busyList = getBusyDays(month, year) #Gets the busy days
    if checkForLeap(year) and month == 2: #If the month is february and the year is a leap year, make the 29th day
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
    for i in range(6): #Place elements from 2d list in the calendar
        for x in range(7):
            if y > 0: #starts at the first day of the month
                if y <= dayInTheMonth:#If the day is in the month
                    frameList[i][x].place(y=i * 50, x=x * 100) #Place the frame
                    if y in busyList: #If the day is busy make the image red
                        tempLabel = tk.Label(frameList[i][x], image=busypicturelist[y - 1])
                    else:
                        tempLabel = tk.Label(frameList[i][x], image=pictureList[y - 1])
                    tempLabel.bind("<Button-1>", lambda event, o = counter, daysInto = getMonthStartDay(year, month), month = month, year = year: frameClick(event, o, daysInto, month, year)) #Bind a command to left click when clicking on a day
                    tempLabel.pack()
            y += 1

def createDatabase(): #Creates a database
    db = sqlite3.connect("database.db") #Connect to the database
    cs = db.cursor() #Create a cursor
    cs.execute("CREATE TABLE IF NOT EXISTS people (name TEXT, nickname TEXT, birthday TEXT, adress TEXT, socialmedia TEXT, email TEXT, phone TEXT, birthdayWishes TEXT, work TEXT, knowsFrom TEXT, notes TEXT)") #Create a table if it doesn't exist
    db.commit()
    return db, cs


def dbAdd(db, cs, name, nickname, birthday, adress, socialmedia, email, phone, birthdayWishes, work, knowsFrom, notes): #Adds a person to the database
    cs.execute("INSERT INTO people VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (name, nickname, birthday, adress, socialmedia, email, phone, birthdayWishes, work, knowsFrom, notes)) #Insert the person into the database
    db.commit()

def dbSearch(db, cs, name): #Searches for a person in the database
    cs.execute("SELECT * FROM people WHERE name LIKE ?", ("%"+name+"%",)) #Search for the person
    return cs.fetchall()

def dbDelete(db, cs, name): #Deletes a person from the database
    cs.execute("DELETE FROM people WHERE name = ?", (name,)) #Delete the person
    db.commit()

def dbUpdate(db, cs, name, nickname, birthday, adress, socialmedia, email, phone, birthdayWishes, work, knowsFrom, notes): #Updates a person in the database
    cs.execute("UPDATE people SET nickname = ?, birthday = ?, adress = ?, socialmedia = ?, email = ?, phone = ?, birthdayWishes = ?, work = ?, knowsFrom = ?, notes = ? WHERE name = ?", (nickname, birthday, adress, socialmedia, email, phone, birthdayWishes, work, knowsFrom, notes, name)) #Update the person
    db.commit()

def getBusyDays(month, year): #Returns a list of busy days in a month
    list = []
    data = open('calendarFile.ics', 'rb') #Open the file
    cal = Calendar.from_ical(data.read()) #Read the file
    if len(str(month)) == 1: #If the month is only one digit add a 0 to the beginning
        month = "0" + str(month)
    else:
        month = str(month)
    for events in cal.walk(): #Walk through the file
        if events.name == "VEVENT": #If the events name is a event
            temp = (events.get('dtstart').dt) #Get the date
            temp = str(temp).split("-") #Split the date
            if temp[1] == month and temp[0] == str(year): #If the month and year are the same as the active month and year
                list.append(int(temp[2])) #Add the day to the list
    data.close() #Close the file
    return list

def getEvent(day, month, year): #Returns the event of a day
    data = open('calendarFile.ics', 'rb') #Open the file
    cal = Calendar.from_ical(data.read()) #Read the file
    if len(str(month)) == 1: #If the month is only one digit add a 0 to the beginning
        month = "0" + str(month)
    else:
        month = str(month)
    if len(str(day)) == 1: #If the day is only one digit add a 0 to the beginning
        day = "0" + str(day)
    else:
        day = str(day)
    for events in cal.walk(): #Walk through the file
        if events.name == "VEVENT":#If the events name is a event
            temp = (events.get('dtstart').dt) #Get the date
            temp = str(temp).split("-") #Split the date
            if temp[1] == month and temp[0] == str(year) and temp[2] == day: #If the month, year and day are the same as the active month, year and day
                return events.get('summary') #Return the event
    data.close()


def addEvent(day, month, year, plan): #Adds an plan to the calendar
    data = open('calendarFile.ics', 'rb') #Open the file
    cal = Calendar.from_ical(data.read()) #Read the file
    data.close()
    event = Event() #Create a new event
    event.add('summary', plan) #Add the plan
    event.add('dtstart', datetime.date(year, month, day)) #Add the date
    cal.add_component(event) #Add the event to the calendar
    data = open('calendarFile.ics', 'wb') #Open the file
    data.write(cal.to_ical()) #Write the calendar to the file
    data.close()


def deleteEvent(day, month, year): #Deletes an event from the calendar
    data = open('calendarFile.ics', 'rb') #Open the file
    cal = Calendar.from_ical(data.read()) #Read the file
    data.close()
    if len(str(month)) == 1: #If the month is only one digit add a 0 to the beginning
        month = "0" + str(month)
    else:
        month = str(month)
    if len(str(day)) == 1: #If the day is only one digit add a 0 to the beginning
        day = "0" + str(day)
    else:
        day = str(day)
    for events in cal.walk(): #Walk through the file
        if events.name == "VEVENT": #If the events name is a event
            temp = (events.get('dtstart').dt) #Get the date
            temp = str(temp).split("-")     #Split the date
            if temp[1] == month and temp[0] == str(year) and temp[2] == day: #If the month, year and day are the same as the active month, year and day
                cal.subcomponents.remove(events) #Remove the event
    data = open('calendarFile.ics', 'wb') #Open the file
    data.write(cal.to_ical()) #Write the calendar to the file
    data.close()

def datePlanPopup(day, month, year): #Shows a popup with the plan of a day
    plan = getEvent(day, month, year)   #Get the plan of the day
    if plan == None: #If there is no plan
        plan = ""
    popup = tk.Tk() #Create a new window
    popup.title("Plan") #Set the title
    popup.geometry("300x125") #Set the size
    textWidget = tk.Text(popup, height=6, width=34) #Create a text widget
    textWidget.insert(tk.END, plan) #Insert the plan
    textWidget.pack()
    closeButton = tk.Button(popup, text="Close", command=lambda popup = popup, textField = textWidget, day = day,
                                                                month = month, year = year: closePopup(popup, textField, day, month, year), height=1, width=6) #Create a close button with a command that closes the popup
    closeButton.place(x=150, y=100) #Place the close button
    popup.mainloop() #Start the window


def closePopup(popup, textField, day, month, year): #Closes a popup
    value = textField.get("1.0", tk.END) #Get the value of the text widget
    if value == "" or value == "\n": #If there is no plan
        deleteEvent(day, month, year) #Delete the event
    else: #If there is a plan
        deleteEvent(day, month, year) #Delete the old plan
        addEvent(day, month, year, value) #Add the new plan
    popup.destroy() #Destroy the popup

def createPermanentWidgets(popupUI, index, databaseOutput, db, cs): #Creates widgets
    nameBox = tk.Text(popupUI, height=1, width=34)  #Create a text widget
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
    if index != len(databaseOutput)-1: #If the index is not the last one in the database create a button to go to the next person
        nextIndexButton = tk.Button(popupUI, text="Next", command=lambda popupUI=popupUI, index=int(index) + 1,databaseOutput=databaseOutput, db = db, cs = cs: newData(popupUI,databaseOutput,index, db, cs),height=1, width=6) #Create a button to go to the next index
        nextIndexButton.place(x=400, y=550) #Place the button
    searchButton = tk.Button(popupUI, text="Search", command=lambda popupUI = popupUI, index = 0, searchTerm = searchEntry, db = db, cs = cs: newSearchData(popupUI, searchTerm, index, db, cs), height=1, width=6) #Create a button to search for a specific entry
    searchButton.place(x=150, y=550)  #Place the button
    indexLabel = tk.Label(popupUI, text=str(index)) #Create a label to show the index
    indexLabel.place(x=350, y=550) #Place the label
    if index != 0: #If the index is not the first one (0) then create a button to go to the previous index
        previousIndexButton = tk.Button(popupUI, text="Previous", command=lambda popupUI=popupUI, index=int(index) - 1,databaseOutput=databaseOutput, db = db, cs = cs: newData(popupUI, databaseOutput, index, db, cs), height=1, width=6) #Create a button to go to the previous index
        previousIndexButton.place(x=300, y=550) #Place the button
    deleteButton = tk.Button(popupUI, text="Delete", command=lambda popupUI = popupUI, index = index, databaseOutput = databaseOutput, db = db, cs = cs: deletePerson(popupUI, index, databaseOutput, db, cs), height=1, width=6) #Create a button to delete the current person
    deleteButton.place(x=450, y=550)#Place the button
    updateButton = tk.Button(popupUI, text="Update", command=lambda db = db, cs = cs, name = nameBox, nickname = nicknameBox, birthday = birthdayBox, address = adressBox, socialmedia = socialMediaBox, email = emailBox, phone = phoneBox, birthdaywishes = birthdayWishesBox, work = workBox, knowsfrom = knowsFromBox, notes= notesBox, index = index, databaseOutput = databaseOutput: updatePerson(db, cs, name, nickname, birthday, address, socialmedia, email, phone, birthdaywishes, work, knowsfrom, notes, index, databaseOutput), height=1, width=6) #Create a button to update the current person
    updateButton.place(x=500, y=550) #Place the button
    addButton = tk.Button(popupUI, text="Add", command=lambda popupUI = popupUI, db = db, cs = cs: addPage(popupUI, db, cs), height=1, width=6) #Create a button to add a new person page
    addButton.place(x=550, y=550) #Place the button


def personDatabaseUI(index, db, cs):
    #sql categories
    #name, nickname, birthday, address, socialmeadia, email, phone, birthdayWishes, work, knowsFrom, notes
    popupUI = tk.Tk() #Create a new window
    popupUI.title("Person Database") #Set the title
    popupUI.geometry("700x600") #Set the size
    popupUI.resizable(False, False) #Make the window un-resizable
    databaseOutput = dbSearch(db, cs, "") #Get the database output
    createPermanentWidgets(popupUI, index, databaseOutput, db, cs) #Create the widgets


def clearPopup(popupUI): #Clear the popup window
    for widget in popupUI.winfo_children(): #For each widget in the window
        widget.destroy() #Destroy the widget

def newData(popupUI, databaseOutput, index, db, cs): #update the data in the window
    clearPopup(popupUI) #Clear the popup window
    createPermanentWidgets(popupUI, index, databaseOutput, db, cs) #Create the widgets

def newSearchData(popupUI, searchTerm, index, db, cs): #update the data in the window with a search term
    databaseOutput = dbSearch(db, cs, searchTerm.get()) #Get the database output
    if databaseOutput != []: #If the database output is not empty
        clearPopup(popupUI) #Clear the popup window
        createPermanentWidgets(popupUI, index, databaseOutput, db, cs) #Create the widgets with the new output

def deletePerson(popupUI, index, databaseOutput, db, cs): #delete the current person
    dbDelete(db, cs, databaseOutput[index][0]) #Delete the current person

def updatePerson(db, cs, name, nickname, birthday, address, socialMedia, email, phone, birthdayWishes, work, knowsFrom, notes, index, databaseOutput): #update the current person
    dbUpdate(db, cs, databaseOutput[index][0], nickname.get("1.0", tk.END), birthday.get("1.0", tk.END), address.get("1.0", tk.END), socialMedia.get("1.0", tk.END), email.get("1.0", tk.END), phone.get("1.0", tk.END), birthdayWishes.get("1.0", tk.END), work.get("1.0", tk.END), knowsFrom.get("1.0", tk.END), notes.get("1.0", tk.END)) #Update the current person

def addPage(popupUI, db, cs): #add a new person page
    temp = tk.simpledialog.askstring("Add new person", "Enter name:", parent=popupUI) #Ask the user for the name of the new person to add to the database with a dialog box
    dbAdd(db, cs, temp, "", "", "", "", "", "", "", "", "", "") #Add the new person to the database with the name the user entered

