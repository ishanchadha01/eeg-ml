import numpy as np
import os
import matplotlib.pyplot as plt

def make_data_dict(fname):
    parent = os.path.split(os.getcwd())[0]
    fname = os.path.join(os.path.join(parent, 'data/csv-data/{}.csv'.format(fname)))
    data =  np.loadtxt(open(fname, 'rb'), delimiter=',')
    header = open(fname, "rb").readline()
    header_arr = header.replace('\n', '').replace('EEG ', '').replace('-REF', '').replace('# ', '').split(',') # labels from 1st line of csv
    data_dict = { key:val for (key,val) in zip(header_arr, data) }
    return data_dict

def step_detection(data_dict, wave_type):
    data = data_dict[wave_type]
    arr = map(float, data)
    arr -= np.average(arr)
    step = np.hstack((np.ones(len(arr)), -1*np.ones(len(arr))))
    arr_step = np.convolve(arr, step, mode='valid') # take convolution of time vs wave
    arr_step = [ np.log(val) if val > 0 else 0 for val in arr_step ]
    step_mean = np.mean(arr_step)
    step_std = np.std(arr_step)
    print(step_mean, step_std)
    return abs(arr_step - step_mean) < 10 * step_std


if __name__=='__main__':
    print(step_detection(make_data_dict('00010100_s001_t000'), 'FP1'))