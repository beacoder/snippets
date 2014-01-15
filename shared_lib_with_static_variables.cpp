// step1: gcc -c -Wall -fpic shared_lib_with_static_variables.cpp
// step2: gcc -shared -o libshared_lib_with_static_variables.so shared_lib_with_static_variables.o

#ifndef foo_h__
#define foo_h__

extern "C"
{
  extern int gStatic = 10000;  
}

#endif  // foo_h__
