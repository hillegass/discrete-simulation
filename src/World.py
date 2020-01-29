import heapq as q
import Room
import sys

class World:

    def __init__(self, params, log):
        self.parameters = params
        self.log = log
        self.day = 0

        # Managed by heap methods: heappush, etc.
        self.queue = []
        self.rooms = Room.CreateEmptyRooms(self)

    def add_event(self, event):
        q.heappush(self.queue, event)

    def has_events(self):
        return len(self.queue) > 0

    # Update the day (may need to update world state)
    def update_for_day(self, new_day):
        sys.stderr.write('Starting day {}\n'.format(new_day))
        self.day = new_day

    def process(self):
        next_event = q.heappop(self.queue)
        if self.day < next_event.day:
            self.update_for_day(next_event.day)

        next_event.execute(self)
    