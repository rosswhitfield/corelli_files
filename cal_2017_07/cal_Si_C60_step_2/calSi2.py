import numpy as np
from mantid.simpleapi import *

LoadNexus(Filename='../align/AlignCombined.nxs', OutputWorkspace='AlignCombined')

#DReference = [0.9179, 0.9600, 1.0451, 1.1085, 1.2458, 1.3576, 1.6374, 1.9200, 3.1353]
DReference = [1.1085, 1.2458, 1.3576, 1.6374, 1.9200, 3.1353]

Load(Filename='CORELLI_47327-47334', OutputWorkspace='rawSi')
CopyInstrumentParameters('AlignCombined', 'rawSi')

SetInstrumentParameter(Workspace="rawSi",ParameterName="t0_formula",Value="(23.5 * exp(-incidentEnergy/205.8))")
ModeratorTzero(InputWorkspace="rawSi",OutputWorkspace="rawSi",EMode="Elastic")

MaskBTP(Workspace='rawSi',Pixel="1-16,241-256")
ConvertUnits(InputWorkspace='rawSi',OutputWorkspace='siliconD',Target='dSpacing')
SumNeighbours(InputWorkspace="siliconD", OutputWorkspace="siliconD", SumX=1, SumY=16)
Rebin(InputWorkspace='siliconD',OutputWorkspace='siliconD',Params='0.5,-0.004,3.5')

GetDetOffsetsMultiPeaks(
    InputWorkspace = 'siliconD',
    DReference = DReference,
    FitWindowMaxWidth=0.1,
    BackgroundType = "Flat",
    OutputWorkspace = 'offset')

SaveCalFile(Filename='cal_Si2_47327-47334_sum16_step2.cal',
            OffsetsWorkspace="offset",
            MaskWorkspace='Mask')
ConvertDiffCal(OffsetsWorkspace="offset",
               OutputWorkspace="cal")
SaveDiffCal(CalibrationWorkspace="cal",
            MaskWorkspace="Mask",
            Filename='cal_Si2_47327-47334_sum16_step2.h5')
maskNumberPeaksFitted = np.where(mtd['NumberPeaksFitted'].extractY() <3)
MaskDetectors('Mask',DetectorList=maskNumberPeaksFitted[0])
SaveCalFile(Filename='cal_Si2_47327-47334_sum16_step2_mask_lt_3.cal',
            OffsetsWorkspace="offset",
            MaskWorkspace='Mask')
ConvertDiffCal(OffsetsWorkspace="offset",
               OutputWorkspace="cal")
SaveDiffCal(CalibrationWorkspace="cal",
            MaskWorkspace="Mask",
            Filename='cal_Si2_47327-47334_sum16_step2_mask_lt_3.h5')
