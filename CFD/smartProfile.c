#include <stdio.h>
#include <memory.h>
#include <string.h>
#include <stdlib.h>
//#include <iostream>
//#include <vector>
//#include <string>
//#include <fstream>


long long instructionCounter = 0;

//std::vector<std::string> callSeqVector;
long long callSeqList[1000000];
//char currentCallSeq[4];
long long currentCallSeq = 1;
long long callSeqSize = 0;

int currentFunctionIndex = -1;
int targetFunctionIndex = -1;
long long targetLlfiIndex = 1347;


//void initParam(){
	//targetLlfiIndex = 00000000;
//}

void functionCall(int functionIndex){

	currentFunctionIndex = functionIndex;

	currentCallSeq = (functionIndex + currentCallSeq) * functionIndex / (functionIndex+1); // Making sure the sequence is unique.

	//char str[4];
	//sprintf(str, "%d", functionIndex);
	//char str3[strlen(currentCallSeq)+5]; 	
	//char *str3 = malloc( sizeof(*currentCallSeq) * ( 5 + 1 ) );
	//strcpy(str3, str);
	//strcat(str3, currentCallSeq);
	
	//memset(&currentCallSeq[0], 0, sizeof(currentCallSeq));

	//currentCallSeq[strlen(str3)];
	//strcat(currentCallSeq, str3);
	//currentCallSeq = str3;
	//printf("%s\n", currentCallSeq);
	//printf("%d\n", strlen());

	//std::string functionIndexString(str);
	//currentCallSeq = currentCallSeq + " " + functionIndexString;

	//std::cout << currentCallSeq << "\n";	
}

void instructionCall(long long llfiIndex){
	if((long long)llfiIndex==(long long)targetLlfiIndex && targetFunctionIndex == -1){
		// init targetFunctionIndex
		targetFunctionIndex = currentFunctionIndex;
		//std::cout << "Target Function Index: " << targetFunctionIndex << "\n";
	}
	
	instructionCounter++;

	if(llfiIndex == targetLlfiIndex){
		// need to know whether this is the FI we want.
		int i;
		for(i=0;i<callSeqSize;i++){
			if(callSeqList[i] == currentCallSeq){
				//do not dump instructionCounter;
  				//memset(&currentCallSeq[0], 0, sizeof(currentCallSeq));
				currentCallSeq = 1;
				return;
			}
		}
		// unique seq
		callSeqList[callSeqSize] = currentCallSeq;
		callSeqSize++;
		//memset(&currentCallSeq[0], 0, sizeof(currentCallSeq));
		currentCallSeq = 1;
		// dump instruction counter;
		//std::cout << "DUMP: " << instructionCounter << "\n";
		FILE *f = fopen("CFD_fi_cycle.txt", "a");
                fprintf(f, "%lld\n", instructionCounter);
                fclose(f);
		//std::ofstream outfile;
		//outfile.open("CFD_fi_cycle", std::ios_base::app);
		//outfile << instructionCounter << "\n"; 
	}
	
}

/*
main(){
	functionCall(11);
	instructionCall(1218);
	instructionCall(1219);
	functionCall(8);
	instructionCall(881);
	instructionCall(882);
	functionCall(12);
	instructionCall(1230);
	instructionCall(1231);
	functionCall(11);
	instructionCall(1218);
	instructionCall(1219);
	functionCall(12);
	instructionCall(1230);
	instructionCall(1231);
	functionCall(11);
	instructionCall(1218);
	instructionCall(1219);
	functionCall(8);
	instructionCall(881);
	instructionCall(882);
	functionCall(12);
	instructionCall(1230);
	instructionCall(1231);
	functionCall(11);
	instructionCall(1218);
	instructionCall(1219);
	functionCall(8);
	instructionCall(881);
	instructionCall(882);
	functionCall(12);
	instructionCall(1230);
	instructionCall(1231);
	functionCall(11);
	instructionCall(1218);
	instructionCall(1219);
}
*/
