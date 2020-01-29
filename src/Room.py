import sys
import random
import Event

all_rooms = {}

class OccupyEvent (Event.Event):
    def __init__(self, day, room):
        super().__init__(day)
        self.room = room
    
    def execute(self, world):
        sys.stderr.write('Executing OccupyEvent for Room \'{}\' on day {}\n'.format(self.room.id, world.day))
        pass


class Room:

    def __init__(self, cluster_num, room_num):
        self.id = '{}:{}'.format(cluster_num, room_num)
        self.room_num = room_num
        self.cluster_num = cluster_num
        self.residents = []
        all_rooms[self.id] = self

    def schedule_for_occupant(self, world):
        empty_date = world.day

        # A room will sit empty for a random number of days between 1 and 90
        event = OccupyEvent(world.day + random.randint(1, 90), self)
        world.add_event(event)

def CreateEmptyRooms(world):
    room_cluster_count = world.parameters['room_cluster_count']
    room_per_cluster_count = world.parameters['room_per_cluster_count']

    for cluster_num in range(room_cluster_count):
        for room_num in range(room_per_cluster_count):
            new_room = Room(cluster_num, room_num)
            new_room.schedule_for_occupant(world)

