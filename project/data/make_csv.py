import numpy as np
import mne
import argparse
import os


if __name__=='__main__':

    # Get input and output directories
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_dir', default='raw-data')
    parser.add_argument('--save_dir', default='csv-data')
    args = parser.parse_args()
    if not os.path.exists(args.save_dir):
        os.makedirs(args.save_dir)

    # Convert edf to csv and save files
    for dirpath, dirnames, fnames in os.walk(args.data_dir):

        for fname in fnames:

            if '.edf' in fname:
                name = fname.replace('.edf','')
                edf = mne.io.read_raw_edf(os.path.join(dirpath, fname))
                header = ','.join(edf.ch_names)
                save_file = '{}/{}.csv'.format(args.save_dir, name)
                np.savetxt(save_file, edf.get_data().T, delimiter=',', header=header)
