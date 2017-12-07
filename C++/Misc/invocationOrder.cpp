/*
 * check the invocation order of constructor, destruct-or.
 *
 * gcc compile command is :
 * g++ -g -Wall invocationOrder.cpp -o invocationOrder
 *
 */

#include <iostream>

using namespace std;

class BaseMember
{
 public:
  BaseMember()
  {
    std::cout << "BaseMember is constructed !" << std::endl << std::endl;
  }

  BaseMember(const BaseMember& rv)
  {
    if (this != &rv)
    {
      std::cout << "BaseMember is copy constructed !" << std::endl << std::endl;
    }
  }

  ~BaseMember()
  {
    std::cout << "BaseMember is destructed !" << std::endl << std::endl;
  }
};

class Base
{
 public:
  Base()
      : mPrintNumber(false)
  {
    std::cout << "Base is constructed !" << std::endl << std::endl;
  }

  explicit Base(int number)
      : mNumber(number),
        mPrintNumber(true)
  {
    std::cout << "Base " << mNumber
              << " is constructed !" << std::endl << std::endl;
  }

  Base(const Base& rv)
  {
    if (this != &rv)
    {
      std::cout << "Base is copy constructed !" << std::endl << std::endl;
    }
  }

  ~Base()
  {
    if (mPrintNumber)
    {
      std::cout << "Base " << mNumber
                << " is destructed !" << std::endl << std::endl;
    }
    else
    {
      std::cout << "Base is destructed !" << std::endl << std::endl;
    }
  }

  BaseMember mBaseMember;
  int mNumber;
  bool mPrintNumber;
};

class Member
{
 public:
  Member()
  {
    std::cout << "Member is constructed !" << std::endl << std::endl;
  }

  Member(const Member& rv)
  {
    if (this != &rv)
    {
      std::cout << "Member is copy constructed !" << std::endl << std::endl;
    }
  }

  ~Member()
  {
    std::cout << "Member is destructed !" << std::endl << std::endl;
  }
};

class Child : public Base
{
 public:
  Child()
      : mPrintNumber(false)
  {
    std::cout << "Child is constructed !" << std::endl << std::endl;
  }

  explicit Child(int number)
      : mNumber(number),
        mPrintNumber(true)
  {
    std::cout << "Child " << number
              << " is constructed !" << std::endl << std::endl;
  }

  Child(const Child& rv)
  {
    if (this != &rv)
    {
      std::cout << "Child is copy constructed !" << std::endl << std::endl;
    }
  }

  ~Child()
  {
    if (mPrintNumber)
    {
      std::cout << "Child " << mNumber
                << " is destructed !" << std::endl << std::endl;
    }
    else
    {
      std::cout << "Child is destructed !" << std::endl << std::endl;
    }
  }

  Member mMember;
  int mNumber;
  bool mPrintNumber;
};

int main(int argc, char *argv[])
{
  Child child;

  Child tmp0 = Child(child);
  Child tmp1 = Child(1);

  return 0;
}

// 1. 如果子类没有定义构造方法，则调用父类的无参数的构造方法。
// 2. 如果子类定义了构造方法，不论是无参数还是带参数，都会隐式的首先调用父类无参数的构造方法，然后执行自己的构造方法。
// 3. 如果父类只定义了有参数的构造方法，则子类必须显式的首先调用父类有参数的构造方法，然后执行自己的构造方法。
// 4. 子类析构时首先执行自己的析构方法，然后隐式的调用父类的析构方法。

// C++ Output:

// BaseMember is constructed !
// Base is constructed !
// Member is constructed !
// Child is constructed !
// BaseMember is constructed !
// Base is constructed !
// Member is constructed !
// Child is copy constructed !
// BaseMember is constructed !
// Base is constructed !
// Member is constructed !
// Child 1 is constructed !

// Child 1 is destructed !
// Member is destructed !
// Base is destructed !
// BaseMember is destructed !
// Child 0 is destructed !
// Member is destructed !
// Base is destructed !
// BaseMember is destructed !
// Child is destructed !
// Member is destructed !
// Base is destructed !
// BaseMember is destructed !
