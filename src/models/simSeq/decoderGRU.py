from __future__ import unicode_literals, print_function, division

import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np

class DecoderGRU(nn.Module):
    """
        Decoder module. Uses GRU as underlying block.
            Context vector will be the input to both GRU and FC layer
        Return:
            Prediction 
            A context vector (last hidden state) given an input sequence
    """

    def __init__(self, output_size, emb_size, hidden_size, dropout=0.2):
        super(DecoderGRU, self).__init__()
        self.hidden_size = hidden_size
        self.output_size = output_size

        self.embedding = nn.Embedding(output_size, emb_size)
        self.gru = nn.GRU(emb_size+hidden_size, hidden_size)
        self.fc = nn.Linear(emb_size + hidden_size * 2, output_size)
        self.dropout = nn.Dropout(dropout)
        self.softmax = nn.LogSoftmax(dim=1)

    def forward(self, input, hidden, context):
        """
            Inputs: 
                a input tensor: [batch_size]
                previous hidden state: [1, batch_size, hidden_size]
                context vector from encoder: [1, batch_size, hidden_size]
        """
        if (hidden == None):
            print("No hidden state to decoder, wrong!")
            exit(1)

        # promote the input shape to 2D
        input = input.unsqueeze(0)

        embedded = self.dropout(self.embedding(input.to(torch.long)))
        #emb_con = [1, batch_size, emb_size + hidden_size]
        emb_con = torch.cat((embedded, context), dim=2)

        output, hidden = self.gru(emb_con, hidden)

        #output = [batch size, emb_size+ hidden_size * 2]
        output = torch.cat((embedded.squeeze(0), hidden.squeeze(0), context.squeeze(0)), dim=1)

        # output_size should be 2 (binary classification, 0 or 1)
        prediction = self.fc(output)

        return prediction, hidden


