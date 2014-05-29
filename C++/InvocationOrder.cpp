/*
 * check the invocation order of constructor, destruct-or.
 *
 * gcc compile command is :
 * g++ -g -Wall InvocationOrder.cpp -o InvocationOrder
 *
 */

#include <iostream>

using namespace std;

class BaseMember {
 public:
  BaseMember() {
    std::cout << "BaseMember is constructed !" << std::endl << std::endl;
  }

  ~BaseMember() {
    std::cout << "BaseMember is destructed !" << std::endl << std::endl;
  }
};

class Base {
 public:
  Base() {
    std::cout << "Base is constructed !" << std::endl << std::endl;
  }

  ~Base() {
    std::cout << "Base is destructed !" << std::endl << std::endl;
  }

  BaseMember mBaseMember;
};

class Member {
 public:
  Member() {
    std::cout << "Member is constructed !" << std::endl << std::endl;
  }

  ~Member() {
    std::cout << "Member is destructed !" << std::endl << std::endl;
  }
};

class Child : public Base {
 public:
  Child() {
    std::cout << "Child is constructed !" << std::endl << std::endl;
  }

  ~Child() {
    std::cout << "Child is destructed !" << std::endl << std::endl;
  }

  Member mMember;
};

int main(int argc, char *argv[]) {

  Child child;

  return 0;
}
