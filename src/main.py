import sys
import random
import params
import World
import Room
from Logger import Logger

# Get the parameters for the simulation
parameters = params.CreateParametersDictionary()

# Create a log file
myLogger = Logger(parameters['logfilename'])


# Create CSV for summary
csvfile = open(parameters['csvfilename'], 'w')
myLogger.writeCSVHeader(csvfile, parameters)

# Loop for multiple runs of the simulation
for i in range(parameters['simulation_repetition']):
    # Clear the logger's cache
    myLogger.clear()

    # Seed the random number generator
    random.seed(i)

    # Create the world
    world = World.World(parameters, myLogger)
    Room.InitRoom(world)

    
    # Run for twelve years
    while world.has_events() and world.day < 365 * 12:
        world.process()

    myLogger.appendToCSV(csvfile)

sys.stderr.write('Done.\n')

myLogger.printSimulationDetail(world)
# Explicitly close the log file
csvfile.close()
