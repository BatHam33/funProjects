#!/usr/bin/env python3
#This scripted will use a a basic smtp mail server from google. It requires allowing less secure access. 
#For security, create a new email account to handle the sending of emails

import sys, os, time, smtplib, ssl, subprocess
#This import will be a file with username/password variables stored
import emailCred

if not os.geteuid() == 0:
    sys.exit("\nOnly root can run this script\n")
print("\nEnter drive location (ex: sdb): ")
driveLoc = input()
subprocess.call(['sudo', 'smartctl', '-t', 'short', '-i', '/dev/'+driveLoc], stdout=open(os.devnull, "w"), stderr=subprocess.STDOUT)
print("\nRunning scan. Wait 3 minutes")
time.sleep(150)
#print("\nTest Complete! Results Below:\n\n")
#subprocess.call(['sudo', 'smartctl', '-a', '/dev/'+driveLoc], stdout=open(os.devnull, "w"), stderr=subprocess.STDOUT)
print("Wear leveling listed below\n")
os.system("sudo smartctl -a /dev/"+driveLoc+" | grep \"Wear_Leveling_Count\"")
print("\nDo you want to view more detailed results (y or n)?\n")
userResp = input()
userResp = userResp.strip()
scanReportForm = ''
if (userResp == 'y' or userResp == 'yes'):
    scanReport = subprocess.Popen(['sudo', 'smartctl', '-a', '/dev/'+driveLoc], stdout=subprocess.PIPE)
    scanReportForm = scanReport.stdout.read().decode()
    print(scanReportForm)
print("Do you want results emailed to you (y or n)?")
userResp = input()
userResp = userResp.strip()
if (userResp == 'n' or userResp == 'no'):
    sys.exit()

smtp_server = "smtp.gmail.com"
port = 587  # For starttls
sender_email = emailCred.email
password = emailCred.password
context = ssl.create_default_context()
receiver_email = "your@gmail.com"
message = """\
Subject: SSD Health report

"""
#Logic to send message
try:
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message+scanReportForm)
except Exception as e:
    # Print any error messages to stdout
    print(e)
finally:
    server.quit() 