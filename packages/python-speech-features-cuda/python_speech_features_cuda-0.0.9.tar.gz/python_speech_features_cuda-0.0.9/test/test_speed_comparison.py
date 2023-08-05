#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 02:38:10 2020

@author: cxue2
"""

import os
os.environ['OMP_NUM_THREADS'] = '1' # export OMP_NUM_THREADS=1
os.environ['OPENBLAS_NUM_THREADS'] = '1' 
os.environ['MKL_NUM_THREADS'] = '1'
os.environ['VECLIB_MAXIMUM_THREADS'] = '1'
os.environ['NUMEXPR_NUM_THREADS'] = '1'

import python_speech_features_cuda as sfc
import python_speech_features as sf_
import matplotlib.pyplot as plt
import timeit
import cupy as cp
import numpy as np

plt.rcParams['axes.facecolor'] = 'w'
plt.rcParams['figure.facecolor'] = 'w'
plt.rcParams['savefig.facecolor'] = 'w'

sfc.env.backend = np
sfc.env.dtype = np.float32

# batch size list
lst_b = [1, 2, 4, 8, 16]

# result dictionary
hmp = {'sf_':[], 'sfc':[], 'mul':[]} 

for func in range(3):
    for be in (np, cp):
        for i in lst_b:
            
            sfc.env.backend = be
            
            sig_sf_ = np.random.rand(i, 500000).astype(sfc.env.dtype)
            sig_sfc = sfc.env.backend.asarray(sig_sf_)
            
            if func == 2:
                sig_sfc = sfc.mfcc(sig_sfc, nfft=512)
                sig_sf_ = cp.asnumpy(sig_sfc)
            
            n_iter = 1000 // i
            
            # test for sf_ mfcc
            beg = timeit.default_timer()
            for _ in range(n_iter):
                for j in range(i):
                    if func == 0:
                        sf_.mfcc(sig_sf_[j,:], nfft=512)
                    elif func == 1:
                        sf_.ssc(sig_sf_[j,:], nfft=512)
                    else:
                        sf_.delta(sig_sf_[j,:,:], 2)
                    # sf_.sigproc.framesig(sig_sf_[j,:], int(16000*.025), int(16000*.01))
            end = timeit.default_timer()
            hmp['sf_'].append((end - beg) / n_iter / i)
            print('sf_ mfcc:\t{}'.format(hmp['sf_'][-1]))
            
            # test for sfc mfcc
            beg = timeit.default_timer()
            for _ in range(n_iter):
                if func == 0:
                    sfc.mfcc(sig_sfc, nfft=512)
                elif func == 1:
                    sfc.ssc(sig_sfc, nfft=512)
                else:
                    sfc.delta(sig_sfc, 2)
                # sfc.powspec(sig_sfc, 512)
                # sfc.framesig(sig_sfc, int(16000*.025), int(16000*.01))
            end = timeit.default_timer()
            hmp['sfc'].append((end - beg) / n_iter / i)
            print('sfc mfcc:\t{}'.format(hmp['sfc'][-1]))
            
            be_str = 'np' if sfc.env.backend is np else 'cp'
            hmp['mul'].append(hmp['sf_'][-1] / hmp['sfc'][-1])
            print('mfcc|{}|{:03d}_batch|float64: x{:.2f}\n'.format(be_str, i, hmp['mul'][-1]))

# plot
fig, ax = plt.subplots(1, 3, figsize=(12, 3))
x = np.arange(5) * 2
width = .618
ax[0].bar(x - width/2, hmp['mul'][:len(lst_b)], width, color='#ffc13b', label='NumPy')
ax[0].bar(x + width/2, hmp['mul'][len(lst_b):len(lst_b)*2], width, color='#1e3d59', label='CuPy')
ax[1].bar(x - width/2, hmp['mul'][len(lst_b)*2:len(lst_b)*3], width, color='#ffc13b', label='NumPy')
ax[1].bar(x + width/2, hmp['mul'][len(lst_b)*3:len(lst_b)*4], width, color='#1e3d59', label='CuPy')
ax[2].bar(x - width/2, hmp['mul'][len(lst_b)*4:len(lst_b)*5], width, color='#ffc13b', label='NumPy')
ax[2].bar(x + width/2, hmp['mul'][len(lst_b)*5:len(lst_b)*6], width, color='#1e3d59', label='CuPy')

for i in range(3):
    ax[i].xaxis.grid(False)
    ax[i].set_xlabel('Batch Size', weight='bold')
    ax[i].set_xticklabels([0] + lst_b)
    ax[i].yaxis.grid(True)
    ax[i].set_yscale('log', basey=2)
    ax[i].set_yticks([1, 2, 2**3, 2**5, 2**7, 2**9])
    ax[i].set_ylim([1, 2**10])

ax[0].set_ylabel('Speedup', weight='bold')
ax[0].set_title('MFCC', weight='bold')
ax[0].legend()
ax[1].set_title('SSC', weight='bold')
ax[2].set_title('Delta', weight='bold')

plt.tight_layout()
# fig.savefig('../readme_plot/plot.jpg', dpi=100)