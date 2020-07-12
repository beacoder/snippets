// check if boost is successfully installed
//
// clang compile command is:
// clang++ -std=c++17 -I /usr/local/boost-1.73.0/include -L /usr/local/boost-1.73.0/lib TestBoost.cpp -o TestBoost -lboost_system -lboost_filesystem
//
// install boost on MacOs:
// https://solarianprogrammer.com/2018/08/07/compiling-boost-gcc-clang-macos/

#include <boost/filesystem.hpp>
#include <iostream>

int main()
{
    // Get the current directory
    auto path = boost::filesystem::current_path();
    std::cout << path << "\n";

    // Print the content of the current directory
    for (auto &entry : boost::filesystem::directory_iterator(path))
    {
        std::cout << entry << std::endl;
    }

    return 0;
}
