from netmiko import ConnectHandler
from datetime import date


ios_l2 = {
	'device_type': 'cisco_ios',
	'username':'wilcom',
	'ip': '',
	'password': '0p3nsky+',
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
	with open("camden/"+hostname[1]+"_"+d1+".txt","w") as f:
		f.write('\n'.join(shrun))
	print("File saved as "+hostname[1]+"_"+d1+".txt"+" in the proper folder!")
