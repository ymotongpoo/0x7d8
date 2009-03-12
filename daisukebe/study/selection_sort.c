#include <stdio.h>
#include <stdlib.h>

#define MAX 100

void insert(int table[])
{
	int i;
	for(i = 0; i < MAX; i++)
		table[i] = rand() % MAX;

}

void slct_sort(int table[])
{
	int i, j, s, min_key, min_id;

	for(i = 0; i < MAX; i++){
		min_key = table[i];
		min_id = i;
		for(j = i; j < MAX; j++){
			if(min_key > table[j]){
				min_key = table[j];
				min_id = j;
			}
		}

		s = table[i];
		table[i] = table[min_id];
		table[min_id] = s;
		
	}

}

int main(int argc, char *argv)
{

	int i;
	int table[MAX];

	insert(table);

	slct_sort(table);

	for(i = 0; i < MAX; i++)
		printf("%d ", table[i]);

	return 0;

}
