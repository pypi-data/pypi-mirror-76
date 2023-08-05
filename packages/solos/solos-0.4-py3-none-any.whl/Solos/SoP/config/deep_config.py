from warnings import warn as _warn
from torch import hann_window

# AUDIO AND VIDEO PARAMETERS
AUDIO_LENGTH = 6 * 11025
AUDIO_LENGTH = 65535 # They don't really use 6*11025 but do a center crop
# https://github.com/hangzhaomit/Sound-of-Pixels/blob/45350346393ab643fbc6c3517eaeb1671b140bcb/dataset/base.py#L170
# self.audioLen is 65535 in their cfg
N_VIDEO_FRAMES = 6 * 25
N_SKELETON_FRAMES = 6 * 25 + 1

AUDIO_FRAMERATE = 11025
VIDEO_FRAMERATE = 25
AUDIO_VIDEO_RATE = AUDIO_FRAMERATE / VIDEO_FRAMERATE

N_FFT = 1022
HOP_LENGTH = 256
STFT_WINDOW = hann_window

# DATASET PARAMETERS
SKELETON_NPY_REL_PATH = 'skeleton_npy/skeleton_npy.npy'
SKELETON_DICT_REL_PATH = 'skeleton_npy/skeleton_dict.json'
DALI_VIDEO_DATASET_PATH = './dali_dataset.txt'
PREFETCH_QUEUE_DEPTH = 1
EXEC_PIPELINED = True


def get_stft_config():
    """
    DALI docs
    https://docs.nvidia.com/deeplearning/dali/user-guide/docs/supported_ops.html?highlight=spectrogram#nvidia.dali.ops.Spectrogram

    PyTorch docs
    https://pytorch.org/docs/stable/torch.html?highlight=stft#torch.stft
    """
    data = {"window": STFT_WINDOW,
            "n_fft": N_FFT,
            "hop_length": HOP_LENGTH
            }
    return data


def get_istft_config():
    data = get_stft_config()
    data['length'] = AUDIO_LENGTH
    data['window'] = STFT_WINDOW(N_FFT)
    return data
