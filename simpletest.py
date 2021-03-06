# Simple example of reading the MCP3008 analog input channels and printing
# them all out.
# Author: Tony DiCola
# License: Public Domain
import time

# Import SPI library (for hardware SPI) and MCP3008 library.
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import enemy
import player
import Map
# from .enemy import Enemy
# inport GPIO library
import numpy as np
import RPi.GPIO as GPIO  # import RPi.GPIO module
from time import sleep
import serial  # importa libreria serial lettura valori usb


# Software SPI configuration:
# CLK  = 23
# MISO = 21
# MOSI = 19
# CS   = 24
# mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

# CS2 = 26
# mcp2 = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS2, miso=MISO, mosi=MOSI)

def illuminaStanza():
    nodes = nemico.nodes
    ser.write(str(nemico.getPos()) + ",3;")
    sleep(0.1)
    string = ""
    for n in range(len(nodes)):
        for m in range(len(nodes[0])):
            if player.roomID == nodes[nemico.tileY][nemico.tileX].roomID:
                if nodes[m][n].roomID == player.roomID:
                    string = string + (str(m + n * 15) + ",4;")
                if nodes[m][n].portal:
                    string = string + (str(m + n * 15) + ",2;")
                elif nodes[m][n].manifestazione:
                    string = string + (str(m + n * 15) + ",1;")
            elif nodes[m][n].roomID == player.roomID:
                string = string + (str(m + n * 15) + ",0;")
            elif nodes[m][n].portal:
                string = string + (str(m + n * 15) + ",2;")
            elif nodes[m][n].manifestazione:
                string = string + (str(m + n * 15) + ",1;")
    print(string)
    ser.write(string)


def clearboard():
    string = "0,5;"
    ser.write(string)


# Hardware SPI configuration: un bus, due MCP3008
SPI_PORT = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

SPI_DEVICE = 1
mcp2 = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

GPIO.setmode(GPIO.BCM)  # choose BCM or BOARD
GPIO.setup(2, GPIO.OUT)  # set GPIO24 as an output
GPIO.setup(3, GPIO.OUT)
GPIO.setup(4, GPIO.OUT)
GPIO.setup(14, GPIO.OUT)
GPIO.setup(15, GPIO.OUT)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(27, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)
GPIO.setup(25, GPIO.OUT)
GPIO.setup(5, GPIO.OUT)
GPIO.setup(6, GPIO.OUT)
GPIO.setup(12, GPIO.OUT)

gpioPin = [2, 3, 4, 14, 15, 17, 18, 27, 22, 23, 24, 25, 5, 6, 12]
ser = serial.Serial('/dev/ttyACM0', 9600)
print('Reading MCP3008 values, press Ctrl-C to quit...')
# Print nice channel column headers.
# print('| {0:>4} | {1:>4} | {2:>4} | {3:>4} | {4:>4} | {5:>4} | {6:>4} | {7:>4} |'.format(*range(8)))
print('partenza del ciclo di lettura della posizione')
print('-' * 57)
# Main program loop.
num = 0
count = 0
player = player.Player()
nemico = enemy.Enemy()
posPlayerX = -1
posPlayerY = -1
try:
    while True:
        for n, p in enumerate(gpioPin):
            GPIO.output(p, 1)
            # Read all the ADC channel values in a list.
            values = [0] * 8
            values2 = [0] * 7
            for i in range(8):
                # The read_adc function will get the value of the specified channel (0-7).
                values[i] = mcp.read_adc(i)
            for i in range(7):
                values2[i] = mcp2.read_adc(i)
            # Print the ADC values.
            # results = np.append(values, values2, axis=0)
            #    			print('| {0:>4} | {1:>4} | {2:>4} | {3:>4} | {4:>4} | {5:>4} | {6:>4} | {7:>4} |'.format(*values))
            for i in range(len(values)):
                if values[i] > 1000:
                    # print('{}{}{}{}'.format('sei in posizione ', i, ' , ', n))
                    num = i + n * 15
                    # print(str(i * 15 + n + 1))
                    posPlayerY = i
                    posPlayerX = n
            for i in range(len(values2)):
                if values2[i] > 1000:
                    # print('{}{}{}{}'.format('sei in posizione ', i , ' , ', n + 8))
                    num = (i + 8) + n * 15
                    # print(str((i + 8) * 15 + n + 1))
                    posPlayerY = i + 8
                    posPlayerX = n
                    print(posPlayerX)
                    print(posPlayerY)
            if posPlayerX == initPosX and posPlayerY == initPosY and not playerOnBoard:
                playerOnBoard = True
                print("ciao giocatore")
                player.x=posPlayerX
                player.y=posPlayerY
                player.aggiornaRoom()
                # inserire illuminazione stanza
                illuminaStanza()
            GPIO.output(p, 0)
        time.sleep(0.1)
except KeyboardInterrupt:  # trap a CTRL+C keyboard interrupt
    GPIO.cleanup()
