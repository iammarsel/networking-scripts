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

print("IP-Mac-Host Information for Switches with Int Status!\n")

ios_l2 = {
	'device_type': 'cisco_ios',
	'username':'wilcom',
	'ip': '',
	'password': '0p3nsky+',
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
	# for i in range(1,255):
	#	print("Pinging 10.52.6."+str(i)+" from "+ip)
	#	pings6 = ssh.send_command("ping 10.52.6."+str(i)+" re 1 ti 1")
	#	print("Pinging 10.52.7."+str(i)+" from "+ip)
	#	pings7 = ssh.send_command("ping 10.52.7."+str(i)+" re 1 ti 1")
	#	print("Pinging 10.52.10."+str(i)+" from "+ip)
	#	pings10 = ssh.send_command("ping 10.52.10."+str(i)+" re 1 ti 1")
	#	print("Pinging 10.52.20."+str(i)+" from "+ip)
	#	ping20 = ssh.send_command("ping 10.52.20."+str(i)+" re 1 ti 1")
	#	print("Pinging 10.52.30."+str(i)+" from "+ip)
	#	pings30 = ssh.send_command("ping 10.52.30."+str(i)+" re 1 ti 1")
	#	print("Pinging 10.52.100."+str(i)+" from "+ip)
	#	pings100 = ssh.send_command("ping 10.52.100."+str(i)+" re 1 ti 1")
	get_arp = ssh.send_command("show arp")
	get_arp = get_arp.splitlines()
	# split arp to get ips and mac addresses
	for i in range(1,len(get_arp)):
		# get mac addresses 
		get_arp[i] = get_arp[i].split()
		if (get_arp[i][-1] != 'Vlan5') and (get_arp[i][-1] != 'ARPA'):
			ips.append(get_arp[i][1])
			macs.append(get_arp[i][3])

	temp = 0
	domain = ssh.send_command("show ip domain")
	domain = domain.split('.')
	show_int = ssh.send_command("show int status")
	show_int = show_int.splitlines()
	for i in range(1,len(show_int)):
		s1.write(5+i,5,show_int[i],boldi)
	for i in range(0, len(macs)):
		show_mac = ssh.send_command("show mac add | i " + macs[i])
		show_mac = show_mac.split()
		for s in range(0,len(show_mac)):
			show_mac[s].strip();

		if (len(show_mac)>2):
			match_ports.append(show_mac[3])
		else:
			match_ports.append('none')
					
	for i in range(0,len(macs)):
		s1.write(6+i,0,ips[i],boldsm)
		s1.write(6+i,1,macs[i],boldsm)
		s1.write(6+i,2,match_ports[i],boldsm)
d1 = today_date.strftime("%m%d%y")
wb.save('excels/'+str(domain[0])+d1+'.xls')
print("Gathering Info Completed.")
print("Spreadsheet file is saved as " + str(domain[0])+d1+'.xls in the excels folder.')
