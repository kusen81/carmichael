#!/usr/bin/python
import argparse
import sys
import os
import time
import RPi.GPIO as gpio
import random
from bluetooth import *

def init():
    gpio.setmode(gpio.BOARD)
    gpio.setwarnings(False) 
    gpio.setup(37, gpio.OUT, initial = 0) # H bridge IN1. Var forut 15
    gpio.setup(35, gpio.OUT, initial = 0) # H bridge IN2. Var forut 13.
    gpio.setup(33, gpio.OUT, initial = 0) # H bridge IN3. Var forut 11.
    gpio.setup(31, gpio.OUT, initial = 0) # H bridge IN4. Var forut 12.
    gpio.setup(38, gpio.OUT, initial = 0) # Ultra sonic sensor out. Var forut 3.
    gpio.setup(36, gpio.IN) # Ultra sonic sensor in. Var forut 7.
    gpio.setup(32, gpio.OUT) # Piezo buzzer. Var forut 16.

    # Motors init
    global duty_cycle
    duty_cycle = 40
    freq = 300
    global p11
    global p12
    global p13
    global p15
    global p16 # Piezo buzzer
    p11 = gpio.PWM(33, freq)
    p12 = gpio.PWM(31, freq)
    p13 = gpio.PWM(35, freq)
    p15 = gpio.PWM(37, freq)
    p16 = gpio.PWM(32, 100)

    # Notes
    global NOTE_B0
    global NOTE_C1
    global NOTE_CS1
    global NOTE_D1
    global NOTE_DS1
    global NOTE_E1
    global NOTE_F1
    global NOTE_FS1
    global NOTE_G1
    global NOTE_GS1
    global NOTE_A1
    global NOTE_AS1
    global NOTE_B1
    global NOTE_C2
    global NOTE_CS2
    global NOTE_D2
    global NOTE_DS2
    global NOTE_E2
    global NOTE_F2
    global NOTE_FS2
    global NOTE_G2
    global NOTE_GS2
    global NOTE_A2
    global NOTE_AS2
    global NOTE_B2
    global NOTE_C3
    global NOTE_CS3
    global NOTE_D3
    global NOTE_DS3
    global NOTE_E3
    global NOTE_F3
    global NOTE_FS3
    global NOTE_G3
    global NOTE_GS3
    global NOTE_A3
    global NOTE_AS3
    global NOTE_B3
    global NOTE_C4
    global NOTE_CS4
    global NOTE_D4
    global NOTE_DS4
    global NOTE_E4
    global NOTE_F4
    global NOTE_FS4
    global NOTE_G4
    global NOTE_GS4
    global NOTE_A4
    global NOTE_AS4
    global NOTE_B4
    global NOTE_C5
    global NOTE_CS5
    global NOTE_D5
    global NOTE_DS5
    global NOTE_E5
    global NOTE_F5
    global NOTE_FS5
    global NOTE_G5
    global NOTE_GS5
    global NOTE_A5
    global NOTE_AS5
    global NOTE_B5
    global NOTE_C6
    global NOTE_CS6
    global NOTE_D6
    global NOTE_DS6
    global NOTE_E6
    global NOTE_F6
    global NOTE_FS6
    global NOTE_G6
    global NOTE_GS6
    global NOTE_A6
    global NOTE_AS6
    global NOTE_B6
    global NOTE_C7
    global NOTE_CS7
    global NOTE_D7
    global NOTE_DS7
    global NOTE_E7
    global NOTE_F7
    global NOTE_FS7
    global NOTE_G7
    global NOTE_GS7
    global NOTE_A7
    global NOTE_AS7
    global NOTE_B7
    global NOTE_C8
    global NOTE_CS8
    global NOTE_D8
    global NOTE_DS8


    NOTE_B0 = 31
    NOTE_C1 = 33
    NOTE_CS1 = 35
    NOTE_D1 = 37
    NOTE_DS1 = 39
    NOTE_E1 = 41
    NOTE_F1 = 44
    NOTE_FS1 = 46
    NOTE_G1 = 49
    NOTE_GS1 = 52
    NOTE_A1 = 55
    NOTE_AS1 = 58
    NOTE_B1 = 62
    NOTE_C2 = 65
    NOTE_CS2 = 69
    NOTE_D2 = 73
    NOTE_DS2 = 78
    NOTE_E2 = 82
    NOTE_F2 = 87
    NOTE_FS2 = 93
    NOTE_G2 = 98
    NOTE_GS2 = 104
    NOTE_A2 = 110
    NOTE_AS2 = 117
    NOTE_B2 = 123
    NOTE_C3 = 131
    NOTE_CS3 = 139
    NOTE_D3 = 147
    NOTE_DS3 = 156
    NOTE_E3 = 165
    NOTE_F3 = 175
    NOTE_FS3 = 185
    NOTE_G3 = 196
    NOTE_GS3 = 208
    NOTE_A3 = 220
    NOTE_AS3 = 233
    NOTE_B3 = 247
    NOTE_C4 = 262
    NOTE_CS4 = 277
    NOTE_D4 = 294
    NOTE_DS4 = 311
    NOTE_E4 = 330
    NOTE_F4 = 349
    NOTE_FS4 = 370
    NOTE_G4 = 392
    NOTE_GS4 = 415
    NOTE_A4 = 440
    NOTE_AS4 = 466
    NOTE_B4 = 494
    NOTE_C5 = 523
    NOTE_CS5 = 554
    NOTE_D5 = 587
    NOTE_DS5 = 622
    NOTE_E5 = 659
    NOTE_F5 = 698
    NOTE_FS5 = 740
    NOTE_G5 = 784
    NOTE_GS5 = 831
    NOTE_A5 = 880
    NOTE_AS5 = 932
    NOTE_B5 = 988
    NOTE_C6 = 1047
    NOTE_CS6 = 1109
    NOTE_D6 = 1175
    NOTE_DS6 = 1245
    NOTE_E6 = 1319
    NOTE_F6 = 1397
    NOTE_FS6 = 1480
    NOTE_G6 = 1568
    NOTE_GS6 = 1661
    NOTE_A6 = 1760
    NOTE_AS6 = 1865
    NOTE_B6 = 1976
    NOTE_C7 = 2093
    NOTE_CS7 = 2217
    NOTE_D7 = 2349
    NOTE_DS7 = 2489
    NOTE_E7 = 2637
    NOTE_F7 = 2794
    NOTE_FS7 = 2960
    NOTE_G7 = 3136
    NOTE_GS7 = 3322
    NOTE_A7 = 3520
    NOTE_AS7 = 3729
    NOTE_B7 = 3951
    NOTE_C8 = 4186
    NOTE_CS8 = 4435
    NOTE_D8 = 4699
    NOTE_DS8 = 4978

    global buzzer_speed

