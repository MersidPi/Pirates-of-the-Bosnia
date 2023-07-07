from battleships.ili934xnew import ILI9341, color565
from machine import Pin
from battleships.display import display, refreshDisplay
from time import sleep

# pico buttons declaration
t0 = Pin(0, Pin.IN)
t1 = Pin(1, Pin.IN)
t2 = Pin(2, Pin.IN)
t3 = Pin(3, Pin.IN)

def selectControls():
    '''
    displaying options for controls, after clicking button
    the option is highlighted and another click will select it
    
    then declaration of controls and updating parameter
    to know which control is chosen, it will be needed
    '''
    
    refreshDisplay()
    display.print("On Pico, click the corresponding button to select controls: ")
    
    # displaying options
    xPos_options = 55
    yPos_options = 80
    yPos_difference = 40
    display.set_pos(xPos_options, yPos_options)
    display.print("Joystick (1)")
    display.set_pos(xPos_options, yPos_options + yPos_difference)
    display.print("Keyboard (2)")
    display.set_pos(xPos_options, yPos_options + 2 * yPos_difference)
    display.print("Phone (3)")
    
    # getting selection for options
    selected = -1
    xPos = 0
    yPos = 0
    xPos_old = 0
    yPos_old = 0
    written = False
    while True:
        if t0.value():
            xPos = xPos_options - 25 
            yPos = yPos_options
            selected = 0
        elif t1.value():
            xPos = xPos_options - 25 
            yPos = yPos_options + yPos_difference
            selected = 1
        elif t2.value():
            xPos = xPos_options - 25 
            yPos = yPos_options + 2 * yPos_difference
            selected = 2
        elif t3.value() and selected != -1:
            break
        
        # when not selected, this text isn't on screen, after initial select, it will be
        if not written and xPos != 0:
            written = True
            display.set_pos(0, 200)
            display.print("Click button 4 to choose option")
        
        # for initial selection
        if xPos != 0:
            display.set_pos(xPos, yPos)
            display.set_color(color565(255, 255, 255), color565(0, 0, 0))
            display.print("->")
            
        # for next selection, delete first arrow and print new one
        if yPos != yPos_old and yPos_old != 0:
            display.set_pos(xPos_old, yPos_old)
            display.set_color(color565(0, 0, 0), color565(0, 0, 0))
            display.print("->")
        
        # update old variables for next iteration
        xPos_old = xPos
        yPos_old = yPos
        
        # so that loop doesn't run too fast
        sleep(0.05)
    
    # chosenControl is string that contains what's chosen
    chosenControl = "Joystick"
    if selected == 1:
        chosenControl = "Keyboard"
    elif selected == 2:
        chosenControl = "Phone"
    
    # printing what is chosen
    display.set_pos(0, 260)
    display.print("You chose: " + chosenControl + ".")
    sleep(2)
    
    # return to main program what is chosen
    return chosenControl
    