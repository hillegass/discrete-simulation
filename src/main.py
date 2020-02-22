import sys
import random
import params
import World
import Room
from Logger import Logger

# Seed the random number generator
random.seed(1)

# Get the parameters for this run of the simulation
parameters = params.CreateParametersDictionary()

# Open a log file that important events will go into
#logfile = open(parameters['logfilename'], 'w')

# Create the world
myLogger = Logger(parameters['logfilename'])
world = World.World(parameters, myLogger)
Room.InitRoom(world)

# Run for twelve years
while world.has_events() and world.day < 365 * 12:
    world.process()

sys.stderr.write('Done\n')

myLogger.printLog(world)
# Explicitly close the log file
#logfile.close()
