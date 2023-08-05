import numpy as np
import cv2
import cv2
from imageio import get_reader
import os

from flerken.video.loader import VideoSampler

__all__ = ['class_reader', 'ID_reader', 'VideoReader']



class VideoReader:
    def __call__(self, path, offset, length):
        if path.endswith(('.webm')):
            cap = cv2.VideoCapture(path)
            flag, frame = cap.read()
            cap.set(cv2.CAP_PROP_POS_FRAMES, offset + 25)
            frame0 = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            cap.set(cv2.CAP_PROP_POS_FRAMES, offset + 75)
            flag, frame = cap.read()
            frame1 = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            cap.set(cv2.CAP_PROP_POS_FRAMES, offset + 125)
            flag, frame = cap.read()
            frame2 = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            return [frame0, frame1, frame2]
        else:
            reader = get_reader(path)
            frame0 = reader.get_data(offset + 25)
            frame1 = reader.get_data(offset + 75)
            frame2 = reader.get_data(offset + 125)
            return [frame0, frame1, frame2]


def class_reader(path):
    key = path.split('/')[-2]
    return key


def ID_reader(path):
    key = path.split('/')[-1]
    return key
