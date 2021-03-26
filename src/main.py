import yaml
import argparse
import time
import sys

# Pytorch package
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset

# Tqdm progress bar
from tqdm import tqdm_notebook, tqdm

# Some utils
from utils import train
from dataset import CustomDataset

parser = argparse.ArgumentParser(prog=sys.argv[0], description='Memory dependency prediction networks')
parser.add_argument('--config', default='./configs/SimpleRNN.yaml', help="specifiy the config file")

def main():
    global args
    args = parser.parse_args()
    config = None
    with open(args.config) as f:
        config = yaml.full_load(f)
    
    for key in config:
        for k, v in config[key].items():
            setattr(args, k, v)

    '''
    # helpful for checking input arguments
    for arg in vars(args):
        print (arg, getattr(args, arg))
    '''
    
    cds = CustomDataset(args.data, args.label)
    train_loader = DataLoader(cds, batch_size=args.batch_size, shuffle=False)
    train(args.epochs, train_loader)











if __name__ == '__main__':
    main()
