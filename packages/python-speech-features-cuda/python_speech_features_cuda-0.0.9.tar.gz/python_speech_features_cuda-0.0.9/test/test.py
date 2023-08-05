"""
Created on Fri Jul 31 17:31:51 2020

@author: cxue2
"""

import python_speech_features_cuda as psf
import python_speech_features as psf_

import timeit
import numpy as np
import cupy as cp

psf.env.backend = cp
psf.env.dtype = np.float64

# check preemphasis
a = psf.env.backend.random.rand(50).astype(psf.env.dtype)
a_ = a.get()

b = psf.preemphasis(a, coeff=0.95)
b_ = psf_.sigproc.preemphasis(a_)
print('preemphasis:',np.allclose(b, b_))

# check magspec
# a = cp.zeros((2, 5)).astype(np.float32)
a = psf.env.backend.random.rand(10, 50).astype(psf.env.dtype)
a_ = a.get()

c = psf.magspec(a)
c_ = psf_.sigproc.magspec(a_, NFFT=a_.shape[1])
print('magspec:', np.allclose(c, c_))

# check powspec
d = psf.powspec(a)
d_ = psf_.sigproc.powspec(a_, NFFT=a_.shape[1])
print('powspec:', np.allclose(d, d_))

# check logpowspec w/norm
e = psf.logpowspec(a)
e_ = psf_.sigproc.logpowspec(a_, NFFT=a_.shape[1])
print('logpowspec w/ norm:', np.allclose(e, e_))

# check logpowspec w/norm
f = psf.logpowspec(a, norm=False)
f_ = psf_.sigproc.logpowspec(a_, NFFT=a_.shape[1], norm=0)
print('logpowspec w/o norm:', np.allclose(f, f_))

a = psf.env.backend.random.rand(11).astype(psf.env.dtype)
a_ = a.get()

g = psf.framesig(a, 10, 11)
g_ = psf_.sigproc.framesig(a_, 10, 11)
print('framesig:', np.allclose(g, g_))

# n_iter = 10000
# starttime = timeit.default_timer()
# for _ in range(n_iter):
#     psf.framesig(a, 10, 9)
# print('The avg. time:', (timeit.default_timer() - starttime) / n_iter)

# n_iter = 10000
# starttime = timeit.default_timer()
# for _ in range(n_iter):
#     psf_.sigproc.framesig(a_, 10, 9)
# print('The avg. time:', (timeit.default_timer() - starttime) / n_iter)

# psf.env.backend = np
# psf.env.dtype = np.float64

# check get filterbank
h = psf.get_filterbanks(samplerate=16000, nfilt=26, nfft=401, lowfreq=0, highfreq=None)
h_ = psf_.get_filterbanks(samplerate=16000, nfilt=26, nfft=401, lowfreq=0, highfreq=None)
print('get_filterbanks:', np.allclose(h, h_))

# check fbank
sig = psf.env.backend.random.rand(2, 20000).astype(psf.env.dtype)
# sig = psf.env.backend.zeros((2, 20000)).astype(psf.env.dtype)
sig_ = sig.get()[1,:]

tmp, eng = psf.fbank(sig, nfft=401)
tmp_, eng_ = psf_.fbank(sig_, nfft=401)
print('fbank_tmp:', np.allclose(tmp[1,:], tmp_))
print('fbank_eng:', np.allclose(eng[1,:], eng_))
    
# check logfbank
tmp, eng = psf.logfbank(sig, nfft=401)
tmp_ = psf_.logfbank(sig_, nfft=401)
print('logfbank_tmp:', np.allclose(tmp[1,:], tmp_))
    
# check mfcc
tmp = psf.mfcc(sig, nfft=401)
tmp_ = psf_.mfcc(sig_, nfft=401)
print('mfcc:', np.allclose(tmp[1,:], tmp_))

# check mfcc with window
win = psf.env.backend.hamming(int(round(16000 * .025))).astype(psf.env.dtype)
tmp = psf.mfcc(sig, nfft=401, winfunc=win)
tmp_ = psf_.mfcc(sig_, nfft=401, winfunc=np.hamming)
print('mfcc_win:', np.allclose(tmp[1,:], tmp_))

# check delta
fea = psf.env.backend.copy(tmp)
tmp = psf.delta(fea, n=2)
tmp_ = psf.delta(fea[1,:], n=2)
print('delta:', np.allclose(tmp[1,:], tmp_))
    
# check scc
tmp = psf.ssc(sig, nfft=401)
tmp_ = psf_.ssc(sig_, nfft=401)
print('ssc:', np.allclose(tmp[1,:], tmp_))

# a = np.random.rand(10)
# window = 5
# step = 3
# shape = a.shape[:-1] + (a.shape[-1] - window + 2, window)
# strides = a.strides + (a.strides[-1],)
# tmp = np.lib.stride_tricks.as_strided(a, shape=shape, strides=strides)[::step]
# tmp_ = psf_.sigproc.framesig(a, window, step)