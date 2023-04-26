import tkinter as tk
from PIL import Image, ImageTk

root = tk.Tk()
img = ImageTk.PhotoImage(Image.open('sudokuboard.png'))
canvas = tk.Canvas(root, height=400, width=400)
canvas.pack()
canvas.create_image(202, 202, image=img)
preFilled = []

grid=[ [9,0,0, 1,7,0, 4,0,2],
       [1,6,0, 0,4,0, 0,9,5],
       [0,0,8, 0,0,3, 0,0,0],

       [0,1,0, 9,0,0, 5,7,3],
       [0,4,0, 0,0,0, 0,2,0],
       [5,8,9, 0,0,7, 0,1,0],

       [0,0,0, 4,0,0, 7,0,0],
       [6,7,0, 0,2,0, 0,5,8],
       [3,0,1, 0,5,8, 0,0,6]  ]

def getPreFilled():
    for rowIndex in range (9):
        for colIndex in range (9):
            if (grid[rowIndex][colIndex] != 0):
                preFilled.append(str(rowIndex)+str(colIndex))
                drawNumber(rowIndex,colIndex)


def drawNumber(r,c):
    canvas.delete("some_tag"+str(r)+str(c))
    root.update()
    canvas.create_text((r+1)*44-10,(c+1)*44-5, tag="some_tag"+str(r)+str(c),
        anchor="se", font="Times 20 bold", text=grid[r][c])
    root.update()

def cycleTest():
    for rowIndex in range (9):
        for colIndex in range (9):
            if (str(rowIndex)+str(colIndex) in preFilled):
                #drawNumber(rowIndex,colIndex)
                pass
            else:
                for i in range (500):
                    grid[rowIndex][colIndex] = i % 10
                    drawNumber(rowIndex,colIndex)


#getPreFilled()
#cycleTest()

root.mainloop()