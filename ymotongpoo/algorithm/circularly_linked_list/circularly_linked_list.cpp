#include "circularly_linked_list.h"

using std::cerr; using std::endl;

Cell::Cell(int _data, Cell* _next, Cell* _prev) {
	data = _data;
	next = _next;
	prev = _prev;
}

Cell::Cell() {
	Cell(0, NULL, NULL);
}

Cell::~Cell() {
	next = NULL;
	prev = NULL;
}

inline Cell* Cell::next_cell() {
	return this->next;
}

inline Cell* Cell::prev_cell() {
	return this->prev;
}

inline void Cell::next_cell(Cell* _cell) {
	this->next = _cell;
}

inline void Cell::prev_cell(Cell* _cell) {
	this->prev = _cell;
}

inline int Cell::get_data() {
	return this->data;
}

CircularlyLinkedList::CircularlyLinkedList() {
	head = NULL;
}

CircularlyLinkedList::~CircularlyLinkedList() {
	Cell* n = NULL;
	for( Cell* c = head; c; ) {
		n = c->next_cell();
		delete c;
		c = n;
	}
}

int CircularlyLinkedList::insert_cell(int _val) {
	if ( head == NULL ) {
		cerr << "head null" << endl;
		head = create_cell(_val);
		head->next_cell(head);
		head->prev_cell(head);
	}
	else {
		Cell* c = head;
		Cell* n = head->next_cell();
		while ( n != head && _val > n->get_data() ) {
			cerr << "ok00" << endl;
			c = n;
			cerr << "ok01" << endl;
			n = n->next_cell();
		}

		if ( n == head ) {
			Cell* new_head = create_cell(_val);
			new_head->next_cell(head);
			head->prev_cell(new_head);
			head = new_head;
		}
		else {
			cerr << "hello" << endl;
			Cell* new_cell = create_cell(_val);
			c->next_cell(new_cell);
			if (n != head)
				n->prev_cell(new_cell);

			new_cell->next_cell(n);
			new_cell->prev_cell(c);
		}
	}

	return 0;
}

int CircularlyLinkedList::delete_cell(int _val) {
	Cell* c = find_cell(_val);
	c->prev_cell()->next_cell(c->next_cell());
	c->next_cell()->prev_cell(c->prev_cell());
	delete c;

	return 0;
}

inline Cell* CircularlyLinkedList::create_cell(int _val) {
	return new Cell(_val, NULL, NULL);
}

Cell* CircularlyLinkedList::find_cell(int _val) {
	Cell* c = NULL;
	for (c = head; c; c = c->next_cell() )
		if ( c->get_data() == _val )
			return c;
}

void CircularlyLinkedList::print_all() {
	Cell* c = head;
	while(1) {
		cerr << c->get_data() << endl;
		if ( !c->next_cell() )
			break;
		c = c->next_cell();
	}
}
