#!/usr/bin/env python3
import ev3dev.ev3 as ev3

ts = ev3.TouchSensor()
ev3.Sound.speak('hi, welcome to the E V 3 demo program, I, will drive the motor in port D for 3 seconds, then, you, can press the touch sensor to turn my L E D to red.').wait()

m = ev3.LargeMotor('outD')
m.run_timed(time_sp=3000, speed_sp=500)
while True:
	ev3.Leds.set_color(ev3.Leds.LEFT, (ev3.Leds.GREEN, ev3.Leds.RED)[ts.value()])
	

