import RPi.GPIO as GPIO
import time
import picamera
import cv2
import numpy as np
from AlphaBot2 import AlphaBot2

Ab = AlphaBot2()

IR = 17
PWM = 50
n=0

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(IR,GPIO.IN)


def getkey():
	if GPIO.input(IR) == 0:
		count = 0
		while GPIO.input(IR) == 0 and count < 200:  #9ms
			count += 1
			time.sleep(0.00006)
		if(count < 10):
			return;
		count = 0
		while GPIO.input(IR) == 1 and count < 80:  #4.5ms
			count += 1
			time.sleep(0.00006)

		idx = 0
		cnt = 0
		data = [0,0,0,0]
		for i in range(0,32):
			count = 0
			while GPIO.input(IR) == 0 and count < 15:    #0.56ms
				count += 1
				time.sleep(0.00006)
				
			count = 0
			while GPIO.input(IR) == 1 and count < 40:   #0: 0.56mx
				count += 1                               #1: 1.69ms
				time.sleep(0.00006)
				
			if count > 7:
				data[idx] |= 1<<cnt
			if cnt == 7:
				cnt = 0
				idx += 1
			else:
				cnt += 1
#		print data
		if data[0]+data[1] == 0xFF and data[2]+data[3] == 0xFF:  #check
			return data[2]
		else:
			print("repeat")
			return "repeat"

			
print('IRremote Test Start ...')										#Start the program
Ab.stop()																#Stop the robot
camera = picamera.PiCamera()

try:
	while True:															#Infinite loop
		key = getkey()
		if(key != None):
			n = 0				 
			if key == 0x18:												#When 2 key pressed		
				Ab.forward()											#Robot moves forward
				print("forward")
			if key == 0x08:												#When 4 key pressed
				Ab.left()												#Robot moves to the left
				print("left")
			if key == 0x1c:												#When 5 key pressed
				Ab.stop()												#Robot stops
				print("stop")
			if key == 0x5a:												#When 6 key pressed
				Ab.right()												#Robot moves to the right
				print("right")
			if key == 0x52:												#When 8 key pressed
				Ab.backward()											#Robot moves backward		
				print("backward")
			if key == 0x15:												#When + key pressed
				if(PWM + 10 < 101):										
					PWM = PWM + 10										#Increase the speed of the robot
					Ab.setPWMA(PWM)
					Ab.setPWMB(PWM)
					print(PWM)											#Display its current speed
			if key == 0x07: 											#When - key pressed
				if(PWM - 10 > -1):
					PWM = PWM - 10										#Decrease the speed of the robot
					Ab.setPWMA(PWM)
					Ab.setPWMB(PWM)
					print(PWM)											#Display its current speed
			if key == 0x09: 											#When EQ key pressed
				print("Camera Preview ON")			
				camera.start_preview()									#Starting the camera preview
				time.sleep(2)
				if key == 0x16:											#If 0 key pressed
					while key == 0x16:					
						print("Taking a picture ...")
						camera.capture('obstacle.jpg')					#Take a picture
						img= cv2.imread('obstacle.jpg')					#Define the image as a variable
						img2bw = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)	#Convert the original picture into a B&W picture
						retval, threshold = cv2.threshold(img2bw,10,255,cv2.THRESH_BINARY)		#Define the B&W threshold
						cv2.imshow('Original',img)						#Display original picture
						cv2.imshow('Black & White',img2bw)				#Display B&W picture
						time.sleep(2)									#Every 2 seconds					
					camera.stop_preview()								#Continue taking pictures while other keys aren't pressed
		else:
			n += 1
			if n > 20000:
				n = 0
				Ab.stop()													
except KeyboardInterrupt:
	GPIO.cleanup();

