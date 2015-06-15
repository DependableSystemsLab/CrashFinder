# CrashFinder
# Author: Guanpeng(Justin) Li


How to install?


1. First copy passes in 'Pass' folder to your LLVM pass folder (e.g. llvm/lib/Transforms/) and run make to build these passes with LLVM (v2.9).
2. Install LLFI 2.9, the one that shipped with CrashFinder is under 'CF-LLFI' folder.
3. Make sure llvm-gcc (v2.9), llvm-link, lli, llvm-ld, gcc, g++ and all LLFI commands are in your envirment pathes, so that scripts of CrashFinder can directly call them.



How to run CrashFinder?


- CrashFinder Static

1. First put indexed LLVM IR file of benchmark under test in root folder of CrashFinder. The index instrumentation can be done via 'instrument' command in LLFI. The indexed LLVM IR file's name should be in the form of 'input-llfi_index.ll', where 'input' is your benchmark name.
2. Under the root folder of CrashFinder, run command:
	'opt -load PathToLlvmBuildFolder/lib/LLVMDT.so -S -bishe_insert input-llfi_index.ll -o null.ll 2>SDDS.txt'
3. Under the root folder of CrashFinder, run command:
	'python filterSddsFast.py'
4. Go to 'CFS' folder, run 'python run-cf-static.py benchmarkName' where 'benchmarkName' is the name of your benchmark name.
5. The generated txt file contains location index that CFS gives for LLC locations.


- CrashFinder Dynamic

1. Go to 'CFD' folder, run 'python driveSmartFi.py input' where 'input' is the name of your benchmark name.
2. The generated txt file contains all static index and their sampled dynamic instance index.


- Selective Fault Injection

1. Go to 'SFI' folder, configure files in 'drive_mult_smart.py' with correct benchmark name and number of threads you want to parallelize for fault injections.
2. Go to 'name-sample' folder, change the folder name with your benchmark name, in the form of '*-sample', where '*' is your benchmark name.
3. Put original LLVM IR file of your benchmark under the 'name-sample' folder, configure 'faultinject.py' with your benchmark name and test input.
4. Go to the root of 'SFI' folder, run 'python drive_mult_smart.py' for the fault injection.
5. After fault injections are all done, run 'python getLlcReport.py' to generate 'final_llc_index.txt' where all identified LLCs are listed in the file.


Have fun with LLCs!
