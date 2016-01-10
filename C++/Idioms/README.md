Following is a list of most useful c++ idioms
@see http://en.wikibooks.org/wiki/More_C++_Idioms

0.Interface_Class         => Separating an interface of a class from its implementation
                             Invoke implementation of an abstraction/class using runtime polymorphism.

1.RAII                    => To guarantee release of resource(s) at the end of a scope
                             To provide basic exception safety guarantee

2.Pimpl                   => Pointer To Implementation

3.Construct_On_First_Use  => Ensure that an object is initialized before its first use, e.g: Singleton pattern

4.Checked_delete          => Increase safety of delete expression

5.Virtual_Constructor     => Creating an object or it's copy without knowing its concrete type

6.Copy-and-swap           => Create an exception safe implementation of overloaded assignment operator
