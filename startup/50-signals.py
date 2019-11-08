run_report(__file__)

from ophyd import EpicsSignalRO

# These might need/make more sense to be split up into separate files later on.
# But while we have so few, I'm just putting them in this single file.

bpm13_sum = EpicsSignalRO('XF:07ID-BI{BPM:13}Stats5:Total_RBV', name='Downstream Izero Phosphor Intensity')

ring_current = EpicsSignalRO('SR:OPS-BI{DCCT:1}I:Real-I', name='NSLS-II Ring Current', kind='normal')

Beamstop_WAXS = EpicsSignalRO('XF:07ID-ES1{DMR:I400-1}:IC1_MON',name = 'WAXS Beamstop')
Beamstop_SAXS = EpicsSignalRO('XF:07ID-ES1{DMR:I400-1}:IC2_MON',name = 'SAXS Beamstop')
IzeroDiode    = EpicsSignalRO('XF:07ID-ES1{DMR:I400-1}:IC4_MON',name = 'Izero Photodiode')

IzeroMesh    = EpicsSignalRO('XF:07ID-ES1{Slt1:I400-1}:IC4_MON',name = 'Izero Mesh')
SlitOut_I    = EpicsSignalRO('XF:07ID-ES1{Slt1:I400-1}:IC1_MON',name = 'Slit Outboard')
SlitBottom_I = EpicsSignalRO('XF:07ID-ES1{Slt1:I400-1}:IC2_MON',name = 'Slit Bottom')
SlitTop_I    = EpicsSignalRO('XF:07ID-ES1{Slt1:I400-1}:IC3_MON',name = 'Slit Top')

TransmissionDiode = EpicsSignalRO('XF:07ID-BI{DM7:I400-1}:IC4_MON',name = 'RSoXS Transmission Photodiode')
DM4_PD            = EpicsSignalRO('XF:07ID-BI{DM5:F4}Cur:I3-I', name='DM4 Current', kind='hinted')


sd.monitors.extend([ring_current,Beamstop_WAXS,Beamstop_SAXS,IzeroDiode,IzeroMesh])
sd.baseline.extend([ring_current,Beamstop_WAXS,Beamstop_SAXS,IzeroDiode,IzeroMesh,
                    SlitOut_I,SlitBottom_I,SlitTop_I,TransmissionDiode,DM4_PD])
