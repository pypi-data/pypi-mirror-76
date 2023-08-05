"""
Helper functions for the Stocker module and main script.

License: LGPLv3

Coming soon:
    Data for multi-step prediction
    Data normalization option
    Compact (last 60) data
"""

import numpy as np
import pandas as pd
import os
from sklearn.preprocessing import MinMaxScaler


def single_step_data(data, target, start, end, history_size, target_size, step, normalize=True):

    """
    Splits numpy array of data into x and y

    args:
        data ---- numpy array of data (x)
        target ---- numpy array of target data (y)
        start, end ---- start and end indices
        history_size ---- past window for model to consider
        target_size ---- future window to predict
        step ---- index increment
    """
    scaler = MinMaxScaler()

    dataset=[]
    labels=[]

    # set start and end
    start = start + history_size
    if end is None:
        end = len(data) - target_size
    
    # for each index, create input and target data
    for i in range(start, end):
        indices = range(i-history_size, i, step)
        dataset.append(data[indices])

        labels.append(target[i+target_size])

    # normalize data if necessary
    if normalize:
        count=0
        for data in dataset:
            data = scaler.fit_transform(data, y=labels[count])
            count += 1

    return np.array(dataset), np.array(labels)

def make_dir(dir):
    """ make path if does not exist """
    if not os.path.exists(dir):
        os.makedirs(dir)

    return dir