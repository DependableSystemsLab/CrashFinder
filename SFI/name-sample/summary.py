#! /usr/bin/python

import os
import os.path
import math

### Stats
minLatencyDistance = 10 # Used for checking latency of crashes
llcCounter = 0 # Count for llc
crashCounter = 0

totalFiNumber = 1000
crashDistanceList = []
for fiNumber in range(0, totalFiNumber):
	errorOutputFilePath = './llfi/error_output/errorfile-run-0-' + `fiNumber`
	if os.path.isfile(errorOutputFilePath) and os.access(errorOutputFilePath, os.R_OK):
		errorOutputFile = open(errorOutputFilePath, 'r')
		errorOutput = errorOutputFile.read()

		if errorOutput.find('crashed') != -1 and errorOutput.find('system') != -1:
			crashCounter += 1
			### If crashed, read fi cycle
			fiStatFile = open('./llfi/llfi_stat_output/llfi.stat.fi.injectedfaults.0-' + `fiNumber` + '.txt', 'r')
			fiStat = fiStatFile.read()
			fiCycle = fiStat.split(', ')[2].split('=')[1]

			# Read FI index
			fiIndex = fiStat.split(', ')[1].split('=')[1]

			# Read FI bit
			fiBit = fiStat.split(', ')[4].split('=')[1].replace("\n", "").replace("FI stat: fi_type", "")

			### Read last cycle tracked before crash
			trackedCycleFilePath = './llfi/prog_output/crashcount_latency.0-' + `fiNumber` + '.txt'
			if os.path.isfile(trackedCycleFilePath) and os.access(trackedCycleFilePath, os.R_OK):
				trackedCycleFile = open(trackedCycleFilePath, 'r')
				crashDistance = trackedCycleFile.read().strip()
			else:
				crashDistance = 0

			#print crashDistance
			print "FI Index: " + `fiIndex` + " - Latency: " + `crashDistance` + " - FI Cycle: " + `fiCycle` +  " - FI Bit: " + `fiBit` + " - NO. of Run: " + `fiNumber`

			crashDistanceList.append(int(crashDistance))

print 'Total Crash: ' + `crashCounter`

# Stat crash distance
#groupCounter = 0
#groupTotalCounter = 0
#for factorCounter in range(1, 15):
#	for distance in crashDistanceList:
#		if distance <= math.pow(minLatencyDistance, factorCounter) and distance > math.pow(minLatencyDistance, factorCounter-1):
#			groupCounter += 1
#	print `int(math.pow(minLatencyDistance, factorCounter))` + ',' + `groupCounter`
#	groupTotalCounter += groupCounter
#	groupCounter = 0
