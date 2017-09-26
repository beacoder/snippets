#!/usr/bin/env python

"""
Event handler interface.
Implement this interface to handle events dispatched from Reactor.
"""


class EventHandler(object):

    def __init__(self):
        pass

    def handle_input(self, sock, fd):
        """handle input event."""

        pass

    def handle_output(self, sock, fd):
        """handle output event."""

        pass

    def handle_exception(self, sock, fd):
        """handle exception event."""

        pass

    def handle_timeout(self, timeout=None):
        """handle timeout event."""

        pass

    def handle_close(self):
        """handle close event."""

        pass

    pass
