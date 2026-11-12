# Modern C++: Old Ways vs. New Ways

A quick reference to standard-library features and language improvements introduced across C++17, C++20, and C++23.

---

## C++17

| Old way | New way | Note |
|---|---|---|
| Switch on a type tag + `dynamic_cast` chains | `std::variant` + `std::visit` | |
| Sentinel values (`-1`, `nullptr`, `boost::optional`) | `std::optional<T>` | |
| `const std::string&` parameters, `const char*` constants | `std::string_view` | non-owning; do not store/dangle |
| `boost::any` / `void*` + cast | `std::any` | |
| `auto it = m.emplace(k, v); bool ok = it.second;` | `auto [it, inserted] = m.emplace(k, v);` | structured bindings |
| `if` condition and initialisation split over two statements | `if (init; cond)` / `switch (init; x)` | init-statement |
| `enable_if` / SFINAE for template branching | `if constexpr` | |
| `std::result_of<...>::type` | `std::invoke_result_t<...>` | |
| `boost::apply_tuple` / manual `std::get<I>` | `std::apply(f, tuple)` | |
| Manual `std::invoke`-style dispatch on member pointers | `std::invoke(f, args...)` | |
| `namespace a { namespace b { ... } }` | `namespace a::b { ... }` | |
| `std::lock(m1, m2)` + `std::unique_lock` wrappers | `std::scoped_lock l(m1, m2)` | |
| Hand-written reader/writer lock | `std::shared_mutex` + `std::shared_lock` | `shared_lock` itself is C++14, `shared_mutex` is C++17 |
| `static const` with ODR headaches | `inline constexpr int x = 42;` | inline variables |
| `char*` / `uint8_t*` for raw bytes | `std::byte` | |
| `boost::filesystem` / POSIX `opendir` + `stat` | `std::filesystem` | |
| Hand-rolled thread fan-out / `std::async` soup | Execution policies `std::execution::par` / `par_unseq` on the standard algorithms | the actual C++17 feature behind the `reduce` row |
| `atoi` / `sscanf` / `sprintf` / iostreams formatting | `std::from_chars` / `std::to_chars` | locale-free, no allocation |
| `__attribute__((warn_unused_result))` / `__attribute__((unused))` / `-Wimplicit-fallthrough` | `[[nodiscard]]` / `[[maybe_unused]]` / `[[fallthrough]];` | `[[nodiscard]]` and `[[maybe_unused]]` address different concerns; `[[fallthrough]]` replaces the warning-flag dance |
| Custom allocator boilerplate / arena hacks | `std::pmr` polymorphic memory resources | |
| `static_cast<const T&>(x)` to force const | `std::as_const(x)` | |
| `std::not1` / `std::not2` / `std::bind` tricks | `std::not_fn` | |
| Hand-rolled `void_t` detection idiom | `std::void_t` | |
| Recursive `_v` metafunctions | `std::conjunction` / `disjunction` / `negation` | short-circuiting |
| `sizeof(a) / sizeof(a[0])` | `std::size(a)` / `std::data(a)` / `std::empty(a)` | |
| Recursive variadic templates | Fold expressions `(ts + ...)` | |
| `template <class T, T v>` | `template <auto N>` | |
| Named function objects for constant expressions | `constexpr` lambdas | |
| `time_point_cast` + manual truncation | `chrono::floor` / `ceil` / `round` | |

---

## C++20

