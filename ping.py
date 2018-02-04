import pyping
import requests
import json
import re
import config
from colorama import Fore, Back, Style
from colorama import init
init()
		
def ewbf_ping(ip, port):
	print (Fore.YELLOW + 'Pinging ') + (Fore.BLUE + ip)
  	#ping ip
  	r = pyping.ping(ip)
	#if pyping gives 0, success
	if r.ret_code == 0:
		print (Back.MAGENTA+(Fore.GREEN + ip)) + (Fore.GREEN + ' is up'),(Style.RESET_ALL)
		print (Fore.CYAN + 'The avg response time is ') + (Fore.GREEN + r.avg_rtt)

		r = requests.get('http://'+ip+port)
		#save ewbf json data to list			
		dict = r.json()
		dict5 = dict['result']
		#go through the keys in the dict and print to console	
		for key in dict5:
			print (Fore.CYAN + key['name']), (Fore.RED + '|speed|'), (Fore.GREEN + str(key['speed_sps'])), (Fore.RED + '|temperature|'), (Fore.GREEN + str(key['temperature'])), (Fore.RED + '|gpu Power Usage|'), (Fore.GREEN + str(key['gpu_power_usage'])), (Style.RESET_ALL)
	else:
		print ip + ' is down'
		print 'restarting computer'

def clay_ping(ip, port):
	print (Fore.YELLOW + 'Pinging ') + (Fore.BLUE + ip)
  	#ping ip
  	r = pyping.ping(ip)
	#if pyping gives 0, success
	if r.ret_code == 0:
		print (Back.MAGENTA+(Fore.GREEN + ip)) + (Fore.GREEN + ' is up'),(Style.RESET_ALL)
		print (Fore.CYAN + 'The avg response time is ') + (Fore.GREEN + r.avg_rtt)
		r = requests.get('http://'+ip+port)
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
	else:
		print ip + ' is down'
		print 'restarting computer'



for n in config.ewbf_rig:
	ewbf_ping(n, config.ewbf_rig[n])

for n in config.clay_rig:
	clay_ping(n, config.clay_rig[n])

	

