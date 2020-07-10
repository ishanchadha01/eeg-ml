import numpy as np
import argparse
import os
import sys
import csv


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

    # Get input and output directories
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_dir', default='csv-data')
    parser.add_argument('--save_dir', default='step-data')
    args = parser.parse_args()
    if not os.path.exists(args.save_dir):
        os.makedirs(args.save_dir)

    # Convert edf to csv and save files
    for dirpath, dirnames, fnames in os.walk(args.data_dir):

        for fname in fnames:

            if fname != '00010100_s001_t000.csv': continue

            if '.csv' in fname:
                name = fname.replace('.csv','')
                save_file = '{}/{}.csv'.format(args.save_dir, name)

                data_dict = make_data_dict(name)
                step_dict = {}
                for key in data_dict.keys():
                    print('Making steps for {}...'.format(key))
                    step_dict[key] = step_detection(data_dict, key)
                
                with open(fname, 'w') as csv_file:
                    writer = csv.writer(csv_file)
                    for k, v in step_dict.items():
                        writer.writerow([k, v])

