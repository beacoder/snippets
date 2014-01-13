/** gcc compile command is :
 *
 * g++ -g -Wall -I/usr/include/boost -L/usr/lib multi-thread-test.cpp -lboost_thread -o test 
*/

#include "boost/shared_ptr.hpp"
#include <iostream>
#include "boost/bind.hpp"
#include "boost/thread.hpp"

using namespace std;

struct Shared_Obj {
            
    Shared_Obj() {
        std::cout << "Shared_Obj is constructed !" << std::endl;        
    }
    
    ~Shared_Obj() {
        std::cout << "Shared_Obj is destructed !" << std::endl;        
    }
};

typedef boost::shared_ptr<Shared_Obj> ResourceType;

void fun1 (ResourceType rs)
{
    std::cout << "fun1 is called !" << std::endl;
    std::cout << "ref_count is  " << rs.use_count() << std::endl;
}

void fun2 (ResourceType rs)
{
    std::cout << "fun2 is called !" << std::endl;
    std::cout << "ref_count is  " << rs.use_count() << std::endl;    
}

int main(int argc, char *argv[]) {

    ResourceType rs (new Shared_Obj());

    std::cout << "ref_count is  " << rs.use_count() << std::endl;    

    boost::function0<void> threadfunc1 = boost::bind(&fun1, rs);

    std::cout << "ref_count is  " << rs.use_count() << std::endl;
        
    boost::function0<void> threadfunc2 = boost::bind(&fun2, rs);

    std::cout << "ref_count is  " << rs.use_count() << std::endl;
        
    boost::thread t1(threadfunc1);
    boost::thread t2(threadfunc2);
    
    t1.join();
    t2.join();
    
    return 0;
}
