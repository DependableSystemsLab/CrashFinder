#! /usr/bin/python

# This script finds load instruction that takes global variable. Then check if the load is used to access an array, then we find points that have dependency with the global variable.

import sys


##########################################
bmName = sys.argv[1]
indexFilePath = "../"+bmName+"-llfi_index.ll"
##########################################
sddsContentList = []
resultIndexList = []
codeLineDic = {}
globalVarNameList = []

#########################################
# Source Code
def getIndexOfLine(line):
	if "!llfi_index" not in line:
		return -1
	return int(line.split("!llfi_index !")[1])

def getLoadParamName(line):
	return line.split()[4].replace(",", "")

# SDD
def readSdds():
        global sddsContentList
        sddsFile = open("../SDDS_filtered.txt", 'r')
        sddsContentList = sddsFile.readlines()

# node operations
def getIndex(node):
        nodeElements = node.split(".")
        return nodeElements[0]

def getInstType(node):
        nodeElements = node.split(".")
        return nodeElements[1]

def isUsedInMem(node):
        nodeElements = node.split(".")
        return nodeElements[2]

def isResultPtr(node):
        nodeElements = node.split(".")
        return nodeElements[3]


#########################################


readSdds()
ins = open(indexFilePath, "r" )
for line in ins:
	if "!llfi_index" in line:
		lineIndex = getIndexOfLine(line)
		codeLineDic[int(lineIndex)] = line

ins = open(indexFilePath, "r" )
for line in ins:
	if getIndexOfLine(line) == -1:
		continue
	if "load" in line and "@" in line:
		lineIndex = getIndexOfLine(line)
		if int(lineIndex) not in resultIndexList:
			print `lineIndex` + " all"
			resultIndexList.append(int(lineIndex))
	if "store" in line and "@" in line:
		lineIndex = int(getIndexOfLine(line))
		for sddsLine in sddsContentList:
			if "->" + `lineIndex` + ".S.0.0" in sddsLine:
				beforeStoreIndex = int(getIndex(sddsLine.split("->")[-3]))
				if int(beforeStoreIndex) not in resultIndexList:
					print `beforeStoreIndex` + " all"
					resultIndexList.append(int(beforeStoreIndex))
	if "getelementptr" in line and "@" in line:
		lineIndex = getIndexOfLine(line)
		if int(lineIndex) not in resultIndexList:
			print `lineIndex` + " all"
			resultIndexList.append(int(lineIndex))
		

'''
		# Check if it is used in getptr with array
		findLoadFlag = False
		for sddsLine in sddsContentList:
			findLoadFlag = False
			if `lineIndex` not in sddsLine:
				continue
			for node in sddsLine.replace("\n", "").split("->"):
				if node == "":
					continue
				nodeIndex = getIndex(node)
				if int(nodeIndex) == int(lineIndex):
					# find the load in sdds
					findLoadFlag = True
				if '.G.' in node and findLoadFlag == True:
					getPtrIndex = getIndex(node)
					# check the gptr in code line
					getPtrLine = codeLineDic[int(getPtrIndex)]
					if "[" in getPtrLine:
						if getLoadParamName(line) not in globalVarNameList:
							globalVarNameList.append(getLoadParamName(line))
							print lineIndex
							print getPtrLine
						continue

print globalVarNameList
			
'''

#########################################
#TEST
#########################################

