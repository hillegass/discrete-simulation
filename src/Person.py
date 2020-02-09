import sys
import random
import Event
import numpy as np

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
        self.has_couple = 0
        self.risk = 0 # this may be just a probability for less than 65 age, or a beta distribution
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

    # 1 is couple, 0 is single, affecting the risk
    def set_couple_status(self, status):
        self.has_couple = status

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
    
    # allocate this person according to the risk
    def risk_allocation(self, world):
        risk = random.uniform(0,1)
        
        # if less than 65
        if self.age < 65:
            self.risk = world.parameters['std_probability']
        else:
            if self.has_couple:
                if self.age < 80:
                    self.risk = world.parameters['paired_std_65_79_HR']
                else:
                    self.risk = world.parameters['paired_std_80_95_LR']

            else:
                # casual partners with different risk
                # they belong to high risk
                if risk <= world.parameters['HR']:
                    if self.age < 80:
                        self.risk = world.parameters['casual_std_65_79_HR']
                    else:
                        self.risk = world.parameters['casual_std_65_79_LR']
                else: # they belong to low risk group
                    if self.age < 80:
                        self.risk = world.parameters['casual_std_65_79_HR']
                    else:
                        self.risk = world.parameters['casual_std_65_79_LR']

    # get the probability of affecting
    def is_affected_probability(self):
        if len(self.risk) == 1:
            return self.risk[0]
        else:
            distribution = self.risk[0]
            if distribution == 'beta':
                alpha = self.risk[1]
                beta = self.risk[2]
                return np.random.beta(alpha, beta)
            else:
                return 0.5
