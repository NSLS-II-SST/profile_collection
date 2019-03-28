print(f'Loading {__file__}...')

from ophyd import EpicsMotor, EpicsSignal
BeamstopW_I = EpicsSignal('XF:07ID-ES1{DMR:I400-1}:IC1_MON', name='BeamstopW_I')
BeamstopS_I = EpicsSignal('XF:07ID-ES1{DMR:I400-1}:IC2_MON', name='BeamstopS_I')
IzeroMesh   = EpicsSignal('XF:07ID-ES1{DMR:I400-1}:IC3_MON', name='IzeroMesh')
IzeroDiode  = EpicsSignal('XF:07ID-ES1{DMR:I400-1}:IC4_MON', name='IzeroDiode')
SlitO_I     = EpicsSignal('XF:07ID-ES1{Slt1:I400-1}:IC1_MON', name='SlitO_I')
SlitB_I     = EpicsSignal('XF:07ID-ES1{Slt1:I400-1}:IC2_MON', name='SlitB_I')
SlitT_I     = EpicsSignal('XF:07ID-ES1{Slt1:I400-1}:IC3_MON', name='SlitT_I')
SlitI_I     = EpicsSignal('XF:07ID-ES1{Slt1:I400-1}:IC4_MON', name='SlitI_I')
