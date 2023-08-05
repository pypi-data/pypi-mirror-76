# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 18:05:20 2020

@author: Gideon Pomeranz
"""

### Packages ###
# This module lets us call shell commands via os.system
import os
# This module allows us to configure this script so it can be called with
# options from the command line

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scanpy as sc

from collections import OrderedDict
from sklearn.decomposition import TruncatedSVD
from sklearn.manifold import TSNE
from sklearn.preprocessing import scale

from sklearn.preprocessing import normalize
from sklearn.neighbors import NeighborhoodComponentsAnalysis
#----------------------------------------------------------------------------#
def visualise(processed_file,num_pca,num_nca,num_tsne,neighbours,top_genes):
    
    ### Read processed data ###
    # define raw file
    processed_file = processed_file
    # read in the combined data that was saved from kb_align.py
    data = sc.read(processed_file)
 #----------------------------------------------------------------------------#     
    ### Parameters ###
    num_TSNE = num_tsne
    state = 42
    metric = "euclidean"
    n_neighbors = neighbours  # 30
    num_PCA = num_pca  # 50
    num_NCA = num_nca  # 10
    
    n_top_genes = top_genes
    n_bins = 20
    flavor="seurat"
 #----------------------------------------------------------------------------#   
    ### Clustering ###

    sc.pp.neighbors(data, n_neighbors=n_neighbors, n_pcs=num_PCA, random_state=state)
    sc.tl.leiden(data, random_state=state)
 #----------------------------------------------------------------------------#  
    ### PCA/NCA ###
    sc.tl.pca(data,n_comps=num_PCA, random_state=state,use_highly_variable=True)






  