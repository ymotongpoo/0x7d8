#include <stdio.h>
#include <stdlib.h>
#define MAX 13

typedef struct cell{
	int key;
	char *name;
} CELL;

CELL table[MAX];

int hash(char var[])
{
	int i, total = 0;
	for(i = 0; var[i] != '\0'; i++)
		total += var[i];

	return total % MAX;

}

int rehash(int h)
{
	return (h + 1) % MAX;

}

void init(CELL table[])
{
	int i;
	for(i = 0; i < MAX; i++){
		table[i].key = 0;
		table[i].name = NULL;
	}

}

void add(char *name)
{
	int h, hh;
	hh = h = hash(name);

	while(table[h].name != NULL){
		h = rehash(h);
		if(h == hh){
			printf("over the range >_<\n");
			return;
		}
	}

	
	table[h].name = name;

}

int main(int argc, char *argv[])
{

	int i = 0;

	init(table);

	add("sony");		/* 2 */
	add("toshiba");		/* 5 */
	add("panasonic");	/* 7 */
	add("sony");		/* 2 -> 3 */
	add("toshiba");		/* 5 -> 6 */
	add("panasonic");	/* 7 -> 8 */
	add("toshiba");		/* 5 -> 9 */

	while(i < MAX){
		printf("%d:\n", i);
		printf("    %s\n", table[i].name);

		i++;
	}

	return 0;

}
