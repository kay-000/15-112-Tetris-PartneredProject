from cmu_112_graphics import *

#################################################
# Tetris 
#################################################

def appStarted(app):

    app.rows, app.cols, app.cellSize, app.margin = gameDimensions()
    app.emptyColor = 'blue'
    app.board =[ ([app.emptyColor] * app.cols) for row in range(app.rows) ]
    app.isGameOver =  False
    app.score = 0
    
    # # pre-load a few cells with known colors for testing purposes
    # app.board[0][0] = "red" # top-left is red
    # app.board[0][app.cols-1] = "white" # top-right is white
    # app.board[app.rows-1][0] = "green" # bottom-left is green
    # app.board[app.rows-1][app.cols-1] = "gray" # bottom-right is gray

    # Seven "standard" pieces (tetrominoes)
    iPiece = [
        [  True,  True,  True,  True ]
    ]

    jPiece = [
        [  True, False, False ],
        [  True,  True,  True ]
    ]

    lPiece = [
        [ False, False,  True ],
        [  True,  True,  True ]
    ]

    oPiece = [
        [  True,  True ],
        [  True,  True ]
    ]

    sPiece = [
        [ False,  True,  True ],
        [  True,  True, False ]
    ]

    tPiece = [
        [ False,  True, False ],
        [  True,  True,  True ]
    ]

    zPiece = [
        [  True,  True, False ],
        [ False,  True,  True ]
    ]

    app.tetrisPieces = [iPiece, jPiece, lPiece, oPiece, sPiece, tPiece, zPiece]
    app.tetrisPieceColors = ["red", "yellow", "magenta", "pink", "cyan", 
                                                              "green", "orange"]
    newFallingPiece(app)
    
def newFallingPiece(app):
    import random
    randomIndex = random.randint(0, len(app.tetrisPieces) - 1)

    app.fallingPiece = app.tetrisPieces[randomIndex]
    app.fallingPieceColor = app.tetrisPieceColors[randomIndex]

    app.numFallingPieceRows = len(app.fallingPiece)
    app.numFallingPieceCols = len(app.fallingPiece[0])

    app.fallingPieceRow = 0
    app.fallingPieceCol = app.cols // 2 - app.numFallingPieceCols // 2


def moveFallingPiece(app, drow, dcol):
    app.fallingPieceRow += drow
    app.fallingPieceCol += dcol

    if(fallingPieceIsLegal(app) == False):
        app.fallingPieceRow -= drow
        app.fallingPieceCol -= dcol
        return False
    else:
        return True

def fallingPieceIsLegal(app):
    for row in range(len(app.fallingPiece)):
        for col in range(len(app.fallingPiece[0])):

            if(app.fallingPiece[row][col] == True):
            #check that the cell is in fact on the board.
                newRow = row + app.fallingPieceRow
                newCol = col + app.fallingPieceCol
                if (newRow < 0 or 
                    newRow >= app.rows or 
                    newCol < 0 or 
                    newCol >= app.cols):
                    return False
                
                if(app.board[newRow][newCol] != 'blue'):
                    return False
    return True

def rotateFallingPiece(app):
    #1.Store the relevant values assoc. w/ the old piece into temp local vars.
    oldRows, oldCols =  len(app.fallingPiece), len(app.fallingPiece[0])
    oldFallPiece = app.fallingPiece
    oldFallPieceColor = app.fallingPieceColor

    #2. Compute the num of new rows and cols according to the old dimensions.
    newRows, newCols =  oldCols, oldRows
    
    #3. New 2D list based on the new dimensions, and fill it with None values. 
    newPiece = [ (['None'] * newCols) for row in range(newRows) ]
    
    #4. Iterate through each cells in the og piece & move each value to new 
    # location in the new piece.
    for oldRow in range(oldRows):
        for oldCol in range(oldCols):
            newPiece[oldCols - 1 - oldCol][oldRow]=oldFallPiece[oldRow][oldCol]

    newRow = app.fallingPieceRow + oldRows // 2 - newRows // 2
    newCol = app.fallingPieceCol + oldCols // 2 - newCols // 2


    #5. Set fallingPiece and the other variables equal to their new values.
    app.fallingPiece = newPiece
    app.numfallingPieceRows = len(app.fallingPiece)
    app.numfallingPieceCols = len(app.fallingPiece[0])
    app.fallingPieceRow = newRow
    app.fallingPieceCol = newCol

    #6. Check whether the new piece is legal. 
    if(fallingPieceIsLegal(app) == False):
       app.fallingPiece = oldFallPiece
       app.numfallingPieceRows = len(app.fallingPiece)
       app.numfallingPieceRows = len(app.fallingPiece[0])
       app.fallingPieceRow = newRow
       app.fallingPieceCol = newCol
       
