/**
 * gcc compile command is :
 * g++ -g -Wall -I/usr/include/boost -L/usr/lib -lboost_thread condition_variable.cpp -o test
 */

#include <iostream>
#include <boost/thread.hpp>

using namespace std;

static boost::mutex mGuard;
static boost::condition mCondition;
static bool hasProduct = false;

void produce(void)
{
  boost::mutex::scoped_lock lock(mGuard);

  std::cout << "produce is called !\n";
  std::cout << "pid is " << pthread_self() << "\n";
  std::cout << std::endl;

  hasProduct = true;
  mCondition.notify_all();
}

void consume(void)
{
  std::cout << "consume is locked !\n";
  std::cout << "pid is " << pthread_self() << "\n";
  std::cout << std::endl;

  {
    boost::mutex::scoped_lock lock(mGuard);
    while (!hasProduct)
    {
      mCondition.wait(lock);
    }
  }

  std::cout << "consume is unlocked !\n";
  std::cout << "pid is " << pthread_self() << "\n";
  std::cout << std::endl;
}

int main(int argc, char *argv[]) {

  boost::function0<void> producer(produce);
  boost::function0<void> consumer(consume);

  boost::thread t1(consumer);
  boost::thread t2(consumer);
  boost::thread t3(consumer);
  boost::thread t4(consumer);
  boost::thread t5(producer);

  // join threads, make sure no memory leaks
  t1.join();
  t2.join();
  t3.join();
  t4.join();
  t5.join();

  return 0;
}
