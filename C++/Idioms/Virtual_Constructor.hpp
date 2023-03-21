#include <memory>

class Employee
{
public:
    using Ptr = std::unique_ptr<Employee>;

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
      return std::make_unique<Manager>();
    }
  
    Ptr clone () const                          // Virtual constructor (copying)
    {
      return std::make_unique<Manager>(*this);
    }
};

// Replace duplicated clone in all subclasses with CRTP hack.
// https://stackoverflow.com/questions/65916601/clone-derived-class-from-base-class-pointer
template <class Derived>
class CloneHelper: public Employee {
    Ptr create() const override
    {
        return std::make_unique<Derived>();
    }

    Ptr clone () const override
    {
      return std::make_unique<Derived>(*this);
    }
};

class Manager : public CloneHelper<Manager>
{
    ...
};
