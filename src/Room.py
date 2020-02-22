import sys
import random
import Event
import Person
import numpy as np

all_rooms = {}


class OccupyEvent (Event.Event):
    def __init__(self, day, room):
        super(OccupyEvent, self).__init__(day)
        self.room = room

    def execute(self, world):
        if self.room.id in world.rooms:
             # Does it go to a married couple?
            prob_new_room_for_married = world.parameters['prob_new_room_for_married']
            world.logger.log("healthy", 1)
            if random.uniform(0, 1) < prob_new_room_for_married:
                world.rooms[self.room.id].male += 1
                world.rooms[self.room.id].female += 1
                world.rooms[self.room.id].healthy += 2
                world.rooms[self.room.id].room_type = 1
                # Create male
                resident1 = Person.Person(True, self.room)
                resident1.set_random_birthday(world)
                # resident1.schedule_for_death(world)
                resident1.set_couple_status(1)
                resident1.risk_allocation(world)
                # Create female
                resident2 = Person.Person(False, self.room)
                # random number at from the partner between -5 and 5 age
                resident2.age = resident1.age + random.randrange(-5, 5)
                resident2.reverse_birthday(world)
                resident2.set_couple_status(1)
                resident2.risk_allocation(world)
                # resident2.schedule_for_death(world)
                sys.stderr.write('Executing OccupyEvent for Marriage couple Room \'{}\' with {} female and {} male on day {}\n'.format(
                    self.room.id, world.rooms[self.room.id].female, world.rooms[self.room.id].male, world.day))
            else:
                world.rooms[self.room.id].room_type = 0
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
                resident.set_couple_status(0)
                resident.risk_allocation(world)
                #sys.stderr.write('resident age {}\n'.format(resident.age))
                # resident.schedule_for_random_departure(world)
                # resident.schedule_for_death(world)

                sys.stderr.write('Executing OccupyEvent for Single Room \'{}\' with {} female and {} male on day {}\n'.format(
                    self.room.id, world.rooms[self.room.id].female, world.rooms[self.room.id].male,  world.day))

            if world.rooms[self.room.id].female > 0 and world.rooms[self.room.id].male > 0:
                event = SexualEvent(
                    world.day + random.randint(1, 90), self.room)
                world.add_event(event)


class TreatmentEvent (Event.Event):
    def __init__(self, day, room):
        super(TreatmentEvent, self).__init__(day)
        self.room = room

    def execute(self, world):
        old_case = world.rooms[self.room.id].affected
        treatment_choice = world.parameters['choice_of_treatment']
        if treatment_choice == 'antibiotics':
            recovery_param = world.parameters['antibiotics']
            male_recovery_chance = female_recovery_chance = np.random.beta(
                recovery_param[1], recovery_param[2])
        else:
            female_recovery_param = world.parameters['woman_nr']
            male_recovery_param = world.parameters['man_nr']
            male_recovery_chance = 1/(52*(1.13+0.5*np.random.beta(
                male_recovery_param[1], recovery_param[2])))
            female_recovery_chance = 1/(52*(1.13+0.5*np.random.beta(
                female_recovery_param[1], recovery_param[2])))

        femaleResident = world.rooms[self.room.id].femaleResidents
        maleResident = world.rooms[self.room.id].maleResidents

        chance_of_success = random.uniform(0, 1)

        for i in range(len(femaleResident)):
            femaleAffected = femaleResident[i].is_infected

            if femaleAffected and chance_of_success <= female_recovery_chance:
                world.rooms[self.room.id].healthy += 1
                world.rooms[self.room.id].affected -= 1
                femaleResident[i].is_infected = False

        for i in range(len(maleResident)):
            maleAffected = maleResident[i].is_infected

            if maleAffected and chance_of_success <= male_recovery_chance:
                world.rooms[self.room.id].healthy += 1
                world.rooms[self.room.id].affected -= 1
                maleResident[i].is_infected = False

        if old_case > 0:
            sys.stderr.write('{} affected of STD at room {} reduced to {} \n'.format(
                old_case, self.room.id, self.room.affected))
        pass


class SexualEvent (Event.Event):
    def __init__(self, day, room):
        super(SexualEvent, self).__init__(day)
        self.room = room

    def execute(self, world):
        chance = random.uniform(0, 1)
        femaleResident = world.rooms[self.room.id].femaleResidents
        maleResident = world.rooms[self.room.id].maleResidents
        number_of_case = 0

        notification_parameter = world.parameters['notification']
        chance_of_notification = np.random.beta(
            notification_parameter[1], notification_parameter[2])

        for i in range(len(femaleResident)):
            femaleRisk = femaleResident[i].is_affected_probability(world)
            # notified by partner, so not doing sexual event
            notificationByPartner = random.uniform(0, 1)
            if chance > femaleRisk and notificationByPartner > chance_of_notification:
                femaleResident[i].is_infected = True
                world.rooms[self.room.id].healthy -= 1
                world.rooms[self.room.id].affected += 1
                number_of_case += 1

                # put in treatment
                event = TreatmentEvent(
                    world.day + random.randint(1, 10), self.room)
                world.add_event(event)

        for i in range(len(maleResident)):
            notificationByPartner = random.uniform(0, 1)
            maleRisk = maleResident[i].is_affected_probability(world)
            if chance > maleRisk and notificationByPartner > chance_of_notification:
                maleResident[i].is_infected = True
                world.rooms[self.room.id].healthy -= 1
                world.rooms[self.room.id].affected += 1
                number_of_case += 1
                # put in treatment
                event = TreatmentEvent(
                    world.day + random.randint(1, 10), self.room)
                world.add_event(event)

        sys.stderr.write('{} case of STD at room {}\n'.format(
            number_of_case, self.room.id))
        pass


class Room:
    def __init__(self, cluster_num, room_num):
        self.id = '{}:{}'.format(cluster_num, room_num)
        self.room_num = room_num
        self.room_type = 0  # 0 is single, 1 is couple room
        self.cluster_num = cluster_num
        self.femaleResidents = []  # female resident list
        self.maleResidents = []  # male resident list
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

    # def schedule_for_treatment(self, world):
    #     event = TreatmentEvent(world.day, self)
    #     world.add_event(event)


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


# def InitTreatment(world):
#     for _, room in world.rooms.items():
#         room.schedule_for_treatment(world)
