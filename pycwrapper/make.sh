gcc -fPIC -o testm.o -c testm.c
gcc -fPIC -I/opt/local/include/python2.5 -o testmWrapper.o -c testmWrapper.c
gcc -undefined dynamic_lookup -bundle testm.o testmWrapper.o -o testmmodule.so

