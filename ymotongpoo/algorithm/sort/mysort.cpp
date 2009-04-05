#include "mysort.h"
#include <ctime>

void Sort::bubble_sort(std::vector<int>& _source) {
	int length = _source.size();

	for (int i = 0; i < length; i++) {
		for (int j = length - 1; j > i; j--) {
			if (_source[j] < _source[j-1])
				std::swap(_source[j], _source[j-1]);
		}
	}
}

void Sort::selection_sort(std::vector<int>& _source) {
	int length = _source.size();
	int min;
	for (int i = 0; i < length; i++) {
		min = i;
		for (int j = i; j < length; j++) {
			if (_source[min] > _source[j])
				std::swap(_source[min], _source[j]);
		}
	}
}

void Sort::insertion_sort(std::vector<int>& _source) {
	int length = _source.size();

	for (int i = 0; i < length; i++) {
		for (int j = i; j > 0 && _source[j-1] > _source[j]; j--) {
			std::swap(_source[j-1], _source[j]);
		}
	}
}

void Sort::shell_sort(std::vector<int>& _source, int _interval = SHELL_SORT_INTERVAL) {
	int length = _source.size();

	int width;
	for (width = 1; width < length / _interval; width = _interval*width + 1);
	for (; width > 0; width /= _interval) {
		for (int i = width; i < length; i++) {
			for (int j = i; j >= width && _source[j-width] > _source[j]; j -= width) {
				std::swap(_source[j-width], _source[j]);
			}
		}
	}
}

void Sort::merge_sort(std::vector<int>& _source) {
	int length = _source.size();
	std::vector<int> tempv;
}

void Sort::heap_sort(std::vector<int>& _source) {

}

void Sort::quick_sort(std::vector<int>& _source) {
	int length = _source.size();

	partial_quick_sort(_source, 0, length-1);
}

void Sort::partial_quick_sort(std::vector<int>& _source, int _from, int _to) {
	if (_from > _to)
		return;

	int v = quick_sort_partition(_source, _from, _to);

	partial_quick_sort(_source, _from, v-1);
	partial_quick_sort(_source, v+1, _to);	
}

int Sort::quick_sort_partition(std::vector<int>& _source, int _from, int _to) {
	int pivot = _source[_to];
	int i = _from - 1;
	int j = _to;

	while (1) {
		while(_source[++i] < pivot);
		while(i < --j && pivot < _source[j]);
		
		if (i >= j)
			break;

		std::swap(_source[i], _source[j]);
	}

	std::swap(_source[i], _source[_to]);

	return i;
}

void Sort::intro_sort(std::vector<int>& _source) {

}

void Sort::share_sort(std::vector<int>& _source) {

}

void Sort::in_place_merge_sort(std::vector<int>& _source) {

}

void Sort::cocktail_sort(std::vector<int>& _source) {

}

void Sort::comb_sort(std::vector<int>& _source) {

}

void Sort::gnome_sort(std::vector<int>& _source) {

}

void Sort::odd_even_transportation_sort(std::vector<int>& _source) {

}

