#!/usr/bin/env python

import h5py
import numpy as np
import matplotlib.pyplot as plt
import glob

filenames = glob.glob('/SNS/CORELLI/IPTS-23139/nexus/CORELLI_*.nxs.h5')

for filename in filenames:
    with h5py.File(filename, 'r') as f:
        try:
            tdc = f['entry/DASlogs/chopper4_TDC/value'].value.astype(np.int64)
            wl = f['entry/DASlogs/BL9:Chop:Skf4:WavelengthSet/value'].value[0]
            phaseDelay = f['entry/DASlogs/BL9:Chop:Skf4:PhaseTimeDelaySet/value'].value[0]
            diff = (tdc[1:] - tdc[:-1])/100
            unique, unique_counts = np.unique(diff, return_counts=True)
            plt.clf()
            plt.plot(unique, unique_counts)
            plt.xlabel("Chopper period (100ns)")
            plt.ylabel("Period frequency")
            plt.title("{} - wavelength = {} - Phase Delay = {:.2f}".format(filename.split('/')[-1],wl, phaseDelay))
            plt.xlim(34060, 34100)
            plt.savefig("images/"+filename.split('/')[-1]+".png")
        except KeyError:
            pass
