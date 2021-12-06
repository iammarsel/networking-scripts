# Getting the current configuration of a device using show run and outputting to a text file. 
# enter username and password lines 11 and 13
# edit the hosts file for ips that need pinging
# should save a txt file in the output folder

from netmiko import ConnectHandler
from datetime import date

ios_l2 = {
	'device_type': 'cisco_ios',
	'username':'',
	'ip': '',
	'password': '',
	'conn_timeout': 9999999
}
sw = open('hosts')
today_date = date.today()
d1 = today_date.strftime("%m%d%y")
for ip in sw.readlines():
	ios_l2['ip'] = ip
	ssh = ConnectHandler(**ios_l2)
	hostname = ssh.send_command("show run | s hostname")
	print("Saving show run of "+ip)
	hostname = hostname.split()
	shrun = ssh.send_command("show run")
	shrun = shrun.splitlines()
	with open("output/"+hostname[1]+"_"+d1+".txt","w") as f:
		f.write('\n'.join(shrun))
	print("File saved as "+hostname[1]+"_"+d1+".txt"+" in the proper folder!")
