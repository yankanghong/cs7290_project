from __future__ import unicode_literals, print_function, division

import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np

class EncoderGRU(nn.Module):
    """
        Encoder module. Uses GRU as underlying block.
        Return:
            All hidden states 
            A context vector (last hidden state) given an input sequence
    """

    def __init__(self, input_size, emb_size, hidden_size, dropout=0.2):
        super(EncoderGRU, self).__init__()

        self.hidden_size = hidden_size
        self.embedding = nn.Embedding(input_size, emb_size)
        self.gru = nn.GRU(emb_size, hidden_size)
        self.dropout = nn.Dropout(dropout)

    def forward(self, inputs):
        """ Forward function of EncoderGRU """
        
        #inputs = [seq_len, batch_size]
        embedded = self.dropout(self.embedding(inputs))
        
        #hidden = [1, batch_size, hidden_size]
        outputs, hidden = self.gru(embedded)

        return outputs, hidden

