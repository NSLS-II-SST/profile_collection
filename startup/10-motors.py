print(f'Loading {__file__}...')

from ophyd import EpicsMotor
sam_X = EpicsMotor('XF:07ID2-ES1{Stg-Ax:X}Mtr', name='sam_X')
sam_Y = EpicsMotor('XF:07ID2-ES1{Stg-Ax:Y}Mtr', name='sam_Y')
sam_Z = EpicsMotor('XF:07ID2-ES1{Stg-Ax:Z}Mtr', name='sam_Z')
sam_Th = EpicsMotor('XF:07ID2-ES1{Stg-Ax:Yaw}Mtr', name='sam_Th')
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




from ophyd import EpicsMotor

## monochromator
# dcm_bragg = BraggEpicsMotor('XF:07ID6-OP{Mono:DCM1-Ax:Bragg}Mtr', name='dcm_bragg')
