// Shrink-to-fit
// Release unused capacity from a container after it has grown and then shrunk.
// The swap trick works on any container, even those without shrink_to_fit().

#include <vector>
#include <string>

void foo()
{
    std::vector<int> v;

    // Grow to 1000 elements
    v.resize(1000);

    // Shrink to 10 — capacity is still ~1000
    v.resize(10);

    // Method 1: member function (C++11+, not guaranteed but widely supported)
    v.shrink_to_fit();

    // Method 2: swap trick — works on any container, even without shrink_to_fit()
    std::vector<int>(v).swap(v);
    // A temporary vector is constructed from v (copy with tight capacity),
    // then swapped with v. The temporary (now holding the old bloated buffer)
    // is destroyed at the end of the statement.

    // Same trick for string
    std::string s = "hello";
    s.reserve(1000);
    s.resize(5);
    std::string(s).swap(s);  // Capacity is now ~5
}
