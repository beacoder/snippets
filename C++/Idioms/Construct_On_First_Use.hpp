// Construct on first use using dynamic allocation
struct Foo {
  Foo () {
    bar().f ();
  }
 Bar & bar () {
    static Bar *b = new Bar ();
    return *b;
 }
};

// If the object has a destructor with non-trivial semantics, 
// local static object is used instead of dynamic allocation as given below.
// Construct on first use using local static
struct Foo {
  Foo () {
    bar().f ();
  }
 Bar & bar () {
    static Bar b;
    return b;
 }
};
