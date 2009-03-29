#ifndef OPEN_ADDRESS_H
#define OPEN_ADDRESS_H

#include <iostream>
#include <map>

typedef std::map<int, std::string> Dictonary;
typedef std::map<int, std::string>::iterator DictonaryIter;

class OpenAddress {
public:
	static const int HASH_DIV = 100;
	void insert_data(std::string _data);
	void delete_data(std::string _data);
	DictionaryIter find_data(std::string _data);
	int hash_function(std::string _data);
	int rehash_function(int _hash_val, std::string _data);
private:
	Dictionary hash_list;
};

#endif
