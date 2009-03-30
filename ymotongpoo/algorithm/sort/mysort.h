#ifndef MYSORT_H
#define MYSORT_H

#include <iostream>
#include <vector>

class Sort {
public:
	static void bubble_sort(std::vector<int>& _source);
	static void selection_sort(std::vector<int>& _source);
	static void insertion_sort(std::vector<int>& _source);
	static void shell_sort(std::vector<int>& _soruce);
	static void merge_sort(std::vector<int>& _source);
	static void heap_sort(std::vector<int>& _source);
	static void quick_sort(std::vector<int>& _source);
	static void intro_sort(std::vector<int>& _source);
	static void share_sort(std::vector<int>& _source);
	static void in_place_merge_sort(std::vector<int>& _source);
	static void cocktail_sort(std::vector<int>& _source);
	static void comb_sort(std::vector<int>& _source);
	static void gnome_sort(std::vector<int>& _source);
	static void odd_even_transportation_sort(std::vector<int>& _source);
};

#endif
