#! /usr/bin/python

# This script finds point that goes back to store instruction. Note the script only finds the store instruction which is the ending point of each dependency chain.

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
	if "add" in line and "indvar" in line and "%" not in line.split(",")[1]:
		indvarIndex = getIndexOfLine(line)
		print `indvarIndex` 


#########################################
#TEST
#########################################

