/*
 * pthread for lua to use
 * gcc -shared -fPIC -o thread4lua.so -I/usr/local/include -I/usr/include
 * -llua -pthread thread4lua.c
 *
 */

#include <pthread.h>
#include <lua.h>
#include <lauxlib.h>
#include <lualib.h>

static int thread_join_c(lua_State *L)
{
  /* -1 refers to the element at the stack top
   *  1 refers to the element at the stack bottom
   */
  pthread_t thread = lua_tonumber(L, -1);
  void* status;
  if (pthread_join(thread, &status))
  {
    lua_pushnumber(L, (long)status);
  }
  return 1;                  /* number of results to be returned  */
}

static int thread_create_c(lua_State *L)
{
  /* -1 refers to the element at the stack top
   *  1 refers to the element at the stack bottom
   */
  pthread_t thread;  
  lua_CFunction proc = lua_tocfunction(L, 1);
  int arg  = lua_tonumber(L, 2);  
  if (pthread_create(&thread, NULL, (void *(*) (void *))proc, &arg))
  {
    lua_pushnumber(L, thread);
  }
  return 1;                  /* number of results to be returned  */
}

/**
 * luaopen_thread4lua must contain the shared library name "thread4lua"
 * so that require("thread4lua") will load thread4lua.so
 */

/* Register both functions */
int luaopen_thread4lua(lua_State *L)
{
  lua_register(L, "thread_create", thread_create_c);  
  lua_register(L, "thread_join", thread_join_c);
  return 0;
}
