#include <stdio.h>
#include <stdlib.h>

#define MAX 20

void insert(int table[])
{
	int i;
	for(i = 0; i < MAX; i++)
		table[i] = rand() % MAX;

}

void view(int table[])
{
	int i;
	for(i = 0; i < MAX; i++)
		printf("%d ", table[i]);

	printf("\n");

}

int  max_interval(void)
{
	int h ;
	for(h = 1; h <= MAX; h = h * 3 + 1)
		;

	return h / 3;
}

void shell_sort(int table[], int h)
{
	int i, j, s;

	for(; h > 0; h = h / 3){
		for(i = h; i < MAX; i += h){
			view(table);
			j = i;
			while(j >= 1 && table[j-h] > table[j]){
				s = table[j];
				table[j] = table[j-h];
				table[j-h] = s;
				
				j -= h;
			}
		}
	}
}

int main(int argc, char *argv)
{

	int i, h;
	int table[MAX];

	insert(table);
	

	h = max_interval();
	//printf("%d", h);
	//return 0;
	
	shell_sort(table, h);

	for(i = 0; i < MAX; i++)
		printf("%d ", table[i]);

	return 0;

}

