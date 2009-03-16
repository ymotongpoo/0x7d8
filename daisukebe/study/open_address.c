#include <stdio.h>
#include <stdlib.h>
#define MAX 13
#define DELETED -1

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

void delete(char *name)
{
	int h, hh;
	hh = h = hash(name);

	while(table[h].name != name){
		h = rehash(h);
		if(h == hh){
			printf("over the range >_<\n");
			return;
		}
	}

	table[h].name = NULL;
	table[h].key = DELETED;
	
}


int main(int argc, char *argv[])
{

	int i = 0;

	init(table);

	add("sony");		/* 2 */
	add("toshiba");		/* 5 */
	add("panasonic");	/* 7 */
	add("honda");		/* 2 */


	while(i < MAX){
		printf("%d:\n", i);
		printf("    %s, %d\n", table[i].name, table[i].key);

		i++;
	}


	printf("\nafter\n");
	delete("honda");

	i = 0;
	while(i < MAX){
		printf("%d:\n", i);
		printf("    %s, %d\n", table[i].name, table[i].key);

		i++;
	}


	return 0;

}
