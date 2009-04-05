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

void gnome_sort(std::vector<int>& _source) {

}

void Sort::odd_even_transportation_sort(std::vector<int>& _source) {

}