def autonomy():
    delay = 0.1
    degr_90 = 1.0/(duty_cycle/30.0)
    print("degre_90: " + str(degr_90))

    time.sleep(delay)
    dist = distance('cm')
    print dist

    if dist < 25:
        stop()
	#print("Setting buzzer set to HIGH")
	#gpio.output(16, gpio.HIGH)
	#print("Sleeping for 0.1 sec")
	#time.sleep(0.1)
	#print("Setting buzzer to LOW")
	#gpio.output(16, gpio.LOW)
	gpio.output(32, True) 
	buzzer_speed = 0.2
	p16.start(10) # 10% duty cycle sounds 'ok'
	p16.ChangeFrequency(200)
	time.sleep(buzzer_speed)
	p16.ChangeFrequency(100)
	time.sleep(buzzer_speed)
	p16.stop()

        rand = random.randrange(0,2);
        if rand == 0:
            pivotLeft(degr_90)
        elif rand == 1:
            pivotRight(degr_90)
        elif rand == 2:
            back()

        print("Pivoting left")
    else:
        forward()
        print("Going forward")

def distance(measure='cm'):
	sig = 0
	nosig = 0
        print("1")
	gpio.output(38, True)
        print("2")
        gpio.output(38, False)
        print("3")
	while gpio.input(36) == 0:
		nosig = time.time()
        print("4")
	while gpio.input(36) == 1:
		sig = time.time()
        print("5")
	tl = sig - nosig

	if measure == 'cm':
		distance = tl / 0.000058
	elif measure == 'in':
		distance = tl / 0.000148
	else:
		print("Improper choice of measurement: in or cm")
		distance = None

	return distance

# Pivot Left function
def pivotRight(runtime = 0.05):
        p12.start(duty_cycle)
        p11.stop()
        p13.stop()
        p15.start(duty_cycle)
	time.sleep(runtime)
	return

# Pivot Right function
def pivotLeft(runtime = 0.05):
        p12.stop()
        p11.start(duty_cycle)
        p13.start(duty_cycle)
        p15.stop()
	time.sleep(runtime)
	return

# Forward Left function
def backLeft(runtime = 0.05):
        p12.start(duty_cycle)
        p11.stop()
        p13.stop()
        p15.stop()
	time.sleep(runtime)
	return

# Forward Right function
def backRight(runtime = 0.05):
        p13.start(duty_cycle)
        p11.stop()
        p12.stop()
        p15.stop()
	time.sleep(runtime)
	return

# Back Left function
def forwardLeft(runtime = 0.05):
        p11.start(duty_cycle)
        p12.stop()
        p13.stop()
        p15.stop()
	time.sleep(runtime)
	return

# Back Right function
def forwardRight(runtime = 0.05):
        p15.start(duty_cycle)
        p11.stop()
        p12.stop()
        p13.stop()
	time.sleep(runtime)
	return

