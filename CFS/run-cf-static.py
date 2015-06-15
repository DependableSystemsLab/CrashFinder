#! /usr/bin/python

import os, sys


##############################
bmName = sys.argv[1]
##############################


os.system("python getPtrStore.py " + bmName + " > cf_static_points.txt")
os.system("python getIndvar.py " + bmName + " >> cf_static_points.txt")
os.system("python getGlobalArray.py " + bmName + " >> cf_static_points.txt")
os.system("python getGlobalState.py " + bmName + " >> cf_static_points.txt")
