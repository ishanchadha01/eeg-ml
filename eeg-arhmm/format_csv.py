import numpy as np
import os

def format_csv(fname):
    parent = os.path.split(os.getcwd())[0]
    fname = os.path.join(os.path.join(parent, 'data/csv-data/{}.csv'.format(fname)))
    data =  np.loadtxt(open(fname, 'rb'), delimiter=',')
    header = open(fname, "rb").readline()
    header_arr = header.replace('\n', '').replace('EEG ', '').replace('-REF', '').replace('# ', '').split(',')
    data_dict = { key:val for (key,val) in zip(header_arr, data) }
    return data_dict
