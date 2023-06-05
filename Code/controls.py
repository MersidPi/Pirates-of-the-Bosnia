from ili934xnew import ILI9341, color565
from machine import Pin, SPI, Timer
from micropython import const
import os
import glcdfont
import tt14
import tt24
import tt32
from time import sleep

def selectControls():
    '''
    displaying options for controls, after clicking button
    the option is highlighted and another click will select it
    
    then declaration of controls and updating parameter
    to know which control is chosen, it will be needed
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
    
    display.set_pos(0,0)
    display.print("Click the corresponding button to select controls: ")
    
    xPos_options = 55
    yPos_options = 80
    yPos_difference = 40
    display.set_pos(xPos_options, yPos_options)
    display.print("Joystick (T0)")
    display.set_pos(xPos_options, yPos_options + yPos_difference)
    display.print("Keyboard (T1)")
    display.set_pos(xPos_options, yPos_options + 2 * yPos_difference)
    display.print("Phone (T2)")
    
    t0 = Pin(0, Pin.IN)
    t1 = Pin(1, Pin.IN)
    t2 = Pin(2, Pin.IN)
    t3 = Pin(3, Pin.IN)
    
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
            display.print("Click T4 to choose option")
        
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
    
    # x is string that contains what's chosen
    x = "Joystick"
    if selected == 1:
        x = "Keyboard"
    elif selected == 2:
        x = "Phone"
    
    # printing what is chosen
    display.set_pos(0, 260)
    display.print("You chose: " + x)
    sleep(2)
    
    # return to main program what is chosen
    return x
    