from netmiko import ConnectHandler
import time
from datetime import date
from datetime import datetime
import xlwt as xw

sw = open('hosts')
wb = xw.Workbook()
boldb = xw.easyxf('font: bold 1,color blue,height 400;')
boldr = xw.easyxf('font: bold 1, height 220,color red;')
boldsm = xw.easyxf('font: bold 1, height 200;')
today_date = date.today()
now = datetime.now()
current_time = now.strftime("%H:%M:%S")
d1 = today_date.strftime("%m%d%y")
d2 = today_date.strftime("%m/%d/%y")
ios_l2 = {
	'device_type': 'cisco_ios',
	'username':'',
	'ip': '',
	'password': '',
	'conn_timeout': 9999999
}
gap = 1
trunks = list()
runtime = int(input("How many minutes would you like to run Trunk Speed Monitoring for? "))
for ip in sw.readlines():
	ios_l2['ip'] = ip
	ssh = ConnectHandler(**ios_l2)
	hostname = ssh.send_command("show run | s hostname")
	hostname = hostname.split()
	s1 = wb.add_sheet(hostname[1].upper())
	first_col = s1.col(0)
	first_col.width = 5120
	sec_col = s1.col(1)
	sec_col.width = 5120
	s1.write(0,0,'Site: ' + str(hostname[1]).upper(),boldb)
	s1.write(1,0,'Date: '+d2,boldr)
	s1.write(2,0,'Time Started: '+current_time,boldr)
	trunks = []
	print("Monitoring "+ip+"...")
	
	get_trunk = ssh.send_command("sh int status | i trunk")
	get_trunk = get_trunk.splitlines()
	for i in get_trunk:
		i = i.split()
		if len(i)>0:
			trunks.append(i[0])
	for t in trunks:
		s1.write(5,0+gap,t,boldr)
		s1.write(6,-1+gap,"Time",boldsm)
		s1.write(6,0+gap,"Input(bits/sec)",boldsm)
		s1.write(6,1+gap,"Output(bits/sec)",boldsm)
		gap += 4
		config_commands = ["int "+t,"load-interval 30","end"]
		measures = ssh.send_config_set(config_commands)
	save = ssh.send_command("wr mem")
	z = 0
	while runtime > 0:
		gap = 1
		z += 1
		for t in trunks:
			print("\nCurrent Interface speed of "+t+"... \n")
			speeds = ssh.send_command("sh int "+t+" | i input rate | output rate")
			speeds = speeds.strip()
			speeds = speeds.splitlines()
			speeds[0] = speeds[0].split()
			speeds[1] = speeds[1].split()
			print("Input: "+ speeds[0][4]+" bits/sec")
			print("Output: " + speeds[1][4]+" bits/sec")
			now = datetime.now()
			current_time = now.strftime("%H:%M:%S")
			s1.write(6+z,-1+gap,current_time,boldsm)
			s1.write(6+z,0+gap,int(speeds[0][4]),boldsm)
			s1.write(6+z,1+gap,int(speeds[1][4]),boldsm)
			gap+=4
			
		i = 30
		print("\n")
		while i > 0:
			print("Next update in "+str(i)+" seconds...")
			time.sleep(0.9)
			i -= 1
		runtime -= 0.5
now = datetime.now()
current_time = now.strftime("%H:%M:%S")
s1.write(3,0,'Time Finished: '+ current_time,boldr)
wb.save("excels/TrunkSpeed"+d1+".xls")
print("Spreadsheet file is saved as TrunkSpeed"+d1+'.xls in the excels folder.')
