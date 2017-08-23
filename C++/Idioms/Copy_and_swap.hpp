class String
{
public:
    String & operator=(const String& s)
    {
        if (this != &s)
        {
            String(s).swap(*this); //Copy-constructor and non-throwing swap
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