| Old way | New way | Note |
|---|---|---|
| Iterator pairs (`begin`, `end`) | Ranges: `r \| std::views::filter(pred)` | |
| `enable_if` / SFINAE tricks | Concepts: `template <std::ranges::input_range R>` | |
| Callback chains, hand-rolled state machines | Coroutines: `co_await`, `co_return` | |
| `std::thread` + manual join in the destructor | `std::jthread` (auto-join + `std::stop_token`) | |
| Raw `T*` + `size_t n` parameters | `std::span<T>` | |
| `erase(v.begin(), std::remove_if(...), v.end())` | `std::erase_if(v, pred)` | also for `string`, `map`, ... |
| Hand-written `operator<`, `>`, `<=`, `>=`, `!=` | `auto operator<=>(const T&) const = default;` | |
| `printf` / `snprintf` / chained `ostream <<` | `std::format("x = {}", x)` | |
| `__FILE__` / `__LINE__` macros | `std::source_location::current()` | |
| `memcpy` type punning | `std::bit_cast<To>(from)` | |
| Hand-rolled barrier with mutex + condition variable | `std::barrier`, `std::latch`, `std::counting_semaphore` | |
| Mutex around `std::cout` | `std::osyncstream(std::cout) << ...;` | the one-statement temporary **is** valid: it emits atomically at the end of the full-expression. Use a *named* `osyncstream` only when the write spans several statements |
| `s.find(x) != s.end()` for `set` / `map` | `s.contains(x)` | container members for **associative/unordered** containers only. For `std::string` / `string_view` the old form is `find(sub) != npos` and `contains` is C++23 |
| `static_cast<std::ptrdiff_t>(v.size())` | `std::ssize(v)` | |
| `int arr[] = {1,2,3};` then copy into a container | `std::to_array({1, 2, 3})` | element type deduced; `std::to_array<int>({1,2,3})` also works |
| `#ifdef` / compiler intrinsics for constexpr checks | `std::is_constant_evaluated()` | prefer C++23 `if consteval` |
| Unsafe signed/unsigned comparison `a < b` | `std::cmp_less(a, b)` (and `cmp_equal`, `cmp_greater`, ...) | |
| `boost::date_time` or C `tm` / `time_t` | `<chrono>` calendar (`year_month_day`, `floor<days>`) and time-zone library (`tzdb`, `zoned_time`) | |
| Header includes (preprocessor, ODR issues) | Modules: `module`/`import` (C++20 core language) | the standard library *named modules* `import std;` / `std.compat` are **C++23**, not C++20 |
| `constexpr` used when the object need not be constexpr | `constinit` | guarantees **constant initialization** of a static/thread_local object (avoids the static-init-order fiasco); the object itself stays mutable |
| `constexpr` functions that must always run at compile time | `consteval` | immediate functions |
| `s.find(prefix) == 0` | `s.starts_with(prefix)` / `s.ends_with(suffix)` | `std::string` and `string_view` |
| `__BYTE_ORDER__` / runtime endian probing | `std::endian::native == std::endian::little` | |
| `__builtin_expect(cond, 1)` | `[[likely]]` / `[[unlikely]]` | |
| Mutex + condition variable for one-shot signalling | `std::atomic<T>::wait()` / `notify_one()` / `notify_all()` | |
| Non-atomic storage that needs atomic access | `std::atomic_ref<T>` | |
| Mutex around a `shared_ptr` | `std::atomic<std::shared_ptr<T>>` | |
| Placement `new` / explicit destructor call | `std::construct_at` / `std::destroy_at` | usable in `constexpr` code |
| `&*it` / `operator->` chains for raw pointers | `std::to_address(p)` | |
| `std::shared_ptr<T>(new T[n], deleter)` | `std::make_shared<T[]>(n)` | |
| `std::bind` | `std::bind_front` | |
| Hand-rolled `decay_t` aliases | `std::remove_cvref_t` / `std::type_identity_t` | |
| `char` / `unsigned char` for UTF-8 | `char8_t` / `std::u8string` | |
| Global tables built at startup via macros | `constexpr` `std::vector` / `std::string` in ordinary code | |
| `std::sort(v.begin(), v.end())` | `std::ranges::sort(v)` (and the other range algorithms) | |
| Raw loops over a range | `views::transform`, `take`, `drop`, `reverse`, `iota`, `split`, `keys`, `values`, `elements`, `common` | |
| Constructor + assignments for aggregate setup | Designated initializers `P{.x = 1, .y = 2}` | |
| `E::a, E::b` qualification everywhere | `using enum E;` | |
| Generic lambda + `decltype` hacks for the parameter type | Templated lambda `[]<class T>(T x) { ... }` | |

---

## C++23

