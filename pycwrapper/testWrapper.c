#include "Python.h"
#include "modsupport.h"

extern int add(int x, int y);
extern void out(const char* address, const char* name);

PyObject* test_add(PyObject* self, PyObject* args) {
	int x, y, g;
	if (!PyArg_ParseTuple(args, "ii", &x, &y))
		return NULL;
	g = add(x, y);
	return Py_BuildValue("i", g);
}

PyObject* test_out(PyObject* self, PyObject* args, PyObject* kw) {
	const char* address = NULL;
	const char* name = NULL;
	
	static char* argnames[] = {"args", "name", NULL};

	if (!PyArg_ParseTupleAndKeywords(args, kw, "|ss",
									 argnames, &address, &name))
		return NULL;

	out(address, name);
	return Py_BuildValue("");
}

static PyMethodDef testmethods[] = {
	{"add", test_add, METH_VARARGS},
	{"out", test_out, METH_VARARGS | METH_KEYWORDS},
	{NULL},
};

void inittest() {
	Py_InitModule("test", testmethods);
}
