// g++ -g -Wall -I/usr/include/boost -L/usr/lib main.cpp -ldl -lboost_thread -o mainTest

#include <dlfcn.h>
#include <stdlib.h>
#include <string>
#include <iostream>
#include "boost/bind.hpp"
#include "boost/thread.hpp"

using namespace std;


static const string libPath = "/home/brightc/private_workspace/libshared_lib_with_static_variables.so";

void threadfunc1 (int* pStatic)
{
  std::cout << libPath << std::endl;
  
  void * hFile = dlopen(libPath.c_str(), (RTLD_LAZY | RTLD_GLOBAL));  
  if(NULL == hFile)
  {
      std::cout << "load library error !" << std::endl;     
  }
  
  int * pointer = (int *)dlsym(hFile, "gStatic");
  if(NULL == pointer)
  {
    std::cout << "load symbol error !" << std::endl;
  }

  std::cout << "threadfunc1 gStatic is : " << (*pointer) << std::endl;

  // increase gStatic by 10;
  *pointer = *pointer + 10;

  std::cout << "threadfunc1 gStatic after modification is : " << (*pointer) << std::endl;
  
  *pStatic = *pointer;  
}

void threadfunc2 (int* pStatic)
{
  std::cout << libPath << std::endl;
  
  void * hFile = dlopen(libPath.c_str(), (RTLD_LAZY | RTLD_GLOBAL));  
  if(NULL == hFile)
  {
      std::cout << "load library error !" << std::endl;
  }
  
  int * pointer = (int *)dlsym(hFile, "gStatic");
  if(NULL == pointer)
  {
    std::cout << "load symbol error !" << std::endl;
  }

  std::cout << "threadfunc2 gStatic is : " << (*pointer) << std::endl;

  // decrease gStatic by 50;
  *pointer = *pointer - 50;

  std::cout << "threadfunc2 gStatic after modification is : " << (*pointer) << std::endl;
    
  *pStatic = *pointer;  
}

int main(int argc, char *argv[]) {

  int threadVal1, threadVal2;
  threadVal1 = threadVal2 = 0;

  boost::function0<void> thread1 = boost::bind(&threadfunc1, &threadVal1);        
  boost::function0<void> thread2 = boost::bind(&threadfunc2, &threadVal2);

  boost::thread t1(thread1);
  boost::thread t2(thread2);
    
  t1.join();
  t2.join();

  std::cout << "threadVal1 is : " << threadVal1 << std::endl;
  std::cout << "threadVal2 is : " << threadVal2 << std::endl;  
  
  return 0;
}
