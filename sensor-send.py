import math
import pyfirmata
import smtplib
import time

From = '' # from e-mail address
To = [''] # to e-mail address

PORT = "/dev/ttyUSB0" # Raspberry Pi serial port connected to Arduino - change to match your Pi
#PORT = "/dev/tty.usbserial-A7006RoW" # Mac Computer serial port connected to Arduino - for testing - change to match your setup

pad = 6700

# function to calculate degrees Celsius from Thermister value
def Thermister(RawADC):
	Resistance  = ((1024 * pad / RawADC) - pad)
	Temp = math.log(Resistance)
	Temp = 1 / (0.001129148 + (0.000234125 * Temp) + (0.0000000876741 * Temp * Temp * Temp))
	Temp = int(round(Temp - 273.15))  #Convert Kelvin to Celcius
	return Temp

#ARDUINO CODE
#Start firmata on the Arduino
board = pyfirmata.Arduino(PORT)
it = pyfirmata.util.Iterator(board)
it.start()

board.analog[0].enable_reporting()

#IMPORTANT! discard first reads until A0 gets something valid
while board.analog[0].read() is None:
	pass

#now ok to read pin or pins
pinValue = board.analog[0].read()
board.exit() #clean exit from Arduino board instance

tempValue = Thermister(round(pinValue * 1000)) #convert pin value to temperature
#END Arduino Code

#send message to recipients
Subject = "Aquaponics greenhouse report"
Text = "Air temperature is " + str(tempValue) + " C"
#Format mail message
mMessage = ('From: Aquaponics Greenhouse<%s>\nTo: %s\nSubject:%s\n%s\n' % (From, To, Subject, Text))
print 'Connecting to Server'
try:
   smtpObj = smtplib.SMTP('smtp.ntlworld.com') #mail server - change to match local network connection

   smtpObj.sendmail(From, To, mMessage)         
   print "Successfully sent email"
except smtplib.SMTPException:
   print "Error: unable to send email"
smtpObj.quit()
