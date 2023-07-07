from battleships.ili934xnew import ILI9341, color565
from machine import Pin, SPI, Timer
from micropython import const
import os
import battleships.glcdfont
import battleships.tt24

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
display.set_font(battleships.tt24)
display.set_color(color565(255, 255, 255), color565(0, 0, 0))

def refreshDisplay():
    # prepare display for printing
    display.erase()
    display.set_pos(0,0)
    #
