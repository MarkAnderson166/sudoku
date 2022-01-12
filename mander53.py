# ------------------------------------------------------------
# --------  Mark Anderson  ------  220180473  ----------------
# -------------  UNE  -------  Cosc350 Assignment 1  ---------
# ----------------------  AI Sudoku   ------------------------
# ------------------------------------------------------------

# This is intended to be a HILL CLIMB style algorythm
# First an initial attempt is made following the basic rules of the game
#           main function: fillGrid()
# Then problems with the solution are searched for and corrected
#           main function: zeroHunter()
# If found problems are not resolved in a short time, fillGrid() is re-run
# both main functions primarly use the choose() function.

# Please note, Python is be no means my first language.
# I haven't used python at all besides cosc110 3 years ago,
# I really shouldn't have picked it for this assignment.
# 2D arrays being passed by reference, was ... an issue.

import tkinter as tk
import random

root = tk.Tk()
root.title("Cosc350 Assignment 1")
canvas = tk.Canvas(root, height=440, width=520)
canvas.pack()

preFilled = []
boxArray  = []
possibles = [1,2,3, 4,5,6, 7,8,9]

startGrid = [[9,0,0, 1,7,0, 4,0,2],
             [1,6,0, 0,4,0, 0,9,5],
             [0,0,8, 0,0,3, 0,0,0],

             [0,1,0, 9,0,0, 5,7,3],
             [0,4,0, 0,0,0, 0,2,0],
             [5,8,9, 0,0,7, 0,1,0],

             [0,0,0, 4,0,0, 7,0,0],
             [6,7,0, 0,2,0, 0,5,8],
             [3,0,1, 0,5,8, 0,0,6]] 

# below is the 'can't be solved by AI' puzzle  (it can't)
#startGrid =[[8,0,0, 0,0,0, 0,0,0],
#            [0,0,3, 6,0,0, 0,0,0],
#            [0,7,0, 0,9,0, 2,0,0],

#            [0,5,0, 0,0,7, 0,0,0],
#            [0,0,0, 0,4,5, 7,0,0],
#            [0,0,0, 1,0,0, 0,3,0],

#            [0,0,1, 0,0,0, 0,6,8],
#            [0,0,8, 5,0,0, 0,1,0],
#            [0,9,0, 0,0,0, 4,0,0]]

grid =[     [0,0,0, 0,0,0, 0,0,0],
            [0,0,0, 0,0,0, 0,0,0],
            [0,0,0, 0,0,0, 0,0,0],

            [0,0,0, 0,0,0, 0,0,0],
            [0,0,0, 0,0,0, 0,0,0],
            [0,0,0, 0,0,0, 0,0,0],

            [0,0,0, 0,0,0, 0,0,0],
            [0,0,0, 0,0,0, 0,0,0],
            [0,0,0, 0,0,0, 0,0,0]]


# ------------------------------------------------- #
# ------ setup and basic functions start here ----- #
# ------------------------------------------------- # 

def drawNumber(r,c):
      # does what it says on the tin,
      # its important to clear old number first, hence the 'tags'
    canvas.delete("color"+str(r)+str(c))
    canvas.delete("tag"+str(r)+str(c))
    root.update()
    number = grid[r][c]
    if number == 0 :
        number = " "
        boxcolor = "red"
    elif str(r)+str(c) in preFilled:
        boxcolor = "orange"
    else: 
        boxcolor = "pink"
    canvas.create_rectangle(6+c*44, 6+r*44, 47+c*44, 47+r*44, width=0,
            outline=boxcolor, fill=boxcolor, tag="color"+str(r)+str(c))
    canvas.create_text((c+1)*44-10,(r+1)*44-5, tag="tag"+str(r)+str(c),
            anchor="se", font="Times 20 bold", text=number)
    root.update()

def copyGrid(hard):
      # copying done with loops, you would think
      # that 'grid=startGrid' would do this... but no.
    for rowIndex in range (9):
            for colIndex in range (9):
                grid[rowIndex][colIndex] = startGrid[rowIndex][colIndex]

      # hard(er) mode just clears a few rows BEFORE prefilled is generated
    random.shuffle(possibles)
    blanks = possibles.copy()[:hard]
    for i in blanks:
        for j in range (9):
            grid[i-1][j] = 0

      # gather location within grid of pre-filled boxes
      # global variable 'preFilled' is a 1D array 
      # of 2 digit strings ie. ["00", "26", "88"]
    for rowIndex in range (9):
        for colIndex in range (9):
            if (grid[rowIndex][colIndex] != 0):
                preFilled.append(str(rowIndex)+str(colIndex))
                drawNumber(rowIndex,colIndex)

