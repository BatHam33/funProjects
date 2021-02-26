#!/usr/bin/env python3
#This scripted will use a a basic smtp mail server from google. It requires allowing less secure access. 
#For security, create a new email account to handle the sending of emails

import sys, os, time, str, smtplib, ssl
#This import will be a file with username/password variables stored
import emailCred

if not os.geteuid() == 0:
    sys.exit("\nOnly root can run this script\n")
print("\nEnter drive location (ex: sdb): ")
driveLoc = input()
os.system("sudo smartctl -t short -i /dev/"+driveLoc)
print("\nRunning scan. Wait 3 minutes")
time.sleep(150)
print("\nTest Complete! Results Below:\n\n")
os.system("sudo smartctl -a /dev/"+driveLoc)
print("Wear leveling listed below\n")
os.system("sudo smartctl -a /dev/"+driveLoc+" | grep \"Wear_Leveling_Count\"")
print("\nDo you want to view more detailed results (y or n)?\n")
userResp = input()
userResp = userResp.strip()
if (userResp == 'y' or userResp == 'yes') 
    scanReport = os.system("sudo smartctl -a /dev/"+driveLoc)
    print(scanReport)
print("Do you want results emailed to you (y or n)?")
userResp = input()
userResp = userResp.strip()
if (userResp == 'n' or userResp == 'no')
    sys.exit()

smtp_server = "smtp.gmail.com"
port = 587  # For starttls
sender_email = emailCred.email
password = emailCred.password
context = ssl.create_default_context()
sender_email = emailCred.email
receiver_email = "your@gmail.com"
message = """\
Subject: SSD Health report

"""+scanReport
#Logic to send message
try:
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
except Exception as e:
    # Print any error messages to stdout
    print(e)
finally:
    server.quit() 