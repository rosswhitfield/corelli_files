import tube
tube.readCalibrationFile('CalibTable','/SNS/users/rwp/corelli/tube_calibration2/CalibTable2_combined.txt')

for run in range(83349,83432+1):
    Load(Filename='CORELLI_{}'.format(run),
         OutputWorkspace='run',
         FilterByTofMin=1000,
         FilterByTofMax=16666)
    ApplyCalibration('run','CalibTable')
    ConvertToMD(InputWorkspace='run',
                OutputWorkspace='output',
                QDimensions='Q3D',
                dEAnalysisMode='Elastic',
                Q3DFrames='Q_sample',
                MinValues=[-15,-5,-15],
                MaxValues=[15,5,15],
                OverwriteExisting=False)
                
SaveMD('output', '/SNS/CORELLI/IPTS-21655/shared/rwp/CORELLI_83349_83432_tubecal_MDE.nxs')
#output=LoadMD('/SNS/CORELLI/IPTS-21655/shared/rwp/CORELLI_83349_83432_tubecal_MDE.nxs')

FindPeaksMD(InputWorkspace='output', PeakDistanceThreshold=0.5, MaxPeaks=2000, OutputWorkspace='peaks')
FindUBUsingFFT(PeaksWorkspace='peaks', MinD=5, MaxD=20)
ShowPossibleCells(PeaksWorkspace='peaks')
SelectCellWithForm(PeaksWorkspace='peaks', FormNumber=26, Apply=True)
IndexPeaks(PeaksWorkspace='peaks')

# 6.684847   18.301256   18.670389   90.003998   90.119247   89.780933

OptimizeLatticeForCellType(PeaksWorkspace='peaks', CellType='Orthorhombic', Apply=True, OutputDirectory='/SNS/users/rwp/.')

# 6.684953   18.316274   18.654818   90.000000   90.000000   90.000000 



SCDCalibratePanels(PeakWorkspace='peaks', a=6.56, b=18.27, c=18.587, alpha=90, beta=90, gamma=90, ChangeL1=False)

SCDCalibratePanels(PeakWorkspace='peaks', a=6.56, b=18.27, c=18.587, alpha=90, beta=90, gamma=90, ChangeL1=False, DetCalFilename='/SNS/users/rwp/SCDCalibrate.DetCal', ColFilename='/SNS/users/rwp/ColCalcvsTheor.nxs', RowFilename='/SNS/users/rwp/RowCalcvsTheor.nxs', TofFilename='/SNS/users/rwp/TofCalcvsTheor.nxs')


SaveIsawPeaks('peaks', Filename='/SNS/users/rwp/corelli/cal_2019_01_Natrolite/peaks_tubeCal.peaks')
