# import mantid algorithms, numpy and matplotlib
from mantid.simpleapi import *
from mantid.kernel import V3D

inst = LoadEmptyInstrument(InstrumentName='TOPAZ')

peaks = CreatePeaksWorkspace(inst, NumberOfPeaks=0)

SetUB(peaks, a=2, b=2, c=2)

peak1 = peaks.createPeakHKL(V3D(1, 1, 0))
peak1.setRunNumber(1)
peaks.addPeak(peak1)
SetGoniometer(peaks, Axis0='180,0,1,0,1')
peak2 = peaks.createPeakHKL(V3D(-1, -1, 0))
peak2.setRunNumber(2)
peaks.addPeak(peak2)

satellite = PredictSatellitePeaks(peaks, ModVector1='0.2,0,0', MaxOrder=1)


peaks2 = CreatePeaksWorkspace(inst, NumberOfPeaks=0)
SetUB(peaks2, a=2, b=2, c=2)
satellite2 = PredictSatellitePeaks(peaks2, ModVector1='0.2,0,0', MaxOrder=1, IncludeAllPeaksInRange=True)
