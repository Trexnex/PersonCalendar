#Import of libraries
import tkinter as tk
from supportFunctions import *
from tkcalendar import Calendar

#initialization of variables
HEIGHT = 350
WIDTH = 700
global month
month, year = getMonthAndYear()
frameList = []

#initialization of the main window and needed elements
core = tk.Tk() #initialization of the main window
core.title("Calendar") #title of the main window
core.geometry(str(WIDTH)+"x"+str(HEIGHT)) #size of the main window
core.resizable(False, False) #main window cannot be resized
picturelist = createPicturelist() #creation of the list of pictures
busypicturelist = createBusyPicturelist() #creation of the list of busy pictures
db, cs = createDatabase() #creation of the database
updateCalendar(core, frameList, picturelist, month, year, busypicturelist) #creation of the calendar


#mainloop and
startVarMonth = tk.StringVar()
startVarMonth.set(monthNames[month-1])
spinboxMonth = tk.Spinbox(core, values = monthNames, width=30, state = "readonly", textvariable = startVarMonth) #spinbox for the month
spinboxMonth.place(x=100, y=310)
startVarYear = tk.StringVar()
startVarYear.set(year)
spinboxYear = tk.Spinbox(core, from_ = 1800, to = 10000, width=30, state = "readonly", textvariable = startVarYear) #spinbox for the year
spinboxYear.place(x=300, y=310)
updateCalButton = tk.Button(core, text="Update", command= lambda: updateCalendar(core, frameList, picturelist
                                                                                , int(monthNames.index(spinboxMonth.get())+1),
                                                                                int(spinboxYear.get()), busypicturelist
                                                                                 ), height=2, width=10) #button to update the calendar
updateCalButton.place(x=500, y=310)
personDatabaseButton = tk.Button(core, text="Person Database", command= lambda: personDatabaseUI(0, db, cs), height=2, width=12) #button to open the person database
personDatabaseButton.place(x=600, y=310)

core.mainloop()