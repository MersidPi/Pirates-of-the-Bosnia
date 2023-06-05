from ili934xnew import ILI9341, color565
from machine import Pin, SPI, Timer
from micropython import const
import os
import glcdfont
import tt14
import tt24
import tt32
from time import sleep

def connect():
    # code for connecting two picos and eventually pico and
    # phone if player selected it
    
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
    
    display.set_pos(50, 140)
    display.print("Connecting...") #myb flickering dots
    sleep(2)
    
    
'''   
    # OVO JE ZA KONEKCIJU NA WIFI
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect('ETF-WiFi-Guest', 'ETF-WiFi-Guest')
    while not wlan.isconnected() and wlan.status() >= 0:
        print("WAINSA")
    time.sleep(1)
    print(wlan.ifconfig())


def sub(topic, msg):
    print('Tema: ' + str(topic))
    print('Poruka: '+ str(msg))
    if topic == b'burek/led1':
        if msg == b'1':
            led0.on()
        else:
            led0.off()
    if topic == b'burek/led2':
        if msg == b'1':
            led4.on()
        else:
            led4.off()
    if topic == b'burek/led3':
        led7.duty_u16(int(float(msg) * 65535))
    
def ocitajTasterIPotenciometar(temp):
    porukaPot = "{\"Potenciometar\": " + str(pot.read_u16()/65535) + "}"
    porukaTas = "{\"Taster\": " + str(taster.value()) + "}"
    mqtt_conn.publish(b'burek/Potenciometar', bytes(porukaPot, 'utf-8'))
    mqtt_conn.publish(b'burek/taster', bytes(porukaTas, 'utf-8'))
tim = Timer(period = 200, mode=Timer.PERIODIC,
callback = ocitajTasterIPotenciometar)

mqtt_conn = MQTTClient(client_id='picoETF',
server='broker.hivemq.com',user='',password='',port=1883)
mqtt_conn.set_callback(sub)
mqtt_conn.connect()
mqtt_conn.subscribe(b"burek/#")
while True:
    mqtt_conn.wait_msg()

'''