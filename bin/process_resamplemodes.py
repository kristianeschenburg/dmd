#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 21 17:34:14 2018

@author: kristianeschenburg
"""

import argparse,h5py

import niio
import numpy as np

from scipy.spatial.distance import cdist

parser = argparse.ArgumentParser()
parser.add_argument('--modefile',help='DMD mode file.',required=True,type=str)
parser.add_argument('--resamplefile',help='Resampled index file.',
                    required=True,type=str)
parser.add_argument('--filteredfile',help='Output file to save filtered modes.',
                    required=True,type=str)

args = parser.parse_args()

modes = niio.load(args.modefile)
samples = niio.load(args.resamplefile).astype(np.int32)

nmodes = modes.shape[1]
nsamps = samples.shape[1]

correlations = np.zeros((nsamps,nmodes))

# loop over each mode
for k in np.arange(nmodes):
    
    # correlate mode with its resampled vectors
    corr = 1-cdist(modes[:,k].T,modes[:,k][samples].T,metric='correlation')
    correlations[:,k] = corr
    
# compute mean and standard deviations of the correlations for each mode
mu = correlations.mean(0)
std = correlations.std(0)

# if the mean mode correlation is greater than (grand mean + 1*std(means))
# keep mode
idx = mu>(correlations.mean() + 1.*np.std(mu))

print 'Keeping %.1f%% (%i) of modes.' % (100.*idx.sum()/len(idx),idx.sum())

passed = modes[:,idx]
failed = modes[:,~idx]

with h5py.File(args.filteredfile,'w') as hf:
    hf.create_dataset(name='passed',data=passed)
    hf.create_dataset(name='failed',data=failed)

hf.close()