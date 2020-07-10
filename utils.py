import numpy as np
import os
import matplotlib.pyplot as plt

def make_data_dict(fname):
    fname = os.path.join('data/csv-data/{}.csv'.format(fname))
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

    step_indices, = np.where(arr_step > 1)
    steps = []
    if step_indices.size == 0: return steps
    steps.append([0, step_indices[0]]) # append beginning range

    # find all intermediate ranges that are not in break range
    for i in range(len(step_indices) - 1):
        if step_indices[i] < step_indices[i + 1] - 1: steps.append([step_indices[i], step_indices[i + 1]])
    steps.append([step_indices[-1], len(arr) - 1]) # append end range
    return steps


if __name__=='__main__':
    print(step_detection(make_data_dict('00010100_s001_t000'), 'FP1'))