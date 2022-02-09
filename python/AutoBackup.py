from netmiko import ConnectHander
from datetime import time

sw = open('hosts')

print("Automated Backup System!")

ios_l2 = {
	'device_type': 'cisco_ios',
	'username':'',
	'ip': '',
	'password': '',
	'conn_timeout': 9999999
}

for ip in sw.readlines():
  ip = ip.strip()
  print("Backup for Device " + ip)
  ios_l2['ip'] = ip
  ssh = ConnectHandler(**ios_l2)
  config_commands = ["copy running-config tftp","172.16.18.238","Backup for "+ip]
	get_backup = ssh.send_config_set(config_commands)

