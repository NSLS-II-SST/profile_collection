print(f'Loading {__file__}...')
from ophyd import (EpicsMotor, Device, Component as Cpt, EpicsSignal)

mir2_type = EpicsSignal('XF:07ID1-OP{Mono:PGM1-Ax:MirX}Mtr_TYPE_MON',name='mir2_type')

class HexapodMirror(Device):
    X = Cpt(EpicsSignal, 'X}Mtr_MON',write_pv='X}Mtr_SP')
    Y = Cpt(EpicsSignal, 'Y}Mtr_MON',write_pv='Y}Mtr_SP')
    Z = Cpt(EpicsSignal, 'Z}Mtr_MON',write_pv='Z}Mtr_SP')
    Roll = Cpt(EpicsSignal, 'R}Mtr_MON',write_pv='R}Mtr_SP')
    Pitch = Cpt(EpicsSignal, 'P}Mtr_MON',write_pv='P}Mtr_SP')
    Yaw = Cpt(EpicsSignal, 'Yaw}Mtr_MON',write_pv='Yaw}Mtr_SP')

mir4 = HexapodMirror('XF:07ID2-OP{Mir:M4CD-Ax:',name='mir4')
mir3 = HexapodMirror('XF:07ID1-OP{Mir:M3ABC-Ax:',name='mir3')
sd.baseline.extend([mir3,mir4,mir2_type])




