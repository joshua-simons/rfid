# Raspberry Pi RFID Login

This project is a proof of concept.  The purpose is to use a MFRC522 compatible rfid reader to set up rfid tags that are used to login to raspbian in lieu of a user inputted password.  This is achieved by modifying the getty process of the pi, and redirecting the login process to a python script that will read an rfid tag, and will identify and authenticate the user based on the UUID stored on the tag.  This is not secure as anyone who can read the tag and clone the UUID will be able to log in to the Pi.  Also, since this method of authentication requires physical access, care was taken so that initiating an ssh connection to the Pi would not trigger the rfid login script.

## Instructions:
These instructions will assume that you have a basic proficiency with raspbian / Linux.

 1. First install raspbian for the Pi that you want to run this code on.  I used Stretch Lite on a Pi 3 B, but I see no reason why it would not work on any Stretch variant.  This will not work on some older versions of Raspbian that still utilize innit instead of systemctl.  After burning the OS image to the SD card, I also created a wpa_supplicant.conf file with my wifi network credentials defined in it (make sure to include 

> country=US

otherwise the wifi will not work so well).  I also created a blank file called ssh to enable ssh on the first boot.

 2. After booting the Pi, I expanded the file system, changed the password, and changed the localization settings for the language, timezone, and keyboard.  Under "Interfacing Options" I enabled SPI.  I waited to reboot the Pi until I had completed wiring the MFRC522 to the breadboard.
 
 3. Wire the MFRC to the breadboard:
 
| MFRC522 | GPIO Pin |
|:---:|:---:|
|SDA|CE0 (8)|
|SCK|SCLK (11)|
|MOSI|MOSI (10)|
|MISO|MISO (9)|
|IRQ|NONE|
|GND|Any Ground Pin|
|RST|25|
|3.3v|Any 3V3 Pin|

4. Now reboot the PI.  When it comes back check to make sure that spi is recognized: 

> lsmod | grep spi

That should list both spidev and spi_bcm2853

5. Update and Upgrade the Pi: 

> sudo apt-get update

> sudo apt-get upgrade

6. Now we are going to install the SPI-py and mfrc522 libraries: 

> git clone https://github.com/lthiery/SPI-Py

> cd SPI-py

> sudo setup.py install

> cd ..

> sudo pip install mfrc522

7. Now, there is a bit of a quirk we are going to be calling the python script from getty@.service, before a user is logged in.  It will be called by the login process itself, but absent the users environmental variables, the Python modules located in the site-packages folder are not accessible from the script, and so we will not be able to import them.  To remedy this we are going to copy those modules into the dist-packages folder: 

> sudo cp -r /home/pi/.local/lib/python2.7/site-packages/mfrc522 /usr/lib/python2.7/dist-packages

> sudo cp -r /home/pi/.local/lib/python2.7/site-packages/spi* /usr/lib/python2.7/dist-packages

8.  OK, so that's about everything you should need to run the auth.py script.  Let's run through it real quick: 

Shabang! Seriously, we need this because we are going to want this in there, because we will be running this in a really weird way.  I really don't know if it will work without it, and at this point I am afraid to ask. Also, I am using env python rather than /usr/bin/python so it is a bit more flexible.

> #!/usr/bin/env python

RPi.GPIO so we can use the GPIO.

mfrc522 so we can use the card reader

os so we can make system calls to Bash commands

time so we can set sleep timers

smtplib so we can send email alerts for failed logins (I actually have mine set up to send to an email to text gateway so I get a text message when there is a failed login attempt). 

> import RPi.GPIO as GPIO

> from mfrc522 import SimpleMFRC522

> import os

> import time

> import smtplib

The SMTP Vars set up the connection to gmail to send the emails.

Next it assigns the reader class to a variable.  It also sets the number of failed attempts to 3 before locking the person out of the system.

Then it prints out some ASCII art, and prompts for the rfid tag.  It reads the id off of the tag, as well as the user name (which was written onto it previously).  If the id matches one of the users in the system it runs through the print commands and then fires up a terminal prompt with this: 

> os.system('su pi -c "/bin/bash"')

This uses os.system to make a Bash call to change to the pi user and call /bin/bash as that user.  There is one quirk about this.  The terminal will open in the root directory.  To fix this, append the .bashrc file in the user's home directory with: 

> cd ~

Make sure that you read the id off of whatever tag you are using and change that and anything else you want to in the commands that are executed after, otherwise you are just going to lock yourself out of the system since you don't have this tag

After 3 failed login attempts, the system locks down for 10 minutes

9. So now we have everything but the bit where we call the python script after the boot process, but before the login prompt.  Before we get to that we are going to set up a bit of a failsafe so we don't lock ourselves out of the Pi if something doesn't work process.  This can be changed back after we verify that our rfid login is working.  What we are going to do is auto-login tty2 at boot so we can Ctrl+Alt+F2 at any point to get a shell prompt and do what we need to do.  All the other tty consoles will be using the rfid login, so this is our easy way out until we verify that everything is working properly.  to achieve this we are going to edit the getty@tty2 service:  

> sudo systemctl edit getty@tty2

That should just open up a blank file.  Write this into it:

> [Service]

> ExecStart=

> ExecStart=/sbin/agetty -a pi --noclear %I $TERM

Go ahead and restart the getty@tty2 service so the changes take effect: 

> sudo systemctl restart getty@tty2

Now if you hit Ctrl+Alt+F2 tty2 should open and should be logged in.

 10. Now that you have created an escape route, it's time to divert the login process to our auth.py script.  For reference, the path to the rfid directory on my system is /home/pi/rfid  You may need to change it to whatever the absolute path to the directory is on your system. 

> sudo nano /lib/systemd/system/getty@.service

You should see a line that looks like this: 

> ExecStart=-/sbin/agetty --noclear %I $TERM

Comment it out.  After that line, add these two lines:

> #ExecStart=-/sbin/agetty --noclear %I $TERM

> ExecStart=

> ExecStart=-/sbin/agetty -a pi -l /home/pi/rfid/login --noclear %I $TERM

Then write out the buffer and exit.  As you can see from the repo, the login bash script simply uses absolute paths to call the auth.py script.  There might be a better way to go about this, but this way works.

## Conclusion
That should be about all you need to get this script working.  Playing around with this taught me a bunch of things I didn't know about the nuts and bolts of the way Raspbian Stretch runs the login process, and got me thinking about more ways that this could be useful.
   

 


