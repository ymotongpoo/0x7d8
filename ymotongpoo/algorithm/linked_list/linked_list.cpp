#include "linked_list.h"

using std::cerr; using std::endl;

Cell::Cell(int _data, Cell* _next) {
	data = _data;
	next = _next;
}

Cell::Cell() {
	Cell(0, NULL);
}

Cell* Cell::next_cell() {
	return this->next;
}

void Cell::next_cell(Cell* _cell) {
	this->next = _cell;
}

int Cell::get_data() {
	return this->data;
}

LinkedList::LinkedList() {
	head = NULL;
}

int LinkedList::insert_cell(int _val) {
	if (head == NULL)
		head = create_cell(_val);
	else {
		Cell* p = head;
		Cell* c = NULL;
		for (c = head; c; c = c->next_cell()) {
			if (c->get_data() > _val)
				break;
			p = c;
		}
		
		if (c == head) {
			Cell* new_head = create_cell(_val);
			new_head->next_cell(head);
			head = new_head;
		}
		else {	
			p->next_cell(create_cell(_val));
			p->next_cell()->next_cell(c);
		}
	}

	return 0;
}

int LinkedList::delete_cell(int _val) {
	return 0;
}

Cell* LinkedList::create_cell(int _val) {
	Cell* cell = new Cell(_val, NULL);
	return cell;
}

void LinkedList::print_all() {
	Cell* c = head;
	while(1) {
		cerr << c->get_data() << endl;
		if (!c->next_cell())
			break;
		c = c->next_cell();
	}
}
