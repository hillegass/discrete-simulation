import sys
import random
import params
import World

# Seed the random number generator
random.seed(1)

# Get the parameters for this run of the simulation
parameters = params.CreateParametersDictionary()

# Open a log file that important events will go into
logfile = open(parameters['logfilename'], 'w')

# Create the world
world = World.World(parameters, logfile)

# Run for twelve years
while world.has_events() and world.day < 365 * 12:
    world.process()

sys.stderr.write('Done\n')

# Explicitly close the log file
logfile.close()
