from tkinter import *
from json import dumps

L = []

class B(Button):
    def __init__(self, master, x, y):
        super().__init__(master)
        self.x = x
        self.y = y
        self.status = 0
        self.config(command=self.changeStatus)

    def changeStatus(self):
        if self.status == 0:
            globals()['L'][self.x][self.y] = 1
            self.status = 1
            self.config(bg="green")
        else:
            globals()['L'][self.x][self.y] = 0
            self.status = 0
            self.config(bg="red")

class W(Tk):
    def __init__(self):
        super().__init__()

        self.geometry("300x300")
        self.title("")

        self.b1 = Entry(self, width=5)
        self.b2 = Entry(self, width=5)

        self.bMake = Button(self, command=self.makeButtons, text="YES")
        self.bSubmit = Button(self, command=self.createFile, text="SUBMIT")

        self.GRID = Frame(self,)

        self.b1.pack()
        self.b2.pack()

        self.bMake.pack()

        self.GRID.pack()

        self.bSubmit.pack()

    

    def makeButtons(self):
        try:
            a = int(self.b1.get())
        except ValueError:
            a = 5
        try:
            b = int(self.b2.get())
        except ValueError:
            b = 5

        globals()['L'] = [list([0]*b) for _ in range(a)]

        for y in range(b):
            for x in range(a):
                button = (lambda x, y: B(self.GRID, x=x, y=y))(x, y)
                button.grid(row=x, column=y)

    def changeBStatus(self):
        pass

    def createFile(self):
        l = globals()['L']
        try:
            with open("data.json", "w") as f:
                f.write(dumps(l))
        except FileNotFoundError:
            with open("data.json", "x") as f:
                f.write(dumps(l))

Main = W()
Main.mainloop()
