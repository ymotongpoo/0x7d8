#include "open_address.h"

int main() {
	OpenAddress* oa = new OpenAddress();
	oa->insert_data("hoge");
	oa->insert_data("piyo");
	oa->insert_data("fuga");

	oa->print_all();

	oa->delete_data("fuga");

	oa->print_all();

	return 0;
}
