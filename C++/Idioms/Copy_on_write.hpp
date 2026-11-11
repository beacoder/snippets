// Copy-on-Write (COW)
// Multiple objects share the same underlying data; a real copy is made only
// when an object needs to modify the shared data. Efficient for read-heavy,
// write-rare scenarios.

template <class T>
class Cow
{
  public:
    Cow() : data_(std::make_shared<T>()) {}

    Cow(const T& v) : data_(std::make_shared<T>(v)) {}

    // Shallow copy — shares the underlying data
    Cow(const Cow&)            = default;
    Cow& operator=(const Cow&) = default;

    // Read access — no copy needed
    const T& read() const { return *data_; }

    // Write access — detach from shared data if more than one owner
    T& write()
    {
        detach();
        return *data_;
    }

  private:
    void detach()
    {
        if (data_.use_count() > 1)
            data_ = std::make_shared<T>(*data_);
    }

    std::shared_ptr<T> data_;
};

void foo()
{
    Cow<std::vector<int>> a{std::vector<int>{1, 2, 3}};
    Cow<std::vector<int>> b = a;  // Shared — no copy

    b.write().push_back(4);       // b detaches, a still sees {1, 2, 3}

    a.read().size();              // 3
    b.read().size();              // 4
}
