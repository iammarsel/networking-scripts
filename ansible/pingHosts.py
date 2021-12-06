# Pinging through all ip ranges for hosts. 
# enter username and password lines 24 and 26
# edit the hosts folder for ips that need pinging
# for loop going through full range of ips starting on line 57

from netmiko import ConnectHandler
import xlwt as xw
from datetime import date

wb = xw.Workbook()
boldr = xw.easyxf('font: bold 1, height 300,color red;')
boldb = xw.easyxf('font: bold 1,color blue,height 500;')
bold = xw.easyxf('font: bold 1, height 300;')
boldsm = xw.easyxf('font: bold 1, height 200;')
bckg = xw.easyxf('pattern: pattern solid, fore_colour green')
boldi = xw.easyxf('font: bold 1, height 200;' "borders: top medium, bottom medium, right medium, left medium;")
today_date = date.today()
sw = open('hosts')

print("Pinging through all ip ranges for hosts.\n")

ios_l2 = {
	'device_type': 'cisco_ios',
	'username':'',
	'ip': '',
	'password': '',
	'conn_timeout': 9999999
}

for ip in sw.readlines():
	macs = list()
	ports = list()
	ips = list()
	match_ports = list()
	ip = ip.strip()
	print('Gathering info for Switch ' + ip)
	print('...')
	ios_l2['ip'] = ip
	ssh = ConnectHandler(**ios_l2)

	hostname = ssh.send_command("show run | s hostname")
	hostname = hostname.split()
	s1 = wb.add_sheet(hostname[1].upper())
	first_col = s1.col(0)
	first_col.width = 5120
	sec_col = s1.col(1)
	sec_col.width = 5120
	fifth_col = s1.col(5)
	fifth_col.width = 20000
	s1.write(0,0,'Site: ' + str(hostname[1]).upper(),boldb)
	s1.write(2,0,'Date: ' + str(today_date),bold)
	s1.write(1,0,'IP: ' + ip,bold)
	s1.write(5,0,'IP',boldr)
	s1.write(5,1,'MAC',boldr)
	s1.write(5,2,'PORT',boldr)
	s1.write(5,5,'INT STATUS', boldr)
	for i in range(1,255): # Edit the ip range needed for pinging
		print("Pinging 10.##.#."+str(i)+" from "+ip)
		pings6 = ssh.send_command("ping 10.##.#."+str(i))
		print("Pinging 10.##.#."+str(i)+" from "+ip)
		pings7 = ssh.send_command("ping 10.##.#."+str(i))
		print("Pinging 10.##.##."+str(i)+" from "+ip)
		pings10 = ssh.send_command("ping 10.##.##."+str(i))
		print("Pinging 10.##.##."+str(i)+" from "+ip)
		ping20 = ssh.send_command("ping 10.##.##."+str(i))
		print("Pinging 10.##.##."+str(i)+" from "+ip)
		pings30 = ssh.send_command("ping 10.##.##."+str(i))
		print("Pinging 10.##.###."+str(i)+" from "+ip)
		pings30 = ssh.send_command("ping 10.##.###."+str(i)
