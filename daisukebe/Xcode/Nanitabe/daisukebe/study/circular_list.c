#include <stdio.h>
#include <malloc.h>

typedef struct cell{
	int val;
	struct cell *next;
} CELL;

CELL header = {0, NULL};

void insert(int num)
{
	CELL *p, *q, *new;
	q = &header;
	p = q->next;
	while (p != NULL && num > p->val){
		q = p;
		p = p->next;
		if(p == &header)
			break;
	}

	if ((new = malloc(sizeof(CELL))) == NULL)
		printf("can't allocate enough memory");

	new->val = num;
	new->next = p;
	q->next = new;

}

void delete(int num)
{
	CELL *p, *q;
	q = &header;
	for(p = header.next; p != &header; ){
		if(p->val == num){
			q->next = p->next;
			p = q->next;
		}else{
			q = p;
			p = p->next;
		}
		/*
		q = p->next;
		p = p->next;
		*/

	}
	
}


int main()
{
	header.next = &header;
	
	insert(3);
	insert(8);
	insert(5);
	insert(-19);
	insert(39);
	insert(8);
	insert(-1);

	CELL *p;
	p = &header;

	for(p = header.next; p != &header; p = p->next)
		printf("%d\n", p->val);

	printf("\n");
	
	delete(8);
		
	for(p = header.next; p != &header; p = p->next)
		printf("%d\n", p->val);

	
	/*
	do {
		p = p->next;
		printf("%d\n", p->val);
	}while (p->next != &header);
	*/

	return 0;
	
}
