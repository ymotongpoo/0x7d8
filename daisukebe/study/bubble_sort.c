#include <stdio.h>
#include <stdlib.h>

#define MAX 1000

void insert(int table[])
{
	int i;
	for(i = 0; i < MAX; i++)
		table[i] = rand() % MAX;

}

void bbbl_sort(int table[])
{
	int i, j, t;

	for(i = 0; i < MAX - 1; i++)
		for(j = MAX - 1; j > 0; j--)
			if(table[j] < table[j-1]){
				t = table[j];
				table[j] = table[j-1];
				table[j-1] = t;
			}

}

int main(int argc, char *argv)
{

	int i;
	int table[MAX];

	insert(table);

	bbbl_sort(table);

	for(i = 0; i < MAX; i++)
		printf("%d ", table[i]);

	return 0;

}
