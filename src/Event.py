import sys


class Event(object):

    def __init__(self, day):
        self.id = 0
        self.day = day

    def __lt__(self, other):
        return self.day < other.day

    def execute(self, world):
        sys.stderr.write('*** Error: Override execute in {} ***'.format(self))
        pass
