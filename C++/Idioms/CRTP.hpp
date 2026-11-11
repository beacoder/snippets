// CRTP (Curiously Recurring Template Pattern)
// The derived class passes itself as a template argument to the base class.
// This enables static (compile-time) polymorphism with zero virtual dispatch overhead.

// Basic CRTP: base class injects common functionality into derived classes
template <class Derived>
class Equality
{
  public:
    bool operator==(const Derived& other) const
    {
        return static_cast<const Derived*>(this)->value() == other.value();
    }

    bool operator!=(const Derived& other) const
    {
        return !(*this == other);
    }
};

class IntValue : public Equality<IntValue>
{
  public:
    explicit IntValue(int v) : v_(v) {}
    int value() const { return v_; }

  private:
    int v_;
};

// CRTP for static polymorphism (alternative to virtual functions)
template <class Derived>
class ShapeBase
{
  public:
    void draw()
    {
        static_cast<Derived*>(this)->draw_impl();
    }

    double area() const
    {
        return static_cast<const Derived*>(this)->area_impl();
    }
};

class Circle : public ShapeBase<Circle>
{
  public:
    explicit Circle(double r) : radius_(r) {}

    void draw_impl()
    {
        // Draw circle
    }

    double area_impl() const
    {
        return 3.14159 * radius_ * radius_;
    }

  private:
    double radius_;
};

class Square : public ShapeBase<Square>
{
  public:
    explicit Square(double s) : side_(s) {}

    void draw_impl()
    {
        // Draw square
    }

    double area_impl() const
    {
        return side_ * side_;
    }

  private:
    double side_;
};

// CRTP mixin: compose multiple independent behaviours
template <class Derived>
class Printable
{
  public:
    void print() const
    {
        static_cast<const Derived*>(this)->print_impl();
    }
};

template <class Derived>
class Serializable
{
  public:
    std::string serialize() const
    {
        return static_cast<const Derived*>(this)->serialize_impl();
    }
};

// Multiple mixins via CRTP chain
class Widget : public Printable<Widget>, public Serializable<Widget>
{
  public:
    void print_impl() const
    {
        // Print widget
    }

    std::string serialize_impl() const
    {
        return "Widget";
    }
};

void foo()
{
    IntValue a(1), b(2);
    if (a != b) { /* ... */ }

    Circle c(5.0);
    Square s(4.0);
    c.draw();
    s.draw();

    Widget w;
    w.print();
    w.serialize();
}
