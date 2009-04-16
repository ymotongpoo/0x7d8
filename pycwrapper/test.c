#include <stdio.h>

int add(int x, int y) {
	return x + y;
}

void out(const char* address, const char* name) {
	printf("こんちはー、おいどんは%sの%sです。\n", address, name);
}

