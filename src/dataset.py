
from __future__ import print_function, division
import os
import torch
from torch.utils.data import Dataset, DataLoader
import pandas as pd
import numpy as np
import linecache
import csv

class CustomDataset(Dataset):
    """ custom dataset class to load data """
    def __init__(self, datafname, labelfname):
        self._data_fname = datafname
        self._label_fname = labelfname
        self._total_data = 0
        with open(datafname, "rb") as f:
            self._total_data = len(f.readlines()) - 1

    def __getitem__(self, idx):
        if torch.is_tensor(idx):
            idx = idx.tolist()

        data = linecache.getline(self._data_fname, idx + 1).split(',')
        label = linecache.getline(self._label_fname, idx + 1).split(',')

        length = len(data)

        # convert to numbers
        for i in range(length):
            data[i] = int(data[i])
            label[i] = int(label[i])

        return (np.array(data), np.array(label))

    def __len__(self):
        return self._total_data
