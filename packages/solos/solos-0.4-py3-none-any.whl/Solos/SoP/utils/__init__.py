import os

from .dataset import *
from .loss import BCEWithLogitsLoss
from torch import nn


def set_path(path):
    if not os.path.exists(path):
        os.makedirs(path)
    return path


SOLOS = {'string': ['Cello', 'cello', 'DoubleBass', 'erhu', 'Viola', 'Violin'],
         'wind': ['Bassoon', 'clarinet', 'flute', 'Horn', 'Oboe', 'sax',
                  'Saxophone', 'Trombone', 'trumpet', 'tuba'],
         'percussion': 'xylophone'}
DUETS = {'string-wind': ['cf', 'clc', 'clv', 'ct', 'ef''tuv', 'vf', 'vt'],
         'string-string': ['ec', 'vc'],
         'wind-wind': ['clf', 'clt', 'cltu', 'tf', 'tut'],
         'percussion': ['xf']}


def unet_params(model: nn.Module):
    unet_modules = ['encoder', 'decoder', 'final_conv', 'pool', 'scaling', 'bias']
    for n, p in model.named_children():
        if n in unet_modules:
            yield from p.parameters()

