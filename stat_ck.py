from gpiozero import PWMLED
import time
import psutil as ps
import datetime as dt
import os

# CONFIG
# Problems to what light is shown
CS_RED = 4
CS_ORG = 1
CS_GRN = 0

# Process list and disc list
PROC_LIST = ['syncthing', 'smbd']
DISC_LIST = ['/media/jack/netdisk1','/media/jack/netdisk2','/media/jack/netdisk3']

# Check every
CHECK_MINS = 5

# FUNCTIONS
def add_to_log(strin):
    log_file = open('log.txt','a')
    log_file.writelines(f"{str(dt.datetime.now())[0:16]}: {strin}\n")
    log_file.close()

# Push button for reset?
    # By pass sleep?
#Import Colours
red_led = PWMLED(14)
org_led = PWMLED(15)
grn_led = PWMLED(18)

red_led.off()
org_led.off()
grn_led.off()

# List of processes we need running
# Syncthing has rest API calls you can use if you need more in depth checking, make that a different module though

# start loop
while True:
    red_led.off()
    org_led.off()
    grn_led.off()
    
    probs = 0

    # Process check
    # Checks for all processes running PROC_List, appends to new list
    # Compares what is running to what is in PROC_LIST
    list_procs_running = []
    for proc in ps.process_iter():
        if proc.name() in PROC_LIST:
            list_procs_running.append(proc.name())
    print(list_procs_running)
    for proc in PROC_LIST:
        if proc not in list_procs_running:
            add_to_log(proc + " is not running")
            probs += 1

    #Disk Check
    for dir in DISC_LIST:
        if not os.path.isdir(dir):
            add_to_log(dir + " is not connected")
            probs += 1

    if probs == CS_GRN:
        grn_led.on()
    elif probs == CS_ORG:
        org_led.blink(0.5,0.5,0.5,0.5)
    else:
        red_led.blink(0.25,0.25,0.25,0.25)
    time.sleep(CHECK_MINS * 60)
    print(probs, " Problems")
# for each **in** the list of processes, look for ones that match
    # add one to the tally for each one NOT running
    # if one is missing add to log file
        #need time and date of when this happened
    # Maybe add functionality 
# sleep for 5 minutes