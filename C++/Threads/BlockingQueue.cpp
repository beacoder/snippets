/**
 * gcc compile command is :
 * g++ -g -Wall BlockingQueue.hpp.cpp -o BlockingQueue
 */

#include <iostream>           // std::cout
#include <string>             // std::string
#include <deque>              // std::deque
#include <thread>             // std::thread
#include <mutex>              // std::mutex, std::unique_lock
#include <condition_variable> // std::condition_variable

template<typename T>
class BlockingQueue
{
  BlockingQueue(const BlockingQueue&);
  BlockingQueue& operator=(const BlockingQueue&);

 public:
  explicit BlockingQueue()
    : mutex_(),
      condition_(),
      queue_()
  {
  }

  void put(const T& x)
  {
    std::unique_lock<std::mutex> lock(mutex_);
    queue_.push_back(x);
    condition_.notify_one();
  }

  T take()
  {
    std::unique_lock<std::mutex> lock(mutex_);
    while (queue_.empty())
    {
      condition_.wait(lock);
    }

    T front(queue_.front());
    queue_.pop_front();
    return front;
  }

  size_t size() const
  {
    std::unique_lock<std::mutex> lock(mutex_);
    return queue_.size();
  }

  bool empty() const
  {
    std::unique_lock<std::mutex> lock(mutex_);
    return queue_.empty();
  }

 private:
  mutable std::mutex      mutex_;
  std::condition_variable condition_;
  std::deque<T>           queue_;
};

int main(int argc, char *argv[])
{
    BlockingQueue<std::string> queue;

    queue.put("Hello");
    queue.put("World");

    std::cout << queue.take() << std::endl;
    std::cout << queue.take() << std::endl;

    return 0;
}
