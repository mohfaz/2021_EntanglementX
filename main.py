from tkinter import *
# TODO form something import somehting
import math
class Cell():
    
    FILLED_COLOR_BG = "green"
    FILLED_COLOR_SELECTED = "#594f4f"
    FILLED_COLOR_HADAMARD = "#Fe4a49"
    FILLED_COLOR_GROVER = "#2ab7ca"
    FILLED_COLOR_OTHER = "#fed766"
    
    EMPTY_COLOR_BG = "white"
    FILLED_COLOR_BORDER = "black"
    EMPTY_COLOR_BORDER = "black"
    
    cell_condtion = ['empty', 'selected', 'hadamard', 'grover', 'other']
    
    def __init__(self, master, x, y, size,boardSize):
        """ Constructor of the object called by Cell(...) """
        self.master = master
        self.abs = x
        self.ord = y
        self.size= size
        self.fill= 0
        self.boardSize = boardSize
        self.xoffset = 25;
        self.yoffset = 25;
        
    def _switch(self,condition_str):
        """ Switch if the cell is filled or not. """
        # self.fill= not self.fill
        if condition_str == self.cell_condtion[0]:
                self.fill = 0;
        if condition_str == self.cell_condtion[1]:
                self.fill = 1;
        if condition_str == self.cell_condtion[2]:
                self.fill = 2;
        if condition_str == self.cell_condtion[3]:
                self.fill = 3;
        if condition_str == self.cell_condtion[4]:
                self.fill = 4;
         
    def draw(self):
        """ order to the cell to draw its representation on the canvas """
        if self.master != None :
            # fill = Cell.FILLED_COLOR_BG
            outline = Cell.FILLED_COLOR_BORDER

            if  self.fill == 0:
                fill = Cell.EMPTY_COLOR_BG
                outline = Cell.EMPTY_COLOR_BORDER
            if  self.fill == 1:
                fill = Cell.FILLED_COLOR_SELECTED
                outline = Cell.FILLED_COLOR_BORDER
            if  self.fill == 2:
                fill = Cell.FILLED_COLOR_HADAMARD
                outline = Cell.FILLED_COLOR_BORDER
            if  self.fill == 3:
                fill = Cell.FILLED_COLOR_GROVER
                outline = Cell.FILLED_COLOR_BORDER
            if  self.fill == 4:
                fill = Cell.FILLED_COLOR_OTHER
                outline = Cell.FILLED_COLOR_BORDER
            
            xmin = self.abs * self.size + self.xoffset
            xmax = xmin + self.size/2
            ymin = self.ord * self.size + self.yoffset
            ymax = ymin + self.size/2
            # self.master.create_rectangle(xmin, ymin, xmax, ymax, fill = fill, outline = outline)
            if self.abs < math.ceil(self.boardSize)-1 :
                
                self.master.create_line(xmax, ymin+ self.size/4, xmax + xmax - xmin, ymin+ self.size/4)
            if self.ord < math.ceil(self.boardSize)-1 :
                self.master.create_line(xmin + self.size/4, ymax , xmin+ self.size/4 , ymax + ymax - ymin)            
            # if self.ord < math.ceil(self.boardSize/2):
                
            self.master.create_oval(xmin, ymin, xmax, ymax, fill = fill, outline = outline)

class CellGrid(Canvas):
    def __init__(self,master, rowNumber, columnNumber, cellSize, boardSize ,*args, **kwargs):
        Canvas.__init__(self, master, width = cellSize * columnNumber , height = cellSize * rowNumber, *args, **kwargs)
        
        self.xoffset = 25;
        self.yoffset = 25;
        self.cellSize = cellSize
        self.rowNumber = rowNumber
        self.columnNumber = columnNumber
        self.grid = []
        for row in range(rowNumber):

            line = []
            for column in range(columnNumber):
                line.append(Cell(self, column, row, cellSize,boardSize))

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
        y = event.y - self.yoffset
        x = event.x - self.xoffset
        
        row = int(event.y / self.cellSize)
        column = int(event.x / self.cellSize)
        
        ymin = column * self.cellSize
        c_x = ymin + self.cellSize/4
        xmin = row * self.cellSize
        c_y = xmin + self.cellSize/4
        if math.sqrt((c_x-x)**2+(c_y-y)**2) > 25:
            
            row = -1;
            column = -1;
        return row, column
    def putGate(self,root,str,cell):
        print(str) # TODO you get the gate here
        cell._switch(str)
        cell.draw()
        root.destroy()
    def ask_gate(self,cell):
        
        root = Toplevel()
        root.title("Gate selection")
    
        w = 400     # popup window width
        h = 400     # popup window height
    
        sw = root.winfo_screenwidth()
        sh = root.winfo_screenheight()
    
        x = (sw - w)/2
        y = (sh - h)/2
        root.geometry('%dx%d+%d+%d' % (w, h, x, y))
    
        w = Label(root, text="Please select your desired gate", width=120, height=10)
        w.pack()
        hadamardGate = Button(root, text="Hadamard Gate", command=lambda : self.putGate(root,'hadamard',cell), width=10).pack()
        groverGate   = Button(root, text="Grover Gate", command=lambda : self.putGate(root,'grover',cell), width=10).pack()
        otherGate    = Button(root, text="Other Gate", command=lambda : self.putGate(root,'other',cell), width=10).pack()
        cancel       = Button(root, text="Cancel", command=lambda : self.putGate(root,'empty',cell), width=10).pack()
        root.protocol("WM_DELETE_WINDOW", lambda : self.putGate(root,'empty',cell))

        root.mainloop()
    

    def handleMouseClick(self, event):
        row, column = self._eventCoords(event)
        if row == -1:
            return
        # TODO your function that gets row and column 
        cell = self.grid[row][column]
        if cell.fill != 0:
            return
        if cell.fill == 0:
            cell._switch('selected')
        # self.switched.append(cell)
        cell.draw()
        # cell_list = list()
        # for row_index in range(row - 1, row+2, 2):
        #     if row_index < 0 or row_index >= self.rowNumber :
        #         continue
        #     cell = self.grid[row_index][column]
        #     cell._switch()
        #     cell_list.append(cell)
         
        # for column_index in range(column - 1, column+2, 2):
        #     if column_index < 0 or column_index >= self.columnNumber :
        #         continue
        #     # print(self.grid[0][0].fill)
        #     cell = self.grid[row][column_index]
        #     cell._switch()
        #     cell_list.append(cell)

        # for element in cell_list :
        #     element.draw()      
        #     self.switched.append(element)
        # window = Tk()
        # window.wm_withdraw()
        self.ask_gate(cell)
    

    
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
    app.title("EntanglementX")
    num = int(input ("Enter number :") )
    
    grid = CellGrid(app, num, num, 100,num)
    grid.pack()

    app.mainloop()