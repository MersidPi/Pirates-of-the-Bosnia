from machine import Pin, PWM, Timer
from battleships.ili934xnew import ILI9341, color565
from time import sleep
from battleships.display import display, refreshDisplay
from battleships.drawBMP import drawBMP
from battleships import tt32
from battleships import tt24

# function for running led that is being called by a timer
led = [PWM(Pin(4)),PWM(Pin(5)),PWM(Pin(6)),PWM(Pin(7)),PWM(Pin(8)),PWM(Pin(9)),PWM(Pin(10)),PWM(Pin(11))]
for i in range(0,8):
    led[i].duty_u16(0)
currLed = 1
lastLed = 0
increment = 1
duty = 0
def runningLed(p):
    global currLed
    global increment
    global lastLed
    led[currLed].duty_u16(65534)
    led[lastLed].duty_u16(0)
    lastLed = currLed
    currLed += increment
    if currLed == 7 or currLed == 0:
        increment *= -1
timerConnection = Timer(period = 60, mode = Timer.PERIODIC, callback = runningLed)
timerConnection.deinit()

def showIntro():
    refreshDisplay()
    display.set_pos(35,90)
    display.set_font(tt32)
    display.print("Pirates of the")
    display.set_pos(70,120)
    display.print("Bosnia")
    display.set_font(tt24)
    drawBMP(50, 150, "logo")
    sleep(3)
    
    refreshDisplay()
    display.set_pos(50,140)
    display.print("Connecting...")
    global timerConnection
    timerConnection = Timer(period = 60, mode = Timer.PERIODIC, callback = runningLed)

def turnOffRunningLeds():
    global timerConnection
    global led
    timerConnection.deinit()
    for i in range(0,8):
        led[i].duty_u16(0)




