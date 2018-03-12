#!/usr/bin/env python

import select
from collections import defaultdict
from demux import *


class KqueueDemux(Demux):

    MAX_EVENTS = 1024

    def __init__(self):
        # epoll exits in BSD, MacOS.
        self._kqueue = select.kqueue()
        self._fds    = {}

    def register_event(self, fd, event):
        """register event for monitoring. """

        events = []
        if event & POLL_IN:
            events.append(select.kevent(fd, select.KQ_FILTER_READ, select.KQ_EV_ADD))
        if event & POLL_OUT:
            events.append(select.kevent(fd, select.KQ_FILTER_WRITE, select.KQ_EV_ADD))
        for e in events:
            self._kqueue.control([e], 0)

        self._fds[fd] = event

    def unregister_event(self, fd):
        """unregister event for monitoring. """

        events = []
        if event & POLL_IN:
            events.append(select.kevent(fd, select.KQ_FILTER_READ, select.KQ_EV_DELETE))
        if event & POLL_OUT:
            events.append(select.kevent(fd, select.KQ_FILTER_WRITE, select.KQ_EV_DELETE))
        for e in events:
            self._kqueue.control([e], 0)

        del self._fds[fd]

    def wait_for_ready(self, timeout=None):
        """waiting until file descriptors become "ready" for I/O operation. """

        if timeout < 0:
            timeout = None  # kqueue behaviour
        events = self._kqueue.control(None, KqueueDemux.MAX_EVENTS, timeout)
        results = defaultdict(lambda: POLL_NULL)
        for e in events:
            fd = e.ident
            if e.filter == select.KQ_FILTER_READ:
                results[fd] |= POLL_IN
            elif e.filter == select.KQ_FILTER_WRITE:
                results[fd] |= POLL_OUT
        return results.items()

    def close(self):
        """close this Demux."""

        self._kqueue.close()

    pass
