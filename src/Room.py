import sys
import random
import Event

all_rooms = {}


class OccupyEvent (Event.Event):
    def __init__(self, day, female, male, room):
        super(OccupyEvent, self).__init__(day)
        self.room = room
        self.female = female  # female number
        self.male = male  # male number

    def execute(self, world):
        if self.room.id in world.rooms:

            world.rooms[self.room.id].female += self.female
            world.rooms[self.room.id].male += self.male
            world.rooms[self.room.id].healthy = self.female + self.male
            sys.stderr.write('Executing OccupyEvent for Room \'{}\' with {} female and {} male on day {}\n'.format(
                self.room.id, self.female, self.male, world.day))

        if world.rooms[self.room.id].female > 0 and world.rooms[self.room.id].male > 0:
            event = SexualEvent(world.day + random.randint(1, 90), self.room)
            world.add_event(event)


class SexualEvent (Event.Event):
    def __init__(self, day, room):
        super(SexualEvent, self).__init__(day)
        self.room = room

    def execute(self, world):
        chance = random.uniform(0, 1)
        if chance > world.parameters['std_probabability']:
            totalhealthy = world.rooms[self.room.id].healthy
            number_of_case = random.randint(1, totalhealthy)
            world.rooms[self.room.id].healthy -= number_of_case
            world.rooms[self.room.id].affected += number_of_case
            sys.stderr.write('{} case of STD at room {}\n'.format(
                number_of_case, self.room.id))
        pass


class Room:
    def __init__(self, cluster_num, room_num):
        self.id = '{}:{}'.format(cluster_num, room_num)
        self.room_num = room_num
        self.cluster_num = cluster_num
        self.residents = []
        self.totalResidents = 0
        self.female = 0  # female population
        self.male = 0  # male population
        self.healthy = 0  # healthy population
        self.affected = 0  # affected population
        all_rooms[self.id] = self

    def schedule_for_occupant(self, world):
        #empty_date = world.day

        # A room will sit empty for a random number of days between 1 and 90, also random number of male and female
        event = OccupyEvent(world.day + random.randint(1, 90),
                            random.randint(1, 3), random.randint(1, 3), self)
        world.add_event(event)


def CreateEmptyRooms(world):
    """ Creating only empty rooms so the world has the whole map 
    """
    house = {}
    room_cluster_count = world.parameters['room_cluster_count']
    room_per_cluster_count = world.parameters['room_per_cluster_count']

    for cluster_num in range(room_cluster_count):
        for room_num in range(room_per_cluster_count):
            new_room = Room(cluster_num, room_num)
            if new_room.id not in house:
                house[new_room.id] = new_room

    return house


def InitRoom(world):
    for _, room in world.rooms.items():
        room.schedule_for_occupant(world)
