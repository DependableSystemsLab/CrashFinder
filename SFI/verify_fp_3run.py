#! /usr/bin/python

import os
import os.path
import math
import sys

##########################################################################################################
bmName = "cvm_scancvm"
latencyThreshold = int(sys.argv[1]) # 10^4
##########################################################################################################

totalIndexCounter = 0
rightCounter = 0
indexList = []

def readIndex():
	with open("threshold_llc_index.txt", "r") as f:
		for line in f:
			indexList.append(int(line.replace("\n", "")))

def verifyForIndex(index):
	global rightCounter, totalIndexCounter
	# Go to the index folder
	os.chdir(bmName + "_" + `index`)
	### Stats
	totalFiNumber = 1000
	totalCountFlag = False
	for fiNumber in range(0, totalFiNumber):
		for runNumber in range(0, 3):
			errorOutputFilePath = './llfi/error_output/errorfile-run-' + `runNumber` + '-' + `fiNumber`
			if os.path.isfile(errorOutputFilePath) and os.access(errorOutputFilePath, os.R_OK):
				errorOutputFile = open(errorOutputFilePath, 'r')
				errorOutput = errorOutputFile.read()
	
				if errorOutput.find('crashed') != -1 and errorOutput.find('system') != -1:
					if totalCountFlag == False:
						totalIndexCounter += 1
						totalCountFlag = True
					if os.access('./llfi/llfi_stat_output/llfi.stat.fi.injectedfaults.' + `runNumber` + '-' + `fiNumber` + '.txt', os.R_OK) == False:
						continue
					### If crashed, read fi cycle
					fiStatFile = open('./llfi/llfi_stat_output/llfi.stat.fi.injectedfaults.' + `runNumber` + '-' + `fiNumber` + '.txt', 'r')
					fiStat = fiStatFile.read()
					fiCycle = fiStat.split(', ')[2].split('=')[1]

					# Read FI index
					fiIndex = fiStat.split(', ')[1].split('=')[1]
	
					# Read FI bit
					fiBit = fiStat.split(', ')[4].split('=')[1].replace("\n", "").replace("FI stat: fi_type", "")
	
					### Read last cycle tracked before crash
					trackedCycleFilePath = './llfi/prog_output/crashcount_latency.' + `runNumber` + '-' + `fiNumber` + '.txt'
					if os.path.isfile(trackedCycleFilePath) and os.access(trackedCycleFilePath, os.R_OK):
						trackedCycleFile = open(trackedCycleFilePath, 'r')
						crashDistance = trackedCycleFile.read().strip()
					else:
						crashDistance = 1
	
					#print crashDistance
					#print "FI Index: " + `fiIndex` + " - Latency: " + `crashDistance` + " - FI Cycle: " + `fiCycle` +  " - FI Bit: " + `fiBit` + " - NO. of Run: " + `fiNumber`

					if crashDistance == "":
						continue
					if math.log(float(crashDistance), 10) >= latencyThreshold:
						rightCounter += 1
						os.chdir("..")
						return

	os.chdir("..")

###############################################################################################################
readIndex()
for index in indexList:
	verifyForIndex(index)
print "Correct: " + `rightCounter` + "/" + `totalIndexCounter`
