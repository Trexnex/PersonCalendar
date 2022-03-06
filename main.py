import tkinter as tk
from supportFunctions import *

HEIGHT = 350
WIDTH = 600

buttonList = []
core = tk.Tk()
core.title("Calendar")
core.geometry(str(WIDTH)+"x"+str(HEIGHT))
core.resizable(False, False)

buttonList = generateCalendar(core)
print(buttonList)
for x in range(6):
    for i in range(7):
        buttonList[x][i].place(x= x*100, y = i*50)


core.mainloop()