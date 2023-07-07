from battleships.ili934xnew import ILI9341, color565
from battleships.display import display, refreshDisplay
from time import sleep
from battleships.input import getInput
from battleships.drawGrid import drawGrid
from battleships.drawBMP import drawBMP

# variables for position of matrix of this player and space between bitmaps
startMatrixMyX = 0
startMatrixMyY = 193 # 319 - 6*21
bitmapSpacing = 21 # size of bitmap is 20px and +1 because of line between

# function for drawing matrix with start coordinates
def drawMatrix(matrix, startX, startY):
    y = startY + 1
    for i in range (len(matrix)):
        x = startX + 1
        for j in range (len(matrix)):
            if matrix[i][j] != 0:
                drawBMP(x, y, matrix[i][j])
            x += bitmapSpacing
        y += bitmapSpacing

# variables for aim positioning
x = 0
y = 0

# function for checking if horizontal ship can be placed
def horizontalCheck(matrix, row, col, ship_size):
    matLen = len(matrix)
    check = (col + ship_size - 1 < matLen and all(matrix[row][col + i] == 0 for i in range(ship_size)))
    upCheck = (row == 0) or (col + ship_size - 1 < matLen and all(matrix[row - 1][col + i] == 0 for i in range(ship_size)))
    downCheck = (row == matLen - 1) or (col + ship_size - 1 < matLen and all(matrix[row + 1][col + i] == 0 for i in range(ship_size)))
    leftCheck = (col == 0) or (matrix[row][col - 1] == 0)
    rightCheck = (col + ship_size == matLen) or (col + ship_size <= matLen - 1) and (matrix[row][col + ship_size] == 0)
    return check and upCheck and downCheck and leftCheck and rightCheck

# function for checking if vertical ship can be placed
def verticalCheck(matrix, row, col, ship_size):
    matLen = len(matrix)
    check = (row + ship_size - 1 < matLen and all(matrix[row + i][col] == 0 for i in range(ship_size)))
    upCheck = (row == 0) or (matrix[row - 1][col] == 0)
    print("row is: " + str(row) + " ship: " + str(ship_size) + " col: " + str(col) + " lenmat: " + str(len(matrix)) + " = " + str((row + ship_size == len(matrix))))
    downCheck = (row + ship_size == matLen) or ((row + ship_size <= matLen - 1) and (matrix[row + ship_size][col] == 0)) # provjeri
    leftCheck = (col == 0) or (row + ship_size - 1 < matLen and all(matrix[row + i][col - 1] == 0 for i in range(ship_size)))
    rightCheck = (col == matLen - 1) or (row + ship_size <= matLen) and (row + ship_size - 1 < matLen and all(matrix[row + i][col + 1] == 0 for i in range(ship_size)))
    print("downcheck: " + str(downCheck) + "check: " + str(check) + "upcheck: " + str(upCheck) + "leftcheck: " + str(leftCheck) + "rightcheck: " + str(rightCheck))
    return check and upCheck and downCheck and leftCheck and rightCheck

# function for writing on display that the ship placement isn't valid
def writeInvalidPosition():
    display.set_pos(20,140)
    display.set_color(color565(255, 0, 0), color565(0, 0, 0))
    display.print("Invalid position. \nTry again")
    display.set_color(color565(255, 255, 255), color565(0, 0, 0))

