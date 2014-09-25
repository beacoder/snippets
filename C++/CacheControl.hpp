/*
 * provide a simple cache utility.
 *
 * gcc compile command is :
 * 
 *
 */
 
#include <map>
#include <stdexcept>
#include <sstream>
#include <boost/thread/mutex.hpp>

using std::endl;
/**
 * Cache
 */
template<class T, class KeyT>
class InstrumentCache 
{
public:
  static InstrumentCache<T, KeyT> *getCache(const KeyT &tag);
  static void releaseCache();
  static void releaseCache(const KeyT &tag);

  void cache(int site, const T &data);

  T& retrieve(int site) const;

  virtual ~InstrumentCache();

private:
  typedef InstrumentCache<T, KeyT> CacheType;
  typedef std::map<KeyT, InstrumentCache<T, KeyT>* > CacheReposity;
  typedef std::map<int, T> CacheMap;

  InstrumentCache();

  CacheMap m_data;

  static CacheReposity m_cache_map;

  // concurrency
  static boost::mutex mGuard;
};

template<class T, class KeyT>
std::map<KeyT, InstrumentCache<T, KeyT>* > InstrumentCache<T, KeyT>::m_cache_map;

template<class T, class KeyT>
boost::mutex InstrumentCache<T, KeyT>::mGuard;

template<class T, class KeyT>
InstrumentCache<T, KeyT>::InstrumentCache()
{
}

template<class T, class KeyT>
InstrumentCache<T, KeyT> *InstrumentCache<T, KeyT>::getCache(const KeyT &tag)
{
  boost::mutex::scoped_lock lock(mGuard);

  CacheType *pCache = NULL;

  typename CacheReposity::iterator it = m_cache_map.find(tag);;
  if (it == m_cache_map.end())
  {
    pCache = new CacheType();
    m_cache_map[tag] = pCache;
  }
  else
  {
    pCache = it->second;
  }
  
  return pCache;
}

template<class T, class KeyT>
void InstrumentCache<T, KeyT>::releaseCache()
{
  boost::mutex::scoped_lock lock(mGuard);

  for (typename CacheReposity::iterator it = m_cache_map.begin();
       it != m_cache_map.end(); ++it)
  {
    CacheType *pCache = it->second;
    delete pCache;
  }

  m_cache_map.clear();
}

template<class T, class KeyT>
void InstrumentCache<T, KeyT>::releaseCache(const KeyT &tag)
{
  boost::mutex::scoped_lock lock(mGuard);

  typename CacheReposity::iterator it = m_cache_map.find(tag);
  if (it != m_cache_map.end())
  {
    CacheType *pCache = it->second;
    delete pCache;
    m_cache_map.erase(it);
  }
}

template<class T, class KeyT>
void InstrumentCache<T, KeyT>::cache(int site, const T &data)
{
  boost::mutex::scoped_lock lock(mGuard);
  
  m_data[site] = data;
}

template<class T, class KeyT>
T& InstrumentCache<T, KeyT>::retrieve(int site) const
{
  boost::mutex::scoped_lock lock(mGuard);

  typename CacheMap::const_iterator it = m_data.find(site);
  if (it == m_data.end())
  {
    std::stringstream errstream;
    errstream << "Error: fail to retrieve to cache of site " << site << "." << endl
              << __PRETTY_FUNCTION__ << endl;
    throw std::runtime_error(errstream.str());
  }
  
  return const_cast<T&>(it->second);
}

template<class T, class KeyT>
InstrumentCache<T, KeyT>::~InstrumentCache()
{
  m_data.clear();
}

/**
 * Partial Specialization for Pointer Type
 */
template<class T, class KeyT>
class InstrumentCache <T*, KeyT>
{  
public:
  static InstrumentCache<T*, KeyT> *getCache(const KeyT &tag);    
  static void releaseCache();  
  static void releaseCache(const KeyT &tag);  

  void cache(int site, T *data);
  
  T* retrieve(int site) const;  

  virtual ~InstrumentCache();  

private:
  typedef InstrumentCache<T*, KeyT> CacheType;
  typedef std::map<KeyT, InstrumentCache<T*, KeyT>* > CacheReposity;
  typedef std::map<int, T*> CacheMap;

  InstrumentCache();  

  CacheMap m_data;

  static CacheReposity m_cache_map;

  // concurrency
  static boost::mutex mGuard;
};

template<class T, class KeyT>
std::map<KeyT, InstrumentCache<T*, KeyT>* > InstrumentCache<T*, KeyT>::m_cache_map;

template<class T, class KeyT>
boost::mutex InstrumentCache<T*, KeyT>::mGuard;

template<class T, class KeyT>
InstrumentCache<T*, KeyT>::InstrumentCache()
{
}

template<class T, class KeyT>
InstrumentCache<T*, KeyT> *InstrumentCache<T*, KeyT>::getCache(const KeyT &tag)
{
  boost::mutex::scoped_lock lock(mGuard);

  CacheType *pCache = NULL;

  typename CacheReposity::iterator it = m_cache_map.find(tag);;
  if (it == m_cache_map.end())
  {
    pCache = new CacheType();
    m_cache_map[tag] = pCache;
  }
  else
  {
    pCache = it->second;
  }
  
  return pCache;
}

template<class T, class KeyT>
void InstrumentCache<T*, KeyT>::releaseCache()
{
  boost::mutex::scoped_lock lock(mGuard);

  for (typename CacheReposity::iterator it = m_cache_map.begin();
       it != m_cache_map.end(); ++it)
  {
    CacheType *pCache = it->second;
    delete pCache;
  }

  m_cache_map.clear();
}

template<class T, class KeyT>
void InstrumentCache<T*, KeyT>::releaseCache(const KeyT &tag)
{
  boost::mutex::scoped_lock lock(mGuard);

  typename CacheReposity::iterator it = m_cache_map.find(tag);
  if (it != m_cache_map.end())
  {
    CacheType *pCache = it->second;
    delete pCache;
    m_cache_map.erase(it);
  }
}

template<class T, class KeyT>
void InstrumentCache<T*, KeyT>::cache(int site, T *data)
{
  boost::mutex::scoped_lock lock(mGuard);
  
  typename CacheMap::iterator it = m_data.begin();
  if (it != m_data.end())
  {
    if (it->second != NULL)
    {
      delete it->second;
      it->second = NULL;
    }
  }

  m_data[site] = data;
}

template<class T, class KeyT>
T* InstrumentCache<T*, KeyT>::retrieve(int site) const
{
  boost::mutex::scoped_lock lock(mGuard);

  typename CacheMap::const_iterator it = m_data.find(site);
  if (it == m_data.end())
  {
    std::stringstream errstream;
    errstream << "Error: fail to retrieve to cache of site " << site << "." << endl
              << __PRETTY_FUNCTION__ << endl;
    throw std::runtime_error(errstream.str());
  }

  return it->second;
}

template<class T, class KeyT>
InstrumentCache<T*, KeyT>::~InstrumentCache()
{
  for (typename CacheMap::iterator it = m_data.begin();
       it != m_data.end(); ++it)
  {
    T *pData = it->second;
    delete pData;
  }
  m_data.clear();
}

// use case:
// typedef InstrumentCache<Object*, std::string> ObjectPtrCache;
// typedef InstrumentCache<Object, std::string> ObjectCache;
