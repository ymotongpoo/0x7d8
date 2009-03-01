#include <stdio.h>
#include <stdlib.h>
#define MAX 200

struct {
	int key;
	int data;
} table[MAX];

int lin_search(int k)
{
	int c = 0;
	while(c < MAX){
		if(table[c].key == k)
			return table[c].data;
		
		c++;
	}

	return 0;

}


int bin_search(int k)
{
	int f = 0;
	int l = MAX - 1;
	int m = 0;

	int c = 0;

	while(f <= l){
		c++;
		m = (f + l) / 2;
		if(k == table[m].key){
			printf("loop:%d\n", c);
			return table[m].data;
		}else if(k < table[m].key)
			l = m - 1;
		else if(k > table[m].key)
			f = m + 1;

	}

	return -1;

}
	

int main(int argc, char *argv[])
{
	int c, check = 0;;

	for(c = 0; c < MAX; c++){
		table[c].key = c;
		table[c].data = c * 2;
	}
	/*
	if((check = lin_search(atoi(argv[1]))))
		printf("\naruyo! -> %d\n", check);
	else
		printf("\nnaiyo!\n");
	*/

	if((check = bin_search(atoi(argv[1]))))
		printf("\naruyo! -> %d\n", check);
	else
		printf("\nnaiyo!\n");



	return 0;

}
