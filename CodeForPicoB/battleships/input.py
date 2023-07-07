from machine import Pin, ADC, Timer, PWM
from time import sleep
from battleships.connection import waitForMessage, sendMessage

# declaration for pico buttons
t0 = Pin(0, Pin.IN)
t1 = Pin(1, Pin.IN)
t2 = Pin(2, Pin.IN)
t3 = Pin(3, Pin.IN)

# declaration for keyboard
R1 = Pin(21, Pin.OUT)
R2 = Pin(22, Pin.OUT)
R3 = Pin(26, Pin.OUT)
R4 = Pin(27, Pin.OUT)
C1 = Pin(0, Pin.IN)
C2 = Pin(1, Pin.IN)
C3 = Pin(2, Pin.IN)
C4 = Pin(3, Pin.IN)

def dummy(p):
    return 0

timGoing = False
tim = Timer(period = 200, mode = Timer.PERIODIC, callback = dummy)
tim.deinit()

# function for leds that are slowly turning off when being called by timer
led = [PWM(Pin(4)),PWM(Pin(5)),PWM(Pin(6)),PWM(Pin(7)),PWM(Pin(8)),PWM(Pin(9)),PWM(Pin(10)),PWM(Pin(11))]
for i in range(0, 8):
    led[i].duty_u16(0)
currentLed = 0
currentDuty = 65534
timeOut = False
def updateLeds(p):
    global currentLed
    global currentDuty
    if currentDuty > 7000:
        currentDuty -= 6553
    elif currentDuty > 2600:
        currentDuty -= 2000
    else:
        currentDuty -= 600
    if currentDuty < 0:
        led[currentLed].duty_u16(0)
        currentLed += 1
        currentDuty = 65534
    if currentLed != 8:
        led[currentLed].duty_u16(currentDuty)
    else:
        global timeOut
        timeOut = True
        global tim
        tim.deinit()
        timGoing = False
        sendMessage(b'battleships/playerA', b'TIMEOUT')

# function that stops timer, turns off leds
def exitProcedure(select = False):
    global tim
    global timGoing
    tim.deinit()
    timGoing = False
    if select == True:
        for i in range(0, 8):
            led[i].duty_u16(0)

# function for getting input and returns: UP DOWN LEFT RIGHT SELECT TIMEOUT
def getInput(inputMode, attack = False):
    # if input is for attack, turn on timer if it's not going
    if attack == True:
        global tim
        global timGoing
        if timGoing == False:
            timGoing = True
            tim = Timer(period = 100, mode = Timer.PERIODIC, callback = updateLeds)
            global timeOut
            global currentLed
            global currentDuty
            timeOut = False
            currentLed = 0
            currentDuty = 65534
            for i in range(0, 8):
                led[i].duty_u16(65534)
    if inputMode == "Joystick":
        # declaration for joystick (its here bc we use same pins for keyboard)
        xAxis = ADC(Pin(26))
        yAxis = ADC(Pin(27))
        SW = Pin(22,Pin.IN, Pin.PULL_UP)
        while True:
            global timeOut
            if timeOut == True:
                exitProcedure(True)
                return "TIMEOUT"
            x = xAxis.read_u16()
            y = yAxis.read_u16()
            if x < 4000:
                return "UP"
            elif x > 60000:
                return "DOWN"
            elif y > 60000:
                return "LEFT"
            elif y < 4000:
                return "RIGHT"
            elif SW.value() == 0:
                exitProcedure(True)
                return "SELECT"
            sleep(0.1)
    elif inputMode == "Phone":
        # phone will send one of these messages: UP DOWN LEFT RIGHT SELECT
        # or pico will send to itself TIMEOUT if timeOut == True
        msg = waitForMessage()
        if msg == b'SELECT' or msg == b'TIMEOUT':
            exitProcedure(True)
        return (msg).decode('utf-8')
    elif inputMode == "Keyboard":
        # turning off all rows
        R1.value(0)
        R2.value(0)
        R3.value(0)
        R4.value(0)
        while True:
            global timeOut
            if timeOut == True:
                exitProcedure(True)
                return "TIMEOUT"
            R1.value(1)
            if C2.value():
                print("up")
                return "UP"
            R1.value(0)
            R2.value(1)
            if C1.value():
                return "LEFT"
            elif C2.value():
                exitProcedure(True)
                return "SELECT"
            elif C3.value():
                return "RIGHT"
            R2.value(0)
            R3.value(1)
            if C2.value():
                return "DOWN"
            R3.value(0)
            sleep(0.1)
