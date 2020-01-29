class Event:
    def __init__(self, day):
        self.day = day
    
    def __lt__(self, other):
        return self.day < other.day

    def execute(self, world):
        sys.stderr.write('*** Error: Override execute in {} ***'.format(self))
        pass
