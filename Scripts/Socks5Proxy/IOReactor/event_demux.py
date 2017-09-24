#!/usr/bin/env python

from abc import ABCMeta, abstractmethod


POLL_NULL = 0x00
POLL_IN   = 0x01
POLL_OUT  = 0x04
POLL_ERR  = 0x08
POLL_HUP  = 0x10
POLL_NVAL = 0x20


class EventDemux(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def register_event(self, fd, event):
        """register event for monitoring."""

        raise NotImplementedError("subclasses must override register_event()!")

    @abstractmethod
    def unregister_event(self, fd, event):
        """unregister event for monitoring."""

        raise NotImplementedError("subclasses must override unregister_event()!")


    @abstractmethod
    def wait_for_ready(self, timeout=None):
        """waiting until file descriptors become "ready" for I/O operation."""

        raise NotImplementedError("subclasses must override wait_for_ready()!")

    @abstractmethod
    def close(self):
        """stop this EventDemux."""

        raise NotImplementedError("subclasses must override close()!")

    pass
