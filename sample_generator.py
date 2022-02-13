import os
import argparse
import sobol_seq
import numpy as np
from random import *

######################
# Argument parser
######################

can = argparse.ArgumentParser()

can.add_argument("-d", "--dimension", default=5, type=int,
          help="Dimension of samples")

can.add_argument("-nb", "--sampling_number", default=10, type=int,
          help="Number of independent samples files")

can.add_argument("-lb", "--lower_bound",default=-5, type=int,
          help="Value of the lower bound in the samples")

can.add_argument("-ub", "--upper_bound", default=5, type=int,
          help="Value of the upper bound in the samples")

can.add_argument("-s", "--search_points", default=30, type=int,
          help="Number of samples points")

the = can.parse_args()

'''
Sample generation
'''
if not os.path.exists("./Sampling"):
    os.mkdir("./Sampling")
os.chdir("./Sampling")

for m in range(the.sampling_number):
    points = []
    seed = randint(1,50000)
    for j in range(the.search_points):
        seed +=1
        points.append(sobol_seq.i4_sobol(the.dimension, seed)[0])
    points = np.array(points)
    points = (the.upper_bound-the.lower_bound)*points+the.lower_bound
    np.savetxt("sampling_sobol"+str(m)+".csv", points, delimiter=",")
