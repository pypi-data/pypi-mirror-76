from torchaudio.functional import istft
from flerken.framework.python_inheritance import ClassDict
from flerken.transforms import Compose, Resize, RandomCrop, RandomHorizontalFlip, ToPILImage, ToTensor
from flerken.audio.transforms import LogFrequencyScale, STFT, rec2polar

from functools import partial
from .deep_config import get_stft_config, get_istft_config
from random import randint, choice, random
from torch.nn.functional import interpolate
import PIL


class Processor(ClassDict):
    def __call__(self, *args):
        return Compose([self[x] for x in args])


def normalize_mean_std(waveform):
    std = waveform.std()
    if std > 0.1:
        waveform_out = (waveform - waveform.mean()) / waveform.std()
    else:
        waveform_out = (waveform - waveform.mean()) / 0.1

    return waveform_out


def normalize_max(waveform):
    if waveform.max() != 0:
        waveform_out = waveform / waveform.max()
    else:
        waveform_out = waveform

    return waveform_out


def random_loudness(x):
    coef = random() * 0.5 + 0.5
    return x * coef


transforms = {
    "stft": STFT(**get_stft_config()),
    "istft": partial(istft, **get_istft_config()),
    "random_loudness": random_loudness,
    "downsample": lambda x: x[::2, ...],
    "log_freq": LogFrequencyScale(True, 'HWC', shape=(512, None)),
    "log_freq_adap": LogFrequencyScale(True, 'HWC', shape=(512, None), adaptative=True),
    "log_freq_downsample": LogFrequencyScale(True, 'HWC', shape=(256, None)),
    "log_freq_downsample_adap": LogFrequencyScale(True, 'HWC', shape=(256, None), adaptative=True),
    "normalize": normalize_mean_std,
    "normalize_max": normalize_max,
    "lin_freq": LogFrequencyScale(False, 'HWC', shape=(512, None)),
    "lin_freq_adap": LogFrequencyScale(False, 'HWC', shape=(512, None), adaptative=True),
    "lin_freq_batch": LogFrequencyScale(False, 'BHWC', shape=(512, None)),
    "lin_freq_batch_adap": LogFrequencyScale(False, 'BHWC', shape=(512, None), adaptative=True),
    "numpy": lambda x: x.detach().cpu().numpy(),
    "rec2polar": rec2polar,
    "log": lambda x: x.log(),
    "sigmoid": lambda x: torch.sigmoid(x),
    "PIL": ToPILImage(),
    "PIL2tensor": ToTensor(),
    "resize256": Resize(256),
    "randomcrop224": RandomCrop(224),
    "flip": RandomHorizontalFlip(),
    "resize512": lambda x: interpolate(x.permute(2, 0, 1).unsqueeze(0), size=(512, 256), mode='bilinear',
                                       align_corners=True).squeeze().permute(1,2,0)}
