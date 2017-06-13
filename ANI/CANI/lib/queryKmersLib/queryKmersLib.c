#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include "queryKmersLib4.h"

//const int MAX = 100000;//100,000, 200,000=fault
//const int MAX = 40; //100,000, 200,000=fault
char** queryKmersIntoArray(const char* dnaChars, int kmerSize, const int numKmers) {
	char** kmersArrayMalloc = (char**) malloc(numKmers*sizeof(char*));
	if(kmersArrayMalloc == NULL) { printf("%s", "1");}
	for(int i = 0; i < numKmers; i++) {
      kmersArrayMalloc[i] = (char *) malloc(sizeof(char)*kmerSize);
   }
	for(int i = 0; i < strlen(dnaChars) - kmerSize + 1; i++) {
		memcpy(kmersArrayMalloc[i], &dnaChars[i], kmerSize);
	}
	return (char**) kmersArrayMalloc;
}