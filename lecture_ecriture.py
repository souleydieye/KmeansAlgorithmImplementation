# -*- coding: utf-8 -*-

import random as np
import sys

def read_data(filename, skip_first_line = False, ignore_first_column = False):
    '''
    Loads data from a csv file and returns the corresponding list.
    All data are expected to be floats, except in the first column.
    
    @param filename: csv file name.
    
    @param skip_first_line: if True, the first line is not read.
        Default value: False.
    
    @param ignore_first_column: if True, the first column is ignored.
        Default value: False.
    
    @return: a list of lists, each list being a row in the data file.
        Rows are returned in the same order as in the file.
        They contains floats, except for the 1st element which is a string
        when the first column is not ignored.
    '''
    
    f = open(filename,'r')
    if skip_first_line:
        f.readline()
    
    data = []
    for line in f:
        line = line.split(",")
        line[0:] = [ float(x) for x in line[0:] ]
        if ignore_first_column:
            line = line[1:]
        data.append(line)
    f.close()
    return data

def write_data(StockDeGroupes, filename):
    '''
    Writes data in a csv file.

    @param data: a list of lists

    @param filename: the path of the file in which data is written.
        The file is created if necessary; if it exists, it is overwritten.
    '''
    # If you're curious, look at python's module csv instead, which offers
    # more powerful means to write (and read!) csv files.
    f = open(filename, 'w')
    for i in StockDeGroupes:
        f.write('groupe %s '%i.numero)
        f.write('\n')
        for j in i.groupe:
        
                f.write(','.join([repr(x) for x in j]))
                f.write('\n')
    f.close()

def write_add_line(data, filename):
    '''
    Writes data in a csv file.

    @param data: a list of lists

    @param filename: the path of the file in which data is written.
        The file is created if necessary; if it exists, it is overwritten.
    '''
    # If you're curious, look at python's module csv instead, which offers
    # more powerful means to write (and read!) csv files.
    f = open(filename, 'w')
    for i in range(len(data)):
        data[i]=[i+1]+data[i]
        
        f.write(','.join([repr(x) for x in data[i]]))
        f.write('\n')
    f.close()
def generate_random_data(nb_objs, nb_attrs):
    '''
    Generates a matrix of random data.
    
    @param frand: the fonction used to generate random values.
        It defaults to random.random.
        Example::

            import random
            generate_random_data(5, 6, lambda: random.gauss(0, 1))
    
    @return: a matrix with nb_objs rows and nb_attrs+1 columns. The 1st
        column is filled with line numbers (integers, from 1 to nb_objs).
    '''
    data = []
    for i in range(nb_objs):
        #line = [i+1]
        #for j in range(numAtt):
        #    line.append(frand())"""
        """
        line = [i+1] + map(lambda x: frand(), range(nb_attrs))
        """
        line=[i+1]
        for j in range(0,nb_attrs):
            line+=[np.random()]
        data.append(line)
    return(data)
#####"""
"""
data=read_data('iristest.csv')
write_add_line(data,'iristest2.csv')
"""
#####
