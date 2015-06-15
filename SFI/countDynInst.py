#! /usr/bin/python

import os

bmName = "462.libquantum"

# reading all index
allIndexList = []
totalProfileCount = 0 
with open("threshold_llc_index.txt", "r") as f:
	for line in f:
		allIndexList.append(int(line.replace("\n", "")))

for index in allIndexList:
	os.chdir(bmName + "_" + `index`)
	with open("llfi.stat.prof.txt", "r") as f:
	        for line in f:
			if "total_cycle=" in line:
				totalProfileCount += int(line.split("=")[1])
	os.chdir("../")

print "totalProfileCount: " + `totalProfileCount`
