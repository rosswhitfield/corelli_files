from mantid.simpleapi import *
import numpy as np

# Generate fit window workspace
DReference = [2.7251,2.8904,4.2694,5.0063,8.1753]
fitwindict = {}
fitwindict[8.1753] = (7.5, 10.0)
fitwindict[5.0063] = (4.85,6.0)
fitwindict[4.2694] = (4.0, 4.9)
fitwindict[2.8904] = (2.82, 3.0)
fitwindict[2.7251] = (2.65, 2.81)
FinalDReference = sorted(fitwindict.keys())

fitwinws = CreateEmptyTableWorkspace()
fitwinws.addColumn("int", "spectrum")
for ipk in xrange(len(FinalDReference)):
	fitwinws.addColumn("double", "Peak_%d_Left"%(ipk))
	fitwinws.addColumn("double", "Peak_%d_Right"%(ipk))

row = [-1]
for refpeak in FinalDReference:
		leftbound = fitwindict[refpeak][0]
		rightbound = fitwindict[refpeak][1]
		row.append(leftbound)
		row.append(rightbound)

fitwinws.addRow(row)

for run in range(20501,20509):
        LoadEventNexus(Filename='/SNS/CORELLI/IPTS-15796/nexus/CORELLI_'+str(run)+'.nxs.h5', OutputWorkspace='rawC60')
        LoadInstrument(Workspace="rawC60",Filename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",RewriteSpectraMap=False)
        SetInstrumentParameter(Workspace="rawC60",ParameterName="t0_formula",Value="(23.5 * exp(-incidentEnergy/205.8))")
        ModeratorTzero(InputWorkspace="rawC60",OutputWorkspace="rawC60",EMode="Elastic")
        MaskBTP(Workspace='rawC60',Pixel="1-16,241-256")
        ConvertUnits(InputWorkspace='rawC60',OutputWorkspace='C60D',Target='dSpacing')
        Rebin(InputWorkspace='C60D',OutputWorkspace='C60D',Params='0.5,-0.004,10')
        SumNeighbours(InputWorkspace="C60D", OutputWorkspace="C60D", SumX=1, SumY=4)
        GetDetOffsetsMultiPeaks(
                InputWorkspace = 'C60D',
                DReference = FinalDReference,
                FitwindowTableWorkspace='fitwinws',
                PeakFunction = "Gaussian",
                BackgroundType = "Linear",
                HighBackground = True,
                OutputWorkspace = 'offset',
                MaskWorkspace='mask')
        # Save calibration
        SaveCalFile(Filename='/SNS/users/rwp/corelli/cal_2016_02/cal_C60_'+str(run)+'_sum4.cal',
                    OffsetsWorkspace="offset",
                    MaskWorkspace='mask')
        maskNumberPeaksFitted = np.where(mtd['NumberPeaksFitted'].extractY() <3)
        MaskDetectors('mask',DetectorList=maskNumberPeaksFitted[0])
        SaveCalFile(Filename='/SNS/users/rwp/corelli/cal_2016_02/cal_C60_'+str(run)+'_sum4_mask_lt_3.cal',
                    OffsetsWorkspace="offset",
                    MaskWorkspace='mask')
