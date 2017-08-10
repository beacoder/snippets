#include <functional>
#include <iostream>

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


// std::bind() vs lambdas in C++14

// move and capture varaibles
auto f1 = std::bind(f, 42, _1, std::move(v));
auto f1 = [v = std::move(v)](auto arg) { f(42, arg, std::move(v)); };

// capture expressions
auto f1 = std::bind(f, 42, _1, a + b);
auto f1 = [sum = a + b](auto arg) { f(42, arg, sum); };

// perfect forwarding
auto f1 = std::bind(f, 42, std::forward<Args>(args)...);
auto f1 = [=](auto&& arg) { f(42, std::forward<decltype(arg)>(arg)); };


// variadic template recursive function

template <typename...> struct SumTs;
template <typename T1> struct SumTs<T1> { typedef T1 type; };

template <typename T1, typename... Ts>
struct SumTs<T1, Ts...>
{
  typedef typename SumTs<Ts...>::type rhs_t;
  typedef decltype(std::declval<T1>() + std::declval<rhs_t>()) type;
};

//now the sum function
template <typename T>
T sum(const T& v)
{
  return v;
}

template <typename T1, typename... Ts>
auto sum(const T1& v1, const Ts&... rest) 
  -> typename SumTs<T1,Ts...>::type //instead of the decltype
{
  return v1 + sum(rest... );
}

int main()
{
  std::cout << sum(1,2,3,4,5);    
}
