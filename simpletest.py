
# Simple example of reading the MCP3008 analog input channels and printing
# them all out.
# Author: Tony DiCola
# License: Public Domain
import time

# Import SPI library (for hardware SPI) and MCP3008 library.
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

# inport GPIO library
import numpy as np
import RPi.GPIO as GPIO            # import RPi.GPIO module
from time import sleep
import serial #importa libreria serial lettura valori usb


# Software SPI configuration:
#CLK  = 23
#MISO = 21
#MOSI = 19
#CS   = 24
#mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

#CS2 = 26
#mcp2 = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS2, miso=MISO, mosi=MOSI)

# Hardware SPI configuration: un bus, due MCP3008
SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

SPI_DEVICE = 1
mcp2 = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))


GPIO.setmode(GPIO.BCM)             # choose BCM or BOARD
GPIO.setup(22, GPIO.OUT)           # set GPIO24 as an output
GPIO.setup(17, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)

gpioPin = [ 22, 17, 24, 23]
ser = serial.Serial('/dev/ttyACM0', 9600)
print('Reading MCP3008 values, press Ctrl-C to quit...')
# Print nice channel column headers.
#print('| {0:>4} | {1:>4} | {2:>4} | {3:>4} | {4:>4} | {5:>4} | {6:>4} | {7:>4} |'.format(*range(8)))
print('partenza del ciclo di lettura della posizione')
print('-' * 57)
# Main program loop.
num=0

try:
	while True:
		for n,p in enumerate(gpioPin):
			GPIO.output(p, 1)
    			# Read all the ADC channel values in a list.
    			values = [0]*8
			values2 = [0]*8
    			for i in range(8):
        			# The read_adc function will get the value of the specified channel (0-7).
        			values[i] = mcp.read_adc(i)
				values2[i] = mcp2.read_adc(i)
    			# Print the ADC values.
			#results = np.append(values, values2, axis=0)
#    			print('| {0:>4} | {1:>4} | {2:>4} | {3:>4} | {4:>4} | {5:>4} | {6:>4} | {7:>4} |'.format(*values))
    			for i in range(len(values2)):
				if values2[i]>1000:
					print('{}{}{}{}'.format('sei in posizione ',i,' , ',n))
					num=i*4+n
					print(str(i*4+n+1))
			# Pause for half a second.
			ser.write(str(num))
    			time.sleep(0.05)
			GPIO.output(p, 0)
except KeyboardInterrupt:          # trap a CTRL+C keyboard interrupt
    GPIO.cleanup()
