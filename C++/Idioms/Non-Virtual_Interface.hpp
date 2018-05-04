class Base {
private:
    ReaderWriterLock lock_;
    SomeComplexDataType data_;
public:
    void read_from( std::istream & i)  { // Note non-virtual
      lock_.acquire();
      assert(data_.check_invariants()); // must be true

      read_from_impl(i);

      assert(data_.check_invariants()); // must be true
      lock_.release();
    }
    void write_to( std::ostream & o) const { // Note non-virtual
      lock_.acquire();
      write_to_impl(o);
      lock_.release();
    }
    virtual ~Base() {}  // Virtual because Base is a polymorphic base class.
private:
    virtual void read_from_impl( std::istream & ) = 0;
    virtual void write_to_impl( std::ostream & ) const = 0;
};
class XMLReaderWriter : public Base {
private:
    virtual void read_from_impl (std::istream &) {
      // Read XML.
    }
    virtual void write_to_impl (std::ostream &) const {
      // Write XML.
    }
};
class TextReaderWriter : public Base {
private:
    virtual void read_from_impl (std::istream &) {}
    virtual void write_to_impl (std::ostream &) const {}
};
