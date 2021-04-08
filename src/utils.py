import getopt
import sys
import time

# Pytorch package
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset

import numpy as np

# Tqdm progress bar
from tqdm import tqdm, tqdm_notebook

##########################################
# Utility
##########################################

def usage(defaut_trace):
    """ (Deprecated) usage function """
    print("Usage: ")
    print("       -t/--trace [trace file] , default trace file "+defaut_trace)
    print("       -m/--model [model name] , no default model ")
    print("       -h or --help")


def parse_args(argv, df_trace_path):
    try:
        opts, args = getopt.getopt(argv[1:], "t:h", ["trace", "help"])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err)  # will print something like "option -a not recognized"
        usage(df_trace_path)
        sys.exit(2)
    
    model_name = None
    trace_path = df_trace_path
    for opt, arg in opts:
        if opt == "-t":
            trace_path = arg
        if opt == "-m":
            model_name = arg
        elif opt in ("-h", "--help"):
            usage(df_trace_path)
            sys.exit()
        else:
            assert False, "unhandled option"

    return (model_name, trace_path)

class AverageMeter(object):
    """Computes and stores the average and current value"""
    def __init__(self):
        self.reset()

    def reset(self):
        self.val = 0
        self.avg = 0
        self.sum = 0
        self.count = 0

    def update(self, val, n=1):
        self.val = val
        self.sum += val * n
        self.count += n
        self.avg = self.sum / self.count


def accuracy(output, target):
    '''
        Computes the accuracy given output and target
        Args:
            output: a tensor with size (batch_size, # of classes)
            target: a tensor with size (batch_size, 1)
    '''
    batch_size = target.shape[0]

    _, pred = torch.max(output, dim=-1)

    correct = pred.eq(target).sum() * 1.0

    acc = correct / batch_size

    return acc


def epoch_time(start_time, end_time):
    elapsed_time = end_time - start_time
    elapsed_mins = int(elapsed_time / 60)
    elapsed_secs = int(elapsed_time - (elapsed_mins * 60))
    return elapsed_mins, elapsed_secs
    
##########################################
# Training functions 
##########################################

def train_simSeq(epoch, model, data_loader, optimizer, criterion, clip_th):
    '''
        Train function of simSeq.  
        Args:
            epoch_idx, model, data_loader, optimizer, criterion,
            clip_th: clip threshold for grad norm
    '''
    model.train()
    epoch_loss = 0

    # Get the progress bar for later modification
    progress_bar = tqdm(data_loader, ascii=True)

    # loop over current batch
    for idx, (data, target) in enumerate(progress_bar):

        optimizer.zero_grad()

        # FIXME: because the input_size for PC is too large for not server computing resource
        #        do a modulo operation to reduce the PC
        data = data % 100000
        
        # change to sequence first
        data = data.transpose(1, 0)
        target = target.transpose(1, 0)

        output = model.forward(data, target)
        # change into a row vector for calculating loss
        target = target.reshape(-1)  # target = [seq_len * batch_size]
        output = output.view(-1, output.shape[-1]) #output = [seq_len * batch_size, output_size]

        loss = criterion(output, target)
        loss.backward()

        # gradient clip to prevent exploding gradient
        torch.nn.utils.clip_grad_norm_(model.parameters(), clip_th)

        optimizer.step()
        epoch_loss += loss.item()
        progress_bar.set_description_str("Train Batch: %d, Loss: %.4f" % ((idx), loss.item()))

    return epoch_loss, epoch_loss / len(data_loader)


##########################################
# Evaluate function
##########################################

def validate(epoch, model, data_loader, criterion):
    '''
        Validate function 
        Args:
            epoch_idx, model, data_loader, criterion
    '''

    model.eval()
    epoch_loss = 0
    acc = AverageMeter()

    # Get the progress bar for later modification
    progress_bar = tqdm(data_loader, ascii=True)
    with torch.no_grad():

        # loop over current batch
        for idx, (data, target) in enumerate(progress_bar):
            # FIXME: because the input_size for PC is too large for not server computing resource
            #        do a modulo operation to reduce the PC
            data = data % 100000

            # change to sequence first
            data = data.transpose(1, 0)
            target = target.transpose(1, 0)

            # turn-off teacher forcing
            output = model.forward(data, target, 0)
            # change into a row vector for calculating loss
            target = target.reshape(-1)  # target = [seq_len * batch_size]
            output = output.view(-1, output.shape[-1]) #output = [seq_len * batch_size, output_size]
            
            batch_acc = accuracy(output, target)
            acc.update(batch_acc, target.shape[0])

            loss = criterion(output, target)
            epoch_loss += loss.item()

            progress_bar.set_description_str("Validate Batch: %d, Loss: %.4f, Batch Acc: %.4f" % ((idx), loss.item(), batch_acc))

    return epoch_loss, epoch_loss / len(data_loader), acc.avg

