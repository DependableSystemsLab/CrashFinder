#! /usr/bin/python

import os

#################################
bmName = "scancvm"
llcThreshold = 1000
#################################


llcIndexList = []
folderList = os.listdir("./")

finalResultsList = []

for folderName in folderList:
	if bmName in folderName and "_" in folderName:
		index = folderName.split("_")[1]
		cycle = folderName.split("_")[2]
		if index not in llcIndexList:
			os.chdir("./" + folderName)
			totalFiNumber = 1000
        		for fiNumber in range(0, totalFiNumber):
		                for runNumber in range(0, 10):
                		        errorOutputFilePath = './llfi/error_output/errorfile-run-' + `runNumber` + '-' + `fiNumber`
		                        if os.path.isfile(errorOutputFilePath) and os.access(errorOutputFilePath, os.R_OK):
                		                errorOutputFile = open(errorOutputFilePath, 'r')
                                		errorOutput = errorOutputFile.read()

		                                if errorOutput.find('crashed') != -1 and errorOutput.find('system') != -1:			
							trackedCycleFilePath = './llfi/prog_output/crashcount_latency.' + `runNumber` + '-' + `fiNumber` + '.txt'
		                                        if os.path.isfile(trackedCycleFilePath) and os.access(trackedCycleFilePath, os.R_OK):
                		                                trackedCycleFile = open(trackedCycleFilePath, 'r')
                                		                crashDistance = trackedCycleFile.read().strip()
                                        		else:
                                                		crashDistance = 0
							
							# check if llc
							if int(crashDistance) >= llcThreshold:
								llcIndexList.append(index)
								print "LLC -> Index: " + `index` + " - Latency: " + `crashDistance`
								if int(index) not in finalResultsList:
									finalResultsList.append(int(index))
								break
							print "NOT LLC -> Index: " + `index` + " - Latency: " + `crashDistance`
			os.chdir("../")

os.system("rm final_llc_index.txt")
for index in finalResultsList:
	with open("final_llc_index.txt", "a") as resultFile:
		resultFile.write(`index`+'\n')

print "Total Final LLC Index: " + `len(finalResultsList)`


