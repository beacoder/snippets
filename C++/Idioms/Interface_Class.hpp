// An interface class
class Shape
{
  public:
    virtual ~Shape();
    virtual void move_x(int x) = 0;
    virtual void move_y(int y) = 0;
    virtual void draw() = 0;

    // Factory Method
    static Shape *getShape(std::string choice);
};

Shape *Shape::getShape(std::string choice)
{
    if ("Line" == choice)
    {
        return new Line();
    }
    else if ("Curve" == choice)
    {
        return new Curve();
    }
    else
    {
        return NullObject();
    }
}


class Line : public Shape
{
  public:
    virtual ~Line();
    virtual void move_x(int x); // implements move_x
    virtual void move_y(int y); // implements move_y
    virtual void draw(); // implements draw

  private:
    point end_point_1, end_point_2;
};

class Curve : public Shape
{
  public:
    virtual ~Curve();
    virtual void move_x(int x); // implements move_x
    virtual void move_y(int y); // implements move_y
    virtual void draw(); // implements draw

  private:
    point  end_point_1, end_point_2;
    doulbe angle;
};


int main (void)
{
    using ShapePtr = std::shared_ptr<Shape>;

    std::vector<ShapePtr> vShapes;
    vShapes.push_back(std::make_shared(Shape::getShape("Line")));
    vShapes.push_back(std::make_shared(Shape::getShape("Curve")));

    std::for_each(vShapes.begin(), vShapes.end(), [](std::vector<ShapePtr>::iterator& iter) { iter->draw(); });
}
