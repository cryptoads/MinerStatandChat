## Synopsis

This is a python script that uses the GPIO pins in a Raspberry Pi and a relay board to reset a mining rig that is using claymore and or EWBF when the generated webserver from the miner is not detected.  Telegram bot integration has been added to allow the user to check the status of the miner from any location, as well as to alert the user when a miner is being restarted.  

## Code Example

To check that the miner is active we use the pyping library to detect if the miner is online, and then the request library to pull the json data. I do some formatting of the json that we recieve and print messages to the console and to telegram, but this is the basis of the logic. <br>
<br>
	r = pyping.ping(ip)<br>
			if r.ret_code == 0:<br>
				try:<br>
					r = requests.get('http://'+ip+port, timeout=5)<br>
				except:<br>
					minerrestart(ip)<br>
			else:<br>
				minerrestart(ip)<br>
This is how I use GPIO pins to restart the machine<br>
def minerrestart(pin):<br>
	GPIO.setmode(GPIO.BCM)<br>
	GPIO.setup(config.pins[pin], GPIO.OUT, initial=GPIO.LOW)<br>
	GPIO.output(config.pins[pin], GPIO.HIGH)<br>
	sleep(5) <br>
	GPIO.output(config.pins[pin], GPIO.LOW) <br>
	sleep(5)<br>
	GPIO.output(config.pins[pin], GPIO.HIGH)<br>
	sleep(10) <br>
	GPIO.output(config.pins[pin], GPIO.LOW) <br>
	sleep(3)<br>
	GPIO.cleanup()<br>

## Motivation

This project was built as a way for me to take more of a hands off approach to ensuring that my mining rigs were always mining. 

## Installation

You will need to run jumper cables from the relay board to the power switch pins on your computer. 


