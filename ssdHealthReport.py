#!/usr/bin/env python3

import sys, os, time, str

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
if (userResp == 'n' or userResp == 'no')
    sys.exit()