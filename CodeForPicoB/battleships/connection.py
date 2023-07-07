from battleships.ili934xnew import ILI9341, color565
from battleships.display import display, refreshDisplay
from machine import Pin, PWM, Timer
from battleships.intro import turnOffRunningLeds
import network
import time
from battleships.umqtt.robust import MQTTClient
from time import sleep

# connecting on wifi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

# here write your wifi SSID and password
wlan.connect('wifiSSID', 'wifiPASSWORD')

# function sub recieves message and puts it in messageForReturning so waitForMessage can return it
messageForReturning = b''
def sub(topic, msg):
    global messageForReturning
    messageForReturning = msg

mqtt_conn = MQTTClient(client_id='PlayerB', server='broker.hivemq.com',user='',password='',port=1883)
mqtt_conn.set_callback(sub)
try:
    mqtt_conn.connect()
    mqtt_conn.subscribe(b"battleships/playerA")
    turnOffRunningLeds()
except OSError:
    turnOffRunningLeds()
    refreshDisplay()
    display.set_pos(0,90)
    display.set_color(color565(255, 0, 0), color565(0, 0, 0))
    display.print("Connection error, please turn off device and check wifi, password and if it's connected to the Internet.")
    while True:
        sleep(10)

refreshDisplay()
display.set_pos(65,140)
display.set_color(color565(0, 255, 0), color565(0, 0, 0))
display.print("Connection successful!")
sleep(1)
display.set_color(color565(255, 255, 255), color565(0, 0, 0))

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

# function for waiting message and it returns that message
def waitForMessage(info = ""):
    global messageForReturning
    messageForReturning = ""
    if info == "waitingAttack":
        timer = Timer(period = 60, mode = Timer.PERIODIC, callback = runningLed)
        mqtt_conn.wait_msg()
        timer.deinit()
    else:
        mqtt_conn.wait_msg()
    print("RECIEVED: \n    topic: battleships/playerA " + "\n    messg: " + str(messageForReturning))
    return messageForReturning

# function for sending message on topic
def sendMessage(topic, message):
    print("SENT: \n    topic: " + str(topic) + "\n    messg: " + str(message))
    mqtt_conn.publish(topic, message)