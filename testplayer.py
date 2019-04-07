#In Tenebras: tesi di laurea magistrale
#Alberto Ronchetti
#A.A. 2017-2018
import RPi.GPIO as GPIO
#from lib_nrf24 import NRF24
#import spidev

#GPIO.setmode(GPIO.BCM)

#pipes = [[0xE8, 0xE8, 0xF0, 0xF0, 0xE1], [0xF0, 0xF0, 0xF0, 0xF0, 0xE1]]

#radio = NRF24(GPIO, spidev.SpiDev())
#radio.begin(0, 17)

#radio.setPayloadSize(32)
#radio.setChannel(0x76)
#radio.setDataRate(NRF24.BR_1MBPS)
#radio.setPALevel(NRF24.PA_MIN)

#radio.setAutoAck(True)
#radio.enableDynamicPayloads()
#radio.enableAckPayload()

#radio.openWritingPipe(pipes[0])
#radio.openReadingPipe(1, pipes[1])
#radio.printDetails()



import time

# Import SPI library (for hardware SPI) and MCP3008 library.
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import enemy
import player
import Map

# inport GPIO library
import numpy as np
from time import sleep
import serial  # importa libreria serial lettura valori usb

def illuminaStanza():
    nodes = nemico.nodes
    ser.write(str(nemico.getPos())+",3;")
    sleep(0.1)
    string=""
    for n in range(len(nodes)):
        for m in range(len(nodes[0])):
            if player.roomID == nodes[nemico.tileY][nemico.tileX].roomID:
                if nodes[m][n].roomID == player.roomID:
                    string=string+(str(m + n * 15) + ",4;")
                if nodes[m][n].portal:
                    string=string+(str(m + n * 15) + ",2;")
                elif nodes[m][n].manifestazione:
                    string=string+(str(m + n * 15) + ",1;")
            elif nodes[m][n].roomID == player.roomID:
                string=string+(str(m + n * 15) + ",0;")
            elif nodes[m][n].portal:
                string=string+(str(m + n * 15) + ",2;")
            elif nodes[m][n].manifestazione:
                string=string+(str(m + n * 15) + ",1;")
    print(string)
    ser.write(string)

def clearboard():
    string="0,5;"
    ser.write(string)

# Software SPI configuration:
# CLK  = 23
# MISO = 21
# MOSI = 19
# CS   = 24
# mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

# CS2 = 26
# mcp2 = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS2, miso=MISO, mosi=MOSI)

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
GPIO.setup(12, GPIO.OUT)  # aggiungere tutti gli altri pin: 15 totali finali

