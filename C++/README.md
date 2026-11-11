C++17                                                                                                                                                                                                                           

                                                                                                               
 Old way                                           New way                                                     
 ───────────────────────────────────────────────────────────────────────────────────────────────────────────── 
 switch on type tag + dynamic_cast chains          std::variant + std::visit                                   
 Sentinel values (-1, nullptr, boost::optional)    std::optional<T>                                            
 const std::string& params, const char* constants  std::string_view                                            
 boost::any / void* + cast                         std::any                                                    
 auto it = m.emplace(k, v); bool ok = it.second;   Structured bindings: auto [it, inserted] = m.emplace(k, v); 
 if (init; cond) split into two statements         Init-statement if/switch                                    
 enable_if SFINAE for template branching           if constexpr                                                
 std::result_of<...>::type                         std::invoke_result_t<...>                                   
 boost::apply_tuple / manual std::get<I>           std::apply(f, tuple)                                        
 Nested namespace a { namespace b { ... } }        namespace a::b { ... }                                      
 std::lock(m1, m2) + std::unique_lock wrapper      std::scoped_lock(m1, m2)                                    
 Hand-rolled reader/writer lock                    std::shared_mutex + std::shared_lock                        
 static const with ODR headaches across TUs        Inline variables: inline constexpr int x = 42;              
 std::vector<T>::iterator explicit template args   CTAD: std::vector v{1, 2, 3};                               
 char* / uint8_t* for raw byte manipulation        std::byte                                                   
 boost::filesystem or POSIX opendir/stat           std::filesystem                                             
 std::min(std::max(x, lo), hi)                     std::clamp(x, lo, hi)                                       
 std::accumulate (sequential only)                 std::reduce (parallelizable)                                
 Compiler-specific __attribute__((unused)) etc.    [[nodiscard]], [[maybe_unused]], [[fallthrough]]            
 Custom allocator boilerplate                      std::pmr polymorphic memory resources                       
                                                                                                               

C++20                                                                                                                                                                                                                                         

                                                                                                                                                 
 Old way                                                              New way                                                                    
 ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────── 
 Iterator pairs (begin, end)                                          Ranges: r | views::filter(...)                                             
 enable_if / SFINAE tricks                                            Concepts: template<std::ranges::input_range R>                             
 Callback chains, hand-rolled state machines                          Coroutines: co_await, co_return                                            
 std::thread + manual join in destructor                              std::jthread (auto-join + stop_token)                                      
 std::function for move-only callables                                (C++23 std::move_only_function) — C++20 gives std::stop_token cancellation 
 Raw T* + size_t n function params                                    std::span<T>                                                               
 erase(v.begin(), std::remove_if(v.begin(), v.end(), pred), v.end())  std::erase_if(v, pred)                                                     
 Hand-written operator<, >, <=, >=, !=                                auto operator<=>(const T&) = default;                                      
 printf / snprintf / ostream << chaining                              std::format("x = {}", x)                                                   
 __FILE__ / __LINE__ macros                                           std::source_location::current()                                            
 memcpy type punning                                                  std::bit_cast<To>(from)                                                    
 Hand-rolled barrier with mutex + cv                                  std::barrier, std::latch, std::counting_semaphore                          
 Mutex around std::cout                                               std::osyncstream(std::cout)                                                
 s.find(x) != s.end() / m.find(k) != m.end()                          s.contains(x) / m.contains(k) (container members)                          
 static_cast<ptrdiff_t>(v.size())                                     std::ssize(v)                                                              
 Manual (a + b) / 2                                                   std::midpoint(a, b)                                                        
 Manual a + t * (b - a)                                               std::lerp(a, b, t)                                                         
 int arr[] = {1,2,3}; then copy to container                          std::to_array<int>({1, 2, 3})                                              
 #ifdef / compiler intrinsics for constexpr check                     std::is_constant_evaluated()                                               
 Hand-rolled ceil(log2(x)) / popcount                                 std::bit_ceil, std::bit_width, std::popcount, std::rotl, std::rotr         
 Unsafe signed/unsigned a < b comparisons                             std::cmp_less(a, b) etc.                                                   
 boost::date_time or C tm/time_t                                      <chrono> calendar + timezone library                                       
 #include headers (preprocessor, ODR issues)                          Modules: import std; (not yet widely adopted)                              
 constexpr where object itself need not be constexpr                  constinit (constant init, non-constexpr object)                            
 constexpr functions that can't be truly constexpr-only               consteval (must evaluate at compile time)                                  
 std::string::find(prefix) == 0                                       std::string::starts_with(prefix) / ends_with(suffix)                       
                                                                                                                                                 

C++23                                                                                                                                                                                                                                         

                                                                                                                          
 Old way                                                        New way                                                   
 ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────── 
 std::copy/transform into pre-sized container                   std::ranges::to<std::vector<T>>()                         
 std::find(r, x) != r.end()                                     std::ranges::contains(r, x)                               
 s.find(sub) != std::string::npos                               std::string::contains(sub)                                
 for (i += batch) hand-chunked loops                            std::views::chunk(n) / std::views::chunk_by(pred)         
 boost::join or manual separator insertion                      std::views::join_with(sep)                                
 Manual parallel iteration with index                           std::views::zip(r1, r2) / std::views::enumerate(r)        
 Manual sliding window loop                                     std::views::slide(n)                                      
 Manual step iteration (i += step)                              std::views::stride(n)                                     
 printf / std::format + manual << '\n'                          std::print("x = {}\n", x) / std::println("x = {}", x)     
 optional<T> + separate error code / exception                  std::expected<T, E>                                       
 if (opt) { auto x = f(*opt); } chains                          opt.and_then(f).or_else(g).transform(h) (monadic ops)     
 static_cast<std::underlying_type_t<E>>(e)                      std::to_underlying(e)                                     
 __builtin_unreachable() / abort()                              std::unreachable()                                        
 Manual static_cast<T&&> in generic forwarding                  std::forward_like<T>(x)                                   
 std::function (requires copyable callable)                     std::move_only_function                                   
 memcpy or arithmetic for byte reversal                         std::byteswap(x)                                          
 std::is_constant_evaluated() in if                             if consteval { ... }                                      
 std::accumulate / manual fold                                  std::ranges::fold_left, fold_right, fold_left_first       
 std::map / std::set (node-based, cache-unfriendly)             std::flat_map / std::flat_set (sorted contiguous storage) 
 Hand-rolled coroutine generator                                std::generator<T> (coroutine-based, lazy)                 
 Raw pointer arithmetic for N-D arrays                          std::mdspan / std::submdspan                              
 std::function-style stateless functor with boilerplate         static operator() (stateless callables)                   
 std::find then reverse iterate for last match                  std::ranges::find_last / find_last_if                     
 std::shift_left / shift_right (C++20 algorithms)               std::ranges::shift_left / shift_right (range overloads)   
 std::stacktrace-less manual backtrace (backtrace(), dladdr())  std::stacktrace                                           
 std::vector with fixed max + overflow logic                    std::inplace_vector<T, N> (stack-allocated, no heap)      
 float / double for ML half-precision                           std::bfloat16_t
