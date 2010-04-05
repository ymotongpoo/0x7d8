from distutils.core import setup, Extension

setup(name='testm',
      version='1.0',
      ext_modules=[Extension('testm', sources=['testm.c', 'testmWrapper.c'])])
