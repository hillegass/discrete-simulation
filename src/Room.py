import sys
import random
import Event
import Person

all_rooms = {}


class OccupyEvent (Event.Event):
    def __init__(self, day, room):
        super(OccupyEvent, self).__init__(day)
        self.room = room

    def execute(self, world):
        if self.room.id in world.rooms:
             # Does it go to a married couple?
            prob_new_room_for_married = world.parameters['prob_new_room_for_married']
            if random.uniform(0, 1) < prob_new_room_for_married:
                world.rooms[self.room.id].male += 1
                world.rooms[self.room.id].female += 1
                world.rooms[self.room.id].healthy += 2
                # Create male
                resident1 = Person.Person(True, self.room)
                resident1.set_random_birthday(world)
                # departure_day = resident1.schedule_for_random_departure(world)
                resident1.schedule_for_death(world)
                # Create female
                resident2 = Person.Person(False, self.room)
                resident2.birthday = resident1.birthday
                # resident2.schedule_for_departure(world, departure_day)
                resident2.schedule_for_death(world)
                sys.stderr.write('Executing OccupyEvent for Marriage couple Room \'{}\' with {} female and {} male on day {}\n'.format(
                    self.room.id, world.rooms[self.room.id].female, world.rooms[self.room.id].male, world.day))
            else:
                # Is this a male?
                is_male = random.uniform(
                    0, 1) < world.parameters['prob_new_single_male']
                if is_male:
                    world.rooms[self.room.id].male += 1
                else:
                    world.rooms[self.room.id].female += 1
                world.rooms[self.room.id].healthy += 1
                resident = Person.Person(is_male, self.room)
                resident.set_random_birthday(world)
                # resident.schedule_for_random_departure(world)
                resident.schedule_for_death(world)

                sys.stderr.write('Executing OccupyEvent for Single Room \'{}\' with {} female and {} male on day {}\n'.format(
                    self.room.id, world.rooms[self.room.id].female, world.rooms[self.room.id].male, world.day))

            if world.rooms[self.room.id].female > 0 and world.rooms[self.room.id].male > 0:
                event = SexualEvent(
                    world.day + random.randint(1, 90), self.room)
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
        # empty_date = world.day

        # A room will sit empty for a random number of days between 1 and 90, also random number of male and female
        event = OccupyEvent(world.day + random.randint(1, 90), self)
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