gpioPin = [2, 3, 4, 14, 15, 17, 18, 27, 22, 23, 24, 25, 5, 6, 12]
ser = serial.Serial('/dev/ttyACM0', 9600)
print('Reading MCP3008 values, press Ctrl-C to quit...')
print('partenza del ciclo di lettura della posizione')
print('-' * 57)
# Main program loop.
num = 0
count = 0
posPlayerX = -1
posPlayerY = -1
playerOnBoard = False
playerEndTurn = False
player = player.Player()
nemico = enemy.Enemy()
initPosX = 7
initPosY = 14
mappa = Map.Map()
specchio=False
piuma=False
fiasca=False
doppioTurno=False
vittoria=False
sconfitta=False
successo=False
risolte=0
battito=0
minTemp=0
try:
    clearboard()
    # accende led
    ser.write(str(
        initPosY + initPosX * 15) + ",0;")  # inizializzazione del giocatore: deve venir posizionato sulla casella 217, e nemico
    # manca battito rilevato
    while not playerOnBoard:
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
    time.sleep(5)
    #####################################################
    #            controllo battito cardiaco             #
    # while battito==0:
    #   message=list("0")
    #   while len(message)<32:
    #       message.append(0)
    #   start = time.time()
    #   radio.write(message)
    #   print("Sent the message: {}".format(message))
    #   radio.startListening()
    #   while not radio.available(0):
    #       time.sleep(1 / 100)
    #       if time.time() - start > 2:
    #           print("Timed out.")
    #           break
    #   receivedMessage = []
    #   radio.read(receivedMessage, radio.getDynamicPayloadSize())
    #   print("Received: {}".format(receivedMessage))
    #
    #   print("traduzione in unicode")
    #   string = ""
    #   for n in receivedMessage:
    #      if (n >= 32 and n <= 126):
    #           string += chr(n)
    #   print("messaggio ricevuto e tradotto: {}".format(string))
    #   if int(string)>battito*1.15:
    #       nemico.maxMovement=4
    #   elsif int(string)>battito*1.3:
    #       nemico.maxMovement=5
    #   radio.stopListening()
    #
    #####################################################
    while not vittoria or not sconfitta:  # gestione del turno giocatore
        #   message=list("2")
        #   while len(message)<32:
        #       message.append(0)
        #   start = time.time()
        #   radio.write(message)
        #   print("Sent the message: {}".format(message))
        #   radio.startListening()
        #   while not radio.available(0):
        #       time.sleep(1 / 100)
        #       if time.time() - start > 2:
        #           print("Timed out.")
        #           break
        #   receivedMessage = []
        #   radio.read(receivedMessage, radio.getDynamicPayloadSize())
        #   print("Received: {}".format(receivedMessage))
        #
        #   print("traduzione in unicode")
        #   string = ""
        #   for n in receivedMessage:
        #      if (n >= 32 and n <= 126):
        #           string += chr(n)
        #   print("messaggio ricevuto e tradotto: {}".format(string))
        #   battito=int(string)
        #   radio.stopListening()
        print("gestione turno giocatore")
        count += 1
        nodes = nemico.getNodes()
        if nodes[player.y][player.x].portal:
            playerEndTurn = True
            nemico.destroyPortal(player.x, player.y)
        elif nodes[player.y][player.x].manifestazione:
            playerEndTurn = True
            ######################################################################################
            # inserire prova sensori per risoluzione manifestazione e gestione evento            #
            # #######################################
            # temperatura
            #########################################
            # prova=np.random.random_integers(2)
            # if prova==1:      temperatura
            #   message=list("1")
            #   while len(message)<32:
            #       message.append(0)
            #   start = time.time()
            #   radio.write(message)
            #   print("Sent the message: {}".format(message))
            #   radio.startListening()
            #   while not radio.available(0):
            #       time.sleep(1 / 100)
            #       if time.time() - start > 2:
            #           print("Timed out.")
            #           break
            #   receivedMessage = []
            #   radio.read(receivedMessage, radio.getDynamicPayloadSize())
            #   print("Received: {}".format(receivedMessage))
            #   print("traduzione in unicode")
            #   string = ""
            #   for n in receivedMessage:
            #      if (n >= 32 and n <= 126):
            #           string += chr(n)
            #   print("messaggio ricevuto e tradotto: {}".format(string))
            #   minTemp=int(string)
            #   radio.stopListening()
            #   for i in range(5):
            #       time.sleep(1)
            #       message=list("3")
            #           while len(message)<32:
            #               message.append(0)
            #       start = time.time()
            #           radio.write(message)
            #           print("Sent the message: {}".format(message))
            #           radio.startListening()
            #           while not radio.available(0):
            #               time.sleep(1 / 100)
            #               if time.time() - start > 2:
            #                   print("Timed out.")
            #                   break
            #           receivedMessage = []
            #           radio.read(receivedMessage, radio.getDynamicPayloadSize())
            #           print("Received: {}".format(receivedMessage))
            #           print("traduzione in unicode")
            #           string = ""
            #           for n in receivedMessage:
            #               if (n >= 32 and n <= 126):
            #                   string += chr(n)
            #           print("messaggio ricevuto e tradotto: {}".format(string))
            #           temp=int(string)
            #           if temp>5*0.5*risolte:
            #               successo=True
            # #######################################
            # giroscopio
            #########################################
            # if prova==2:
            #
            ######################################################################################
            if successo:
                successo=False
                nemico.risolviManifestazione(player.x, player.y)
                risolte+=1
        else:
            oldPosx = player.x
            oldPosy = player.y
            playerOnBoard = False
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
                        playerOnBoard = True
                        #print('{}{}{}{}'.format('sei in posizione ', i, ' , ', n))
                        num = i + n * 15
                        print(str(i + n * 15))
                        posPlayerY = i
                        posPlayerX = n
                for i in range(len(values2)):
                    if values2[i] > 1000:
                        playerOnBoard = True
                        #print('{}{}{}{}'.format('sei in posizione ', i, ' , ', n + 8))
                        num = (i + 8) + n * 15
                        print(str((i + 8) + n * 15))
                        posPlayerY = i + 8
                        posPlayerX = n
                        # Pause for half a second.
                if playerOnBoard and (posPlayerX != oldPosx or posPlayerY != oldPosy):
                    if abs(posPlayerX-oldPosx)>4 or abs(posPlayerY-oldPosy)>4:
                        print("xdiff")
                        print(abs(posPlayerX-oldPosx))
                        print("ydiff")
                        print(abs(posPlayerY-oldPosy))
                    else:

                        playerEndTurn = True
                else:
                    if ser.in_waiting>0:        # uso oggetto
                        print("usato un oggetto")
                        oggetto=ser.readline()
                        print(oggetto)
                        if '04 27 84 EA E6 4C 81' in oggetto and not piuma:
                            piuma=True
                            doppioTurno=True
                            print("piuma")
                        elif '04 38 83 BA 90 5B 81' in oggetto and not fiasca:
                            fiasca=True
                            player.addStamina(3)
                            print("fiasca")
                        elif '04 40 83 BA 90 5B 81' in oggetto and not specchio:
                            ser.write(str(nemico.getPos())+",3;")
                            specchio=True
                            print("specchio")
                    #####################################################
                    #                          riposo                   #
                    #####################################################
                    #   message=list("4")
                    #   while len(message)<32:
                    #       message.append(0)
                    #   start = time.time()
                    #   radio.write(message)
                    #   print("Sent the message: {}".format(message))
                    #   radio.startListening()
                    #   while not radio.available(0):
                    #       time.sleep(1 / 100)
                    #       if time.time() - start > 2:
                    #           print("Timed out.")
                    #           break
                    #   receivedMessage = []
                    #   radio.read(receivedMessage, radio.getDynamicPayloadSize())
                    #   print("Received: {}".format(receivedMessage))
                    #
                    #   print("traduzione in unicode")
                    #   string = ""
                    #   for n in receivedMessage:
                    #      if (n >= 32 and n <= 126):
                    #           string += chr(n)
                    #   print("messaggio ricevuto e tradotto: {}".format(string))
                    #   if int(string)>175 and int(string)<185:
                    #       playerEndTurn = True
                    #       player.addStamina(1)
                    #   message=list("5")
                    #   while len(message)<32:
                    #       message.append(0)
                    #   start = time.time()
                    #   radio.write(message)
                    #   print("Sent the message: {}".format(message))
                    #   radio.startListening()
                    #   while not radio.available(0):
                    #       time.sleep(1 / 100)
                    #       if time.time() - start > 2:
                    #           print("Timed out.")
                    #           break
                    #   receivedMessage = []
                    #   radio.read(receivedMessage, radio.getDynamicPayloadSize())
                    #   print("Received: {}".format(receivedMessage))
                    #
                    #   print("traduzione in unicode")
                    #   string = ""
                    #   for n in receivedMessage:
                    #      if (n >= 32 and n <= 126):
                    #           string += chr(n)
                    #   print("messaggio ricevuto e tradotto: {}".format(string))
                    #   if int(string)>175 and int(string)<185:
                    #       playerEndTurn = True
                    #       player.addStamina(1)
                    #   radio.stopListening()
                    playerEndTurn = False
                time.sleep(0.05)
                GPIO.output(p, 0)
        if playerEndTurn and not doppioTurno:
            clearboard()
            print("fine turno")
            time.sleep(2)
            playerEndTurn = False
            player.x=posPlayerX
            player.y=posPlayerY
            player.aggiornaRoom()
            nemico.move1=True
            nemico.updatePlayerPos(player.x, player.y)
            nemico.update()
            if nemico.playerTarget.fede==0:
                sconfitta=True
            elif nemico.countportal()==6:
                sconfitta=True
            illuminaStanza()
            ser.write(str(nemico.getPos())+",3;")
        elif playerEndTurn and doppioTurno:
            print("doppioturno")
            playerEndTurn = False
            player.x=posPlayerX
            player.y=posPlayerY
            player.aggiornaRoom()
            doppioTurno=False
        if count == 100:
            ser.flushInput()
            count = 0
except KeyboardInterrupt:  # trap a CTRL+C keyboard interrupt
    GPIO.cleanup()



