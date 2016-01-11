/*
 * @note Modified from chenshuo's "muduo/base/BlockingQueue.h"
 */

#include <mutex>
#include <condition_variable>
#include <boost/noncopyable.hpp>

class CountDownLatch : boost::noncopyable
{
 public:

  explicit  CountDownLatch(int count)
            : mutex_(),
            condition_(mutex_),
            count_(count)
  {
  }

  void wait()
  {
    std::lock_guard lock(mutex_);
    while (count_ > 0)
    {
      condition_.wait();
    }
  }

  void countDown()
  {
    std::lock_guard lock(mutex_);
    --count_;
    if (count_ == 0)
    {
      condition_.notifyAll();
    }
  }

  int getCount() const
  {
    std::lock_guard lock(mutex_);
    return count_;
  }

 private:
  mutable std::mutex      mutex_;
  std::condition_variable condition_;
  int count_;
};
