#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>

long long fi_cycle_counter = 0;
long long cycleInterval = 1;
long long cycleFactor = 1;
extern int fiFlag;
long long bbCounter = 0;

void latencyCount(long llfiIndex){

	if(fiFlag == 1){
		fi_cycle_counter++;
		if(fi_cycle_counter >= cycleInterval*10){
			cycleInterval *= 10;
			cycleFactor = 1;
		}
		if(fi_cycle_counter > cycleInterval * cycleFactor){
			cycleFactor++;
			FILE *f = fopen("crashcount_latency.txt", "w");
			fprintf(f, "%lld", fi_cycle_counter);
			fclose(f);
		}
	}

}

