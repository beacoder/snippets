# Most Useful C++ Idioms

@see [More_C++_Idioms] (http://en.wikibooks.org/wiki/More_C++_Idioms)

#### Interface_Class
```
  Separating an interface of a class from its implementation
  Invoke implementation of an abstraction/class using runtime polymorphism.
```
#### RAII
```
To guarantee release of resource(s) at the end of a scope
To provide basic exception safety guarantee
```
#### Handle-Body/Pimpl
```
Changing private member variables of a class does not require recompiling classes that depend on it
The header file does not need to #include classes that are used 'by value' in private member variables
```
#### Construct_On_First_Use
```
Ensure that an object is initialized before its first use, e.g: Singleton pattern
```
#### Virtual_Constructor
```
Creating an object or it's copy without knowing its concrete type
```
#### Non-throwing_swap
```
To implement an exception safe and efficient swap operation.
To provide uniform interface to it to facilitate generic programming.
```
#### Copy-and-swap
```
Create an exception safe implementation of overloaded assignment operator
```
#### Checked_delete
```
Increase safety of delete expression
```
