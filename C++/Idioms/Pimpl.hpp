/* public.h */
class Book
{
public:
  Book();
  ~Book();
  void print();

private:
  class BookImpl;
  BookImpl* m_p;
}

/* private.h */
#include "public.h"
#include <iostream>

class Book::BookImpl
{
public:
  void print();

private:
  std::string  m_Contents;
  std::string  m_Title;
}

/* public.cpp */
Book::Book()
{
  m_p = new BookImpl();
}

Book::~Book()
{
  delete m_p;
}

void Book::print()
{
  m_p->print();
}

/* then BookImpl functions */

void Book::BookImpl::print()
{
  std::cout << "print from BookImpl" << std::endl;
}

/* invocation.cpp */
int main()
{
  Book *b = new Book();
  b->print();
  delete b;
}
