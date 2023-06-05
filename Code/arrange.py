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
    
    
    
    