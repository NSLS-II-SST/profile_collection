from ophyd import EpicsMotor

## monochromator
dcm_bragg = BraggEpicsMotor('XF:07ID6-OP{Mono:DCM1-Ax:Bragg}Mtr', name='dcm_bragg')
