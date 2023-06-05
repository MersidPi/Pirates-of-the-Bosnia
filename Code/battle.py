from ili934xnew import ILI9341, color565
from machine import Pin, SPI, Timer
from micropython import const
import os
import glcdfont
import tt14
import tt24
import tt32
from time import sleep

def battle():
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
    

    '''
    send matrices on topic 
    send random number and recieve from another pico
    whose is bigger goes first
    while not gameEnd:    
        p1 attacks, goes on topic
        update matrix
        p2 attacks, goes on topic
        update matrix
        gameEnd = checkWin()
    
    
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
    
    display.set_pos(50,140)
    display.print("Battle....")
    sleep(2)
    display.erase()
    display.set_pos(0,100)
    display.print("Do you want to win?")
    display.print(" Yes - T0\n No - T1")
    win = False
    t0 = Pin(0, Pin.IN)
    t1 = Pin(1, Pin.IN)
    while True:
        if t0.value():
            win = True
            display.print("You won!")
            sleep(2)
            break
        elif t1.value():
            win = False
            display.print("You lost!")
            sleep(2)
            break
        sleep(0.1)
    display.print("Going on end screen...")
    sleep(1)
    return win
    