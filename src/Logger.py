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
    
    def printLog(self):
        with open(self.logfile, 'w') as f:
            f.write("Summary of the simulation\n")
            f.write("----------------------------------------------\n")
            for key, value in self.mydict.items():
                f.write("{}: {}".format(key, value))

