#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Licensed under a 3-clause BSD style license - see LICENSE.rst

"""

"""

import numpy as np
from numpy import ma



N = len(x)
dx = np.diff(x)
fwd = []
bwd = []
for i in range(1,N):


def bin_noise(x, l):
    """
    """
    dx = np.diff(x, axis=0)
    N = len(x)
    noise = ma.masked_all(N)
    half_window = math.ceil(l/2)
    for i in range(half_window, N-half_window):
        ini = max(0, i - half_window)
        fin = min(N, i + half_window)
        tmp = dx[ini:fin]
        if tmp.size >= l/2.:
            noise[i] = np.absolute(tmp).mean(axis=0) - np.absolute(tmp.mean(axis=0))
            #tmp = np.absolute(tmp).sum()/tmp.sum()
            #noise[i] = tmp - np.sign(tmp)
    return noise


class Bin_Variance(object):
    def __init__(self, data, varname, cfg):
        self.data = data
        self.varname = varname
        self.cfg = cfg

        self.set_features()

    def keys(self):
        return self.features.keys() + \
            ["flag_%s" % f for f in self.flags.keys()]

    def set_features(self):
        self.features = {'bin_variance': bin_variance(self.data[self.varname],
            self.cfg['l'])}

    def test(self):
        self.flags = {}
        try:
            threshold = self.cfg['threshold']
        except:
            print("Deprecated cfg format. It should contain a threshold item.")
            threshold = self.cfg

        try:
            flag_good = self.cfg['flag_good']
            flag_bad = self.cfg['flag_bad']
        except:
            print("Deprecated cfg format. It should contain flag_good & flag_bad.")
            flag_good = 1
            flag_bad = 4

        assert (np.size(threshold) == 1) and \
                (threshold is not None) and \
                (np.isfinite(threshold))   

        flag = np.zeros(self.data[self.varname].shape, dtype='i1')
        flag[np.nonzero(self.features['bin_variance'] > threshold)] = \
                flag_bad
        flag[np.nonzero(self.features['bin_variance'] <= threshold)] = \
                flag_good
        flag[ma.getmaskarray(self.data[self.varname])] = 9
        self.flags['bin_variance'] = flag
