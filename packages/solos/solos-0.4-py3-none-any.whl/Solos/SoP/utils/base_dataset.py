import os
import inspect
from warnings import warn
from random import randint, choice

import torch

from flerken.utils import BaseDict
from flerken.datasets import AVDataset

from .readers import *
from ..config.deep_config import *
from .. import config
__all__ = ['SKDataset']


class SKDataset(AVDataset):
    def __init__(self, root, preprocessing, exclude=[], debug=False, onehot=None,
                 visualization=[],
                 handle_empty_stamps=True, yield_mode='yield_file', **kwargs):
        args = {}
        for arg in inspect.getfullargspec(SKDataset.__init__).args:
            if arg != 'self':
                args.update({arg: locals()[arg]})
        self._build_info(root)
        super(SKDataset, self).__init__(root, in_memory=True, as_generator=False, exclude=exclude, debug=debug,
                                        yield_mode=yield_mode,
                                        **kwargs)
        self.yield_mode = yield_mode
        self.N = N_VIDEO_FRAMES
        self.debug = debug
        self.vis = visualization
        self.prepr = preprocessing
        self.rsr_idx = self.filemanager.resources.index('info')
        self.reader.init_reader(**self.get_reader_kwargs())
        if onehot is None:
            self.is_classinformed = False
            len(self.filemanager)
            self._zeros = torch.zeros(len(self.filemanager.clusters))
            self.class2idx = {x: y for x, y in
                              zip(self.filemanager.clusters.keys(), range(len(self.filemanager.clusters)))}
        else:
            self.is_classinformed = True
            self._zeros = torch.zeros(len(onehot)).float()
            self.class2idx = onehot
        self._check_stamps(**args)
        self.MAX_VAL = get_stft_config()['window'](N_FFT).sum().item()

    def _build_info(self, root):
        path = '/'+os.path.join(*config.__path__[0].split('/')[:-2],'json_files','solos_timestamps.json')
        timestamps = BaseDict().load(path)
        info_path = os.path.join(root, 'info')
        print("Building info")
        print(f"Path is {info_path}")
        if not os.path.exists(info_path):
            os.mkdir(info_path)
        for category in timestamps:
            cat_path = os.path.join(info_path, category)
            if not os.path.exists(cat_path):
                os.mkdir(cat_path)
            for key in timestamps[category]:
                file_path = os.path.join(cat_path, key + '.json')
                json = BaseDict()
                if os.path.exists(file_path):
                    json.load(file_path)
                json['stamps'] = timestamps[category][key]
                json.write(file_path)

    def _check_stamps(self, handle_empty_stamps, *args, **kwargs):
        def is_empty(x):
            return not bool(x)

        exclude = []
        counter = {}
        for rel_path, _ in self.info.named_parameters():
            cat, key = rel_path.split('/')
            if cat not in counter:
                counter[cat] = 0
            if is_empty(self.info[key]['stamps']):
                warn('Sample %s contains no stamps. Exclude it from further initializations.' % key)
                if handle_empty_stamps and key not in kwargs['exclude']:
                    exclude.append(key)
                    counter[cat] += 1
        kwargs['exclude'] += exclude

        if not is_empty(exclude):
            self.__init__(*args, **kwargs)

        self._exclude_empty_stamps = exclude

    def class2onehot(self, cat):
        x = self._zeros.clone()
        x[self.class2idx[cat]] = 1.
        return x

    @property
    def info(self):
        return self.filemanager.info

    def sample_idx(self, idx):

        if self.yield_mode == 'yield_module':
            path = self.filemanager[idx][0]
            key = path.split('/')[-1]
        elif self.yield_mode == 'yield_file':
            path = self.filemanager[idx][-2]
            key = path.split('/')[-1].split('.')[0]
        stamp0, stamp1 = choice(self.info[key]['stamps'])

        stamp = randint(stamp0, stamp1 - N_VIDEO_FRAMES)

        return self.get_idx_kwargs(stamp)

    def get_idx_kwargs(self, idx):

        return {'audio': {'offset': round(idx * AUDIO_VIDEO_RATE), 'length': AUDIO_LENGTH},
                'frames': {'offset': idx, 'length': N_VIDEO_FRAMES},
                'videos': {'offset': idx, 'length': N_VIDEO_FRAMES},
                }

    def get_reader_kwargs(self):
        out = {
            'videos': VideoReader()
        }
        return out

    def split_dataset(self, pc):
        from random import choices
        videos = list(self.filemanager.info.keys())
        n = len(videos)
        coef = pc / 100 if pc > 1 else pc
        k = round(coef * n)
        return choices(videos, k=k)
