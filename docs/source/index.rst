.. dmd documentation master file, created by
   sphinx-quickstart on Thu Oct 17 20:49:12 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to dmd's documentation!
===============================

*************
Introduction
*************

DMD, or *Dynamic Mode Decomposition*, is a modal decomposition algorithm that
solves for the linear operator that advances some dynamical system.  The algorithm 
was first proposed by 
`Peter Schmid <https://hal-polytechnique.archives-ouvertes.fr/hal-01020654/file/DMS0022112010001217a.pdf>`_ [1]_ to study coherent features of fluid flow.  
We recently applied this method to study coherent patterns of brain activation using 
`resting-state fMRI <https://www.frontiersin.org/articles/10.3389/fncom.2019.00075/abstract>`_ [2]_.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   modules
   usage


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. [1] Schmid, Peter.  (2010).  Dynamic Mode Decomposition of Numerical and Experimental Data. 
   Journal of Fluid Mechanics.

.. [2] Kunert-Grag, James, Eschenburg, Kristian, Galas, David, Kutz, J. Nathan, Rane, Swati, & Brunton, Bingni.  (2019).
   Extracting Reproducible Time-Resolved Resting State Networks using Dynamic Mode Decomposition. Froniters Comp. Neuro.