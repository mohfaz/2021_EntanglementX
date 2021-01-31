from tkinter import *
# TODO form something import somehting

class Cell():
    FILLED_COLOR_BG = "green"
    EMPTY_COLOR_BG = "white"
    FILLED_COLOR_BORDER = "green"
    EMPTY_COLOR_BORDER = "black"

    def __init__(self, master, x, y, size):
        """ Constructor of the object called by Cell(...) """
        self.master = master
        self.abs = x
        self.ord = y
        self.size= size
        self.fill= False

    def _switch(self):
        """ Switch if the cell is filled or not. """
        # self.fill= not self.fill
        self.fill = True
          
    def draw(self):
        """ order to the cell to draw its representation on the canvas """
        if self.master != None :
            fill = Cell.FILLED_COLOR_BG
            outline = Cell.FILLED_COLOR_BORDER

            if not self.fill:
                fill = Cell.EMPTY_COLOR_BG
                outline = Cell.EMPTY_COLOR_BORDER

            xmin = self.abs * self.size
            xmax = xmin + self.size
            ymin = self.ord * self.size
            ymax = ymin + self.size

            self.master.create_rectangle(xmin, ymin, xmax, ymax, fill = fill, outline = outline)

class CellGrid(Canvas):
    def __init__(self,master, rowNumber, columnNumber, cellSize, *args, **kwargs):
        Canvas.__init__(self, master, width = cellSize * columnNumber , height = cellSize * rowNumber, *args, **kwargs)

        self.cellSize = cellSize
        self.rowNumber = rowNumber
        self.columnNumber = columnNumber
        self.grid = []
        for row in range(rowNumber):

            line = []
            for column in range(columnNumber):
                line.append(Cell(self, column, row, cellSize))

            self.grid.append(line)

        #memorize the cells that have been modified to avoid many switching of state during mouse motion.
        self.switched = []

        #bind click action
        self.bind("<Button-1>", self.handleMouseClick)  
        #bind moving while clicking
        self.bind("<B1-Motion>", self.handleMouseMotion)
        #bind release button action - clear the memory of midified cells.
        self.bind("<ButtonRelease-1>", lambda event: self.switched.clear())

        self.draw()



    def draw(self):
        for row in self.grid:
            for cell in row:
                cell.draw()

    def _eventCoords(self, event):
        row = int(event.y / self.cellSize)
        column = int(event.x / self.cellSize)
        return row, column
    def putGate(self,root,str):
        print(str) # TODO you get the gate here
        root.destroy()
    def ask_gate(self):
        
        root = Tk()
        root.title("title")
    
        w = 400     # popup window width
        h = 400     # popup window height
    
        sw = root.winfo_screenwidth()
        sh = root.winfo_screenheight()
    
        x = (sw - w)/2
        y = (sh - h)/2
        root.geometry('%dx%d+%d+%d' % (w, h, x, y))
    
        w = Label(root, text="Please select your desired gate", width=120, height=10)
        w.pack()
        hadamardGate = Button(root, text="Hadamard Gate", command=lambda : self.putGate(root,'Hadamard is selected'), width=10).pack()
        groverGate   = Button(root, text="Grover Gate", command=lambda : self.putGate(root,'Grover is selected'), width=10).pack()
        otherGate    = Button(root, text="other Gate", command=lambda : self.putGate(root,'other gate is selected'), width=10).pack()
        
        mainloop()
    

    def handleMouseClick(self, event):
        row, column = self._eventCoords(event)
        
        # TODO your function that gets row and column 
        
        cell_list = list()
        for row_index in range(row - 1, row+2, 2):
            if row_index < 0 or row_index >= self.rowNumber :
                continue
            cell = self.grid[row_index][column]
            cell._switch()
            cell_list.append(cell)
         
        for column_index in range(column - 1, column+2, 2):
            if column_index < 0 or column_index >= self.columnNumber :
                continue
            # print(self.grid[0][0].fill)
            cell = self.grid[row][column_index]
            cell._switch()
            cell_list.append(cell)

        for element in cell_list :
            element.draw()      
            self.switched.append(element)
        window = Tk()
        window.wm_withdraw()
        self.ask_gate()
    
# #message at x:200,y:200
#         window.geometry("1x1+200+200")#remember its .geometry("WidthxHeight(+or-)X(+or-)Y")
#         # tkMessageBox.showerror(title="error",message="Error Message",parent=window)

# #centre screen message
#         window.geometry("1x1+"+str(window.winfo_screenwidth()/2)+"+"+str(window.winfo_screenheight()/2))
#         # tkMessageBox.showinfo(title="Greetings", message="Hello World!")
#         #add the cell to the list of cell switched during the click
        
    
    def handleMouseMotion(self, event):
        row, column = self._eventCoords(event)
        cell = self.grid[row][column]

        if cell not in self.switched:
            #cell._switch() # not sure what this do so I commented it 
            cell.draw()
            self.switched.append(cell)
    def neighbors(row,column):
        cordinates = list();
        

if __name__ == "__main__" :
    app = Tk()
   # num = int(input ("Enter number :") )
    num = 10
    grid = CellGrid(app, num, num, 100)
    grid.pack()

    app.mainloop()