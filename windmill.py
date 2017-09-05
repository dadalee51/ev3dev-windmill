#!/usr/bin/env python3
import ev3dev.ev3 as ev3
import time
import atexit
import math
from threading import Thread, Lock,Condition
motorCR = Condition() 
recBtn = ev3.TouchSensor()
ev3.Sound.speak('WindMill')
mD = ev3.LargeMotor('outD')
mA = ev3.LargeMotor('outA')
ts1 = ev3.TouchSensor('in1')
ts2 = ev3.TouchSensor('in4')

ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.ORANGE)
#mode loop
#while True:
	#print("Motor is at:" + repr( mD.position))

#color to string method
colorCode = {
		0:"No color", 
		1:"Black", 
		2:"Blue", 
		3:"Green",
		4:"Yellow",
		5:"Red",
		6:"White",
		7:"Brown"}
def colorToString(c):
	return colorCode.get(c)
	
#implement a colour sensor loop switching modes to start and stop different threads
testColor = ev3.ColorSensor()
#print(testColor.color)
lastColor = testColor.color

#mimic game, get the position from outA and output to outD
mimic = True
def mimicGame():
	print("mimic starting:" + repr(mimic))
	mA.reset()
	mD.reset()
	mA.run_to_abs_pos(position_sp = 0 , speed_sp=500, stop_action ="coast")
	mD.run_to_abs_pos(position_sp = 0 , speed_sp=500, stop_action ="coast")
	#mini p controller
	pActor = 1
	kP = 0.7
	while mimic: 
		try:
			motorCR.acquire()
			followerPos = mD.position
			actorPos = mA.position
		finally:
			motorCR.release()
			e = followerPos - actorPos
			pActor = kP * e
		try:
			motorCR.acquire()
			mA.run_to_abs_pos(position_sp = followerPos - pActor , speed_sp=500, stop_action ="brake")
		finally:
			motorCR.release()
		time.sleep(0.01)
#music wheel game

musicalNotes = [130,147,165,174,196,220,247,261,293,329,349,392,440,493,523,587,659,698,784,880,987,1046]
#quantize to each music note frequency. 
def round_up(x):
	print(repr(int(x % 720 % 21)))
	return musicalNotes[int(x % 720 % 21)]
	
	
#this game runs when the mimic game is running. 
music = True
def musicGame():
	print("music starting")
	while music:
		try: 
			motorCR.acquire()		
			mapos = mD.position
		finally:
			motorCR.release()
		if ts1.value() : 	
			mapos = abs(mapos)
			musicPosition = round_up(mapos)
			ev3.Sound.tone([(musicPosition, 100, 0)])
			#print("mA.pos = " + repr(mapos) + " musicPosition: " + repr(musicPosition))		
		time.sleep(0.01)
		
		
#main loop		
while True:
	#main loop, color detects, stop and start different threads.
	#we only recognize red 5, blue 2, yellow 4, green 3 - note on a white surface blue is usually picked up.
	thisColor = testColor.color

	if (thisColor in [5,2,4,3]) and (lastColor != thisColor):
		#print((thisColor in [5,2,4,3]))
		#a change in mode is initiated
		if thisColor==4: #yellow - mimic
		#if True:
			ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.YELLOW)
			ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.YELLOW)
			#stop all other game and start mimic game
			music = False
			time.sleep(0.01)
			mimic = True
			music = True
			t1 = Thread(target=mimicGame)
			t1.start()
			t2 = Thread(target=musicGame)
			t2.start()
		elif thisColor ==2: # blue - music
			ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.GREEN)
			ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.YELLOW)
			music = False
			mimic = False
			time.sleep(0.01)
			music = True
			t2 = Thread(target=musicGame)
			t2.start()
		elif thisColor ==5:
			ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.RED)
			ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.RED)
			mimic = False
		elif thisColor ==3:
			ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.GREEN)
			ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.GREEN)
			mimic = False
		
		ev3.Sound.speak(' ' + colorToString(thisColor) + " challenge ")
		lastColor = thisColor
		
		time.sleep(0.01)

		
		
def exit_handler():
	try:
		print ('My application is ending!')
	except KeyboardInterrupt:
		raise
	
atexit.register(exit_handler)
	