// Type Erasure
// Store heterogeneous objects behind a uniform interface without exposing
// their concrete types or requiring a common base class.
// std::function and std::any are built on this idiom.

// A type-erased object wrapper — similar to std::function but for a custom interface
class Drawable
{
  public:
    // Construct from any type that has a draw() method
    template <class T>
    Drawable(T obj) : self_(std::make_unique<Model<T>>(std::move(obj))) {}

    Drawable(const Drawable& other) : self_(other.self_->clone()) {}
    Drawable(Drawable&&) noexcept = default;

    Drawable& operator=(const Drawable& other)
    {
        Drawable tmp(other);
        self_ = std::move(tmp.self_);
        return *this;
    }
    Drawable& operator=(Drawable&&) noexcept = default;

    void draw() const { self_->draw(); }

  private:
    struct Concept
    {
        virtual ~Concept() = default;
        virtual void draw() const = 0;
        virtual std::unique_ptr<Concept> clone() const = 0;
    };

    template <class T>
    struct Model : Concept
    {
        explicit Model(T obj) : data_(std::move(obj)) {}

        void draw() const override { data_.draw(); }

        std::unique_ptr<Concept> clone() const override
        {
            return std::make_unique<Model>(data_);
        }

        T data_;
    };

    std::unique_ptr<Concept> self_;
};

// Example types — no common base class needed
class Circle
{
  public:
    void draw() const { /* draw circle */ }
};

class Square
{
  public:
    void draw() const { /* draw square */ }
};

void foo()
{
    std::vector<Drawable> shapes;
    shapes.emplace_back(Circle{});
    shapes.emplace_back(Square{});

    for (const auto& s : shapes)
        s.draw();
}
