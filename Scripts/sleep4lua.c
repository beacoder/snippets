/*
 * sleep() function for lua to use
 * gcc -shared -fPIC -o sleep4lua.so -I/usr/local/include -llua sleep4lua.c
 *
*/

#include <unistd.h>
#include <lua.h>
#include <lauxlib.h>
#include <lualib.h>

static int msleep_c(lua_State *L){
	long msecs = lua_tointeger(L, -1);
	usleep(1000*msecs);
	return 0;                  /* No items returned */
}

static int sleep_c(lua_State *L){
	long secs = lua_tointeger(L, -1);
	sleep(secs);
	return 0;                  /* No items returned */
}

/**
 * luaopen_sleep4lua must contain the shared library name "sleep4lua"
 * so that require("sleep4lua") will load sleep4lua.so
 */

/* Register both functions */
int luaopen_sleep4lua(lua_State *L){
	lua_register( L, "msleep", msleep_c);  
	lua_register(L, "sleep", sleep_c);
	return 0;
}
