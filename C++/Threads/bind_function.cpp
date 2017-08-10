/**
 * gcc compile command is :
 * g++ -g -Wall -I/usr/include/boost -L/usr/lib -lboost_thread bind_function.cpp -o test
 */

#include <memory>
#include <iostream>
#include <boost/bind.hpp>
#include <boost/thread.hpp>

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

  ResourceType rs = boost::make_shared<Shared_Obj>();

  std::cout << "ref_count is  " << rs.use_count() << std::endl;

  boost::function0<void> threadfunc1 = boost::bind(&fun1, rs);

  std::cout << "ref_count is  " << rs.use_count() << std::endl;

  boost::function0<void> threadfunc2 = boost::bind(&fun2, rs);

  std::cout << "ref_count is  " << rs.use_count() << std::endl;

  functor fun;
  boost::function0<void> threadfunc3 = boost::bind(&functor::operator(), &fun, boost::cref(rs));

  std::cout << "ref_count is  " << rs.use_count() << std::endl;

  boost::thread t1(threadfunc1);
  boost::thread t2(threadfunc2);
  boost::thread t3(threadfunc3);

  // join threads, make sure no memory leaks
  t1.join();
  t2.join();
  t3.join();

  return 0;
}
