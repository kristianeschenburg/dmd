#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 21 13:24:40 2018

@author: kristianeschenburg
"""

import argparse,sys

import niio
import numpy as np

sys.path.append('../dmd/')
from dmd import DMD

parser = argparse.ArgumentParser()
parser.add_argument('--restfile',help='Resting state file.',
                    required=True,type=str)
parser.add_argument('--output',help='Output DMD mode file.',
                    required=True,type=str)
parser.add_argument('--hemi',help='Hemisphere to process.',
                    required=True,type=str,choices=['L','R'])

args = parser.parser_args()

hemi_map = {'L': 'CortexLeft',
            'R': 'CortexRight'}

try:
    resting = niio.load(args.restfile)
except:
    raise('Resting state file does not exist.')

# compute DMD modes
[modes,power,_] = DMD(resting)

# Remove mode conjugate pair
inds = np.arange(0,len(power),2)
modes = modes[:,inds]

modes = modes.T.tolist()
niio.save(modes,args.output,hemi_map[args.hemi])