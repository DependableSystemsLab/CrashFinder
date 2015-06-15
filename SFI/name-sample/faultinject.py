#! /usr/bin/python

import subprocess

irfile = "name.ll" # benchmark ir file
irbase = "name"    # benchmark name

# instrument
subprocess.call(["instrument", "--readable", irfile])
subprocess.call(["bash", "recompileWithLatencyCount.sh"])

# profile
subprocess.call(["profile", "llfi/" + irbase + "-profiling.exe", "input"]) # benchmark test input

# fault injection
subprocess.call(["injectfault", "llfi/" + irbase + "-faultinjection.exe", "input"]) # benchmark test input
