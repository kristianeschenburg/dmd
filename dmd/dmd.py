#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 19 12:11:25 2018

@author: kristianeschenburg
"""

import numpy as np

def DMD(C,n=[],p=[],h=[]):
    
    """
    Compute Dynamic Mode Decomposition of dynamical system.
    
    Parameters:
    - - - - -
        C: input data measurements of size (n x t) where n is the number of 
            variables and t the number of time points
        n: number of DMD modes to keep
        p: fraction of energy of system to keep
        h: timestep between measurements (sampling frequency)
    
    Returns:
    - - - -
        phi:
        power:
        freq: 
    """
    
    # split data matrix into one-time-step shifted arrays
    # such that Xp = A*X
    C -= np.mean(C,axis=1)[:,None]
    X = C[:,:-1]
    Xp = C[:,1:]
    
    # compute SVD of X
    [U,S,V] = np.linalg.svd(X,full_matrices=False)
    
    if (n==[]) & (p!=[]):
        n = np.where((np.cumsum(S)/np.sum(S)) >= p)[0][0]+1
        print 'Keeping {:} modes to capture {:} of energy.'.format(n,p)
        
    if n == []:
        n = X.shape[0]
    
    Ut = U[:,:n]
    Sinv = np.diag(1./S[:n])
    Vt = V[:n].T
    
    # compute reduced-dimensional representation of A-matrix
    Ap=(Ut.T).dot(Xp.dot(Vt.dot(Sinv)))
    
    # weight Ap by singular values so that modes reflect explained variance
    Ah = np.diag(S[:n]**-0.5).dot(Ap.dot(np.diag(S[:n]**0.5)))
    
    # compute eigendecomposition of weighted A matrix
    [w,v] = np.linalg.eig(Ah)
    v = np.diag(S[:n]**0.5).dot(v)
    
    # compute DMD modes from eigenvectors
    # using this approach, modes are not normalized -- norm gives power
    # of mode in data
    Phi = Xp.dot(Vt.dot(Sinv.dot(v)))
    power = np.real(np.sum(Phi*Phi.conj(),0))
    
    # by default, uses sampling frequency of HCP data
    if h == []:
        h = (14.*60+33)/1200
    # using h to convert complex eigenvalues into corresponding 
    # oscillation frequencies
    freq = np.angle(w)/(2*np.pi*h)

    return Phi,power,freq