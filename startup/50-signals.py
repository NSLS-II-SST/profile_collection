print(f'Loading {__file__}...')

from ophyd import EpicsSignal, EpicsSignalRO

# These might need/make more sense to be split up into separate files later on.
# But while we have so few, I'm just putting them in this single file.

bpm13_sum = EpicsSignalRO('XF:07ID-BI{BPM:13}Stats5:Total_RBV', name='bpm13_sum')

dm3_c1 = EpicsSignalRO('XF:07ID-BI{DM3:I400-1}:IC1_MON', name='dm3_c1')

BeamstopW_I = EpicsSignal('XF:07ID-ES1{DMR:I400-1}:IC1_MON', name='BeamstopW_I')
BeamstopS_I = EpicsSignal('XF:07ID-ES1{DMR:I400-1}:IC2_MON', name='BeamstopS_I')
IzeroMesh   = EpicsSignal('XF:07ID-ES1{DMR:I400-1}:IC3_MON', name='IzeroMesh')
IzeroDiode  = EpicsSignal('XF:07ID-ES1{DMR:I400-1}:IC4_MON', name='IzeroDiode')
SlitO_I     = EpicsSignal('XF:07ID-ES1{Slt1:I400-1}:IC1_MON', name='SlitO_I')
SlitB_I     = EpicsSignal('XF:07ID-ES1{Slt1:I400-1}:IC2_MON', name='SlitB_I')
SlitT_I     = EpicsSignal('XF:07ID-ES1{Slt1:I400-1}:IC3_MON', name='SlitT_I')
SlitI_I     = EpicsSignal('XF:07ID-ES1{Slt1:I400-1}:IC4_MON', name='SlitI_I')


# Not sure how best to do this image yet... 

#BPM13 Image:
#XF:07ID-BI{BPM:13}image1:ArrayData
