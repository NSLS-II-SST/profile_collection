run_report(__file__)

from .RSoXSObjects.signals import *

sd.monitors.extend([ring_current,Beamstop_WAXS,Beamstop_SAXS,Izero_Mesh, Sample_TEY])
sd.baseline.extend([ring_current,Beamstop_WAXS,Beamstop_SAXS,Izero_Diode,Izero_Mesh,
                    Slit1_Top_I, Slit1_IB_I,DM4_PD,mir1_pressure])  #DM7_Diode
