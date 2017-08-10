/**
 * gcc compile command is :
 * g++ -g -Wall -L/usr/lib bind_function.cpp -o test
 */

#include <memory>
#include <functional>
#include <iostream>
#include <thread.hpp>

using namespace std;

class Shared_Obj {
 public:
  using Ptr = std::shared_ptr<Shared_Obj> ;
 
  Shared_Obj() {
    std::cout << "Shared_Obj is constructed !" << std::endl;
  }

  ~Shared_Obj() {
    std::cout << "Shared_Obj is destructed !" << std::endl;
  }
};

using ResourceType = Shared_Obj::Ptr;

void fun1 (ResourceType rs)
{
  std::cout << "fun1 is called !" << std::endl;
  std::cout << "ref_count is  " << rs.use_count() << std::endl;
}

void fun2 (ResourceType rs)
{
  std::cout << "fun2 is called !" << std::endl;
  std::cout << "ref_count is  " << rs.use_count() << std::endl;
}

struct functor {
  void operator()(const ResourceType& rs) const
  {
    std::cout << "functor is called !" << std::endl;
    std::cout << "ref_count is  " << rs.use_count() << std::endl;
  }
};

int main(int argc, char *argv[]) {

  ResourceType rs = std::make_shared<Shared_Obj>();

  std::cout << "ref_count is  " << rs.use_count() << std::endl;

  std::function<void> threadfunc1 = std::bind(&fun1, rs);

  std::cout << "ref_count is  " << rs.use_count() << std::endl;

  std::function<void> threadfunc2 = std::bind(&fun2, rs);

  std::cout << "ref_count is  " << rs.use_count() << std::endl;

  functor fun;
  std::function<void> threadfunc3 = std::bind(&functor::operator(), &fun, std::cref(rs));

  std::cout << "ref_count is  " << rs.use_count() << std::endl;

  std::thread t1(threadfunc1);
  std::thread t2(threadfunc2);
  std::thread t3(threadfunc3);

  // join threads, make sure no memory leaks
  t1.join();
  t2.join();
  t3.join();

  return 0;
}