# Forward function
def back(runtime = 0.05):
        p12.start(duty_cycle)
        p13.start(duty_cycle)
        p11.stop()
        p15.stop()
	time.sleep(runtime)
	return

# Back function
def forward(runtime = 0.05):
        p11.start(duty_cycle)
        p15.start(duty_cycle)
        p12.stop()
        p13.stop()
	time.sleep(runtime)
	return

# Stop function
def stop():
        p11.stop()
        p12.stop()
        p13.stop()
        p15.stop()
        return

# Main loop
def main():
        global duty_cycle
        ###print "Start"

        # We need to wait until Bluetooth init is done
        time.sleep(1)

        # Make device visible
        os.system("hciconfig hci0 piscan")

        # Create a new server socket using RFCOMM protocol
        server_sock = BluetoothSocket(RFCOMM)
        # Bind to any port
        server_sock.bind(("", PORT_ANY))
        # Start listening
        server_sock.listen(1)

        # Get the port the server socket is listening
        port = server_sock.getsockname()[1]

        # The service UUID to advertise
        uuid = "7be1fcb3-5776-42fb-91fd-2ee7b5bbb86d"
        #uuid = "29075e46-f0d4-44e2-a9e7-55ac02d6e6cc"

        # Start advertising the service
        advertise_service(server_sock, "RaspiBtSrv",
                       service_id=uuid,
                       service_classes=[uuid, SERIAL_PORT_CLASS],
                       profiles=[SERIAL_PORT_PROFILE])

        # Main Bluetooth server loop
        while True:

                init()

                # Startup completed sound
                gpio.output(32, True)
            	buzzer_speed = 0.2
                p16.start(10)
                p16.ChangeFrequency(NOTE_E6)
                time.sleep(buzzer_speed)
                p16.ChangeFrequency(NOTE_G6)
                time.sleep(buzzer_speed)
                p16.ChangeFrequency(NOTE_E7)
                time.sleep(buzzer_speed)
                p16.ChangeFrequency(NOTE_C7)
                time.sleep(buzzer_speed)
                p16.ChangeFrequency(NOTE_D7)
                time.sleep(buzzer_speed)
                p16.ChangeFrequency(NOTE_G7)
                time.sleep(buzzer_speed)
                p16.stop()

                print "Waiting for connection on RFCOMM channel %d" % port

                try:
                        client_sock = None

                        # This will block until we get a new connection
                        print("Please connect bluetooth controller")
                        client_sock, client_info = server_sock.accept()
                        print "Accepted connection from ", client_info

                        # Blutetooth connected sound
	                gpio.output(32, True) 
            	        buzzer_speed = 0.2
                	p16.start(10)
                	p16.ChangeFrequency(NOTE_A5)
                	time.sleep(buzzer_speed)
                	p16.ChangeFrequency(NOTE_B5)
                	time.sleep(buzzer_speed)
                	p16.ChangeFrequency(NOTE_C5)
                	time.sleep(buzzer_speed)
                	p16.ChangeFrequency(NOTE_B5)
                	time.sleep(buzzer_speed)
                	p16.stop()

			auto = False # Begin with manual control. Sets to True when car should be autonomous.

                        # Read the data sent by the client
                        while True:
                                ###print "Waiting for command"
                                data = client_sock.recv(1024)
                                print "Received: %s" % repr(data)

				if auto == False:
	                                if ("F" in data):
        	                                print "Moving forward"
                	                        forward(0.05)
                        	        elif ("B" in data):
                                	        print "Moving backward"
                                        	back(0.05)
	                                elif ("L" in data):
        	                                print "Pivot left"
                	                        pivotLeft(0.05)
	                                elif ("R" in data):
        	                                print "Pivot right"
                	                        pivotRight(0.05)
	                                elif ("G" in data):
        	                                print "Forward left"
                	                        forwardLeft(0.05)
                        	        elif ("I" in data):
                                	        print "Forward right"
                                        	forwardRight(0.05)
	                                elif ("H" in data):
        	                                print "back left"
                	                        backLeft(0.05)
                        	        elif ("J" in data):
                                	        print "Back right"
                                        	backRight(0.05)
	                                elif ("S" in data):
        	                                stop()
	                                elif (data in str(range(9))):
                                                print("Changing speed to: " + data)
        	                                duty_cycle = 10 + int(data) * 10
                                                print("Duty cycle is: " + str(duty_cycle))
					elif ("V" in data):
						auto = not auto
                                        elif (data == "q\r\n"):
                                                stop()
	                                        print ("Quit")
        	                                break
				elif auto == True:
                                	if ("v" in data):
                                        	auto = not auto
					else:
                                                autonomy()
                except IOError:
                        stop()
                        pass

                except KeyboardInterrupt:

                        if client_sock is not None:
                                client_sock.close()

                        server_sock.close()
                        stop()

                        print "Server going down"
                        break

main()
gpio.cleanup()
print("Cleanup")
