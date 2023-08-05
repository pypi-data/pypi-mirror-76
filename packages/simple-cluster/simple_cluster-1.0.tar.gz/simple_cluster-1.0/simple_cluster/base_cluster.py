from pylab import *
from numpy import *
import matplotlib.pyplot as plt

""" Base class for clustering
Attributes: 
k (int ) representing number of clusters
data (set of points) a list of points extracted from the data file
"""
class Base():
    def __init__(self, k=3):
        self.k = k
        self.data = []

    """
    Function to read in data from a txt file. The txt file should have two number (float) per line. The numbers are stored in the data attribute.
    Args: file_name (string): name of a file to read from
    Returns: None
    """
    def read_data_file(self, file_name):
        with open(file_name) as file:
            data_set = []
            for line in file.readlines():
                x, y = line.strip().split('\t')
                data_set.append([float(x),float(y)])
        file.close()
        self.data = array(data_set)

    """ Function to calculate the distance between two points.
    Args:
    x1: coordinate of point 1
    x2: coordinate of point 2
    Returns:
    Distance(float) between x1 and x2
    """
    def distance(self, x1,x2):
        return sqrt(sum(power(x1-x2,2)))