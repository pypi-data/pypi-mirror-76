from flerken.framework.framework import Trainer
from flerken.framework.meters import TensorStorage, TensorHandler, get_nested_meter
from flerken.utils.losses import SI_SDR

from .config import transforms
from .config.deep_config import AUDIO_FRAMERATE
from .models import get_network
from . import utils,config
from .utils.dataset import get_dataset
from .. import get_solos_timestamps
import torch
from torchvision.utils import make_grid
import numpy as np

from random import randint
from functools import partial

SOP_PATH=__path__[0]
class Trainer(Trainer):
    def hook(self, vrs):
        self.IO.writer.add_image(self.state + 'GT', make_grid(vrs['gt']), global_step=self.absolute_iter)
        self.IO.writer.add_image(self.state + 'predictions', make_grid(torch.sigmoid(vrs['pred'])),
                              global_step=self.absolute_iter)
        idx = randint(0, vrs['pred'].size(0) - 1)
        pred_sp = torch.sigmoid(vrs['pred'][idx].detach().cpu().squeeze().unsqueeze(-1)) * vrs['vs'][0][
            idx]  # * torch.hamming_window(510).sum()
        audio = self.processor('resize512', 'istft')(pred_sp)
        self.IO.writer.add_audio(self.state + '_audio', audio.view(-1) / audio.abs().max(),
                              global_step=self.absolute_iter,
                              sample_rate=AUDIO_FRAMERATE,
                              walltime=None)

def get_sdr_meter():
    f = SI_SDR(ignore_nan=True)
    handler = TensorHandler('lin_freq_batch_adap', 'istft', **transforms)

    def func(pred, gt, vs):
        pred_sp = pred.squeeze(1).unsqueeze(-1) * vs[0]
        audio = handler(pred_sp)
        audio_gt = vs[1][0]
        sdr = f(audio, audio_gt)
        return sdr

    def func2(pred, gt, vs):
        pred_sp = gt.squeeze(1).unsqueeze(-1) * vs[0]
        audio = handler(pred_sp)
        audio_gt = vs[1][0]
        sdr = f(audio, audio_gt)
        return sdr

    def func3(pred, gt, vs):
        pred_sp = pred.squeeze(1).unsqueeze(-1) * vs[0]
        gt_sp = gt.squeeze(1).unsqueeze(-1) * vs[0]
        audio = handler(pred_sp)
        audio_gt = handler(gt_sp)
        sdr = f(audio_gt, audio)
        return sdr

    handlers = {}
    handlers['gt'] = TensorHandler('detach', 'to_cpu', **transforms)
    handlers['pred'] = TensorHandler('detach', 'to_cpu', 'sigmoid', **transforms)
    # handlers['sdr'] = func
    handlers['vs'] = lambda x: x
    # handlers['oracle'] = func2
    handlers['sdr_oracle'] = func3
    opt = {'gt': {'type': 'input', 'store': 'list'},
           'pred': {'type': 'input', 'store': 'list'},
           'vs': {'type': 'input', 'store': 'list'},
           # 'sdr': {'type': 'output', 'store': 'list'},
           # 'oracle': {'type': 'output', 'store': 'list'},
           'sdr_oracle': {'type': 'output', 'store': 'list'}
           }
    return get_nested_meter(
        partial(TensorStorage, handlers=handlers, opt=opt, on_the_fly=True,
                # redirect={'sdr': 'sdr', 'oracle': 'oracle', 'sdr_oracle': 'sdr'}), 1)
                redirect={'sdr_oracle': 'sdr'}))