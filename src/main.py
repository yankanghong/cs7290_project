import yaml
import argparse
import time
import sys
import copy

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

parser = argparse.ArgumentParser(prog=sys.argv[0], description='Memory dependency prediction networks')
parser.add_argument('--config', default='./configs/SimSeq.yaml', help="specifiy the config file")

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
    '''
    
    ###############################
    # load dataset
    ###############################
    train_set = CustomDataset(args.data, args.label)
    train_loader = DataLoader(train_set, batch_size=args.batch_size, 
                        shuffle=args.shuffle, num_workers=2)
    
    ###############################
    # declare model
    ###############################
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

    ###############################
    # declare optimizer
    ###############################
    optimizer = optim.Adam(model.parameters(), lr=args.learning_rate)
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer)

    ###############################
    # loss function
    ###############################
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

    ###############################
    # train loop
    ###############################
    best_eval_loss = 0.0
    eval_loss = 0.0
    best_model = None
    for epoch_idx in range(args.epochs):
        print("-----------------------------------")
        print("Epoch %d" % (epoch_idx))
        print("-----------------------------------")
        start_time = time.time()
        # train loop
        train_loss = None
        if (args.model == "SimSeq"):
            train_loss, avg_train_loss = train_simSeq(epoch_idx, model, train_loader, optimizer, criterion, args.clip)
        scheduler.step(train_loss)

        # validation loop
        val_loss, avg_val_loss = validate(model, valid_loader, criterion)
        
        end_time = time.time()
        epoch_mins, epoch_secs = epoch_time(start_time, end_time)

        if (val_loss < best_val_loss):
            best_val_loss = val_loss
            best_model = copy.deepcopy(model)

        print(f'Epoch: {epoch+1:02} | Time: {epoch_mins}m {epoch_secs}s')
        print(f'\tTrain Loss: {train_loss:.3f} | Train PPL: {math.exp(train_loss):7.3f}')
        print(f'\t Validate Loss: {val_loss:.3f} |  Validate PPL: {math.exp(val_loss):7.3f}')

    if (args.save_best):
        torch.save(best_model.state_dict(), './checkpoints/' +
                   args.model.lower() + '.pth')











if __name__ == '__main__':
    main()
