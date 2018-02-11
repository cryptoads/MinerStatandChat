import pyping
import requests
import json
import re
import config
import telebot
import threading
#import RPi.GPIO as GPIO
from time import sleep
from colorama import Fore, Back, Style
from colorama import init
init()
#pull in telegram token
token = config.token
print token
#initiate telebot
bot = telebot.TeleBot(token)
#owner check function (currently unused)
def is_owner(message):
    if message.from_user.id == config.my_id:
        return True
    else:
        bot.reply_to(message, "You aint the guy")	
        
#when bot start up, send owner a dank message
bot.send_message(config.my_id, "Suhhhhh Dude.");

def minerrestart(pin):
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(config.pins[pin], GPIO.OUT, initial=GPIO.LOW)
 # Turn relay ON
	GPIO.output(config.pins[pin], GPIO.HIGH)
	# Sleep for 5 seconds
	sleep(5) 
	# Turn relay OFF
	GPIO.output(config.pins[pin], GPIO.LOW) 
	# Sleep for 5 seconds
	sleep(5)
	GPIO.output(config.pins[pin], GPIO.HIGH)
	# Sleep for 5 seconds
	sleep(10) 
	# Turn relay OFF
	GPIO.output(config.pins[pin], GPIO.LOW) 
	# Sleep for 5 seconds
	sleep(3)
	GPIO.cleanup()
	bot.send_message(config.my_id, "Computer "+pin+ " is being restarted.");

#check ewbf miners and show their stats in console
def minercheckloop():
	while True:

		def ewbf_ping(ip, port):
			print (Fore.YELLOW + 'Pinging ') + (Fore.BLUE + ip)
		  	#ping ip
		  	r = pyping.ping(ip)
			#if pyping gives 0, success
			if r.ret_code == 0:
				try:
				

					print (Back.MAGENTA+(Fore.GREEN + ip)) + (Fore.GREEN + ' is up'),(Style.RESET_ALL)
					print (Fore.CYAN + 'The avg response time is ') + (Fore.GREEN + r.avg_rtt)

					r = requests.get('http://'+ip+port, timeout = 5)
					#save ewbf json data to list			
					dict = r.json()
					dict5 = dict['result']

					#go through the keys in the dict and print to console	
					for key in dict5:
						print (Fore.CYAN + key['name']), (Fore.RED + '|speed|'), (Fore.GREEN + str(key['speed_sps'])), (Fore.RED + '|temperature|'), (Fore.GREEN + str(key['temperature'])), (Fore.RED + '|gpu Power Usage|'), (Fore.GREEN + str(key['gpu_power_usage'])), (Style.RESET_ALL)
				except:
					print "connection failed"
					minerrestart(ip)
			else:
				print ip + ' is down'
				print 'restarting computer'
				minerrestart(ip)
		# go through claymore miners and show stats in console
		def clay_ping(ip, port):
			print (Fore.YELLOW + 'Pinging ') + (Fore.BLUE + ip)
		  	#ping ip
		  	r = pyping.ping(ip)
			#if pyping gives 0, success
			if r.ret_code == 0:
				try:
					print (Back.MAGENTA+(Fore.GREEN + ip)) + (Fore.GREEN + ' is up'),(Style.RESET_ALL)
					print (Fore.CYAN + 'The avg response time is ') + (Fore.GREEN + r.avg_rtt)
					r = requests.get('http://'+ip+port, timeout=5)
					t = re.search('\{[^\}]+\}', r.text)
					j = json.loads(t.group(0))
					dict = j['result']
					i=0
					print (Fore.RED + 'Avg Hashrate |'), (Fore.GREEN + str(float(j['result'][2].split(';')[0]) / 1000)), (Style.RESET_ALL)
					for n in j['result'][3].split(';'):
						print (Fore.RED +'Speed |'), (Fore.GREEN +str(float(j['result'][3].split(';')[i])/ 1000)),(Style.RESET_ALL)
						i=+ 1

					i=0
					k = 1
					while i <12:
						print (Fore.RED+'temperature |'), (Fore.GREEN + j['result'][6].split(';')[i]),(Fore.RED + '| Fan |'), (Fore.CYAN + j['result'][6].split(';')[k]),(Fore.CYAN + '%'),(Style.RESET_ALL)
						k+=1
						i+=2
				except:
					print 'connection failed'
					minerrestart(ip)
			else:
				print ip + ' is down'
				print 'restarting computer'
				minerrestart(ip)


		#call console function for ewbf miners
		for n in config.ewbf_rig:
			ewbf_ping(n, config.ewbf_rig[n])
		#call console function for clay miners
		for n in config.clay_rig:
			clay_ping(n, config.clay_rig[n])
		sleep(600)	
