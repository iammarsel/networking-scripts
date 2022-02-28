# Automated backup script for Cisco devices using weekly scheduler and TFTP server
from netmiko import ConnectHandler
from datetime import date
import schedule
import time

sw = open('hosts')
filelines = sw.readlines()
counties = ["county1","county2","etc"]
ios_l2 = {
  'device_type': 'cisco_ios',
  'username':'',
  'ip': '',
  'password': '',
  'conn_timeout': 3
  }
def run_backup():
  print("Weekly Automated Backup Pull Now...")
  i=0
  for ip in filelines:
    i+=1
    ip = ip.strip()
    ios_l2['ip'] = ip
    ipcheck = ip.split(".")
    folder = ""
    # checking for octect values to separate counties and credentials
    if ipcheck[1] == "16":
      folder = counties[0]
      ios_l2['username'] = 'username1'
      ios_l2['password'] = 'password1'
    elif ipcheck[1] == "6":
      folder = counties[1]
      ios_l2['username'] = 'username2'
      ios_l2['password'] = 'password2'
    elif ipcheck[1] == "7":
      folder = counties[2]
      ios_l2['username'] = 'password3'
      ios_l2['password'] = 'password3'
    else:
      folder = "random"
      print("ip not matching known folders")
    print("Current county is "+folder)
    if folder != "random":
      try:
        ssh = ConnectHandler(**ios_l2)
        hostname = ssh.send_command("show run | s hostname")
        hostname = hostname.split()
        date1 = date.today()
        df = date1.strftime("%m%d%y")
        print("Backup for Device " + ip)
        cp1 = "copy running-config tftp"
        serv = "##.##.##.##"
        output = ssh.send_command_timing(cp1)
        output += ssh.send_command_timing(serv)
        output += ssh.send_command_timing(folder+"/"+folder+"_"+hostname[1]+"_"+df+"\n")
        print(output)
        print("Backup file saved for "+ hostname[1]+" to "+serv+" at /tftp/"+folder)
      # if ssh connection failed print out the error
      except Exception as e:
        print(e)
# automate backup with schedule module using the following format: (uncomment one of the following lines and edit)
# schedule.every(10).seconds.do(run_backup)
# schedule.every().saturday.at("14:00").do(run_backup)
while True:
  schedule.run_pending()
  time.sleep(1)
