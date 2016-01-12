#include <boost/noncopyable.hpp>
#include <boost/thread/mutex.hpp>
#include <boost/thread/condition_variable.hpp>
#include <boost/thread/locks.hpp>
#include <deque>
#include <assert.h>

template<typename T>
class BlockingQueue : boost::noncopyable
{
 public:
  void put(const T& x)
  {
    boost::lock_guard lock(mutex_);
    queue_.push_back(x);
    condition_.notify(); // wait morphing saves us
    // http://www.domaigne.com/blog/computing/condvars-signal-with-mutex-locked-or-not/
  }

  T take()
  {
    boost::lock_guard lock(mutex_);
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
    boost::lock_guard lock(mutex_);
    return queue_.size();
  }
  
  bool empty() const
  {
    boost::lock_guard lock(mutex_);
    return queue_.empty();
  }

 private:
  mutable boost::mutex      mutex_;
  boost::condition_variable condition_;
  std::deque<T>             queue_;
};
