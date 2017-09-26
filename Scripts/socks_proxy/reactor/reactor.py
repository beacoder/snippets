#!/usr/bin/env python

"""
Handles registering and unregistering of event handlers.
Dispatches events to their associated event handlers.
"""


from __future__ import division, print_function, with_statement # absolute_import,
import os
import time
import socket
import select
import errno
import logging


# check timeouts every TIMEOUT_PRECISION seconds
TIMEOUT_PRECISION = 10


# from shadowsocks
class Reactor(object):

    def __init__(self, demux=None):
        if demux is None:
            if hasattr(select, 'epoll'):
                from demux.epoll_demux import EpollDemux
                self._demux = EpollDemux()
            elif hasattr(select, 'kqueue'):
                from demux.kqueue_demux import KqueueDemux
                self._demux = KqueueDemux()
            elif hasattr(select, 'select'):
                from demux.select_demux import SelectDemux
                self._demux = SelectDemux()
            else:
                raise Exception('can not find any available functions in select package')
        else:
            self._demux = demux

        self._handler_map = {}  # {fd => (sock, handler)}
        self._stopping    = False

    def register_handler(self, sock, event, handler):
        """register event_handler of particular event on a socket."""

        fd = sock.fileno()
        self._handler_map[fd] = (sock, handler)
        self._demux.register_event(fd, event)

    def unregister_handler(self, sock):
        """unregister event_handler on a handle."""

        fd = sock.fileno()
        del self._handler_map[fd]
        self._demux.unregister_event(fd)

    def handle_events(self):
        """start the event loop."""

        from demux.demux import POLL_IN, POLL_OUT, POLL_ERR
        events = []
        while not self._stopping:
            try:
                events = self._wait_for_ready(TIMEOUT_PRECISION)
            except Exception as e:
                if errno_from_exception(e) in (errno.EPIPE, errno.EINTR):
                    # EPIPE: Happens when the client closes the connection
                    # EINTR: Happens when received a signal
                    # handles them as soon as possible
                    # asap = True
                    # logging.debug('poll:%s', e)
                    pass
                else:
                    # logging.error('poll:%s', e)
                    import traceback
                    traceback.print_exc()
                    continue

            for sock, fd, event in events:
                handler = self._handler_map.get(fd, None)
                if handler is not None:
                    handler = handler[1]
                    try:
                        if event & POLL_IN:
                            handler.handle_input(sock, fd)
                        if event & POLL_OUT:
                            handler.handle_output(sock, fd)
                        if event & POLL_ERR:
                            handler.handle_exception(sock, fd)
                    except Exception as e:
                        # logging.error(e)
                        import traceback
                        traceback.print_exc()
        pass

    def _wait_for_ready(self, timeout=None):
        events = self._demux.wait_for_ready(timeout)
        return [(self._handler_map[fd][0], fd, event) for fd, event in events]

    def __del__(self):
        self._demux.close()

    pass


# from tornado
def errno_from_exception(e):
    """Provides the errno from an Exception object.

    There are cases that the errno attribute was not set so we pull
    the errno out of the args but if someone instatiates an Exception
    without any args you will get a tuple error. So this function
    abstracts all that behavior to give you a safe way to get the
    errno.
    """

    if hasattr(e, 'errno'):
        return e.errno
    elif e.args:
        return e.args[0]
    else:
        return None


# from tornado
def get_sock_error(sock):
    error_number = sock.getsockopt(socket.SOL_SOCKET, socket.SO_ERROR)
    return socket.error(error_number, os.strerror(error_number))
