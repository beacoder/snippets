class String
{
public:
    // These two will do a member-wise move from the source object (rvalue) to the destination object.
    String(String&& s)             = default;
    String & operator=(String&& s) = default; // Don't use this when you have manually allocated resources.
                                              // OK to use when you have smart pointers or containers from stl.

    String(const String& s) : str(s.str) {}

     // When you don't have swap defined
    String & operator=(const String& s)
    {
        if (this != &s)
        {
            *this = String(s); // Copy-constructor and member-wise move
        }
      
        // Need to make sure old resources are properly released by move-assignment operator
        return *this;
    }

    // When you have swap defined
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
