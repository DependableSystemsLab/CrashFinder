#! /usr/bin/python

import os
import subprocess

################################################################################################

noOfCores = 200 # no of processes
bmName = "cvm_scancvm"
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
with open("threshold_llc_index.txt", "r") as f:
        for line in f:
                indexList.append(line.replace("\n", ""))

# split into n index file
coreIndexList = chunks(indexList, noOfCores)
coreNo = 0
for currentList in coreIndexList:
	# for each process/core, prepare the input index list first.
	f = open("driver_index_" + `coreNo`,'a')
	for index in currentList:
		f.write(index + '\n') # python will convert \n to os.linesep
	f.close()
	
	# launch driver for each core
	p = subprocess.Popen(["python", "core_driver.py", `coreNo`, bmName])

	print "Launched core " + `coreNo` + " with " + `len(currentList)` + " index"
	coreNo += 1
