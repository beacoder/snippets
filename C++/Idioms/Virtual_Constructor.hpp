#include <memory>

class Employee
{
  public:
    using Ptr = std::shared_ptr<Employee>;

    virtual ~Employee ()        = default;      // Native support for polymorphic destruction.
    virtual Ptr create () const = 0;            // Virtual constructor (creation)
    virtual Ptr clone ()  const = 0;            // Virtual constructor (copying)
};

class Manager : public Employee                 // "is-a" relationship
{
  public:
    Manager () {}                               // Default constructor
    Manager (Manager const &) {}                // Copy constructor
    virtual ~Manager () {}

  private:
    Ptr create () const                         // Virtual constructor (creation)
    {
      return Ptr(new Manager());
    }
  
    Ptr clone () const                          // Virtual constructor (copying)
    {
      return Ptr(new Manager (*this));
    }
};
