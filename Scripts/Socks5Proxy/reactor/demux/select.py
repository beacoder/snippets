#!/usr/bin/env python

import select
from demux import Demux
from collections import defaultdict


class SelectDemux(Demux):

    def __init__(self):
        self._r_list = set()
        self._w_list = set()
        self._x_list = set()

    def register_event(self, fd, event):
        """register event for monitoring."""

        if event & POLL_IN:
            self._r_list.add(fd)
        if event & POLL_OUT:
            self._w_list.add(fd)
        if event & POLL_ERR:
            self._x_list.add(fd)

    def unregister_event(self, fd, event):
        """unregister event for monitoring. """

        if event & POLL_IN:
            self._r_list.remove(fd)
        if event & POLL_OUT:
            self._w_list.remove(fd)
        if event & POLL_ERR:
            self._x_list.remove(fd)

    def wait_for_ready(self, timeout=None):
        """waiting until file descriptors become "ready" for I/O operation. """

        r, w, x = select.select(self._r_list, self._w_list, self._x_list, timeout)

        results = defaultdict(lambda: POLL_NULL)
        for p in [(r, POLL_IN), (w, POLL_OUT), (x, POLL_ERR)]:
            for fd in p[0]:
                results[fd] |= p[1]
        return results.items()

    def close(self):
        """close this Demux."""

        pass

    pass
