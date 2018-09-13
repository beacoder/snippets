// C++ guarantees that the destructors of objects on the stack will be called, even if an exception is thrown
// e.g: resources are passed around with std::unique_ptr

template <class T>
class AutoDelete
{
  public:
    AutoDelete           (T* p = 0) : ptr_(p) {}
    ~AutoDelete          () noexcept          { delete ptr_; }

    // NonCopyable
    AutoDelete           (const AutoDelete&) = delete;
    AutoDelete& operator=(const AutoDelete&) = delete;

  private:
    T *ptr_;
};

// Scoped Lock idiom
class ScopedLock
{
  public:
    ScopedLock           (Lock& l) : lock_(l) { lock_.acquire(); }
    ~ScopedLock          () noexcept          { lock_.release(); }

    // NonCopyable
    ScopedLock           (const ScopedLock&) = delete;
    ScopedLock& operator=(const ScopedLock&) = delete;

  private:
    Lock& lock_;
};

void foo ()
{
  X * p = new X;
  AutoDelete<X> safe_del(p); // Memory will not leak
  p = 0;
  // Although, above assignment "p = 0" is not necessary
  // as we would not have a dangling pointer in this example. 
  // It is a good programming practice.

  if (...)
    if (...)
      return; 
 
  // No need to call delete here.
  // Destructor of safe_del will delete memory
}

void X::bar()
{
  ScopedLock safe_lock(l); // Lock will be released certainly
  if (...)
    if (...)
      throw "ERROR";

  // No need to call release here.
  // Destructor of safe_lock will release the lock
}
