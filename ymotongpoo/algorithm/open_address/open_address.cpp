#include "open_address.h"

void OpenAddress::insert_data(std::string _data) {
	int key = hash_function(_data);
	DictionaryIter itr = hash_list.find(key);
	if (itr != hash_list.end())
		key = rehash_function(_data);

	hash_list.insert( Dictionary::value_type(key, _data) );
}

void OpenAddress::delete_data(std::string _data) {
}

DictionaryIter OpenAddress::find_data(std::string _data) {
}

int OpenAddress::hash_function(std::string _data) {
	int hash_val = 0;
	for (int i = 0; i < _data.length(); i++) {
		hash_val += _data.at(i);
	}
	return hash_val % HASH_DIV;
}

int OpenAddress::rehash_function(int _hash_val, std::string _data) {
	DictionaryIter itr = hash_list.begin();
	int i = 0;
	for (i = 1; itr != hash_list.end(); i++) {
		itr = hash_list.find(_hash_val + HASH_DIV*i)
	}
	return _hash_val + HASH_DIV*i;
}
