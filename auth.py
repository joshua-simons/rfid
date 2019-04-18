#!/usr/bin/env python

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import os
import time
import smtplib

#SMTP Vars
eFROM = "kd2egt@gmail.com"
eTO = "8453094409@msg.fi.google.com"
Subject = "Alert!"
server = smtplib.SMTP_SSL('smtp.gmail.com', 465)

#RFID Vars
reader = SimpleMFRC522()
tries = 3

def readTag():
        global name
        id, name = reader.read()
        return id

try:
	while True:
		os.system('clear')
		print("""/
MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM?+?I7+++MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMO?MNMMMMM8?DMMM7+MMMMMMMM??MMM??M????I$MMMM7IM?MMMMM$?MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMZ+M+MMMM+O+DMMM?MM888888MMMMMM+?MMMMMMZ+IMMI+M++MMMM$+MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMZ+M+$MM++O+DMM+NM88888888MMMMM++MMMMMMM+?MMI+MM++MMM$+MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMZ+MO+MD?N8+DMM+MM88888888NMMMM++M+++++++MMMI+MMM++MM$+MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMZ+MM+?+?M8+DMM+8MD8888888MMMMM++MIII++DMMMMI+MMMM++M$+MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMZ+MMN??MM8+DMMM?MMD88888MMMMMM+?MMMMM??IMMMI+MMMMM+O$+MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM+?MMMMMMN+?MMMMMMMMMMMMMMMMNMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMD++++++IMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
			""")
		print ("Please swipe tag to authenticate.")
		id = readTag()
		if id == 729820977831:
			print ("Authentication Successful")
			print ("Welcome " +name)
			time.sleep(2)
			GPIO.cleanup()
			os.system('clear')
			os.system('su pi -c "/usr/bin/env bash"')
			exit(0)

		if id == 659671112226:
                        print ("Authentication Successful")
                        print ("Root User Authenticated")
                        time.sleep(2)
                        GPIO.cleanup()
                        os.system('clear')
                        os.system('/bin/bash')
                        exit(0)

		else:
			print ("Authrentication Failed")
			tries -= 1

			Text = "Authentication Failure on joshpi"
			eMessage = 'Subject: {}\n\n{}'.format(Subject, Text)
			server.login("kd2egt@gmail.com", "ybihbernfcvynzju")
			server.sendmail(eFROM, eTO, eMessage)
			server.quit
			time.sleep(2)

		if tries == 0:
			os.system('clear')
			print ("Number of Attempts Exceeded")
			sleep(600)
			tries = 3

except KeyboardInterrupt:
	os.system('clear')
	GPIO.cleanup()
	print ("Exited Cleanly")
	exit(0)
