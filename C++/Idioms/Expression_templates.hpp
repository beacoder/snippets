// Expression Templates
// Represent expressions as types so that chained operations (e.g. a + b + c)
// are evaluated in a single pass without intermediate temporary objects.
// Widely used in linear algebra libraries (Eigen, Blaze).

#include <cstddef>

// A vector wrapper that holds an expression, not actual data
template <class E>
class VecExpression
{
  public:
    double operator[](size_t i) const { return static_cast<const E&>(*this)[i]; }
    size_t size()               const { return static_cast<const E&>(*this).size(); }
};

// Concrete vector storing real data
class Vec : public VecExpression<Vec>
{
  public:
    explicit Vec(size_t n) : data_(n) {}

    double operator[](size_t i) const { return data_[i]; }
    double& operator[](size_t i)      { return data_[i]; }
    size_t size()               const { return data_.size(); }

  private:
    std::vector<double> data_;
};

// Expression node: sum of two vectors of any expression type
template <class L, class R>
class VecSum : public VecExpression<VecSum<L, R>>
{
  public:
    VecSum(const L& l, const R& r) : lhs_(l), rhs_(r) {}

    double operator[](size_t i) const { return lhs_[i] + rhs_[i]; }
    size_t size()               const { return lhs_.size(); }

  private:
    const L& lhs_;
    const R& rhs_;
};

// Operator+ returns an expression object, not a Vec — no temporary allocation
template <class L, class R>
VecSum<L, R> operator+(const VecExpression<L>& l, const VecExpression<R>& r)
{
    return VecSum<L, R>(static_cast<const L&>(l), static_cast<const R&>(r));
}

void foo()
{
    Vec a(3), b(3), c(3), d(3);

    // No intermediate Vec temporaries — single loop evaluation
    d = a + b + c;  // Conceptually: d[i] = a[i] + b[i] + c[i] for each i
}
