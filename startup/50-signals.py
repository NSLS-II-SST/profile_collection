print(f'Loading {__file__}...')

from ophyd import EpicsSignal, EpicsSignalRO

# These might need/make more sense to be split up into separate files later on.
# But while we have so few, I'm just putting them in this single file.

bpm13_sum = EpicsSignalRO('XF:07ID-BI{BPM:13}Stats5:Total_RBV', name='bpm13_sum')

dm3_c1 = EpicsSignalRO('XF:07ID-BI{DM3:I400-1}:IC1_MON', name='dm3_c1')

ring_current = EpicsSignalRO('SR:OPS-BI{DCCT:1}I:Real-I', name='ring_current', kind='normal')

BeamstopW_I = EpicsSignal('XF:07ID-ES1{DMR:I400-1}:IC1_MON', name='BeamstopW_I')
BeamstopS_I = EpicsSignal('XF:07ID-ES1{DMR:I400-1}:IC2_MON', name='BeamstopS_I')
IzeroMesh   = EpicsSignal('XF:07ID-ES1{DMR:I400-1}:IC3_MON', name='IzeroMesh', kind='normal')
IzeroDiode  = EpicsSignal('XF:07ID-ES1{DMR:I400-1}:IC4_MON', name='IzeroDiode')

sd.monitors.extend([IzeroMesh, ring_current])
sd.baseline.extend([IzeroMesh, ring_current])
# Not sure how best to do this image yet... 

#BPM13 Image:
#XF:07ID-BI{BPM:13}image1:ArrayData
