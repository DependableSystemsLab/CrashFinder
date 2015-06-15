#! /usr/bin/python

sddsList = []
resultList = []
with open("SDDS.txt") as f:
        for line in f:
		if " --- " in line:
			sddsList.append(line.split(" --- ")[1])


for line in sddsList:
	if line not in resultList:
		resultList.append(line)
		with open("SDDS_filtered.txt", "a") as f:
			f.write(line)
