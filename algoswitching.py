#!/usr/bin/python
import urllib.request
import csv
import sys, getopt
import os, signal, subprocess
from time import time

goodAlgoTime = 10
useGPU = True
csvAlgo = "algo.csv"
address = "1Cc2KYv5fUiZdpjPrKU87jMBD5UD3Ypss7"
currency = "BTC"
launchMinerCommand = "ccminer"
launchOptions = "--max-temp=70" 
API = "http://www.zpool.ca/api/status"
user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
headers = {'User-Agent':user_agent,}

with open(csvAlgo, 'r') as f:
    reader = csv.reader(f)
    hash_rates = list(reader)



#start generating profitability factor string from csv
first = True
option_string = "-p "
for item in hash_rates[1:]:
    if not first:
        option_string += ","
    else:
        first = False
    option_string += item[0] + "=" + item[1]
#end generation
#setting right wallet currency
option_string += ",c=" + currency

#get algos and ports
try:
    request = urllib.request.Request(API, None, headers)
    status = urllib.request.urlopen(request).read()
    pool = eval(status);
except :
    print("Error connecting to " + API)
    print("Is it online?")
    sys.exit(1)

#Start mining
exit = False
lastMined = ""
while not exit:
    for algo in [item[0] for item in hash_rates]:
        if algo not in pool.keys(): #is the algo available in mining pool?
            continue             #if not -> next algo
        #Since lastMined isn't the best algo we can jump it
        if algo == lastMined:
            continue
        port = pool[algo]['port']
        command = launchMinerCommand + " " + launchOptions + " -r 0 -a " + algo + " -o stratum+tcp://" + algo + ".mine.zpool.ca:" + str(port) + " -u " + address + " " + option_string
        print("\nLaunching: " + command + "\n")

        initialTime = time()
        retvalue = os.system(command)
        timeElapsed = time() - initialTime

        #1792: strange retvalue when there is a SIGINT
        if retvalue == 1792:
            print("Mining terminated")
            exit = True

        #Not in best algo anymore, restart loop from the best algo
        if timeElapsed > goodAlgoTime :
            lastMined = algo
            for item in hash_rates:
                if item[0] == algo :
                    #Add elapsed time to the algo csv
                    item[2] = str(float(item[2]) + timeElapsed)
            break
        elif retvalue == 1792:
            break

    header = hash_rates.pop(0) #remove csv header
    hash_rates.sort(key=lambda x: float(x[2]), reverse=True) #sort by time (most used algo first)
    hash_rates.insert(0, header) #reinsert header

#Before exiting save time on algos file
with open(csvAlgo, "w") as f:
        writer = csv.writer(f)
        writer.writerows(hash_rates)
