#! /usr/bin/python

import os
import sys
import subprocess
from random import randint

# read args
coreNo = int(sys.argv[1])
bmName = sys.argv[2]
latencyThreshold = 1000
llcIndexList = []

# read index for this core
totalIndex = 0
with open ("driver_index_" + `coreNo`,'r') as f:
	for line in f:
        	totalIndex += 1

coreIndexCounter = 0
with open("driver_index_" + `coreNo`, "r") as f:
	print "Reading driver index ..."
	indexCounter = 0
        for line in f:
		# print progress
		print "Core " + `coreNo` + ": " + `indexCounter` + "/" + `totalIndex`
		indexCounter += 1
		coreIndexCounter += 1

		line = line.replace("\n", "")
                index = line.split()[0].replace("'", "")
		cycle = line.split()[1].replace("'", "")

		# check if index is already llc
		if index in llcIndexList:
			continue
			
		# copy fi folder for each core
		os.system("cp -r " + bmName + "-sample " + bmName + "_" + index + "_" + cycle + "_" + `coreNo` + "_" + `coreIndexCounter`)

		# modify input.yaml
		os.chdir("./" + bmName + "_" + index + "_" + cycle + "_" + `coreNo` + "_" + `coreIndexCounter`)
		inpf = open("input.yaml")

		# generate sampling
		bit1 = randint(1,6)
		bit2 = randint(27,31)
		bit3 = randint(59,63)

		inpfContent = inpf.read().replace("XXXX", index).replace("YYYY", cycle).replace("AAAA", `bit1`).replace("BBBB", `bit2`).replace("CCCC", `bit3`)

		with open("input.yaml", "w") as inpf:
			inpf.write(inpfContent)

		# launch faultinject.py
		subprocess.call(["python", "faultinject.py"])

		# check if llc
		totalFiNumber = 10
        	for fiNumber in range(0, totalFiNumber):
                	errorOutputFilePath = './llfi/error_output/errorfile-run-0-' + `fiNumber`
	                if os.path.isfile(errorOutputFilePath) and os.access(errorOutputFilePath, os.R_OK):
        	                errorOutputFile = open(errorOutputFilePath, 'r')
                	        errorOutput = errorOutputFile.read()
	
        	                if errorOutput.find('crashed') != -1 and errorOutput.find('system') != -1:
	                                ### If crashed, read fi cycle
        	                        #fiStatFile = open('./llfi/llfi_stat_output/llfi.stat.fi.injectedfaults.0-' + `fiNumber` + '.txt', 'r')
                	                #fiStat = fiStatFile.read()
                        	        #fiCycle = fiStat.split(', ')[2].split('=')[1]
	
        	                        # Read FI index
                	                #fiIndex = fiStat.split(', ')[1].split('=')[1]
	
        	                        # Read FI bit
                	                #fiBit = fiStat.split(', ')[4].split('=')[1].replace("\n", "").replace("FI stat: fi_type", "")
	
        	                        ### Read last cycle tracked before crash
                	                trackedCycleFilePath = './llfi/prog_output/crashcount_latency.0-' + `fiNumber` + '.txt'
                        	        if os.path.isfile(trackedCycleFilePath) and os.access(trackedCycleFilePath, os.R_OK):
                                	        trackedCycleFile = open(trackedCycleFilePath, 'r')
                                        	crashDistance = trackedCycleFile.read().strip()
	                                else:
        	                                crashDistance = 0
	
        	                        #print crashDistance
                	                #print "FI Index: " + `fiIndex` + " - Latency: " + `crashDistance` + " - FI Cycle: " + `fiCycle` +  " - FI Bit: " + `fiBit` + " - NO. of Run: " + `fiNumber`
                        	        if int(crashDistance) >= latencyThreshold:
						llcIndexList.append(index)			
						break



		os.chdir("../")
