#!/usr/bin/env python

import select
from event_demux import EventDemux


class KqueueDemux(EventDemux):

    MAX_EVENTS = 1024

    def __init__(self):
        # epoll exits in BSD, MacOS.
        self._kqueue = select.kqueue()
        self._fds    = {}

    def register_event(self, fd, event):
        """register event for monitoring. """

        if event & POLL_IN:
            select.kevent(fd, select.KQ_FILTER_READ, select.KQ_EV_ADD)
        if event & POLL_OUT:
            select.kevent(fd, select.KQ_FILTER_WRITE, select.KQ_EV_ADD)

        self._fds[fd] = event
        self._kqueue.control([event], 0)

    def unregister_event(self, fd, event):
        """unregister event for monitoring. """

        if event & POLL_IN:
            select.kevent(fd, select.KQ_FILTER_READ, select.KQ_EV_DELETE)
        if event & POLL_OUT:
            select.kevent(fd, select.KQ_FILTER_WRITE, select.KQ_EV_DELETE)

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
        """close this EventDemux."""

        self._kqueue.close()

    pass
