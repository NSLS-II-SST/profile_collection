print(f'Loading {__file__}...')

from ophyd import EpicsMotor, EpicsSignal
sam_X = EpicsMotor('XF:07ID2-ES1{Stg-Ax:X}Mtr', name='sam_X')
sam_Y = EpicsMotor('XF:07ID2-ES1{Stg-Ax:Y}Mtr', name='sam_Y')
sam_Z = EpicsMotor('XF:07ID2-ES1{Stg-Ax:Z}Mtr', name='sam_Z')
sam_Th = EpicsMotor('XF:07ID2-ES1{Stg-Ax:Yaw}Mtr', name='sam_Th')
sam_Th.kind = 'hinted'
BeamStopW = EpicsMotor('XF:07ID2-ES1{BS-Ax:1}Mtr', name='BeamStopW')
BeamStopS = EpicsMotor('XF:07ID2-ES1{BS-Ax:2}Mtr', name='BeamStopS')
Slt1_T = EpicsMotor('XF:07ID2-ES1{Slt1-Ax:T}Mtr', name='Slt1_T')
Slt1_B = EpicsMotor('XF:07ID2-ES1{Slt1-Ax:B}Mtr', name='Slt1_B')
Slt1_O = EpicsMotor('XF:07ID2-ES1{Slt1-Ax:O}Mtr', name='Slt1_O')
Slt1_I = EpicsMotor('XF:07ID2-ES1{Slt1-Ax:I}Mtr', name='Slt1_I')
Slt2_T = EpicsMotor('XF:07ID2-ES1{Slt2-Ax:T}Mtr', name='Slt2_T')
Slt2_B = EpicsMotor('XF:07ID2-ES1{Slt2-Ax:B}Mtr', name='Slt2_B')
Slt2_O = EpicsMotor('XF:07ID2-ES1{Slt2-Ax:O}Mtr', name='Slt2_O')
Slt2_I = EpicsMotor('XF:07ID2-ES1{Slt2-Ax:I}Mtr', name='Slt2_I')
Slt3_T = EpicsMotor('XF:07ID2-ES1{Slt3-Ax:T}Mtr', name='Slt3_T')
Slt3_B = EpicsMotor('XF:07ID2-ES1{Slt3-Ax:B}Mtr', name='Slt3_B')
Slt3_O = EpicsMotor('XF:07ID2-ES1{Slt3-Ax:O}Mtr', name='Slt3_O')
Slt3_I = EpicsMotor('XF:07ID2-ES1{Slt3-Ax:I}Mtr', name='Slt3_I')
Det_W = EpicsMotor('XF:07ID2-ES1{Det-Ax:1}Mtr', name='Det_W')
Det_S = EpicsMotor('XF:07ID2-ES1{Det-Ax:2}Mtr', name='Det_S')
Shutter_Y = EpicsMotor('XF:07ID2-ES1{FSh-Ax:1}Mtr', name='Shutter_Y')
Izero_Y = EpicsMotor('XF:07ID2-ES1{Scr-Ax:1}Mtr', name='Izero_Y')
#epu_gap = EpicsMotor('SR:C07-ID:G1A{SST1:1-Ax:Gap}-Mtr', name='epu_gap')

## monochromator
# dcm_bragg = BraggEpicsMotor('XF:07ID6-OP{Mono:DCM1-Ax:Bragg}Mtr', name='dcm_bragg')
mono_en = EpicsSignal(read_pv='XF:07ID1-OP{Mono:PGM1-Ax::ENERGY_MON',
                     write_pv='XF:07ID1-OP{Mono:PGM1-Ax::ENERGY_SP',
                     name='mono_en')

from ophyd import PVPositioner, EpicsSignalRO
from ophyd import Component as Cpt

class undulatorgap(PVPositioner):
    setpoint = Cpt(EpicsSignal,'-Ax:Gap}-Mtr-SP')
    readback = Cpt(EpicsSignalRO, '-Ax:Gap}-Mtr.RBV')
    done = Cpt(EpicsSignalRO, '-Ax:Gap}-Mtr.MOVN')
    done_value = 0
    stop_signal = Cpt(EpicsSignal, '-Ax:Gap}-Mtr.STOP')

print('SR:C07-ID:G1A{SST1:1-Ax:Gap}-Mtr-SP')
epu_gap = undulatorgap('SR:C07-ID:G1A{SST1:1',name='epu_gap', read_attrs=['readback'],
                configuration_attrs=[])


    #EpicsSignal(read_pv='SR:C07-ID:G1A{SST1:1-Ax:Gap}-Mtr.RBV',
    #                 write_pv='SR:C07-ID:G1A{SST1:1-Ax:Gap}-Mtr-SP',
    #                name='epu_gap')