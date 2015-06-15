CrashFinder
===================



What is CrashFinder?
-----------------

CrashFinder is an automatic tool that can identify program locations causing long-latency crashes(LLCs). The paper about CrashFinder can be found at http://blogs.ubc.ca/karthik/files/2015/04/gpli_DSN2015.pdf



How to install?
-----------------


 - First copy passes in 'Pass' folder to your LLVM pass folder (e.g. llvm/lib/Transforms/) and run make to build these passes with LLVM (v2.9).
 - Install LLFI 2.9, the one that shipped with CrashFinder is under 'CF-LLFI' folder.
 - Make sure llvm-gcc (v2.9), llvm-link, lli, llvm-ld, gcc, g++ and all LLFI commands are in your envirment pathes, so that scripts of CrashFinder can directly call them.



How to configure and run CrashFinder?
------------------------


**CrashFinder Static**

 - First put indexed LLVM IR file of benchmark under test in root folder of CrashFinder. The index instrumentation can be done via 'instrument' command in LLFI. The indexed LLVM IR file's name should be in the form of 'input-llfi_index.ll', where 'input' is your benchmark name.
 - Under the root folder of CrashFinder, run command:
	'opt -load PathToLlvmBuildFolder/lib/LLVMDT.so -S -bishe_insert input-llfi_index.ll -o null.ll 2>SDDS.txt'
 - Under the root folder of CrashFinder, run command:
	'python filterSddsFast.py'
 - Go to 'CFS' folder, run 'python run-cf-static.py benchmarkName' where 'benchmarkName' is the name of your benchmark name.
 - The generated txt file contains location index that CFS gives for LLC locations.


**CrashFinder Dynamic**

 - Go to 'CFD' folder, run 'python driveSmartFi.py input' where 'input' is the name of your benchmark name.
 - The generated txt file contains all static index and their sampled dynamic instance index.


**Selective Fault Injection**

 - Go to 'SFI' folder, configure files in 'drive_mult_smart.py' with correct benchmark name and number of threads you want to parallelize for fault injections.
 - Put the txt file generate from last phase under the root of 'SFI' folder.
 - Go to 'name-sample' folder, change the folder name with your benchmark name, in the form of 'X-sample', where 'X' is your benchmark name.
 - Put original LLVM IR file of your benchmark under the 'name-sample' folder, configure 'faultinject.py' with your benchmark name and test input.
 - Go to the root of 'SFI' folder, run 'python drive_mult_smart.py' for the fault injection.
 - After fault injections are all done, run 'python getLlcReport.py' to generate 'final_llc_index.txt' where all identified LLCs are listed in the file.



Have fun with LLCs!
