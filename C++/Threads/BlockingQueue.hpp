
/*
 * @note Modified from chenshuo's "muduo/base/BlockingQueue.h"
 */

#include <mutex>
#include <condition_variable>
#include <deque>
#include <assert.h>
#include <boost/noncopyable.hpp>

template<typename T>
class BlockingQueue : boost::noncopyable
{
 public:
  BlockingQueue()
    : mutex_(),
      condition_(mutex_),
      queue_()
  {
  }

  void put(const T& x)
  {
    std::lock_guard lock(mutex_);
    queue_.push_back(x);
    condition_.notify(); // wait morphing saves us
    // http://www.domaigne.com/blog/computing/condvars-signal-with-mutex-locked-or-not/
  }

  T take()
  {
    std::lock_guard lock(mutex_);
    // always use a while-loop, due to spurious wakeup
    while (queue_.empty())
    {
      condition_.wait();
    }
    assert(!queue_.empty());
    T front(queue_.front());
    queue_.pop_front();
    return front;
  }

  size_t size() const
  {
    std::lock_guard lock(mutex_);
    return queue_.size();
  }
  
  bool empty() const
  {
    std::lock_guard lock(mutex_);
    return queue_.empty();
  }

 private:
  mutable std::mutex      mutex_;
  std::condition_variable condition_;
  std::deque<T>           queue_;
};
