// Copy-on-Write (COW)
// Multiple objects share the same underlying data; a real copy is made only
// when an object needs to modify the shared data. Efficient for read-heavy,
// write-rare scenarios.

class CowString
{
  public:
    CowString(const char* s = "")
      : data_(std::make_shared<std::string>(s)) {}

    // Shallow copy — shares the underlying data
    CowString(const CowString&) = default;
    CowString& operator=(const CowString&) = default;

    // Read access — no copy needed
    const char& operator[](size_t i) const
    {
        return (*data_)[i];
    }

    // Write access — detach from shared data if more than one owner
    char& operator[](size_t i)
    {
        detach();
        return (*data_)[i];
    }

    void append(const char* s)
    {
        detach();
        data_->append(s);
    }

    const std::string& str() const { return *data_; }

  private:
    // Copy-on-write: if the data is shared, make a private copy before mutating
    void detach()
    {
        if (data_.use_count() > 1)
            data_ = std::make_shared<std::string>(*data_);
    }

    std::shared_ptr<std::string> data_;
};

void foo()
{
    CowString a("hello");
    CowString b = a;      // Shared — no copy

    b[0] = 'H';           // b detaches, a still sees "hello"

    a.append(" world");   // a detaches (if still shared)
}
