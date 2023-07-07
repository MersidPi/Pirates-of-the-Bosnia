from battleships.ili934xnew import ILI9341, color565
from battleships.display import display, refreshDisplay
from battleships.input import getInput
from battleships.connection import sendMessage, waitForMessage
from battleships.drawBMP import drawBMP
from time import sleep

def credits():
    refreshDisplay()
    display.print("Game design and programming: ")
    display.set_pos(10, 48)
    display.print("Mersid Pilipovic, Ahmed Ljubuncic, Edis Jasarevic, Benjamin Hasanagic")
    display.set_pos(0, 144)
    display.print("Made possible by: ")
    display.set_pos(10, 168)
    display.print("Dr. Samim Konjicija")
    display.set_pos(10, 192)
    display.print("Ass. Selmir Gajip")
    display.set_pos(0, 216)
    display.print("ETF Sarajevo Ugradbeni sistemi")
    drawBMP(0, 264, "copyright")
    display.set_pos(23, 264)
    display.print("2023 All rights reserved")
    drawBMP(175, 265, "etf")

def endScreen(inputMode):
    '''
    code to draw the final screen on the screen and then prompts
    if players want to play again, they both need to agree 
    
    '''
    
    refreshDisplay()
    # prompt for playing again
    display.set_pos(40, 100)
    display.print("Do you want to play again?")
    display.set_pos(50, 150)
    display.set_color(color565(0, 255, 0), color565(0, 0, 0))
    display.print("UP - yes")
    display.set_color(color565(255, 0, 0), color565(0, 0, 0))
    display.print("DOWN - no")
    display.set_color(color565(255, 255, 255), color565(0, 0, 0))
    
    input = getInput(inputMode)
    while input != "UP" and input != "DOWN":
        input = getInput(inputMode)
        sleep(0.1)
    if input == "UP":
        sendMessage(b'battleships/playerB', b'playAgain')
        display.set_pos(0, 210)
        display.print("Waiting if other player wants to play again...")
        msg = b''
        while not (msg == b'playAgain' or msg == b'noPlayAgain'):
            msg = waitForMessage()
        if msg == b'playAgain':
            refreshDisplay()
            display.set_pos(23, 140)
            display.print("Starting new game")
            sendMessage(b'battleships/playerB', b'playAgain')
            sleep(1)
            return True
        elif msg == b'noPlayAgain':
            refreshDisplay()
            display.set_pos(0, 140)
            display.print("Game over! Other player doesn't want to play again :(")
            sleep(1)
            credits()
            return False
    else:
        sendMessage(b'battleships/playerB', b'noPlayAgain')
        refreshDisplay()
        display.set_pos(0, 140)
        display.print("Game over!")
        waitForMessage()
        sendMessage(b'battleships/playerB', b'noPlayAgain')
        sleep(1)
        credits()
        return False

