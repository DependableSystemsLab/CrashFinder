#! /usr/bin/python

# This script finds the induction variables and their dependencies.
# The rules are:
#	1. Find %indvar in phi node, and tell from parameters about update/assignment variable's name.
#	2. If the name is in form of 'tmp' or 'indvar', then it is local variable. Only need to protect the instructions that assign to these variables.
#	3. If the name is not in form of local variables, Looks for the phi instructions that have dependency to these variables.
  

import sys, os


##########################################
bmName = sys.argv[1]
indexFilePath = "../"+bmName+"-llfi_index.ll"
##########################################
sddsContentList = []
resultIndexList = []
phiIndexList = []

#########################################
# Source Code
def getIndexOfLine(line):
	if "!llfi_index" not in line:
		return -1
	return int(line.split("!llfi_index !")[1])

def getAssignmentNameOfLine(line):
	if "=" in line and "%" in line:
		varName = line.split(" = ")[0].replace("%", "")
		return varName.replace(" ", "")
	return ""

# SDD
def readSdds():
        global sddsContentList
        sddsFile = open("../SDDS_filtered.txt", 'r')
        sddsContentList = sddsFile.readlines()

# Read loop header phi node index
def readLoopHeaderPhi():
	global phiIndexList
	# Run loop header pass first, which finds phi llfi_index in loop header.
	os.system("opt -load ~/llvm-2.9-build/lib/IndvarDetector.so -S -loop-dep " + indexFilePath + " -o null.ll 2>IndvarPhiList.txt")
	with open("IndvarPhiList.txt") as f:
		for line in f:
			phiIndexList.append(int(line))
	
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
readLoopHeaderPhi()

ins = open(indexFilePath, "r" )

# Keep all alias' name from indvar phi
phiArgNameList = []

# Locate all the indvar and its dependency
for line in ins:
	lineIndex = getIndexOfLine(line)
	if lineIndex in phiIndexList and "phi" in line:
		paramList = line.split()
		# 5th is the first arg
		firstArg = paramList[5].replace(",", "")
		# 9th is the second arg
		secondArg = paramList[9].replace(",", "")

		if "%" in firstArg and firstArg.replace("%", "").isdigit() == False:
			if firstArg not in phiArgNameList:
				phiArgNameList.append(firstArg.replace("%", ""))
		if "%" in secondArg and secondArg.replace("%", "").isdigit() == False:
			if secondArg not in phiArgNameList:
				phiArgNameList.append(secondArg.replace("%", ""))

ins = open(indexFilePath, "r" )

terminationVarNameList = []

for line in ins:
	lineIndex = getIndexOfLine(line)
	varName = getAssignmentNameOfLine(line)
	if "tmp" in varName or "indvar" in varName:
		if "indvar" in varName and lineIndex not in resultIndexList:
			print `lineIndex` + " single"
			resultIndexList.append(lineIndex)
			
		if varName in phiArgNameList:
			# only protect its assignment instruction as their dependency is used in load to cause SLC
			if lineIndex not in resultIndexList:
				print `lineIndex` + " single"
				resultIndexList.append(lineIndex)
	elif "phi" in line:	
		for name in varName:
			if name in line:
				phiIndex = int(getIndexOfLine(line))
				for sddsLine in sddsContentList:
					if `phiIndex` not in sddsLine:
						continue
					foundFlag = False
					for node in sddsLine.split("->"):
						if node == "\n":
							continue
						if int(getIndex(node)) == phiIndex:
							foundFlag = True
						if foundFlag == True:
							if "L.1.0" in node:
								if int(getIndex(node)) not in resultIndexList:
									resultIndexList.append(int(getIndex(node)))
									print `int(getIndex(node))` + " all"
	
	# Find termination variable of indvar
	if "exitcond" in line and "=" in line and "!llfi_index" in line:
		lineIndex = int(getIndexOfLine(line))
		for sddsLine in sddsContentList:
			if "->" + `lineIndex` + ".C." in sddsLine:
				if len(sddsLine.split("->")) >= 4:
					beforeCmpIndex = int(getIndex(sddsLine.split("->")[-4]))
					if beforeCmpIndex not in resultIndexList:
						print `beforeCmpIndex` + " total"
						resultIndexList.append(beforeCmpIndex)
		
	



#########################################
#TEST
#########################################

