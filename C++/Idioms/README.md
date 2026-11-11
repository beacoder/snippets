# Most Useful C++ Idioms

@see [More_C++_Idioms] (http://en.wikibooks.org/wiki/More_C++_Idioms)

#### Interface_class
```
Separate interface of class from its implementation, e.g: Strategy pattern
Invoke implementation of class using runtime polymorphism
Make unit testing easier
```
#### RAII
```
To guarantee release of resource(s) at the end of a scope
To provide basic exception safety guarantee
```
#### Pimpl
```
Hide implementation details of interface from clients, e.g: Bridge pattern
```
#### Construct_on_first_use
```
Ensure that an object is initialized before its first use, e.g: Singleton pattern
```
#### Virtual_constructor
```
Creating an object without knowing its concrete type
```
#### Non_throwing_swap
```
To implement an exception safe and efficient swap operation
To provide uniform interface to it to facilitate generic programming
```
#### Copy_and_swap
```
Create an exception safe implementation of overloaded assignment operator
```
#### Non_virtual_interface
```
Separate a class interface into two distinct interfaces:
Client interface: This is the public non-virtual interface
Subclass interface: This is the private interface, which can have any combination virtual and non-virtual methods
```
#### CRTP
```
Static (compile-time) polymorphism with zero virtual dispatch overhead
Inject common functionality into derived classes via template base class
Implement mixin composition
```
#### Type_erasure
```
Store heterogeneous objects behind a uniform interface without a common base class
Hide concrete types at ABI boundaries
Custom alternatives to std::function / std::any
```
#### Copy_on_write
```
Share data between multiple objects; copy only when an object needs to mutate
Efficient for read-heavy, write-rare scenarios
```
#### Expression_templates
```
Represent chained operations as types to avoid intermediate temporaries
Single-pass evaluation for a + b + c without allocating intermediate results
Widely used in linear algebra libraries (Eigen, Blaze)
```
#### Shrink_to_fit
```
Release unused capacity from a container after it has grown and then shrunk
The swap trick works on any container, even without shrink_to_fit()
```