def clearGrid():
      # clearing done with loops, you would think
      # that 'grid= startGrid' would do this... but no.
    for rowIndex in range (9):
        for colIndex in range (9):
            if (str(rowIndex)+str(colIndex) in preFilled ):
                pass
            else:
                toGoIn = 0
                grid[rowIndex][colIndex] = toGoIn
                drawNumber(rowIndex,colIndex)

def makeBox(boxR,boxC):
      # We need to check contents of an element's 'box' 
      # but there is no such data struture, so we need to make one.
      # Its a surprizingly nasty bit of math.
    boxR = (boxR // 3)*3
    boxC = (boxC // 3)*3
    boxArray.clear()
    for j in range(3):
        for k in range(3):
            boxArray.append(grid[j+boxR][k+boxC])

def getGridScore(passedGrid):
      # Get the 'score' of the current grid
      # just counts how many blank boxes their are.
    total = 0
    for i in range (9):
        for j in range (9):
            if passedGrid[i][j] > 0:
                total += 1
    return total


# ------------------------------------------------- #
# -------- GUI and Text functions start here ------ #
# ------------------------------------------------- # 

def drawString(textMes):
      # Draws the little messages in the bottom left
      # ie. 'this is taking too long' and the finished report
    canvas.delete("drawString")
    root.update()
    canvas.create_text(10,425, tag="drawString",
        anchor="sw", font="Times 11", text=textMes)
    root.update()

def tooLongJoke(jokeNumber):
      # Once I removed debug print()s, tracking progress was 
      # impossible, so this is effectively an iteration counter
    jokes =["hmmmm this is taking a little long", 
            "I swear this never happens", 
            "I'm afraid I can't do that Dave", 
            "What does a robot call a one night stand?",
            "A nut and bolt",
            "Who do robot Karens like to call?",
            "The task manager",
            "Google failed badly at 'robot jokes'" ]
    jokeNumber =  jokeNumber % len(jokes)
    drawString(jokes[jokeNumber])

def dlcJoke(jokeNumber):
      # this WAS a 'hardmode' button, but python with tkinter
      # struggled with changing globals, so now its just a joke.
      # the argument passing doesn't do anything anymore, but I've left
      # it in for reference next time I need python GUI.
    jokes =["There isn't really any DLC for this", 
            "How could this possibly have DLC?", 
            "If only I could monetise this", 
            "this button is never going to do anything",
            "this button is only a joke",
            "Please insert disc 21",
            "DLC requires Voodoo 2 3DFX",
            "DLC requires Soundblaster 2 or greater" ]
    drawString(jokes[random.randint(0,len(jokes)-1)])

def makeGUI():
      # setup buttons
    buttonReset=tk.Button(root, bg='aqua', text="Clear", width=10, height=3,
             command=clearGrid)
    buttonReset.place(x=412, y=80)
    buttonSolve=tk.Button(root, bg='green', text="Solve", width=10, height=3,
             command=solve)
    buttonSolve.place(x=412, y=160)
    buttonExit=tk.Button(root, bg='red', text="Exit", width=10, height=1,
             command=root.destroy)
    buttonExit.place(x=412, y=405)
    buttonDLC=tk.Button(root, bg='yellow', text="$ $ DLC $ $", width=10,
             height=3, command=lambda:dlcJoke(1))
    buttonDLC.place(x=412, y=240)

      # draw static text
    canvas.create_text(414,10, anchor="nw",font="Times 11",text= "    Sudoku")
    canvas.create_text(412,30, anchor="nw",font="Times 11",text="Cleaver-Name")
    canvas.create_text(417,50, anchor="nw",font="Times 11",text="     9000  ")
    canvas.create_text(412,330, anchor="sw",font="Times 12",text=" Mark   ")
    canvas.create_text(412,350, anchor="sw",font="Times 12",text=" Anderson")
    canvas.create_text(412,370, anchor="sw",font="Times 11",text=" UNE    ")
    canvas.create_text(412,390, anchor="sw",font="Times 11",text=" Cosc350 ")

      # draw grid lines
    for i in range (4, 444, 132):
        canvas.create_line(i, 4, i, 401,width=3 )
        canvas.create_line(4, i, 401, i,width=3 )


# --------------------------------------------------- #
# --------- interesting functions start here -------- #
# --------------------------------------------------- # 

def choose(rowIndex,colIndex):
  # This function puts a number in the box, if nothing fits in
  # the box as per the game rules, it puts a 0 in the box.
  # The 0's are delt with in other functions
      # first check that the box in question is not a 'prefilled' box
    if (str(rowIndex)+str(colIndex) in preFilled ):
        pass
    else:
      # then setup our data structures for the comparisons: 
        toGoIn = 0
        possiblesLeft = possibles.copy()
        random.shuffle(possiblesLeft)
        makeBox(rowIndex,colIndex)
        toRemove = []
      # make a list of every option we CANNOT pick for this box
        for i in possiblesLeft:
            if (i in boxArray or                         # 3x3 box group
                i in [row[colIndex] for row in grid] or  # column
                i in grid[rowIndex]):                    # row
              toRemove.append(i)
      # remove wrong choices from possibles list, place a remaining possible
        for i in toRemove:
            possiblesLeft.remove(i)
        if len(possiblesLeft) > 0:
            toGoIn = possiblesLeft[0]
        grid[rowIndex][colIndex] = toGoIn
        drawNumber(rowIndex,colIndex)


def fillGrid():
      # reset first or new values are compaired against old
    clearGrid()
      # Makes an intelligent choice for each box 1 by 1.
      # this is very likely to get extremely close to a full answer, 
      # but rarely gets all the way.
    for rowIndex in range (9):
        for colIndex in range (9):
            choose(rowIndex,colIndex)


def zeroHunter():
      # This gets us from close to finished by finding and solving problems
      # Finds all the blank boxes, clears and re-chooses those rows
      # Also picks another row entirely at random to clear if there
      # is only 1 row with a zero(s)
      # This is the 'I' part of 'AI'
    rowsWithAZero = []
    for rowIndex in range (9):
        for colIndex in range (9):
            if (grid[rowIndex][colIndex]==0):
                rowsWithAZero.append(rowIndex)

    if len(rowsWithAZero) < 2:
        extraRow = random.randint(0,8)
        if extraRow in rowsWithAZero and extraRow != 0: extraRow -= 1
        rowsWithAZero.append(extraRow)

    rowsWithAZero = list(set(rowsWithAZero))  # remove duplicate rows
    print("Targetting blank boxes found in rows: "+str(rowsWithAZero))
    
      # clear them THEN re-pick them, these can't be 1 loop
    for j in rowsWithAZero:
        for i in range (9):
            grid[j][i] = startGrid[j][i]
    for j in rowsWithAZero:
        for i in range (9):
            choose(j,i)


def solve():
      # clear message box
    drawString(" ")
      # Combines the 3 main functions: choose(), zeroHunter(), fillGrid()
      # Will always solve the puzzle, reports number of row changes it takes.
    attempts = 0

    while (getGridScore(grid) != 81):

          # every 10 runs of zeroHunter (including the first) do a full reset
        if attempts % 10 == 0: 

              # get a fresh grid, if its rubbish, get a new one. 
            if attempts // 10 > 0: print("Attempt "+str(attempts // 10)+
                                " appears unfinshable, refreshing grid")
            print("-----------------------------------------------------")

            fillGrid()
            while getGridScore(grid) < 72: fillGrid()
            print("Attempt "+str((attempts // 10)+1)+
                    " starting with: "+str(81-getGridScore(grid))+
                    " empty boxes")

           # we need to check getGridScore(grid) again here because its
           # possible for fillGrid() to get it all right the first time.
        if getGridScore(grid) != 81:
            zeroHunter()  # <-- the main thing here
        attempts += 1
        if attempts % 50 == 0 and attempts != 50: tooLongJoke(int(attempts/50)-1)

      # once we get a score of 81: end loop, print message, game over.
    print(" # Finished after "+str(attempts)+" corrections # ")
    drawString("  Finished after "+str(attempts)+" corrections")
   

# --------------------------- #
# ------ end functions ------ #
# --------------------------- #   


copyGrid(0) # change this 0 to 1 or 2 for hard(er) mode.

makeGUI()

root.mainloop()