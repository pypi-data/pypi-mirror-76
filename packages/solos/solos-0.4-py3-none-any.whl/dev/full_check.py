from flerken.utils import BaseDict
from flerken.video.utils import get_duration_fps
from torchtree import Directory_Tree
import shutil
import os
from tqdm import tqdm
import Solos

sk_dict = BaseDict().load('/home/jfm/GitHub/Solos/Solos/skeleton_files/skeleton_dict.json')
d_dict = {}
videos_path = '/media/jfm/Slave/Solos'
tree = Directory_Tree(videos_path)
# w = []
# for path in tqdm(list(tree.videos.paths('/media/jfm/Slave/Solos/videos'))):
#     try:
#         key = path.split('/')[-1].split('.')[0]
#         # d_dict[key] = sk_dict[key][1]-sk_dict[key][0]
#         duration, fps = get_duration_fps(path, display=False)
#         vdur = int((duration[1] * 60 + duration[2] + duration[3] / 1000) * 25)
#         if  fps != 25:
#             # if  fps!=25:
#             print(path)
#             assert key in sk_dict
#             w.append(path)
#     except Exception as ex:
#         print('not in dict',path)
#         raise ex

# assert len(list(tree.videos.paths('/media/jfm/Slave/Solos/videos'))) == len(sk_dict)
for name,module in tree.skeleton.named_children():
    for n,m in module.named_children():
        if d_dict.get(name)==None:
            d_dict[name] = []
        d_dict[name].append(n)
gt = Solos.get_solos_ids()
ssk=[]
for cat in gt:
    for key in gt[cat]:
        if key not in d_dict[cat] and key in sk_dict:
            ssk.append(key)
        elif key in d_dict[cat]:
            pass
        else:
            print((cat,key))