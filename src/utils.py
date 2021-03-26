import getopt
import sys
import time

# Pytorch package
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset

import numpy as np

# custom models
from models import SimpleRNN


def usage(defaut_trace):
    """ discarded usage function """
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

# def train(epoch, data_loader, model, optimizer, criterion):
def train(epoch, data_loader):
    """ train function """
    # iter_time = AverageMeter()
    # losses = AverageMeter()
    # acc = AverageMeter()

    for idx, (data, target) in enumerate(data_loader):
        # start = time.time()
        print("idx:",idx)
        print(data)
        print(target)
        if (idx == 0):
            break
        # if torch.cuda.is_available():
            # data = data.cuda()
            # target = target.cuda()

        # optimizer.zero_grad()  # clear prev gradient
        # # print(data.shape)
        # out = model.forward(data)
        # loss = criterion.forward(out, target)
        # loss.backward()
        # optimizer.step()

        # batch_acc = accuracy(out, target)

        # losses.update(loss, out.shape[0])
        # acc.update(batch_acc, out.shape[0])

        # iter_time.update(time.time() - start)
        # if idx % 10 == 0:
        #     print(('Epoch: [{0}][{1}/{2}]\t'
        #            'Time {iter_time.val:.3f} ({iter_time.avg:.3f})\t'
        #            'Loss {loss.val:.4f} ({loss.avg:.4f})\t'
        #            'Prec @1 {top1.val:.4f} ({top1.avg:.4f})\t')
        #           .format(epoch, idx, len(data_loader), iter_time=iter_time, loss=losses, top1=acc))
