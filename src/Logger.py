import sys
import os

class Logger():
    def __init__(self, logfile):
        self.logfile = logfile
        self.keys = ['Healthy male', 'Healthy Female', 'Affected Male','Affected Female', 'Total Male', 'Total Female', 'Total Couple', 'Total Male Recovered', 'Total Female Recovered']
        self.mydict = {'Healthy male':0, 'Healthy Female':0, 'Affected Male':0,'Affected Female':0, 'Total Male':0, 'Total Female':0, 'Total Couple':0, 'Total Male Recovered':0, 'Total Female Recovered':0}
    
    def log(self, my_item, my_value):
        if my_item not in self.mydict:
            self.mydict[my_item] = my_value
        else:
            self.mydict[my_item] += my_value

    def clear(self):
        self.mydict = {'Healthy male':0, 'Healthy Female':0, 'Affected Male':0,'Affected Female':0, 'Total Male':0, 'Total Female':0, 'Total Couple':0, 'Total Male Recovered':0, 'Total Female Recovered':0}
    

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

    def printSimulationDetail(self, world):
        with open(self.logfile, 'w') as f:
            f.write("Summary of the simulation\n")
            f.write("----------------------------------------------\n")
            f.write("Treatment involved: {}\n".format(world.parameters['choice_of_treatment']))
            f.write("Intervention involved: Use Condom: {}\n".format(world.parameters['use_condom']))
            f.write("Intervention involved: Notification of Partner: {}\n\n".format(world.parameters['notify_partner']))
            f.write("Number of simulation: {}\n\n".format(world.parameters['simulation_repetition']))
#            for key, value in self.mydict.items():
#                f.write("{}: {}\n".format(key, value))
        
    def appendToCSV(self, csvfile):
        for i in range(len(self.keys)):
            key = self.keys[i]
            if key in self.mydict:
                csvfile.write("{}".format(self.mydict[key]))
            if i < len(self.keys) - 1:
                csvfile.write(',')
            else:
                csvfile.write('\n')

    def writeCSVHeader(self, csvfile, parameters):
#        csvfile.write("Summary of the simulation\n")
#        csvfile.write("----------------------------------------------\n")
#        csvfile.write("Treatment involved: {}\n".format(parameters['choice_of_treatment']))
#        csvfile.write("Intervention involved: Use Condom: {}\n".format(parameters['use_condom']))
#        csvfile.write("Intervention involved: Notification of Partner: {}\n\n".format(parameters['notify_partner']))
        for i in range(len(self.keys)):
            key = self.keys[i]
            csvfile.write("{}".format(key))
            if i < len(self.keys) - 1:
                csvfile.write(',')
            else:
                csvfile.write('\n')


