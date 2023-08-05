SOLOS = {'string': ['Cello', 'cello', 'DoubleBass', 'erhu', 'Viola', 'Violin', 'violin'],
         'wind': ['Bassoon', 'clarinet', 'flute', 'Horn', 'Oboe', 'sax',
                  'Saxophone', 'Trombone', 'trumpet', 'tuba'],
         'percussion': 'xylophone'}
DUETS = {'string-wind': ['cf', 'clc', 'clv', 'ct', 'ef''tuv', 'vf', 'vt'],
         'string-string': ['ec', 'vc'],
         'wind-wind': ['clf', 'clt', 'cltu', 'tf', 'tut'],
         'percussion': ['xf']}

from .transforms import transforms,Processor
