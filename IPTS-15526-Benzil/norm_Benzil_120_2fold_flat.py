from mantid.simpleapi import *
outputdir="/SNS/CORELLI/IPTS-15526/shared/"
LoadNexus(Filename='/SNS/CORELLI/shared/Vanadium/2016B/SolidAngle20160720NoCC.nxs', OutputWorkspace='sa')
LoadNexus(Filename='/SNS/CORELLI/shared/Vanadium/2016B/Spectrum20160720NoCC.nxs', OutputWorkspace='flux')

#MaskBTP(workspace='sa',Pixel='1-16,241-256')
MaskBTP(workspace='sa',Bank='69-72')


#load in background
bkg=LoadEventNexus('/SNS/CORELLI/IPTS-15796/nexus/CORELLI_28124.nxs.h5')
MaskDetectors(Workspace=bkg,MaskedWorkspace='sa')
pc_bkg=sum(bkg.getRun()['proton_charge'].value)
print 'pc_bkg=:'+str(pc_bkg)

#mesh scan at 100K, 20 mins/angle, combined both 5mins and 20 mins at 100K
runs = range(29533,29536)+range(29556,29589)+range(29589,29625)

#runs = range(29533,29536)+range(29556,29589)
#runs = [29625]
if mtd.doesExist('normMD'):
    DeleteWorkspace('normMD')
if mtd.doesExist('dataMD'):
    DeleteWorkspace('dataMD')

for r in runs:
        filename='/SNS/CORELLI/IPTS-15526/nexus/CORELLI_'+str(r)+'.nxs.h5'
        print 'Loading run number:'+ str(r)
        dataR=LoadEventNexus(Filename=filename)
        LoadInstrument(Workspace= dataR, Filename='/SNS/CORELLI/shared/Calibration/CORELLI_Definition_cal_20160310.xml',RewriteSpectraMap=False)
        MaskDetectors(Workspace=dataR,MaskedWorkspace='sa')
        pc_data=sum(dataR.getRun()['proton_charge'].value)
        print 'pc_data=:'+str(pc_data)
        dataR=dataR - bkg*pc_data/pc_bkg
        dataR=ConvertUnits(dataR,Target="Momentum",EMode="Elastic")
        dataR=CropWorkspace(dataR,XMin=2.5,XMax=10)
        SetGoniometer(dataR,Axis0="BL9:Mot:Sample:Axis1,0,1,0,1") 
        LoadIsawUB(InputWorkspace=dataR,Filename="/SNS/users/rwp/benzil/benzil_Hexagonal.mat")
        md=ConvertToMD(InputWorkspace=dataR,QDimensions='Q3D',dEAnalysisMode='Elastic', Q3DFrames='HKL',
                       QConversionScales='HKL',LorentzCorrection='0',MinValues='-10.1,-10.1,-5.1',MaxValues='10.1,10.1,5.1')
        a1,b1=MDNormSCD(InputWorkspace='md',FluxWorkspace='flux',SolidAngleWorkspace='sa',
                      AlignedDim0="[H,0,0],-10.1,10.1,401",
                      AlignedDim1="[0,K,0],-10.1,10.1,401",
                      AlignedDim2="[0,0,L],-5.1,5.1,101")
        ub=dataR.sample().getOrientedLattice().getUB()
        SetUB(dataR, UB=ub*-1)
        md=ConvertToMD(InputWorkspace=dataR,QDimensions='Q3D',dEAnalysisMode='Elastic', Q3DFrames='HKL',
                       QConversionScales='HKL',LorentzCorrection='0',MinValues='-10.1,-10.1,-5.1',MaxValues='10.1,10.1,5.1')
        a2,b2=MDNormSCD(InputWorkspace='md',FluxWorkspace='flux',SolidAngleWorkspace='sa',
                      AlignedDim0="[H,0,0],-10.1,10.1,401",
                      AlignedDim1="[0,K,0],-10.1,10.1,401",
                      AlignedDim2="[0,0,L],-5.1,5.1,101")
        if mtd.doesExist('dataMD'):
                dataMD=dataMD+a1+a2
        else:
                dataMD=CloneMDWorkspace(a1)
                dataMD+=a2
        if mtd.doesExist('normMD'):
                normMD=normMD+b1+b2
        else:
                normMD=CloneMDWorkspace(b1)
                normMD+=b2
normData_100K=dataMD/normMD
SaveMD(Inputworkspace=dataMD,Filename='/SNS/users/rwp/benzil/benzil_100K_data_2.nxs')
SaveMD(Inputworkspace=normMD,Filename='/SNS/users/rwp/benzil/benzil_100K_norm_2.nxs')
SaveMD(Inputworkspace=normData_100K,Filename='/SNS/users/rwp/benzil/benzil_100K_normData_2.nxs')
