run_report(__file__)

from ophyd import EpicsSignalRO, EpicsSignal

# These might need/make more sense to be split up into separate files later on.
# But while we have so few, I'm just putting them in this single file.

bpm13_sum = EpicsSignalRO('XF:07ID-BI{BPM:13}Stats5:Total_RBV', name='Downstream Izero Phosphor Intensity')

ring_current = EpicsSignalRO('SR:OPS-BI{DCCT:1}I:Real-I', name='NSLS-II Ring Current', kind='normal')
Beamstop_WAXS = EpicsSignalRO('XF:07ID-ES1{DMR:I400-1}:IC1_MON',name = 'WAXS Beamstop', kind='normal')
Beamstop_SAXS = EpicsSignalRO('XF:07ID-ES1{DMR:I400-1}:IC2_MON',name = 'SAXS Beamstop', kind='normal')
Izero_Diode    = EpicsSignalRO('XF:07ID-ES1{DMR:I400-1}:IC3_MON',name = 'Izero Photodiode', kind='normal')

#IzeroMesh    = EpicsSignalRO('XF:07ID-ES1{Slt1:I400-1}:IC4_MON',name = 'Izero Mesh I400', kind='normal')
#Sample_EY = EpicsSignalRO('XF:07ID-ES1{Slt1:I400-1}:IC1_MON',name = 'RSoXS Drain', kind='normal')
SlitBottom_I = EpicsSignalRO('XF:07ID-ES1{Slt1:I400-1}:IC2_MON',name = 'RSoXS Slit 1 Bottom Current', kind='normal')
#SlitTop_I    = EpicsSignalRO('XF:07ID-ES1{Slt1:I400-1}:IC3_MON',name = 'Slit Top', kind='normal')


#Beamstop_SAXS  = EpicsSignalRO('XF:07ID1-BI{EM:1}EM180:Current3:MeanValue_RBV',
#                           name = 'SAXS Beamstop', kind='hinted')
Izero_Mesh  = EpicsSignalRO('XF:07ID1-BI{EM:1}EM180:Current2:MeanValue_RBV',
                           name = 'RSoXS Au Mesh Current', kind='normal')
Sample_TEY  = EpicsSignalRO('XF:07ID1-BI{EM:1}EM180:Current1:MeanValue_RBV',
                           name = 'RSoXS Sample Current', kind='normal')
Slit1_Top_I  = EpicsSignalRO('XF:07ID1-BI{EM:1}EM180:Current3:MeanValue_RBV',
                           name = 'RSoXS Slit 1 Top Current', kind='normal')
Slit1_IB_I   = EpicsSignalRO('XF:07ID1-BI{EM:1}EM180:Current4:MeanValue_RBV',
                           name = 'RSoXS Slit 1 Inbound Current', kind='normal')

DiodeRange = EpicsSignal('XF:07ID-ES1{DMR:I400-1}:RANGE_BP')

DM7_Diode = EpicsSignalRO('XF:07ID-BI{DM7:I400-1}:IC4_MON',name = 'DM7 Photodiode', kind='normal')
DM4_PD            = EpicsSignalRO('XF:07ID-BI{DM5:F4}Cur:I3-I', name='DM4 Photodiode', kind='normal')


sd.monitors.extend([ring_current,Beamstop_WAXS,Beamstop_SAXS,Izero_Mesh, Sample_TEY])
sd.baseline.extend([ring_current,Beamstop_WAXS,Beamstop_SAXS,Izero_Diode,Izero_Mesh,
                    SlitBottom_I, Slit1_Top_I, Slit1_IB_I,DM7_Diode,DM4_PD])
