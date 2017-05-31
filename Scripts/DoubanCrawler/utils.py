"""Utilities facilities include encoding, stack, queue.

* encode_with_utf8  convert to unicode and encode with utf-8
* Stack             LIFO Container.
* Queue             FIFO Container.

"""

# public symbols
__all__ = ["encode_with_utf8", "decode_with_utf8", "Queue", "Stack"]

from collections import deque


################################################################################
### Rules for encoding
################################################################################
#1 always use unicode in application
#2 encode it with 'utf-8' only when writing to file/database/socket
#3 decode it with 'utf-8' when reading it back
################################################################################
def encode_with_utf8(in_string):
    "Convert string to utf-8 encoding."
    if isinstance(in_string, str):
        ret_string = u' '.join(in_string).encode('utf-8').strip()
    elif isinstance(in_string, unicode):
        ret_string = in_string.encode('utf-8')
    else:
        pass
    return ret_string

def decode_with_utf8(in_string):
    "Decode string with utf-8 encoding."

    ret_string = in_string.decode('utf-8')
    if isinstance(ret_string, str):
        ret_string = u' '.join(ret_string).strip()
    return ret_string


################################################################################
### _QueueAndStackBase
################################################################################
class _QueueAndStackBase(object):
    """Base class for Queue and Stack."""
    def __init__(self):
        self.items = deque()

    def isEmpty(self):
        return (len(self.items) == 0)

    def __iter__(self):
        return self

    def size(self):
        return len(self.items)


################################################################################
### Queue
################################################################################
class Queue(_QueueAndStackBase):
    """FIFO Container."""
    def next(self):
        try:
            return self.deque()
        except IndexError:
            raise StopIteration

    def enqueue(self, item):
        self.items.append(item)

    def deque(self):
        return self.items.popleft()


################################################################################
### Stack
################################################################################
class Stack(_QueueAndStackBase):
    """LIFO Container."""
    def next(self):
        try:
            return self.pop()
        except IndexError:
            raise StopIteration

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[len(self.items)-1]
