#include <stdio.h>
#include <stdlib.h>

#define MAX 100

void insert(int table[])
{
	int i;
	for(i = 0; i < MAX; i++)
		table[i] = rand() % MAX;

}

void insertion_sort(int table[])
{
	int i, j, s;

	for(i = 1; i < MAX; i++){
		j = i;
		while(j >= 1 && table[j-1] > table[j]){
			s = table[j];
			table[j] = table[j-1];
			table[j-1] = s;

			j--;
		}
	}

}

int main(int argc, char *argv)
{

	int i;
	int table[MAX];

	insert(table);

	insertion_sort(table);

	for(i = 0; i < MAX; i++)
		printf("%d ", table[i]);

	return 0;

}

