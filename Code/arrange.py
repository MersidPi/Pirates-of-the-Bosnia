from ili934xnew import ILI9341, color565
from machine import Pin, SPI, Timer
from micropython import const
import os
import glcdfont
import tt14
import tt24
import tt32
from time import sleep

def arrangeShips():
    '''
    this function displays grid and available ships, player then selects a ship
    chooses its rotation - or | and then puts it on the grid, it needs a matrix
    and some logic implemented to disable overlap, impossible rotations (if its
    not possible to rotate a ship because theres no space) etc.
    it also needs function for key press (or joystick move, or key press on phone) reading
    and moving ship on screen according to that
    '''

    #Function that creates a matrix and allows the user to place his ships:
    #The function iterates through all the ships to be placed, largest to smallest
    #The user first chooses the orientation of the ship //using one of two buttons//
    #The user then chooses the coordinates to attempt to place the ship //using up/down left/right and confirm//
    #The function then determines if the given ship can fit within the matrix if placed at these coordinates
    #If yes fills matrix with 1's at proper locations
    #If not restarts input for this particular ship size
    ###!still needs input and display integration!###
    def place_ships():
        # We first create an empty 10x10 matrix
        matrix = [[0] * 10 for _ in range(10)]

        # We then define the sizes of the ships
        ship_sizes = [4, 3, 3, 2]

        # We Iterate through each ship size
        for ship_size in ship_sizes:

            while True:
                display.print("Placing a ship of size:", ship_size)
                # Prompt the user to choose the orientation and initial coordinates
                display.print("Choose the orientation (vertical or horizontal): ")
                ###!!!Add input here ###
                #example: if(t0.value): orientation = h elif(t1.value): orientation = v

                #Temporary orientation for development without input:
                orientation = 'h'

                display.print("Choose the starting coordinates (row, column): ")
                ###!!!Add input here ###
                #The player moves a blinking dot to the place they want to place their ship:
                #For Horizontal the ship is placed left-right in the selected row starting at the selected collumn
                #For Vertical the ship is placed top-down in the selected collumn starting at the selected row

                #Temporary row and col for development without input:
                row = 1
                col = 1


                # Check if the coordinates are valid and the ship can be placed there
                if 0 <= row < 10 and 0 <= col < 10 and matrix[row][col] == 0:
                    if orientation == 'h':
                        # Check if the ship can be placed horizontally
                        if col + ship_size < 10 and all(matrix[row][col + i] == 0 for i in range(ship_size)):
                            # Valid position, place the ship horizontally
                            for i in range(ship_size):
                                matrix[row][col + i] = 1
                            break
                        else:
                            display.print("Invalid position or ship overlap. Try again.")
                    elif orientation == 'v':
                        # Check if the ship can be placed vertically
                        if row + ship_size < 10 and all(matrix[row + i][col] == 0 for i in range(ship_size)):
                            # Valid position, place the ship vertically
                            for i in range(ship_size):
                                matrix[row + i][col] = 1
                            break
                        else:
                            display.print("Invalid position or ship overlap. Try again.")
                    else:
                        display.print("Orientation can only be horizontal or vertical")
                else:
                    display.print("Invalid position. Try again.")

        # Return the populated matrix
        return matrix


    '''
    start timer 
    show display with ship and rotation that is possible
    get input for rotation
        rotate if possible
    get input for moving
    see if its possible
        do nothing or move ship
        repeat until input for selection
    next ship until all ships are arranged
    interrupt for timer, if it ends, player loses
    when done, send to topic
    
    '''
    
    # display stuff
    SCR_WIDTH = const(320)
    SCR_HEIGHT = const(240)
    SCR_ROT = const(2)
    CENTER_Y = int(SCR_WIDTH/2)
    CENTER_X = int(SCR_HEIGHT/2)
    TFT_CLK_PIN = const(18)
    TFT_MOSI_PIN = const(19)
    TFT_MISO_PIN = const(16)
    TFT_CS_PIN = const(17)
    TFT_RST_PIN = const(20)
    TFT_DC_PIN = const(15)
    spi = SPI(
        0,
        baudrate=62500000,
        miso=Pin(TFT_MISO_PIN),
        mosi=Pin(TFT_MOSI_PIN),
        sck=Pin(TFT_CLK_PIN))
    display = ILI9341(
        spi,
        cs=Pin(TFT_CS_PIN),
        dc=Pin(TFT_DC_PIN),
        rst=Pin(TFT_RST_PIN),
        w=SCR_WIDTH,
        h=SCR_HEIGHT,
        r=SCR_ROT)
    # end of display stuff
    
    # prepare display for printing
    display.erase()
    display.set_pos(0,0)
    display.set_font(tt24)
    display.set_color(color565(255, 255, 255), color565(0, 0, 0))
    #
    
    display.set_pos(20,70)
    display.print("Arranging....")
    sleep(1)
    display.print("Press any key to continue...")
    t0 = Pin(0, Pin.IN)
    t1 = Pin(1, Pin.IN)
    t2 = Pin(2, Pin.IN)
    t3 = Pin(3, Pin.IN)
    while not (t0.value() or t1.value() or t2.value() or t3.value()):
        sleep(0.1)
    display.print("(potentionally) \nwaiting for opponent to finish arranging...")
    sleep(1)
    display.print("\n\nBattle will begin shortly...")
    sleep(2)
    display.erase()
    
    
    
    