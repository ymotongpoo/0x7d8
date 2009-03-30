#ifndef MYSORT_H
#define MYSORT_H

#include <iostream>
#include <vector>

class Sort {
public:
	static void bubble_sort(std::vector<int>& _source);
	static void selection_sort(std::vector<int>& _source);
	static void insertion_sort(std::vector<int>& _source);
};

#endif
