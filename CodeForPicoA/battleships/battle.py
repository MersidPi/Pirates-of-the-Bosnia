from battleships.ili934xnew import ILI9341, color565
from battleships.display import display, refreshDisplay
from time import sleep
from battleships.connection import sendMessage, waitForMessage
from battleships.input import getInput
from battleships.drawGrid import drawGrid, drawLineAlongX
from battleships.drawBMP import drawBMP
import random

# global definitions for matrices and number of ships (my and enemy)
matrixMy = [[0] * 6 for _ in range(6)]
myNumOfShips = 0
matrixEnemy = [[0] * 6 for _ in range(6)]
enemyNumOfShips = 0
xEnemyHP = 0
xMyHP = 0

# drawing matrices stuff
startMatrixEnemyX = 0
startMatrixEnemyY = 21
startMatrixMyX = 0
startMatrixMyY = 193
bitmapSpacing = 21
        
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

# global variables for aim position and input mode
x = 0
y = 0
inputMode = ""

# function for aiming, attacking, sending the attack, and updating enemy matrix
def aimPositionAttackSendUpdate(firstAttack):
    hit = False
    global x
    global y
    if firstAttack == False:
        sendMessage(b'battleships/playerA', bytes([7, y]))
        return False # hit is false
    while True:        
        # aiming is on x y coordinates
        if matrixEnemy[y][x] == 2:
            drawBMP(startMatrixEnemyX + bitmapSpacing * x + 1, startMatrixEnemyY + bitmapSpacing * y + 1, "aimSkull")
        elif matrixEnemy[y][x] == 3:
            drawBMP(startMatrixEnemyX + bitmapSpacing * x + 1, startMatrixEnemyY + bitmapSpacing * y + 1, "aimTestMiss")
        else:
            drawBMP(startMatrixEnemyX + bitmapSpacing * x + 1, startMatrixEnemyY + bitmapSpacing * y + 1, "aim")
        # waiting for input
        global inputMode
        input = getInput(inputMode, True)
        
        # delete target from old coordinate
        if matrixEnemy[y][x] == 1:
            # if there's ship in enemy matrix, just delete target
            drawBMP(startMatrixEnemyX + bitmapSpacing * x + 1, startMatrixEnemyY + bitmapSpacing * y + 1, 0)
        else:
            drawBMP(startMatrixEnemyX + bitmapSpacing * x + 1, startMatrixEnemyY + bitmapSpacing * y + 1, matrixEnemy[y][x])
        
        # update coordinates, in the next iteration, target will be displayed on new location
        if input == "RIGHT" and x < len(matrixEnemy) - 1:
            x += 1
        elif input == "DOWN" and y < len(matrixEnemy) - 1:
            y += 1
        elif input == "LEFT" and x > 0:
            x -= 1
        elif input == "UP" and y > 0:
            y -= 1
        elif input == "TIMEOUT":
            sendMessage(b'battleships/playerA', bytes([7, y]))
            return False # hit is false
            break
        elif input == "SELECT":
            break
        sleep(0.1)
    # send coordinates of attack
    sendMessage(b'battleships/playerA', bytes([x, y]))
    # now update value of enemy matrix with x y, and draw updated cell
    if matrixEnemy[y][x] == 0:
        matrixEnemy[y][x] = 3 # 3 means miss
        drawBMP(startMatrixEnemyX + bitmapSpacing * x + 1, startMatrixEnemyY + bitmapSpacing * y + 1, matrixEnemy[y][x])
    elif matrixEnemy[y][x] == 1:
        matrixEnemy[y][x] = 2 # 2 means hit
        drawBMP(startMatrixEnemyX + bitmapSpacing * x + 1, startMatrixEnemyY + bitmapSpacing * y + 1, matrixEnemy[y][x])
        hit = True
        global enemyNumOfShips
        enemyNumOfShips -= 1
        global xEnemyHP
        drawBMP(xEnemyHP, 0, "heartDelete")
        xEnemyHP -= 13
        
    # return information if ship was hit or not
    return hit

