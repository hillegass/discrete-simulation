import heapq as q
import Room
import sys

class World:

    def __init__(self, params, log):

        # All the parameters for this execution of the simulation
        self.parameters = params

        # A file to log important events to
        self.log = log

        # The current day
        self.day = 0

        # Managed by heap methods: heappush, etc.
        self.queue = []

        # To loop up events for removal
        self.event_index = {}

        # To create unique event handles for possible removal
        self.next_event_id = 1

        # Make empty rooms
        self.rooms = Room.CreateEmptyRooms(self)

    # Adds event to queue and returns handle for removal
    def add_event(self, event):
        eid = self.next_event_id
        event.id = eid
        self.next_event_id = self.next_event_id + 1
        q.heappush(self.queue, event)
        self.event_index[eid] = event
        return eid

    # Takes event handle
    def remove_event(self, eid):
        if eid in self.event_index:
            event = self.event_index[eid]
            self.queue.remove(event)
            del self.event_index[eid]

    # Are there more events to execute?
    def has_events(self):
        return len(self.queue) > 0

    # Update the day (may need to update world state)
    def update_for_day(self, new_day):
        sys.stderr.write('Starting day {}\n'.format(new_day))
        self.day = new_day

    # Pop the next event off the priority queue and execute it
    def process(self):
        next_event = q.heappop(self.queue)
        eid = next_event.id
        del self.event_index[eid]

        if self.day < next_event.day:
            self.update_for_day(next_event.day)

        next_event.execute(self)
    