import sys
import os

class Logger():
    def __init__(self, logfile):
        self.logfile = logfile
        self.mydict = {}
    
    def log(self, my_item, my_value):
        if my_item not in self.mydict:
            self.mydict[my_item] = my_value
        else:
            self.mydict[my_item] += my_value

    def logMaleHealthy(self, value):
        self.log('Healthy male' , value)
    
    def logFemaleHealthy(self, value):
        self.log('Healthy Female', value)

    def logMaleAffected(self, value):
        self.log('Affected Male', value)

    def logFemaleAffected(self, value):
        self.log('Affected Female', value)
    
    def logTotalMale(self, value):
        self.log('Total Male', value)

    def logTotalFemale(self,value):
        self.log('Total Female', value)

    def logTotalCouple(self, value):
        self.log('Total Couple', value)

    def logMaleRecovered(self, value):
        self.log('Total Male Recovered', value)

    def logFemaleRecovered(self, value):
        self.log('Total Female Recovered', value)

    def printLog(self, world):
        with open(self.logfile, 'w') as f:
            f.write("Summary of the simulation\n")
            f.write("----------------------------------------------\n")
            f.write("Treatment involved: {}\n".format(world.parameters['choice_of_treatment']))
            f.write("Intervention involved: Use Condom: {}\n".format(world.parameters['use_condom']))
            f.write("Intervention involved: Notification of Partner: {}\n\n".format(world.parameters['notify_partner']))
            for key, value in self.mydict.items():
                f.write("{}: {}\n".format(key, value))

