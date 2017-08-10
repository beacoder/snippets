#include <boost/thread/mutex.hpp>
#include <boost/thread/condition_variable.hpp>
#include <boost/thread/locks.hpp>

class CountDownLatch : boost::noncopyable
{
 public:

  // NonCopyable
  CountDownLatch           (const CountDownLatch&) = delete;
  CountDownLatch& operator=(const CountDownLatch&) = delete;

  explicit  CountDownLatch(int count);

  void wait();

  void countDown();

  int getCount() const;

 private:
  mutable boost::mutex      mutex_;
  boost::condition_variable condition_;
  int count_;
};

CountDownLatch::CountDownLatch(int count)
  : mutex_(),
  condition_(),
  count_(count)
{
}

void CountDownLatch::wait()
{
  boost::lock_guard lock(mutex_);
  while (count_ > 0)
  {
    condition_.wait();
  }
}

void CountDownLatch::countDown()
{
  boost::lock_guard lock(mutex_);
  --count_;
  if (count_ == 0)
  {
    condition_.notifyAll();
  }
}

int CountDownLatch::getCount() const
{
  boost::lock_guard lock(mutex_);
  return count_;
}
