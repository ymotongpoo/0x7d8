#include "mysort.h"

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
