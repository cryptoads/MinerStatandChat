import pyping
import requests
import json
import re
from colorama import Fore, Back, Style
from colorama import init
init()
#set up range for mining pc's, going to eventually set this up with config
range = [3, 7, 5]#for lop that goes through the ip address range and then using pyping to check if a computer is alive on a network.  If it finds the computer, use request to pull the json 
#from the mining web server and prints it to console


for n in range:
	ip = '10.0.0.' + str(n)
   	print (Fore.YELLOW + 'Pinging ') + (Fore.BLUE + ip)
  	#ping ip
   	r = pyping.ping(ip)
	#if pyping gives 0, success
	if r.ret_code == 0:
		print (Back.MAGENTA+(Fore.GREEN + ip)) + (Fore.GREEN + ' is up'),(Style.RESET_ALL)
		print (Fore.CYAN + 'The avg response time is ') + (Fore.GREEN + r.avg_rtt)
		#still need to set up a config and get the claymour json data working.
		if ip=='10.0.0.3':
			#use request to read json data from address
			r = requests.get('http://10.0.0.'+str(n)+':42000/getstat')
			#save ewbf json data to list			
			dict = r.json()
			dict5 = dict['result']
			#go through the keys in the dict and print to console	
			for key in dict5:
				print (Fore.CYAN + key['name']), (Fore.RED + '|speed|'), (Fore.GREEN + str(key['speed_sps'])), (Fore.RED + '|temperature|'), (Fore.GREEN + str(key['temperature'])), (Fore.RED + '|gpu Power Usage|'), (Fore.GREEN + str(key['gpu_power_usage'])), (Style.RESET_ALL)
		#will remove once i set up ewbf miner config
		elif ip =='10.0.0.7':
			r = requests.get('http://10.0.0.'+str(n)+':42001/getstat')
			dict = r.json()
			dict5 = dict['result']
			for key in dict5:
				print (Fore.CYAN + key['name']), (Fore.RED + '|speed|'), (Fore.GREEN + str(key['speed_sps'])), (Fore.RED + '|temperature|'), (Fore.GREEN + str(key['temperature'])), (Fore.RED + '|gpu Power Usage|'), (Fore.GREEN + str(key['gpu_power_usage'])), (Style.RESET_ALL)
		#will remove once all json data is being read
		elif ip == '10.0.0.5':
			url = 'http://10.0.0.'+str(n)+':3333/'
			r = requests.get(url)
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
			




