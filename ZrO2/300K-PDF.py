outDir = '/SNS/users/rwp/corelli/ZrO2/'

ConvertMultipleRunsToSingleCrystalMD(Filename='CORELLI_8192:8246',SetGoniometer=True,Axis0='BL9:Mot:Sample:Axis1,0,1,0,1',OutputWorkspace='md',MinValues=[-15,-15,-15],MaxValues=[15,15,15])
FindPeaksMD(InputWorkspace='md', PeakDistanceThreshold=0.25, DensityThresholdFactor=1000000, OutputWorkspace='peaks')
FindUBUsingFFT(PeaksWorkspace='peaks', MinD=4, MaxD=6)
ShowPossibleCells(PeaksWorkspace='peaks')
SelectCellOfType(PeaksWorkspace='peaks', CellType='Orthorhombic', Centering='F', Apply=True)
IndexPeaks(PeaksWorkspace='peaks')

SaveIsawUB('peaks', outDir+'ZrO2_300K.mat')


SingleCrystalDiffuseReduction(Filename='CORELLI_8192:8246',
                              SolidAngle='/SNS/CORELLI/shared/Vanadium/2015A/SolidAngle20150411.nxs',
                              Flux='/SNS/CORELLI/shared/Vanadium/2015A/Spectrum20150411.nxs',
                              OutputWorkspace='output',
                              SetGoniometer=True,
                              Axis0="BL9:Mot:Sample:Axis1,0,1,0,1",
                              UBMatrix=outDir+'ZrO2_300K.mat',
                              BinningDim0='-10.02,10.02,501',
                              BinningDim1='-10.02,10.02,501',
                              BinningDim2='-10.02,10.02,501')
