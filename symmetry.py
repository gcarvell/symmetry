from tkinter import *
from tkinter import ttk
import random as r
import math

class App(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.title("4x4 Symmetries")
        self.gridSize = 4
        self.cellSize = 100
        self.canvasSize = self.cellSize*(self.gridSize)+200
        self.c = Canvas(width = self.canvasSize, height = self.canvasSize)
        self.c.pack()
        self.c.bind("<Button-1>", self.swapColour)
        self.addButton()
        self.displayStage = True
        self.gridStatus = []
        self.userGridStatus = []
        self.initGrid()
        self.userResult=[]

    def initGrid(self):
        self.whiteCount = 0
        self.blackCount = 0

        for i in range(0, self.gridSize):
            row = []
            userRow = []
            for j in range(0, self.gridSize):
                x1 = self.cellSize*(j+1)
                x2 = x1 + self.cellSize
                y1 = self.cellSize*(i+1)
                y2 = y1 + self.cellSize
                # col = self.colourPicker()
                self.c.create_rectangle(x1, y1, x2, y2, fill = "white", outline = "grey")
                row.append("white")
                userRow.append("white")
            self.gridStatus.append(row)
            self.userGridStatus.append(userRow)

    def addButton(self):
        self.generateBtn = ttk.Button(master = self, text = "Generate", command=self.drawGrid)
        self.generateBtn.pack()
        self.hideBtn = ttk.Button(master = self, text = "Hide", command=self.hideGrid)
        self.hideBtn.pack()
        self.submitBtn = ttk.Button(master = self, text = "Submit", state = DISABLED, command=self.check)
        self.submitBtn.pack()
        self.resetBtn = ttk.Button(master = self, text = "Reset", command=self.resetGrid)
        self.resetBtn.pack()

    def check(self):
        self.submitBtn.config(state=DISABLED)
        print("gridStatus: {}".format(self.gridStatus))
        print("userGridStatus: {}".format(self.userGridStatus))
        for i in range(0, self.gridSize):
            row = []
            for j in range(0, self.gridSize):
                if self.gridStatus[i][j]==self.userGridStatus[i][j]:
                    row.append(("Correct",self.userGridStatus[i][j]))
                else:
                    row.append(("Incorrect",self.userGridStatus[i][j]))
            self.userResult.append(row)
        print("self.userResult: {}".format(self.userResult))

    def swapColour(self, sq):
        try:
            if self.c.find_withtag(CURRENT)[0]:
                sq=self.c.find_withtag(CURRENT)[0]
            else:
                print("Out of bounds")
                return
            if not self.displayStage:
                #get fill colour for canvas item rect
                col = self.c.itemcget(sq,"fill")
                # if black, swap to white, vice versa
                if col=="black":
                    self.userWhiteCount +=1
                    self.userBlackCount -=1
                    newCol="white"
                else:
                    if self.userBlackCount >=self.gridSize**2/2:
                        print("No more black squares allowed")
                        newCol = "white"
                    else:
                        self.userBlackCount +=1
                        self.userWhiteCount -=1
                        newCol="black"
                self.c.itemconfig(sq,fill = newCol)

                for k in range(0, self.gridSize):
                    if sq < (k+1)*self.gridSize+1:
                        row = k
                        break
                if sq % self.gridSize == 0:
                    column = self.gridSize-1
                else:
                    column = sq %self.gridSize-1
                self.userGridStatus[row][column] = newCol

                if self.userBlackCount >=self.gridSize**2/2:
                    self.submitBtn.config(state=NORMAL)
                else:
                    self.submitBtn.config(state=DISABLED)
            else:
                print("Can't change colours in the display stage")
        except IndexError:
            pass

# Pick black or white at random
    def colourPicker(self):
        x=r.randint(1,2)
        if (self.whiteCount>=self.gridSize**2/2):
            x=2
        elif (self.blackCount>=self.gridSize**2/2):
            x=1
        if(x==1):
            self.whiteCount +=1
            col = "white"
        else:
            self.blackCount +=1
            col = "black"
        return(col)

    #Draw random 4x4 grid
    def drawGrid(self):
        self.gridStatus = []
        self.generateBtn.config(state=DISABLED)
        self.displayStage = True
        self.whiteCount = 0
        self.blackCount = 0
        k=0
        for i in range(0, self.gridSize):
            row = []
            for j in range(0, self.gridSize):
                k += 1
                x1 = self.cellSize*(j+1)
                x2 = x1 + self.cellSize
                y1 = self.cellSize*(i+1)
                y2 = y1 + self.cellSize
                col = self.colourPicker()
                self.c.itemconfig(k, fill = col)
                row.append(col)
            self.gridStatus.append(row)

    #Draw empty 4x4 grid
    def resetGrid(self):
        self.submitBtn.config(state=DISABLED)
        self.gridStatus = []
        self.hideGrid()

    def hideGrid(self):
        self.generateBtn.config(state=NORMAL)
        self.userWhiteCount = self.gridSize**2
        self.userBlackCount = 0
        self.displayStage = False
        print("On Hide gridStatus: {}".format(self.gridStatus))
        for i in range(1,(self.gridSize**2+1)):
            self.c.itemconfig(i,fill = "white")

app = App()
try:
    app.mainloop()
except (KeyboardInterrupt, SystemExit):
    raise