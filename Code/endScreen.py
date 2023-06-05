from ili934xnew import ILI9341, color565
from machine import Pin, SPI, Timer
from micropython import const
import os
import glcdfont
import tt14
import tt24
import tt32
from time import sleep

def endScreen(thisPlayerVictory):
    '''
    code to draw the final screen on the screen and then prompts
    if players want to play again, they both need to agree 
    
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
    
    # print correct message 
    display.set_pos(0,100)
    if thisPlayerVictory:
        display.print("YOU WON! CONGRATULATIONS!!!")
    else:
        display.print("YOU LOST! BETTER LUCK NEXT TIME :P")
    sleep(1)
    
    # prompt for playing again
    display.print("Play again?\n Yes - T0\n No - T1")
    playAgain = False
    t0 = Pin(0, Pin.IN)
    t1 = Pin(1, Pin.IN)
    while True:
        if t0.value():
            playAgain = True
            display.print("Starting new game...")
            sleep(2)
            break
        elif t1.value():
            playAgain = False
            display.print("Goodbye...")
            sleep(2)
            break
        sleep(0.1)
    display.erase()
    return playAgain
    

