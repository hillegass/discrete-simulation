import sys
import random
import Event

class DeathEvent (Event.Event):
    def __init__(self, day, person):
        super().__init__(day)
        self.person = person
    
    def execute(self, world):
        room = self.person.room
        age = round((world.day - self.person.birthday) / 365)
        sys.stderr.write('Death in Room {} at age {}\n'.format(room.id, age))
        if self.person.is_male:
            room.maleResidents.remove(self.person)
        else:
            room.femaleResidents.remove(self.person)

        # Is the room empty now?
        if len(room.maleResidents) + len(room.femaleResidents) == 0:
            room.schedule_for_occupant(world)


class Person:
    
    def __init__(self, is_male, room):
        self.is_male = is_male
        self.birthday = 0
        self.age = 0
        self.risktype = ''
        self.is_infected = False
        self.is_symptomatic = False
        self.room = room
        if is_male:
            room.maleResidents.append(self)
        else:
            room.femaleResidents.append(self)

    def __repr__(self):
        if (self.is_male):
            return 'Male'
        else:
            return 'Female'

    def set_random_birthday(self, world):
        today = world.day
        mean = world.parameters['mean_age_new_resident']
        sd = world.parameters['sd_age_new_resident']
        self.birthday = today - round(random.gauss(mean, sd))
        self.age = round((today - self.birthday)/365)

    def reverse_birthday(self, world):
        today = world.day
        self.birthday = today - self.age * 365

    def schedule_for_death(self, world):
        if self.is_male:
            max_age = world.parameters['max_age_male_resident']
        else:
            max_age = world.parameters['max_age_female_resident']

        age_today = world.day - self.birthday
        max_life_left = max_age - age_today
        deathday = world.day + round(random.random() * max_life_left)
        deathevent = DeathEvent(deathday, self)
        self.death_handle = world.add_event(deathevent)
        
