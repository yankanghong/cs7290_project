from __future__ import unicode_literals, print_function, division

import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np

import random

class SimSeq(nn.Module):
    '''
        A simple sequence to sequence model for dependency prediction
            Utilize Encoder and Decoder architecture
            The encoder uses GRU 
            The decoder uses GRU, reuse context vector

        Teacher forcing is on by default (see forward() function), ratio = 0.5
    '''

    def __init__(self, encoder, decoder, device):
        super().__init__()
        self.encoder = encoder
        self.decoder = decoder
        self.device = device

        assert encoder.hidden_size == decoder.hidden_size, "Hidden dimensions of encoder and decoder must be equal!"

    def forward(self, data, target, teacher_forcing_ratio=0.5):
        """
            data tensor: [seq_len, batch_size]
            target tensor: [target_len, batch_size]
            teacher_forcing_ratio is probability to use teacher forcing
            e.g. if teacher_forcing_ratio is 0.75 we use ground-truth inputs 75% of the time
        """
        batch_size = target.shape[1]
        target_len = target.shape[0]

        #tensor to store decoder outputs
        outputs = torch.zeros(target_len, batch_size, self.decoder.output_size ).to(self.device)

        #last hidden state of the encoder is the context
        _, context = self.encoder(data)

        #context also used as the initial hidden state of the decoder
        hidden = context

        #first input to the decoder, empty
        input = torch.zeros(batch_size)

        for t in range(0, target_len):
            #insert input token embedding, previous hidden state and the context state
            #receive output tensor (predictions) and new hidden state
            output, hidden = self.decoder(input, hidden, context)

            #place predictions in a tensor holding predictions for each token
            outputs[t] = output

            #decide if we are going to use teacher forcing or not
            teacher_force = random.random() < teacher_forcing_ratio
            
            #if teacher forcing, use actual next token as next input
            #if not, use predicted token
            input = target[t] if teacher_force else torch.argmax(output, dim=1)

        return outputs
