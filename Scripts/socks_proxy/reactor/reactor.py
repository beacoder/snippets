#!/usr/bin/env python

import select
from collections  import defaultdict


class Reactor(object):

    def __init__(self, demux=None):
        if demux is None:
            if hasattr(select, 'epoll'):
                from demux.epoll import EpollDemux
                self._demux = EpollDemux()
            elif hasattr(select, 'kqueue'):
                from demux.kqueue import KqueueDemux
                self._demux = KqueueDemux()
            elif hasattr(select, 'select'):
                from demux.select import SelectDemux
                self._demux = SelectDemux()
            else:
                raise Exception('can not find any available functions in select package')
        else:
            self._demux = demux

        self._handler_map = defaultdict(lambda: set())
        self._stopping    = False

    def register_handler(self, fd, handler, event):
        """register event_handler of particular event on a handle."""

        key      = (fd, event)
        handlers = self._handler_map[key]

        if not handler in handlers:
            handlers.add(handler)
            self._demux.register_event(fd, event)
        pass

    def unregister_handler(self, fd, handler, event):
        """unregister event_handler of particular event on a handle."""

        key      = (fd, event)
        handlers = self._handler_map[key]

        if handler in handlers:
            handlers.remove(handler)
            self._demux.unregister_event(fd, event)
        pass

    def handle_events(self, timeout=None):
        """start the event loop."""

        while not self._stopping:
            for (fd, events) in self._demux.wait_for_ready():
                if events & POLL_IN:
                    for handler in self._handler_map[(fd, POLL_IN)]:
                        handler.handle_input(fd)

                if events & POLL_OUT:
                    for handler in self._handler_map[(fd, POLL_OUT)]:
                        handler.handle_output(fd)

                if events & POLL_ERR:
                    for handler in self._handler_map[(fd, POLL_ERR)]:
                        handler.handle_exception(fd)
        pass

    def __del__(self):
        self._demux.close()

    pass
