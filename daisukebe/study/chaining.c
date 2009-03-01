#include <stdio.h>
#include <stdlib.h>
#define MAX 10

typedef struct cell{
	int key;
	char *name;
	struct cell *next;
} CELL;

CELL *table[MAX];

int hash(char var[])
{
	int i, total = 0;
	for(i = 0; var[i] != '\0'; i++)
		total += var[i];

	return total % MAX;

}

void init(CELL *table[])
{
	int i;
	for(i = 0; i < MAX; i++){
		if((table[i] = malloc(sizeof(CELL))) == NULL)
			break;
		table[i] = NULL;
	}

}

int find(char *name)
{
	CELL *p;
	for(p = table[hash(name)]; p != NULL; p = p->next){
		if(p->name == name){
			printf("%s\n", p->name);
			return 1; /* exist */
		}

	}

	return 0;		/* do not exist */
}

int add(char *name)
{
	int i, h;
	CELL *new, *p;
	/* printf("%d\n", hash(name)); */

	if(find(name) == 1)
		return 1;


	h = hash(name);
	if((new = malloc(sizeof(CELL))) == NULL){
		printf("out of memory\n");
		return -1;
	}

	new->key = h;
	new->name = name;
	p = table[h];
	if(table[h] != NULL){
		while(p->next != NULL)
			p = p->next;

		new->next = p->next;
		p->next = new;
	}else {
		table[h] = new;
	}
		
	return 0;

}

int main(int argc, char *argv[])
{
	int i = 0, c = 0;
	CELL *p;

	init(table);

	add("daisuke");		/* 2 */
	add("hugauga");		/* 8 */
	add("hugahuga");	/* 2 */
	add("yosuke");		/* 2 */
	add("yosukebe");
	add("pho");
	add("shiumachi");
	add("kany");

	while(i < MAX){
		printf("%d:\n", i);
		for(p = table[i]; p != NULL; p = p->next){
			printf("    %s\n", p->name);
			if(p->next == table[i])
				break;
		}
		
		
		i++;
	}



	return 0;

}
