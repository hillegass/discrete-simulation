import sys
import random
import Event
import Person
import utility as u

all_rooms = {}

class OccupyEvent (Event.Event):
    def __init__(self, day, room):
        super().__init__(day)
        self.room = room
    
    def execute(self, world):
        
        # Does it go to a married couple?
        prob_new_room_for_married = world.parameters['prob_new_room_for_married']
        if random.uniform(0,1) < prob_new_room_for_married:
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

        else:
            # Is this a male?
            is_male = random.uniform(0,1) < world.parameters['prob_new_single_male']
            resident = Person.Person(is_male, self.room)
            resident.set_random_birthday(world)
            # resident.schedule_for_random_departure(world)
            resident.schedule_for_death(world)

        sys.stderr.write('New residents: {} for Room \'{}\' on day {}\n'.format(self.room.residents, self.room.id, u.str_for_day(world.day)))
        



class Room:

    def __init__(self, cluster_num, room_num):
        self.id = '{}-{}'.format(cluster_num, room_num)
        self.room_num = room_num
        self.cluster_num = cluster_num
        self.residents = []
        all_rooms[self.id] = self

    def schedule_for_occupant(self, world):
        empty_date = world.day
        max_days_room_empty = world.parameters['max_days_room_empty']

        # A room will sit empty for a random number of days between 1 and max_days_room_empty
        event = OccupyEvent(world.day + random.randint(1, max_days_room_empty), self)
        world.add_event(event)

def CreateEmptyRooms(world):
    room_cluster_count = world.parameters['room_cluster_count']
    room_per_cluster_count = world.parameters['room_per_cluster_count']

    for cluster_num in range(room_cluster_count):
        for room_num in range(room_per_cluster_count):
            new_room = Room(cluster_num, room_num)
            new_room.schedule_for_occupant(world)

