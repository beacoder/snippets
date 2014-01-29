/*
 * call lua function in C
 * gcc -Wall -fPIC -I/usr/local/include -L/usr/local/lib -llua test_pcall.c -o test_pcall
 *
 */

#include <stdlib.h>     /* For function exit() */
#include <stdio.h>      /* For input/output */
#include <assert.h>     /* For assert() */

#include <lua.h>        /* Always include this when calling Lua */
#include <lauxlib.h>    /* Always include this when calling Lua */
#include <lualib.h>     /* Always include this when calling Lua */

// pcall4c.lua contents
// function f (x, y)
//      return (x^2 * math.sin(y))/(1 - x)
//    end

/* call a function `f' defined in Lua */
static double f(lua_State* L, double x, double y)
{
  double z;
    
  /* push functions and arguments */
  lua_getglobal(L, "f");  /* function to be called */
  lua_pushnumber(L, x);   /* push 1st argument */
  lua_pushnumber(L, y);   /* push 2nd argument */
    
  /* do the call (2 arguments, 1 result) */
  if (lua_pcall(L, 2, 1, 0) != 0)
    assert(0);  
        
  /* retrieve result */
  if (!lua_isnumber(L, -1))
    assert(0);  
  
  z = lua_tonumber(L, -1);
  lua_pop(L, 1);  /* pop returned value */
  
  return z;
}

int main(int argc, char *argv[])
{
  lua_State *L;

  /* Create Lua state variable */
  L = luaL_newstate();

  /* Load Lua libraries */
  luaL_openlibs(L);                           

  /* Load but don't run the Lua script */
  if (luaL_loadfile(L, "pcall4c.lua"))
    /* Error out if file can't be read */
    bail(L, "luaL_loadfile() failed");      

  /* Call lua function */ 
  f(L, 1.0, 2.0);

  /* Clean up, free the Lua state var */
  lua_close(L);                              

  return 0;  
}
