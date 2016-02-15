#LoadEventNexus(Filename='/SNS/CORELLI/IPTS-12310/nexus/CORELLI_13045.nxs.h5',outputWorkspace='van')
#LoadInstrument(Workspace='van', InstrumentName='CORELLI')
#MaskBTP(Workspace='van',Pixel="1-10,247-256")
#MaskBTP(Workspace='van',Bank="54",Tube="1")
#MaskBTP(Workspace='van',Bank="57",Tube="1")
#MaskBTP(Workspace='van',Bank="73",Tube="13")
#MaskBTP(Workspace='van',Bank="1-6,18-30,60-70,86-91")

rawVan=LoadEventNexus(Filename='/SNS/CORELLI/IPTS-12310/nexus/CORELLI_13042.nxs.h5')
LoadInstrument(Workspace=rawVan, InstrumentName='CORELLI')
rawVan2=LoadEventNexus(Filename='/SNS/CORELLI/IPTS-12310/nexus/CORELLI_13045.nxs.h5')
LoadInstrument(Workspace=rawVan2, InstrumentName='CORELLI')
rawVan =Plus(rawVan,rawVan2,ClearRHSWorkspace=True)
rawVan=ChangeBinOffset(InputWorkspace=rawVan, Offset=1336)
MaskBTP(Workspace='rawVan',Pixel="1-15,242-256")
MaskBTP(Workspace='rawVan',Bank="8",Tube="16")
MaskBTP(Workspace='rawVan',Bank="54",Tube="1")
#MaskBTP(Workspace='rawVan',Bank="58",Tube="13-16",Pixel="80-130")
#MaskBTP(Workspace='rawVan',Bank="59",Tube="1-4",Pixel="80-130")
MaskBTP(Workspace='rawVan',Bank="1-6,18-30,62-70,91")

van=mtd['rawVan']
van=ConvertUnits(van,Target="Momentum",EMode="Elastic")
van=CropWorkspace(van,XMin=2.5,XMax=10)
van=Rebin(InputWorkspace=van,Params='2.5,10,9')
sa=Rebin(InputWorkspace=van,Params='2.5,10,9',PreserveEvents='0')
flux=SumSpectra(van)
flux=Rebin(InputWorkspace=flux,Params='2.5,10,9')
flux=CompressEvents(flux,1e-5)
flux/=flux.readY(0)[0]
flux=IntegrateFlux(flux)
SaveNexus(InputWorkspace='flux',Filename='/SNS/users/rwp/Spectrum20150825New9.nxs')
SaveNexus(InputWorkspace='sa',Filename='/SNS/users/rwp/SolidAngle20150825New9.nxs')
