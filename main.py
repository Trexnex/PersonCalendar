import tkinter as tk
from supportFunctions import *

HEIGHT = 350
WIDTH = 600


frameList = []
core = tk.Tk()
core.title("Calendar")
core.geometry(str(WIDTH)+"x"+str(HEIGHT))
core.resizable(False, False)

emptyImage = tk.PhotoImage(height=0, width=0)

frameList = generateCalendar(core)
print(frameList)
for x in range(6):
    for i in range(7):
        tk.Button(frameList[x][i], text="Test", command=print).pack(expand = True, fill = 'both', side=tk.LEFT)
        frameList[x][i].place(x= x*100, y = i*50)




core.mainloop()