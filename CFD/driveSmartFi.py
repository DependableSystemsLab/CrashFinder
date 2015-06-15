#! /usr/bin/python

import os, sys

############################################
bmName = "libquantum" # Benchmark Name
bmInput = "33 5" # Benchmark Input
############################################

cf_static_points_list = []
currentProgress = 0

# read fi point
with open("../CFS/cf_static_points.txt", "r") as ins:
	for line in ins:
		cf_static_points_list.append(int(line.split()[0]))

os.system("rm multSmartFiList.txt")
		
# now sample with CFD
for static_index_point in cf_static_points_list:

	currentProgress += 1

	# rm CFD_cycle file
	os.system("rm CFD_fi_cycle.txt")

	inpf = open("smartProfile.c.sample")
        inpfContent = inpf.read().replace("XXXX", `static_index_point`)
        with open("smartProfile.c", "w") as inpf:
        	inpf.write(inpfContent)

	# compile the smartProfile.c
	os.system("llvm-gcc -S -emit-llvm smartProfile.c -o smartProfile.ll")

	# use CFD pass to instrument the counter
	os.system("opt -load ~/llvm-2.9-build/lib/CFD.so -S -bishe_insert ../" +bmName+ "-llfi_index.ll -o "+bmName+"_sf.ll -target_index='" +`static_index_point`+ "'")

	# link
	os.system("llvm-link "+bmName+"_sf.ll smartProfile.ll -o "+bmName+"_sf_linked.ll")

	# generate CFD_cycle file
	os.system("lli "+bmName+"_sf_linked.ll " + bmInput)
	
	# read CFD_cycle file
	if os.path.exists("CFD_fi_cycle.txt"):
		with open("CFD_fi_cycle.txt") as cfds:
			for cycle in cfds:
				with open("multSmartFiList.txt", "a") as inpf2:
					inpf2.write(`static_index_point` + " " + `int(cycle)` + "\n")

	print "\n\n\n\n************************************\nCurrent Progress: " + `currentProgress` + "/" + `len(cf_static_points_list)`
