class String
{
public:
    // These two will do a **member-wise move** from the source object (rvalue) to the destination object.
    String(String&& s)             = default;
    String & operator=(String&& s) = default;

    String(const String& s) : str(s.str) {}

    String & operator=(const String& s)
    {
        if (this != &s)
        {
            *this = String(s); // Do **member-wise move**
        }
      
        // Old resources are released after **member-wise move**
        return *this;
    }

    String & operator=(const String& s)
    {
        if (this != &s)
        {
            String(s).swap(*this); // Copy-constructor and non-throwing swap
        }
      
        // Old resources are released with the destruction of the temporary above
        return *this;
    }

    void swap(String& s) noexcept // Also see non-throwing swap idiom
    {
        std::swap(str, s.str);
    }

private:
    char * str;
};
