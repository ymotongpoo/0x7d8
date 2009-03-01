#include <stdio.h>
#include <malloc.h>

typedef struct cell{
	struct cell *next;
	struct cell *prev;
	int num;
} CELL;

CELL root = {NULL, NULL, 0};

void add(int val)
{
	CELL *p, *new;

	p = &root;
	while(p != NULL && val > p->num){
		if(p->next == &root){
			p = p->next;
			break;
		}
		
		p = p->next;
	}

	if((new = malloc(sizeof(CELL))) == NULL)
		printf("out of memory\n");

	new->num = val;
	new->next = p;
	new->prev = p->prev;
	p->prev->next = new;
	p->prev = new;
}

void delete(int val)
{
	CELL *p = &root;
	while(p != NULL){
		if(p->num == val){
			p->prev->next = p->next;
			p->next->prev = p->prev;
		}
		if(p->next == &root) break;
		p = p->next;
	}
	
}

int main()
{

	root.next = &root;
	root.prev = &root;

	add(5);
	add(10);
	add(6);
	add(3);
	add(10);
	add(6);
	add(2);
	add(10);

	CELL *c = &root;
	for(c = c->next; c != &root && c != NULL; c = c->next)
		printf("%d\n", c->num);

	printf("\n");

	delete(10);

	c = &root;
	for(c = c->next; c != &root && c != NULL; c = c->next)
		printf("%d\n", c->num);

	return 0;

}