#start the minercheckloop thread
threading.Thread(target=minercheckloop).start()
#run the telegram responder thread using polling
@bot.message_handler(commands=['start','help'])
def start(message):
	resp = 'Type /stat to see miner stats'
	bot.reply_to(message, resp)

@bot.message_handler(commands=['stat'])
def stat(message):
  	for n in config.clay_rig:
  	#ping ip
	  	r = pyping.ping(n)
		#if pyping gives 0, success
		try:

			if r.ret_code == 0:
				r = requests.get('http://'+n+config.clay_rig[n], timeout = 5)
				#if the response code is good, send the update to telegram
				if r.status_code == requests.codes.ok:
					t = re.search('\{[^\}]+\}', r.text)
					j = json.loads(t.group(0))
					card_temp1=''
					card1 = 0 
					dict = j['result']
					i=0
					k = 1
					while i <12:
						card1 += 1
						card_temp1 += 'Card'+ str(card1)+ ' temp | '+ str(j['result'][6].split(';')[i]) + '| Fan |' + str(j['result'][6].split(';')[k]) + '%' + '\n'
						k+=1
						i+=2
					resp = ('580 Miner' + '\n'+ str(j['result'][7]) + '\n' + 'Hashrate '+ str((float(j['result'][2].split(';')[0]) / 1000))) + '\n' + card_temp1
				  	bot.reply_to(message, resp)
			  	else:
			  		bot.reply_to(message, "bad status code from server")
			  		minerrestart(n)
			else:
				resp = "cant ping "+str(n)
			  	bot.reply_to(message, resp)
			  	minerrestart(n)
		except:
			bot.reply_to(message, 'Computer is responding but I cant connect to webserver at ' + str(n))
			minerrestart(n)


	for n in config.ewbf_rig:
		r = pyping.ping(n)
		speed_avg = 0 
		card_temp = ''
		card = 0
		server = ''
		try:
		
			if r.ret_code == 0:
				r = requests.get('http://'+ n + config.ewbf_rig[n], timeout = 5)
				if r.status_code == requests.codes.ok:
					dict = r.json()
					dict5 = dict['result']
					server = dict['current_server']
					#go through the keys in the dict and print to console	
					for key in dict5:
						#resp = key['name']+ '|speed|' + str(key['speed_sps']) + '|temperature|' +str(key['temperature'])+ '|gpu Power Usage|'+ str(key['gpu_power_usage'])
						speed_avg += key['speed_sps']
						card += 1
						card_temp += 'Card' + str(card) + ' temp ' + str(key['temperature']) + '\n'
						resp = str(key['name']) + '\n' + 'Current Server ' + server + '\n'+ 'Hashrate ' + str(speed_avg) + '\n' + card_temp
			         
					bot.reply_to(message, resp)
				else:
					bot.reply_to(message, "bad status code from server")
					minerrestart(n)
			else:
				resp = 'cant ping '+str(n)
			  	bot.reply_to(message, resp)
			  	minerrestart(n)
		except:
			bot.reply_to(message, 'Computer is responding but I cant connect to webserver at ' + str(n))
			minerrestart(n)

bot.polling()
