import yaml
import argparse
import time
import sys
import copy
import math 
import os

# Pytorch package
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset

# Tqdm progress bar
from tqdm import tqdm_notebook, tqdm

# Some utils
from utils import *
from dataset import CustomDataset
from models.simSeq import EncoderGRU, DecoderGRU, SimSeq

##########################################
# Args setting
##########################################
parser = argparse.ArgumentParser(prog=sys.argv[0], description='Memory dependency prediction networks')
parser.add_argument('--config', default='./configs/SimSeq.yaml', metavar='CONFIG_FILE' ,
                    help="Specifiy the config file. Default set to SimSeq.yaml")
parser.add_argument('--mode', default='train', metavar="MODE",
                    help="Two modes available: train or test. If set to test, specify the path to weights in config file. Default: train")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

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
    exit(1)
    '''
    
    ##########################################
    # load dataset
    ##########################################
    IW_SIZE = 64  # define the sequence length
    train_set = CustomDataset(args.train_data, args.train_label, iw_size=IW_SIZE)
    valid_set = CustomDataset(args.valid_data, args.valid_label, iw_size=IW_SIZE)
    train_loader = DataLoader(train_set, batch_size=args.tra_batch_size, 
                        shuffle=args.shuffle)
    valid_loader = DataLoader(valid_set, batch_size=args.val_batch_size,
                              shuffle=args.shuffle)

    ##########################################
    # declare model
    ##########################################
    # INPUT_SIZE = 2**30 # equal to address space, for PC
    INPUT_SIZE = 100000 # equal to address space, for PC
    OUTPUT_SIZE = 2
    ENC_EMB_SIZE = 32
    DEC_EMB_SIZE = 32
    HIDDEN_SIZE = 128
    ENC_DROPOUT = 0.5
    DEC_DROPOUT = 0.5

    if (args.model == "SimpleRNN"):
        model = SimpleRNN(INPUT_SIZE, HIDDEN_SIZE, OUTPUT_SIZE)
    elif (args.model == "SimSeq"):
        encoder = EncoderGRU(INPUT_SIZE, ENC_EMB_SIZE, HIDDEN_SIZE, dropout=ENC_DROPOUT)
        decoder = DecoderGRU(OUTPUT_SIZE, DEC_EMB_SIZE, HIDDEN_SIZE, dropout=DEC_DROPOUT)
        model = SimSeq(encoder, decoder, device)
        pass
    else:
        print("Model not defined!")
        exit(1)

    # check if pre-trained model exists when test mode
    if (args.mode.lower() == 'test'):
        # set epoch to 1 if in test mode
        args.epoch = 1
        if (not os.path.exists(args.pt_path)):
            print("Pre-trained model '"+args.pt_path+"' not exists, please check yaml file for 'pt_path'")
            exit(1)
        model.load_state_dict(torch.load(args.pt_path)) # load pre-train model
    else:
        # declare optimizer
        optimizer = optim.Adam(model.parameters(), lr=args.learning_rate)
        scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer)

    ##########################################
    # loss function
    ##########################################
    if (args.loss_type == "CE"):
        criterion = nn.CrossEntropyLoss()
    elif (args.loss_type == "Focal"): # Focal loss
        cls_num_list = train_set.get_cls_num_list()
        if (args.reweight):
            per_cls_weights = reweight(cls_num_list, beta=args.beta)
            if (torch.cuda.is_available()):
                per_cls_weights = per_cls_weights.cuda()
        else:
            per_cls_weights = None
        criterion = FocalLoss(weight=per_cls_weights, gamma=1)
    elif (args.loss_type == "NLL"):
        criterion = nn.NLLLoss()
    else:
        print("Unknown loss type: ", args.loss_type)
        exit(1)

    ##########################################
    # Epoch loop
    ##########################################
    best_val_loss = 10000.0
    best_val_acc = 0.0
    best_model = None
    
    for epoch_idx in range(args.epochs):
        print("-----------------------------------")
        print("Epoch %d" % (epoch_idx))
        print("-----------------------------------")
        start_time = time.time()

        # train loop
        train_loss = None
        if ( args.mode == 'train' and args.model == "SimSeq"):
            train_loss, avg_train_loss = train_simSeq(epoch_idx, model, train_loader, optimizer, criterion, args.clip)
            scheduler.step(train_loss) # adjust learning rate

        # validation loop
        val_loss, avg_val_loss, avg_acc = validate(epoch_idx, model, valid_loader, criterion)
        
        end_time = time.time()
        epoch_mins, epoch_secs = epoch_time(start_time, end_time)

        if (avg_val_loss < best_val_loss and avg_acc > best_val_acc):
            best_val_loss = avg_val_loss
            best_val_acc = avg_acc
            best_model = copy.deepcopy(model)

        print(f'Epoch: {epoch_idx+1:02} | Time: {epoch_mins}m {epoch_secs}s')
        if (args.mode == 'train'): print(f'\tTrain Loss: {avg_train_loss:.3f} | Train PPL: {math.exp(avg_train_loss):7.3f}')
        print(f'\tValidate Loss: {avg_val_loss:.3f} | Validate PPL: {math.exp(avg_val_loss):7.3f} | Validate Accuracy: {avg_acc:.4f}')

    if (args.mode=='train' and args.save_best):
        torch.save(best_model.state_dict(), './checkpoints/' +
                   args.model.lower() + '.pth')

    print("Pytorch Done...")










if __name__ == '__main__':
    main()
