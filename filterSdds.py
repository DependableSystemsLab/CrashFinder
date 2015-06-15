#! /usr/bin/python

sddsList = []
dupIndexList = []
resultList = []
with open("SDDS.txt") as f:
        for line in f:
		if " --- " in line:
			sddsList.append(line.split(" --- ")[1])

for i in range(0, len(sddsList)):
	for j in range(0, len(sddsList)):
		if sddsList[i].replace("\n", "") in sddsList[j] and sddsList[i] != sddsList[j]:
			dupIndexList.append(i);
			break

for k in range(0, len(sddsList)):
	if k not in dupIndexList:
		#resultList.append(sddsList[k].replace("\n", ""))
		with open("SDDS_filtered.txt", "a") as f:
			f.write((sddsList[k]))
