#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 21 22:24:01 2018

@author: kristianeschenburg
"""

import argparse

import niio
import numpy as np

from sklearn.decomposition import FastICA

parser = argparse.ArgumentParser()
parser.add_argument('--restfile',help='Resting state file.',
                    required=True,type=str)
parser.add_argument('--output',help='Output DMD mode file.',
                    required=True,type=str)
parser.add_argument('--ncomponents',help='Number of ICA components.',
                    required=True,type=int)
parser.add_argument('--hemi',help='Hemisphere to process.',
                    required=True,type=str,choices=['L','R'])

args = parser.parse_args()

hemi_map = {'L': 'CortexLeft',
            'R': 'CortexRight'}

try:
    resting = niio.load(args.restfile)
except:
    raise('Resting state file does not exist.')
else:
    n,p = resting.shape
    print 'State: {:}, Time: {:}'.format(n,p)

# compute Independent Components
F = FastICA(n_components=args.ncomponents)
F.fit(resting.T)

components = F.components.tolist()

niio.save(components,args.output,hemi_map[args.hemi])