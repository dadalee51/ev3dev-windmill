#!/usr/bin/env python3
import ev3dev.ev3 as ev3

recBtn = ev3.TouchSensor()
ev3.Sound.speak('Windmill version 1.0 by Tigo Robotics')
m = ev3.LargeMotor('outD')
ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.YELLOW)
ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.ORANGE)
#mode loop
#while True:
	#print("Motor is at:" + repr( m.position))

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
while True:
	#main loop, color detects, stop and start different threads.
	#we only recognize red 5, blue 2, yellow 4, green 3
	thisColor = testColor.color
	if (thisColor in [5,2,4,3]) and (lastColor != thisColor):
		#print((thisColor in [5,2,4,3]))
		#a change in mode is initiated
		ev3.Sound.speak('Tigo see ' + colorToString(thisColor)).wait()
		lastColor = thisColor


