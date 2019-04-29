print(f'Loading {__file__}...')

from ophyd import EpicsSignal, EpicsSignalRO

# These might need/make more sense to be split up into separate files later on.
# But while we have so few, I'm just putting them in this single file.

bpm13_sum = EpicsSignalRO('XF:07ID-BI{BPM:13}Stats5:Total_RBV', name='Downstream Izero Phosphor Intensity')
en
dm3_c1 = EpicsSignalRO('XF:07ID-BI{DM3:I400-1}:IC1_MON', name='Diagnostic Module 3 Current')

ring_current = EpicsSignalRO('SR:OPS-BI{DCCT:1}I:Real-I', name='NSLS-II Ring Current', kind='normal')

BeamstopW_I = EpicsSignal('XF:07ID-ES1{DMR:I400-1}:IC1_MON', name='WAXS Beamstop Current', kind='normal')
BeamstopS_I = EpicsSignal('XF:07ID-ES1{DMR:I400-1}:IC2_MON', name='SAXS Beamstop Current', kind='normal')
IzeroMesh   = EpicsSignal('XF:07ID-ES1{DMR:I400-1}:IC3_MON', name='Izero Mesh Drain Current', kind='normal')
IzeroDiode  = EpicsSignal('XF:07ID-ES1{DMR:I400-1}:IC4_MON', name='Izero Diode Current', kind='normal')
DM4_PD  = EpicsSignal('XF:07ID-BI{DM5:F4}Cur:I1-I', name='DM4 Current', kind='hinted')

sd.monitors.extend([IzeroMesh, ring_current])
sd.baseline.extend([IzeroMesh, ring_current, IzeroDiode, BeamstopW_I, BeamstopS_I])
# Not sure how best to do this image yet... 

#BPM13 Image:
#XF:07ID-BI{BPM:13}image1:ArrayData
