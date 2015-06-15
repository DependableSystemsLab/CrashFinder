#! /usr/bin/python

import os
import subprocess

################################################################################################

noOfCores = 100 # no of processes per processes
bmName = "name" # benchmark name
indexList = []

################################################################################################

def chunks(l, n):
	if n < 1:
        	n = 1
	return [l[i:i + n] for i in range(0, len(l), n)]

################################################################################################

os.system("rm -rf driver_index_*")
os.system("rm -rf " + bmName + "_*")

# read index
with open("multSmartFiList.txt", "r") as f:
        for line in f:
		#line = line.replace("\n", "")
		#fiIndex = line.split()[0].replace("'" ,"")
		#fiCycle = line.split()[1].replace("'", "")
                indexList.append(line)

# split into n index file
coreIndexList = chunks(indexList, noOfCores)
coreNo = 0
for currentList in coreIndexList:
	# for each process/core, prepare the input index list first.
	f = open("driver_index_" + `coreNo`,'a')
	for line in currentList:
		#fiBit = bitDic[index]
		#f.write(`index`.replace("'", "") + " " + `fiBit`.replace("'", "") + '\n') # python will convert \n to os.linesep
		f.write(line)
	f.close()
	
	# launch driver for each core
	p = subprocess.Popen(["python", "core_driver.py", `coreNo`, bmName])

	print "Launched core " + `coreNo` + " with " + `len(currentList)` + " index"
	coreNo += 1
