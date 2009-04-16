gcc -fPIC -o test.o -c test.c
gcc -fPIC -I/opt/local/include/python2.5 -o testWrapper.o -c testWrapper.c
gcc -undefined dynamic_lookup -bundle test.o testWrapper.o -o testmodule.so

