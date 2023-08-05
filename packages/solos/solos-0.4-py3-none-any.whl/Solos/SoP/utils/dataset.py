import torch

from .base_dataset import SKDataset
from ..config.transforms import transforms, Processor

from flerken.audio.transforms import rec2polar
from flerken.utils import BaseDict, get_transforms
from flerken.framework.allocator import Allocator

from random import shuffle

__all__ = ['BSSDataset', 'get_dataset']


class BSSDataset(SKDataset):
    def __init__(self, root, preprocessing, exclude=[], debug=False, onehot=None, n_sources=1, visualization=[],
                 handle_empty_stamps=False, read_video=False, weighted_loss=False,
                 **kwargs):
        super().__init__(root, preprocessing, exclude=exclude, debug=debug, onehot=onehot, visualization=visualization,
                         handle_empty_stamps=handle_empty_stamps, **kwargs)
        self.weighted_loss = weighted_loss
        self.read_video = read_video
        self.n_sources = n_sources
        self.cuda1 = Allocator(1, dataparallel=False)
        self.cpu = Allocator('cpu', dataparallel=False)

    @staticmethod
    def binary_max(sp, debug):
        sp = torch.stack(sp)
        spm_with_phase = sum(sp)
        spm = rec2polar(spm_with_phase)[..., 0]  # unsqueeze to fit required channel dim in conv2d
        if debug:
            for i in sp:
                if torch.isnan(i).any() or torch.isinf(i).any():
                    raise Exception('NaN or Inf found in raw spectrograms.')
            if torch.isnan(spm).any() or torch.isinf(spm).any():
                raise Exception('NaN or Inf found in spm after getting mag and phase.')
        sp = torch.stack([rec2polar(s) for s in sp])[..., 0]
        indices = sp.max(dim=0)[1]
        gt = torch.zeros_like(sp)
        for idx, sp_i in enumerate(gt):
            sp_i.masked_fill_(indices == idx, 1.)

        return spm_with_phase, spm, sp, gt[0]

    def __getitem__(self, idx):
        audio, trace = self.getitem(idx, self.n_sources, ['audio'], trazability=True,
                                    repeat_class=True, classes=None)
        audio_ = audio[0]
        audio = [self.prepr['audio'](x) for x in audio_]

        if self.read_video:
            # TODO
            vd = self.getitem(idx, 1, ['videos'], trazability=False)
            vd = vd[0][0]
            vd = self.prepr['video'](vd)
            if isinstance(vd,list):
                vd = torch.stack(vd,dim=1)
        try:
            sp = [self.prepr['audio2sp'](x) for x in audio]

            # Preprocessing
            sp_post = [self.prepr['spectrograms_npy'](x) for x in sp]

            # Ground-truth computation
            spm_with_phase, spm, sp_post, gt = self.binary_max(sp_post, self.debug)

            # Signal saturation if waveform values of sum >1
            # https://dsp.stackexchange.com/questions/44366/what-is-the-amplitude-range-of-a-spectrogram
            # Considering not squared window max val equals window sum
            spm.clamp_(0, self.MAX_VAL)
            if self.weighted_loss:
                weight = torch.log1p(spm)
                weight = torch.clamp(weight, 1e-3, 10).unsqueeze(0)

            # log spectrogram
            epsilon = 1e-4
            spm = (spm + epsilon).log()
            spm = (spm - spm.mean()) / (spm.std() + epsilon)
            vis = []
            for x in self.vis:  # Cannot use comprehension list as locals() would map the inner comprehension function
                vis.append(locals()[x])
            ground_truth = gt.unsqueeze_(0)
            inputs = [spm.unsqueeze_(0)]
            if self.read_video:
                inputs.append(vd)
            return ground_truth, inputs, vis
        except Exception as ex:
            print(trace)
            raise ex


def get_dataset(root, preprocessing, exclude=[], debug=False, n_sources=1, visualization=[], weighted_loss=False,
                read_video=False, one_hot=None):
    processor = get_transforms() + Processor(transforms)
    prepr = BaseDict()
    prepr['spectrograms_npy'] = processor(*preprocessing.sp_preprocessing)
    prepr['audio2sp'] = processor(*preprocessing.audio2sp)
    prepr['audio'] = processor(*preprocessing.audio_preprocessing)
    prepr['video'] = processor(*preprocessing.video_preprocessing)
    # Warning. There are Video_io processors which are defined at reader.py They are computed on-the-fly while reading
    # frames from buffer to be memory efficient
    dataset = BSSDataset(root, prepr, exclude, debug, one_hot, n_sources, visualization, weighted_loss=weighted_loss,
                         read_video=read_video)
    return dataset
