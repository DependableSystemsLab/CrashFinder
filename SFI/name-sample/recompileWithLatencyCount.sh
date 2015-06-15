opt -load ~/llvm-2.9-build/lib/LLVMCL.so -S -bishe_insert llfi/scancvm-faultinjection.ll -o llfi/scancvm-faultinjection-cc.ll
llvm-link llfi/scancvm-faultinjection-cc.ll crash_count.ll -o llfi/scancvm-faultinjection-cc.ll
llc -filetype=obj -o llfi/scancvm-faultinjection.o llfi/scancvm-faultinjection-cc.ll
llvm-gcc llfi/scancvm-faultinjection.o -o llfi/scancvm-faultinjection.exe -L/home/gpli/LLFI-BUILD/runtime_lib/ -lllfi-rt -Wl,-rpath /home/gpli/LLFI-BUILD/bin/../runtime_lib