def defeatProcedure(matrix, startX, startY):
    #display.set_pos(0, 130)
    #display.print("Unbelievable! Some enemy ships are still intact, not obliterated like they should be.")
    #display.print("Can't even win a simple game...")
    display.set_pos(0,150)
    display.set_color(color565(0, 0, 0), color565(0, 0, 0))
    display.print("000000000000000000")
    display.print("000000000000000000")
    display.print("000000000000000000")
    display.print("000000000000000000")
    display.print("000000000000000000")
    display.print("000000000000000000")
    display.print("000000000000000000")
    display.set_pos(0,295)
    display.print("000000000000000000")
    drawLineAlongX(319, 0, 240, color565(0,0,0))
    display.set_color(color565(255, 0, 0), color565(0, 0, 0))
    display.set_pos(70,170)
    display.print("Defeat!")
    display.set_color(color565(255, 255, 255), color565(0, 0, 0))
    display.set_pos(0,195)
    display.print("You can now see where were remaining enemy ships hiding.")
    display.set_pos(0,280)
    display.print("Good luck next time!")
    global bitmapSpacing
    y = startY + 1
    x = 0
    for i in range (len(matrix)):
        x = startX + 1
        for j in range (len(matrix)):
            if matrix[i][j] == 1:
                drawBMP(x, y, matrix[i][j])
            x += bitmapSpacing
        y += bitmapSpacing
    display.set_pos(145, 0)
    display.set_color(color565(0, 0, 0), color565(0, 0, 0))
    display.print("000000")
    display.print("000000")
    display.print("000000")
    sleep(2)
    display.set_color(color565(255, 255, 255), color565(0, 0, 0))
    display.set_pos(135, 45)
    display.print("Press any key to continue...")
    global inputMode
    input = getInput(inputMode)
    

def victoryProcedure():
    #display.set_pos(0, 130)
    #display.print("Unbelievable! Some enemy ships are still intact, not obliterated like they should be.")
    #display.print("Can't even win a simple game...")
    display.set_pos(0,150)
    display.set_color(color565(0, 0, 0), color565(0, 0, 0))
    display.print("000000000000000000")
    display.print("000000000000000000")
    display.print("000000000000000000")
    display.print("000000000000000000")
    display.print("000000000000000000")
    display.print("000000000000000000")
    display.print("000000000000000000")
    display.set_pos(0,295)
    display.print("000000000000000000")
    drawLineAlongX(319, 0, 240, color565(0,0,0))
    display.set_color(color565(0, 255, 0), color565(0, 0, 0))
    display.set_pos(70,170)
    display.print("Victory!")
    display.set_color(color565(255, 255, 255), color565(0, 0, 0))
    display.set_pos(0,195)
    display.print("All enemy ships demolished! You've emerged as the ultimate naval conqueror!")
    sleep(2)
    display.set_pos(145, 0)
    display.set_color(color565(0, 0, 0), color565(0, 0, 0))
    display.print("0000000")
    display.print("0000000")
    display.print("0000000")
    display.print("0000000")
    display.print("0000000")
    display.print("0000000")
    display.print("0000000")
    display.set_color(color565(255, 255, 255), color565(0, 0, 0))
    display.set_pos(135, 45)
    display.print("Press any key to continue...")
    global inputMode
    input = getInput(inputMode)

