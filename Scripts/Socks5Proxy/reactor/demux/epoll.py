#!/usr/bin/env python

import select
from demux import Demux


class EpollDemux(Demux):

    def __init__(self):
        # epoll exits in linux, unix.
        self._epoll = select.epoll()

    def register_event(self, fd, event):
        """register event for monitoring."""

        self._epoll.register(fd, event)

    def unregister_event(self, fd, event):
        """unregister event for monitoring."""

        self._epoll.unregister(fd)

    def wait_for_ready(self, timeout=None):
        """waiting until file descriptors become "ready" for I/O operation."""

        events = self._epoll.poll(timeout)
        return [(fd, event) for fd, event in events]

    def close(self):
        """close this Demux."""

        self._epoll.close()

    pass
