import torch
import torch.nn as nn


class Model(nn.Module):
    def __init__(self):
        super(Model, self).__init__()
        self.weight = nn.Parameter(torch.FloatTensor(2, 2))
        self.bias = nn.Parameter(torch.FloatTensor(1))
        self.bias.data.zero_()


model = Model()

for name, param in model.named_parameters():
    print(name, param)