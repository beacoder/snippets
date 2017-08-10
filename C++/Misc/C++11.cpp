#include <functional>

// combine std::bind(), variadic templates, and perfect forwarding

void third_party(int n, std::function<void(int)> f)
{
  f(n);
}

struct foo
{
  template <typename... Args>
  void invoke(int n, Args&&... args)
  {
    auto bound = std::bind(&foo::invoke_impl<Args&...>, this,
                           std::placeholders::_1, std::forward<Args>(args)...);
 
    third_party(n, bound);
  }
 
  template <typename... Args>
  void invoke_impl(int, Args&&...)
  {
  }
};
 
int main()
{
    foo f;
    f.invoke(1, 2);
}