def placeFallingPiece(app):
    color = app.fallingPieceColor
    
    for row in range(len(app.fallingPiece)):
        for col in range(len(app.fallingPiece[0])):

            if(app.fallingPiece[row][col] == True):
                
                newRow = app.fallingPieceRow + row
                newCol = app.fallingPieceCol + col

                app.board[newRow][newCol] = color
                
def removeFullRows(app):
    newBoard = []
    count = 0
    
    for row in range(app.rows):
            if(app.emptyColor in app.board[row]):
                #the row is not full
                newBoard.append(app.board[row])
            else:
                #the row is full so don't add to the board
                count += 1

    newRows = [([app.emptyColor] * app.cols) for row in range(count)]
    app.board = newRows + newBoard
    app.score += (count) ** 2

def hardDrop(app):
    while moveFallingPiece(app, +1, 0) == True:
        continue
    placeFallingPiece(app)

#########################
# controller functions
#########################

def keyPressed(app, event):
    drow, dcol = 0, 0 

    if event.key == 'r':
        appStarted(app)

    if app.isGameOver:
        return 

    if event.key == "Up":
        rotateFallingPiece(app)
    elif event.key == "Down":
        drow, dcol = +1, 0
    elif event.key == "Left":
        drow, dcol = 0, -1
    elif event.key == "Right":
        drow, dcol = 0, +1
    elif event.key == "Space":
        hardDrop(app)
    else:
        newFallingPiece(app)
    moveFallingPiece(app, drow, dcol)

def timerFired(app):
    if(app.isGameOver == True):
            return 
    if(moveFallingPiece(app, +1, 0) == False):
        placeFallingPiece(app)
        removeFullRows(app)
        newFallingPiece(app)

        if(fallingPieceIsLegal(app) == False):
            app.isGameOver = True


#########################
# model to view; view to model
#########################
#source: https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
def getCellBounds(app, row, col):
    
    gridWidth  = app.width - 2*app.margin
    gridHeight = app.height - 2*app.margin
    x0 = app.margin + gridWidth * col / app.cols
    x1 = app.margin + gridWidth * (col+1) / app.cols
    y0 = app.margin + gridHeight * row / app.rows
    y1 = app.margin + gridHeight * (row+1) / app.rows
    return (x0, y0, x1, y1)

#########################
# view functions
#########################

def drawFallingPiece(app, canvas):
    color = app.fallingPieceColor

    for row in range(len(app.fallingPiece)):
        for col in range(len(app.fallingPiece[0])):

            if(app.fallingPiece[row][col] == True):
                drawCell(app,canvas,row + app.fallingPieceRow , 
                        col + app.fallingPieceCol , color)


def drawCell(app,canvas,row, col, color):
    cellOutlineWidth = 4
    x0, y0, x1, y1 = getCellBounds(app, row, col)
    canvas.create_rectangle(x0, y0, x1, y1, fill = color, 
                            outline = 'black', width = cellOutlineWidth)

def drawBoard(app, canvas): 
    for row in range(app.rows):
        for col in range(app.cols):
            color =  app.board[row][col]
            drawCell(app,canvas,row, col, color)

def redrawAll(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill = 'orange')
    drawBoard(app, canvas)
    drawFallingPiece(app, canvas)
    if(app.isGameOver):
        canvas.create_text(app.width/2, app.height/2, text = 'GAME OVER', 
                         fill = 'orange', font='Helvetica 26 bold')
    canvas.create_text(app.width/2 ,app.margin/2 , 
                       text = f'Score: {app.score}', fill = 'purple',
                       font= 'Helvetica 25 bold')

#########################

def gameDimensions():
    #default values
    rows = 15
    cols = 10
    cellSize = 20
    margin = 25
    return (rows, cols, cellSize, margin)

def playTetris():
    (rows, cols, cellSize, margin) = gameDimensions()
    width = (cellSize * cols) + (2* margin)
    height = (cellSize * rows) + (2* margin) 

    runApp(width=width, height=height)

playTetris()