| Old way | New way | Note |
|---|---|---|
| `std::copy` / `std::transform` into a pre-sized container | `r \| std::ranges::to<std::vector<T>>()` | |
| `std::find(r, x) != r.end()` | `std::ranges::contains(r, x)` | |
| `s.find(sub) != std::string::npos` | `s.contains(sub)` | `std::string` / `string_view` |
| Hand-chunked loops (`i += batch`) | `std::views::chunk(n)` / `views::chunk_by(pred)` | |
| `boost::join` or manual separator insertion | `std::views::join_with(sep)` | |
| Manual parallel iteration with an index | `std::views::zip(r1, r2)` / `views::enumerate(r)` | |
| Manual sliding-window loop | `std::views::slide(n)` | |
| Manual step iteration (`i += step`) | `std::views::stride(n)` | |
| `printf` / `std::format` + manual `'\n'` | `std::print("x = {}\n", x)` / `std::println("x = {}", x)` | `{{` and `}}` are *escape sequences* that emit literal braces, so `"{{}}"` prints `{}` and never the value |
| `optional<T>` + separate error code / exception | `std::expected<T, E>` | |
| `if (opt) { auto x = f(*opt); }` chains | `opt.and_then(f).or_else(g).transform(h)` | monadic ops on `optional`; `expected` adds `transform_error` |
| `static_cast<std::underlying_type_t<E>>(e)` | `std::to_underlying(e)` | |
| `__builtin_unreachable()` / `abort()` | `std::unreachable()` | |
| Manual `static_cast<T&&>` in generic forwarding | `std::forward_like<decltype(x)>(y)` | |
| `std::function` when the callable must be copyable | `std::move_only_function` | **C++23**, not C++20 |
| `std::bind` with trailing arguments bound | `std::bind_back` | |
| `memcpy` or arithmetic for byte reversal | `std::byteswap(x)` | |
| `std::is_constant_evaluated()` in an `if` | `if consteval { ... }` | |
| `std::accumulate` / manual fold | `std::ranges::fold_left`, `fold_right`, `fold_left_first` | |
| `std::map` / `std::set` (node-based, cache-unfriendly) | `std::flat_map` / `std::flat_set` (sorted contiguous storage) | **not** drop-ins: insertion/erasure are linear and iterator-invalidation rules differ |
| Hand-rolled coroutine generator | `std::generator<T>` (lazy, coroutine-based) | |
| Raw pointer arithmetic for N-dimensional arrays | `std::mdspan` | `std::submdspan` is **C++26** |
| Stateless functor with boilerplate | `static operator()` / `static operator[]` | |
| `std::find` then reverse-iterate for the last match | `std::ranges::find_last` / `find_last_if` | |
| `std::shift_left` / `std::shift_right` | `std::ranges::shift_left` / `shift_right` | range overloads |
| `iota` into a pre-sized range | `std::ranges::iota(r, value)` | |
| Manual stack trace via `backtrace()` / `dladdr()` | `std::stacktrace::current()` | requires platform backtrace support in the toolchain |
| Hand-rolled overflow logic on a fixed-size buffer | *(no C++23 answer)* | `std::inplace_vector<T, N>` is **C++26**; for now use `std::array` + a size, or `std::vector` with `reserve` |
| `float` / `double` for ML half precision | `std::bfloat16_t` (and `std::float16_t` for IEEE half) | `<stdfloat>`; all of these types are **optional** in the standard — IEEE half is `float16_t`, not `bfloat16_t` |
| `__builtin_assume(p)` / `__builtin_unreachable()` | `[[assume(p)]]` | |
| `const&` / `&` / `&&` overload sets + forwarding boilerplate | Explicit object parameter ("deducing `this`"): `int f(this Self&& self)` | collapses the whole overload set into one function |
| `std::equal(p.begin(), p.end(), r.begin())` and friends | `std::ranges::starts_with` / `ends_with` / `contains_subrange` | |
| Nested loops for the cartesian product | `views::cartesian_product` | |
| Two-range `transform` with a lambda tuple | `views::zip_transform(f, r1, r2)` | |
| Manual look-behind / overlapping windows | `views::adjacent<N>` / `views::adjacent_transform<N>(f)` | |
| `views::cycle`-style repetition workarounds | `views::repeat(value, n)` | |
| `views::as_const` workarounds with `const_cast` | `views::as_const(r)` | |
| `p.release(); api(&p);` dance for out-parameters | `std::out_ptr(p)` / `std::inout_ptr(p)` | |
| `resize(n)` + `&s[0]` / `data()` hack for C APIs | `std::string::resize_and_overwrite(n, f)` | |
| `std::invoke` + `static_cast` on the result | `std::invoke_r<R>(f, args...)` | |
| Custom fixed-buffer `streambuf` / `<strstream>` | `<spanstream>` (`ispanstream` / `ospanstream` / `spanstream`) | |
| `__is_scoped_enum(T)` compiler builtin | `std::is_scoped_enum` | |
| `std::launder` + `memcpy` tricks for implicit-lifetime types | `std::start_lifetime_as` / `start_lifetime_as_array` | |
| Manual `operator<<` for ranges | Range formatting: `std::format("{}", v)` and `std::range_formatter` | |

---

## C++26 — not yet C++23 (keep out of the C++23 table)

These are frequently mislabelled as C++23. They are C++26 papers.

| Old way | New way |
|---|---|
| `std::vector` with a fixed maximum plus overflow bookkeeping | `std::inplace_vector<T, N>` (inline storage; the object itself may live anywhere) |
| Manual index arithmetic on an `mdspan` | `std::submdspan` |
| `std::map`/`std::set` or hand-rolled open addressing | `std::hive` |
| `optional<T>` + separate "empty but present" flag | `std::optional<T&>` |
| `std::thread` pools / `std::async` | `std::execution` (senders/receivers) |
| Intrinsics / vector extensions for SIMD loops | `std::simd` |
| `std::function<...>` for non-owning callables | `std::function_ref` / `std::copyable_function` |
| LAPACK/BLAS calls | `std::linalg` |
| `assert` / `[[assume]]` for preconditions | Contracts |

---
