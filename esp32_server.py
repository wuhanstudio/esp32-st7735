import network
import utime
import socket
import gc

from machine import SPI,Pin
from ST7735 import TFT,TFTColor

# Change to your settings
WIFI_SSID = ''
WIFI_PWD  = ''

TFT_SCK  = 18
TFT_MOSI = 23
TFT_MISO = 19

TFT_LED = 13
TFT_RST = 16
TFT_RS  = 17
TFT_CS  = 26

# Connect to WIFI
sta_if = network.WLAN(network.STA_IF)
if not sta_if.active():
    sta_if.active(True)

if not sta_if.isconnected():
    sta_if.connect(WIFI_SSID, WIFI_PWD)
    for i in range(0, 5):
        if(not sta_if.isconnected()):
            utime.sleep_ms(1000)

print(sta_if.ifconfig())

# Initialize TFT
back_light = Pin(TFT_LED, Pin.OUT)
back_light.on()

spi = SPI(2, baudrate=20000000, polarity=0, phase=0, sck=Pin(TFT_SCK), mosi=Pin(TFT_MOSI), miso=Pin(TFT_MISO))
tft=TFT(spi, TFT_RS, TFT_RST, TFT_CS)

tft.initr()
tft.rgb(True)
tft.fill(TFT.WHITE)

# Listening on Port 9191
addr = socket.getaddrinfo('0.0.0.0', 9191)[0][-1]

s = socket.socket()
s.bind(addr)
s.listen(1)

print('listening on', addr)

while True:
    cl, addr = s.accept()
    print('client connected from', addr)
    try:
        # Check magic number
        data = cl.recv(2)
        if not data:
            cl.close()
            continue
        if(data[0] == 0xAA and data[1] == 0x55):
            # Check width and height
            data = cl.recv(2)
            width = int(data[0])
            height = int(data[1])
            print(width, height)
            if(width > 0 and width <= 128 and height > 0 and height <= 128):
                tft.rgb(True)
                tft.fill(TFT.WHITE)

                # Displaying the image at the center
                start_x = int(64 - width / 2)
                start_y = int(64 - height / 2)
                end_x = start_x + width - 1
                end_y = start_y + height - 1
                print(start_x, start_y)
                print(end_x, end_y)
                tft._setwindowloc((start_x, start_y), (end_x, end_y))

                print('Displaying Image')

                for i in range(0, width*height):
                    data = cl.recv(3)
                    if(len(data) == 3):
                        tft._pushcolor(TFTColor(data[2], data[1], data[0]))
                    else:
                        print(data)
                        print('Invalid Pixel ' + str(i))
                        print(gc.mem_free())
                        break
        else:
            cl.send('Error')
    finally:
        cl.close()
