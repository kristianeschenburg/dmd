#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 21 17:13:26 2018

@author: kristianeschenburg
"""

import argparse,sys
import scipy.io as sio

sys.path.append('../../surface_utilities/')
sys.path.append('../../metrics/metrics/')
import adjacency as adj
import resampling

parser = argparse.ArgumentParser()
parser.add_argument('--surfacefile',help='Input surface file.',
                    required=True,type=str)
parser.add_argument('-d','--distances',help='Distances to compute resample for.',
                    required=True,type=int,nargs='+')
parser.add_argument('--samples',help='Number of vertex reasmples to take.',
                    required=True,type=int)
parser.add_argument('--output',help='Output file basename to sample resamples.',
                    required=True,type=str)

args = parser.parse_args()

S = adj.SurfaceAdjacency(args.surfacefile)
S.generate()

samples = args.samples

for d in args.distances:
    
    output = ''.join([args.output,'.Distance.{:}.mat'.format(d)])
    
    resamples = resampling.indexresample(S.adjacency,distance=d,samples=samples)
    rsamp = {'resamples': resamples}
    sio.savemat(output,rsamp)