#!/usr/bin/env python3
#This scripted will use a a basic smtp mail server from google. It requires allowing less secure access. 
#For security, create a new email account to handle the sending of emails
#This version of the program can be used with Cron in order to run weakly checks. 

import sys, os, time, smtplib, ssl, subprocess
#This import will be a file with username/password variables stored
import emailCred

scanLength = 'long' #change scan length here to 'short' if desired
if not os.geteuid() == 0:
    sys.exit("\nOnly root can run this script\n")
driveLoc = 'sdb' #change drive location here
subprocess.call(['sudo', 'smartctl', '-t', scanLength, '-i', '/dev/'+driveLoc], stdout=open(os.devnull, "w"), stderr=subprocess.STDOUT)
if scanLength == 'long':
    time.sleep(9000)
else:
    time.sleep(150)
#save results
scanReport = subprocess.Popen(['sudo', 'smartctl', '-a', '/dev/'+driveLoc], stdout=subprocess.PIPE)
scanReportForm = scanReport.stdout.read().decode()
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