def battle(matrix, inptMd):
    '''
    function that will be run while players are attacking each other
    player that goes first can be randomly determined, for example
    picos send random number on topic and whose is bigger, goes first
    attack will have time limit, which will be shown on 8 LEDs
    while opponent is attacking LEDs will "run" back and forth
    aim function is needed here, like in arrangeShips
    matrix will change values
    all of this will be sent on topic so that both players can see
    whats going on (not being able to see opponents ships ofc xD)
    when all ships of one player are
    destroyed, game will end, loop and this function will end
    '''
    # when players playAgain, reset aiming position on 0,0
    global x, y
    x = 0
    y = 0
    # update global matrix of this player and input mode
    global matrixMy
    matrixMy = matrix
    global inputMode
    inputMode = inptMd
    # count number of ships for this player A
    global myNumOfShips
    myNumOfShips = 0
    for i in range(len(matrixMy)):
        for j in range(len(matrixMy)):
            if matrixMy[i][j] == 1:
                myNumOfShips += 1
    # enemy number of ships is the same 
    global enemyNumOfShips
    enemyNumOfShips = myNumOfShips
    
    #######################################
    # sending on topic my matrix
    matrixMyValues = []
    for i in range(len(matrixMy)):
        for j in range(len(matrixMy)):
            matrixMyValues.append(matrixMy[i][j])
    sendMessage(b'battleships/playerA', bytes(matrixMyValues))
    
    # recieving enemy matrix from topic
    # we need to wait for message that is as long as matrix because of the same topic for phone
    matrixEnemyValues = list(b'\\x01')
    while len(matrixEnemyValues) != len(matrix) * len(matrix):
        matrixEnemyValues = list(waitForMessage())
    # sending matrix on topic again, if this player finishes first
    sendMessage(b'battleships/playerA', bytes(matrixMyValues))
    k = 0
    global matrixEnemy
    for i in range (len(matrixEnemy)):
        for j in range(len(matrixEnemy)):
            matrixEnemy[i][j] = matrixEnemyValues[k]
            k += 1
    refreshDisplay()
    
    # displaying text
    display.set_pos(145, 0)
    display.print("Enemy territory")
    
    display.set_pos(145, 270)
    display.print("Your ships ")
    
    # grid for enemy matrix
    drawGrid(startMatrixEnemyX, startMatrixEnemyY, 21, 6, color565(255, 255, 255))
    
    # display enemy health points
    global xEnemyHP
    xEnemyHP = 0
    for i in range(0, 10):
        drawBMP(xEnemyHP, 0, "heart")
        xEnemyHP += 13
    xEnemyHP -= 13
    
    # display my health points
    global xMyHP
    xMyHP = 0
    for i in range(0, 10):
        drawBMP(xMyHP, startMatrixMyY - 21, "heartMy")
        xMyHP += 13
    xMyHP -= 13
    
    # grid for my matrix
    drawGrid(startMatrixMyX, startMatrixMyY, 21, 6, color565(255, 255, 255))
    
    # draw our matrix
    drawMatrix(matrixMy, startMatrixMyX, startMatrixMyY)
    
    # firstly, firstAttack is True
    firstAttack = True
    
    # determining which player goes first
    myRandomNumber = random.randint(1, 254)
    if firstAttack == True:
        number = list(b'\x01\x02')
        while len(number) != 1:
            number = list(waitForMessage())
        enemyRandomNumber = number[0]
        if myRandomNumber < enemyRandomNumber:
            firstAttack = False
    
    # now goes battle
    while True:
        # this player A attacks or not, based on random numbers
        display.set_pos(134, 180)
        display.set_color(color565(0,0,0), color565(0,0,0))
        display.print("00000000")
        display.print("00000000")
        display.print("00000000")
        display.set_color(color565(100,100,100), color565(0,0,0))
        display.set_pos(135, 60)
        if firstAttack == True:
            display.print("Your turn, ATTACK!")
        hit = True
        while hit == True:
            hit = aimPositionAttackSendUpdate(firstAttack)
            if firstAttack == False:
                firstAttack = True
            sleep(0.5)
            # checking win/loss
            if myNumOfShips == 0:
                defeatProcedure(matrixEnemy, startMatrixEnemyX, startMatrixEnemyY)
                return False
            elif enemyNumOfShips == 0:
                victoryProcedure()
                return True
        #######################################
            
        # this player A recieves attack from player B
        hit = True
        while hit == True:
            display.set_pos(135, 60)
            display.set_color(color565(0, 0, 0), color565(0, 0, 0))
            display.print("0000000")
            display.print("0000000")
            display.print("0000000")
            display.print("0000000")
            display.set_pos(134, 180)
            display.set_color(color565(100, 100, 100), color565(0, 0, 0))
            display.print("Enemy attacks! Stay alert!")
            # waiting in loop until message of correct format is recieved
            xAttackPosition = 11
            attackPosition = [2]
            while xAttackPosition > 10 or len(attackPosition) != 2:
                attackPosition = list(waitForMessage("waitingAttack"))
                xAttackPosition = attackPosition[0]
                yAttackPosition = attackPosition[1]
            # now update our matrix with x y, and draw that updated cell
            if xAttackPosition == 7:
                hit = False
            elif matrixMy[yAttackPosition][xAttackPosition] == 0:
                matrixMy[yAttackPosition][xAttackPosition] = 3 # 3 means miss
                hit = False
            elif matrixMy[yAttackPosition][xAttackPosition] == 1:
                matrixMy[yAttackPosition][xAttackPosition] = 2 # 2 means hit
                hit = True
                global myNumOfShips
                myNumOfShips -= 1
                drawBMP(xMyHP, startMatrixMyY - 21, "heartDelete")
                xMyHP -= 13
            elif matrixMy[yAttackPosition][xAttackPosition] == 3: # he hit the same place
                hit = False
            elif matrixMy[yAttackPosition][xAttackPosition] == 2: # he hit the same place
                hit = False
            # draw that updated cell, if its 7, other player timed out and we dont print anything here
            if xAttackPosition != 7:
                drawBMP(startMatrixMyX + bitmapSpacing * xAttackPosition + 1, startMatrixMyY + bitmapSpacing * yAttackPosition + 1, matrixMy[yAttackPosition][xAttackPosition])
            
            # checking win/loss
            if myNumOfShips == 0:
                defeatProcedure(matrixEnemy, startMatrixEnemyX, startMatrixEnemyY)
                return False
            elif enemyNumOfShips == 0:
                victoryProcedure()
                return True
