#! /usr/bin/python

import os

bmName = "462.libquantum"

# reading all index
allIndexList = []
totalExecutedIndex = 0
with open("threshold_llc_index.txt", "r") as f:
	for line in f:
		allIndexList.append(int(line.replace("\n", "")))

for index in allIndexList:
	os.chdir(bmName + "_" + `index`)
	with open("llfi.stat.prof.txt", "r") as f:
	        for line in f:
			if "total_cycle=" in line:
				#totalProfileCount += int(line.split("=")[1])
				if int(line.split("=")[1]) > 0:
					totalExecutedIndex = totalExecutedIndex + 1
	os.chdir("../")

print "Total Executed Index: " + `totalExecutedIndex`
