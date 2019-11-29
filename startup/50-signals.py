run_report(__file__)

from ophyd import EpicsSignalRO

# These might need/make more sense to be split up into separate files later on.
# But while we have so few, I'm just putting them in this single file.

bpm13_sum = EpicsSignalRO('XF:07ID-BI{BPM:13}Stats5:Total_RBV', name='Downstream Izero Phosphor Intensity')

ring_current = EpicsSignalRO('SR:OPS-BI{DCCT:1}I:Real-I', name='NSLS-II Ring Current', kind='normal')
Beamstop_WAXS = EpicsSignalRO('XF:07ID-ES1{DMR:I400-1}:IC1_MON',name = 'WAXS Beamstop', kind='normal')
Beamstop_SAXS = EpicsSignalRO('XF:07ID-ES1{DMR:I400-1}:IC2_MON',name = 'SAXS Beamstop', kind='normal')
IzeroDiode    = EpicsSignalRO('XF:07ID-ES1{DMR:I400-1}:IC4_MON',name = 'Izero Photodiode', kind='normal')

IzeroMesh    = EpicsSignalRO('XF:07ID-ES1{Slt1:I400-1}:IC4_MON',name = 'Izero Mesh I400', kind='normal')
Sample_Drain = EpicsSignalRO('XF:07ID-ES1{Slt1:I400-1}:IC1_MON',name = 'RSoXS Drain', kind='normal')
SlitBottom_I = EpicsSignalRO('XF:07ID-ES1{Slt1:I400-1}:IC2_MON',name = 'Slit Bottom', kind='normal')
SlitTop_I    = EpicsSignalRO('XF:07ID-ES1{Slt1:I400-1}:IC3_MON',name = 'Slit Top', kind='normal')


quadem1    = EpicsSignalRO('XF:07ID1-BI{EM:1}EM180:Current1:MeanValue_RBV',name = 'QuadEM Channel 1', kind='normal')
quadem2    = EpicsSignalRO('XF:07ID1-BI{EM:1}EM180:Current2:MeanValue_RBV',name = 'QuadEM Channel 2', kind='normal')
quadem3    = EpicsSignalRO('XF:07ID1-BI{EM:1}EM180:Current3:MeanValue_RBV',name = 'QuadEM Channel 3', kind='normal')
quadem4    = EpicsSignalRO('XF:07ID1-BI{EM:1}EM180:Current4:MeanValue_RBV',name = 'QuadEM Channel 4', kind='normal')



TransmissionDiode = EpicsSignalRO('XF:07ID-BI{DM7:I400-1}:IC4_MON',name = 'RSoXS Transmission Photodiode', kind='normal')
DM4_PD            = EpicsSignalRO('XF:07ID-BI{DM5:F4}Cur:I3-I', name='DM4 Current', kind='normal')


sd.monitors.extend([ring_current,Beamstop_WAXS,Beamstop_SAXS,IzeroDiode,IzeroMesh, quadem1, quadem2, quadem3, quadem4])
sd.baseline.extend([ring_current,Beamstop_WAXS,Beamstop_SAXS,IzeroDiode,IzeroMesh,
                    SlitBottom_I,SlitTop_I,TransmissionDiode,DM4_PD])