def arrangeShips(inputMode):
    refreshDisplay()
    
    # if playagain was chosen, this ensures that on new game it starts on 0,0
    global x
    global y
    x = 0
    y = 0
    
    # draw lines that form a grid 6x6
    drawGrid(startMatrixMyX, startMatrixMyY, 21, 6, color565(255, 255, 255))
    
    display.set_pos(150, 214)
    display.print("Your ships")
    
    # We first create an empty 6x6 matrix
    matrix_size = 6
    matrix = [[0] * matrix_size for _ in range(matrix_size)]
    
    # We Iterate through each ship size 4 3 2 1
    ship_size = 4
    while (ship_size >= 1):
        # displaying which ship size is being placed
        display.set_pos(0,0)
        display.print("Ship size: ")
        offset = 0
        i = 4
        while i > 0:
            display.set_pos(105 + offset, 0)
            if i == ship_size:
                display.set_color(color565(255, 0, 0), color565(0, 0, 0))
                display.print(str(i))
                display.set_color(color565(255, 255, 255), color565(0, 0, 0))
            else:
                display.print(str(i))
            offset += 20
            i -= 1
            
        # displaying how to choose orientation    
        if ship_size != 1:
            display.set_pos(0, 20)
            display.print("Orientation: ")
            display.set_pos(20, 40)
            display.print("RIGHT - horizontal")
            display.set_pos(20, 60)
            display.print("DOWN - vertical")
        
        # Getting input for orientation
        orientation = ''
        input = "s"
        if ship_size == 1:
            orientation = "horizontal"
        else:
            while input != "RIGHT" and input != "DOWN":
                input = getInput(inputMode)
                if input == "RIGHT":
                    orientation = "horizontal"
                elif input == "DOWN":
                    orientation = "vertical"
        
        # deletion of some pixels
        display.set_pos(150,60)
        display.set_color(color565(0, 0, 0), color565(0, 0, 0))
        display.print("000")
        display.set_color(color565(255, 255, 255), color565(0, 0, 0))
        display.set_pos(150,40)
        display.set_color(color565(0, 0, 0), color565(0, 0, 0))
        display.print("00000")
        display.set_color(color565(255, 255, 255), color565(0, 0, 0))
        
        # displaying some info about placement of ship
        if ship_size == 1:
            display.set_pos(0, 40)
            display.print("The ship will be placed on the aiming position. Keep ships apart!")
        else:
            display.set_pos(0, 20)
            display.print("Orientation:")
            display.set_color(color565(255, 0, 0), color565(0, 0, 0))
            display.set_pos(125, 20)
            display.print(orientation)
            display.set_color(color565(255, 255, 255), color565(0, 0, 0))
            display.set_pos(0, 40)
            if orientation == "horizontal":
                display.print("The ship will be placed to the right of the aiming position. Keep ships apart!")
            else:
                display.print("The ship will be positioned down from the aiming position. Keep ships apart!")
        
        # placing ship
        placed = False
        while not placed:
            # x and y are global so that next aiming starts from the last one
            global x
            global y
            # Getting input for position
            while True:                
                # aiming is on x y coordinates
                if matrix[y][x] == 1:
                    drawBMP(startMatrixMyX + bitmapSpacing * x + 1, startMatrixMyY + bitmapSpacing * y + 1, "aimShip")
                else:
                    drawBMP(startMatrixMyX + bitmapSpacing * x + 1, startMatrixMyY + bitmapSpacing * y + 1, "aim")
                # waiting for input
                input = getInput(inputMode)
                
                # delete + from old coordinate
                drawBMP(startMatrixMyX + bitmapSpacing * x + 1, startMatrixMyY + bitmapSpacing * y + 1, matrix[y][x])
                
                # update coordinates, in the next iteration, target will be displayed on new location
                if input == "UP" and y > 0:
                    y -= 1
                elif input == "DOWN" and y < matrix_size - 1:
                    y += 1
                elif input == "RIGHT" and x < matrix_size - 1:
                    x += 1
                elif input == "LEFT" and x > 0:
                    x -= 1
                elif input == "SELECT":
                    break
                sleep(0.1)

            row = y
            col = x
            
            # Check if ship can be placed there
            if matrix[row][col] != 0:
                writeInvalidPosition()
            elif orientation == "horizontal":
                # Check if the ship can be placed horizontally
                if not horizontalCheck(matrix, row, col, ship_size):
                    writeInvalidPosition()
                else:
                    # Valid position, place the ship horizontally
                    for i in range(ship_size):
                        matrix[row][col + i] = 1
                        drawBMP(startMatrixMyX + bitmapSpacing * (col + i) + 1, startMatrixMyY + bitmapSpacing * row + 1, matrix[row][col + i])
                    placed = True
            else:
                # Check if the ship can be placed vertically
                if not verticalCheck(matrix, row, col, ship_size):
                    writeInvalidPosition()
                else:
                    # Valid position, place the ship vertically
                    for i in range(ship_size):
                        matrix[row + i][col] = 1
                        drawBMP(startMatrixMyX + bitmapSpacing * col + 1, startMatrixMyY + bitmapSpacing * (row + i) + 1, matrix[row + i][col])
                    placed = True
            if placed == True:
                ship_size -= 1
            
        # deletion of upper half of the display
        display.set_pos(0,0)
        display.set_color(color565(0, 0, 0), color565(0, 0, 0))
        display.print("000000000000000000")
        display.print("000000000000000000")
        display.print("000000000000000000")
        display.print("000000000000000000")
        display.print("000000000000000000")
        display.print("000000000000000000")
        display.print("000000000000000000")
        display.print("000000000000000000")
        display.set_color(color565(255, 255, 255), color565(0, 0, 0))
        display.set_pos(0, 140)
    
    # when this player finishes arranging, displaying this text
    display.print("Waiting for enemy to finish arranging...")
    return matrix
