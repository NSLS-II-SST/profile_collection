print(f'Loading {__file__}...')

from ophyd import EpicsMotor
sample_x = EpicsMotor('XF:07ID2-ES1{Stg-Ax:X}Mtr', name='sample_x')


from ophyd import EpicsMotor

## monochromator
# dcm_bragg = BraggEpicsMotor('XF:07ID6-OP{Mono:DCM1-Ax:Bragg}Mtr', name='dcm_bragg')
