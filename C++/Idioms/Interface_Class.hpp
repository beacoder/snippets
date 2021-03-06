// An interface class
class IShape
{
  public:
    virtual ~IShape()          = default;
    virtual void move_x(int x) = 0;
    virtual void move_y(int y) = 0;
    virtual void draw() = 0;

    // Factory Method
    static IShape *getShape(std::string choice);
};

IShape *IShape::getShape(std::string choice)
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

class Line : public IShape
{
  public:
    virtual ~Line();
    
  private:
    virtual void move_x(int x); // implements move_x
    virtual void move_y(int y); // implements move_y
    virtual void draw();        // implements draw

  private:
    point end_point_1, end_point_2;
};

class Curve : public IShape
{
  public:
    virtual ~Curve();

  private:
    virtual void move_x(int x); // implements move_x
    virtual void move_y(int y); // implements move_y
    virtual void draw();        // implements draw

  private:
    point  end_point_1, end_point_2;
    doulbe angle;
};


int main (void)
{
  using ShapePtr = std::unique_ptr<IShape>;

  std::vector<ShapePtr> vShapes;
  vShapes.emplace_back(std::make_unique(Shape::getShape("Line")));   // favor emplace_back over push_back
  vShapes.emplace_back(std::make_unique(Shape::getShape("Curve")));  // favor emplace_back over push_back
  
  auto drawer = [&vShapes]()
  { 
    for (const auto& shape : vShapes)
    {
      shape->drawer();
    }
  };
    
  drawer();
}
