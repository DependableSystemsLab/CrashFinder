#! /usr/bin/python

# This script finds global variables used in states or locks.

import sys


##########################################
bmName = sys.argv[1]
indexFilePath = "../"+bmName+"-llfi_index.ll"
##########################################
sddsContentList = []
resultIndexList = []

#########################################
# Source Code
def getIndexOfLine(line):
	return int(line.split("!llfi_index !")[1])

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
	if "load" in line and "@" in line:
		loadIndex = getIndexOfLine(line)
		#print `loadIndex` + " all" 
		for sddsLine in sddsContentList:
			if `loadIndex` + ".L." in sddsLine and ".B." in sddsLine:
				#index = int(getIndex(sddsLine.split("->")[-3]))
				if loadIndex not in resultIndexList:
					resultIndexList.append(loadIndex)
					print `loadIndex` + " all"


#########################################
#TEST
#########################################

