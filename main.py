import tkinter as tk
from supportFunctions import *
from tkcalendar import Calendar

HEIGHT = 350
WIDTH = 700
global month



month, year = getMonthAndYear()
print(getMonthStartDay(year, month ))
frameList = []
core = tk.Tk()
core.title("Calendar")
core.geometry(str(WIDTH)+"x"+str(HEIGHT))
core.resizable(False, False)
picturelist = createPicturelist()
db, cs = createDatabase()
#dbAdd(db, cs, "nam", "nicknam", "birthda", "addres", "socialmeadi", "emai", "phon", "birthdayWishe", "wor", "knowsFro", "note")


for s in (dbSearch(db, cs, "")):
    print(s)



updateCalendar(core, frameList, picturelist, month, year)

startVarMonth = tk.StringVar()
startVarMonth.set(monthNames[month-1])
spinboxMonth = tk.Spinbox(core, values = monthNames, width=30, state = "readonly", textvariable = startVarMonth)
spinboxMonth.place(x=100, y=310)
startVarYear = tk.StringVar()
startVarYear.set(year)
spinboxYear = tk.Spinbox(core, from_ = 1800, to = 10000, width=30, state = "readonly", textvariable = startVarYear)
spinboxYear.place(x=300, y=310)
updateCalButton = tk.Button(core, text="Update", command= lambda: updateCalendar(core, frameList, picturelist
                                                                                , int(monthNames.index(spinboxMonth.get())+1),
                                                                                int(spinboxYear.get())), height=2, width=10)
updateCalButton.place(x=500, y=310)


core.mainloop()