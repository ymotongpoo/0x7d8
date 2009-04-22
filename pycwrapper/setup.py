from distutils.core import setup, Extension

setup(name='testm',
      version='1.0',
      ext_modules=[Extension('testm', sources=['test.c', 'testWrapper.c'])])
