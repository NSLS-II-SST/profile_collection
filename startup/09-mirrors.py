run_report(__file__)
from ophyd import (EpicsMotor, Device, Component as Cpt, EpicsSignal)

mir2_type = EpicsSignal('XF:07ID1-OP{Mono:PGM1-Ax:MirX}Mtr_TYPE_MON',name='SST 2 Mirror 2 Stripe')

class HexapodMirror(Device):
    X = Cpt(EpicsSignal, 'X}Mtr_MON',write_pv='X}Mtr_SP',kind='hinted')
    Y = Cpt(EpicsSignal, 'Y}Mtr_MON',write_pv='Y}Mtr_SP',kind='hinted')
    Z = Cpt(EpicsSignal, 'Z}Mtr_MON',write_pv='Z}Mtr_SP',kind='hinted')
    Roll = Cpt(EpicsSignal, 'R}Mtr_MON',write_pv='R}Mtr_SP',kind='hinted')
    Pitch = Cpt(EpicsSignal, 'P}Mtr_MON',write_pv='P}Mtr_SP',kind='hinted')
    Yaw = Cpt(EpicsSignal, 'Yaw}Mtr_MON',write_pv='Yaw}Mtr_SP',kind='hinted')
#    def read(self):
#        self.X.read()
#        self.Y.read()
#        self.Z.read()
#        self.Roll.read()
#        self.Pitch.read()
#        self.Yaw.read()



mir4 = HexapodMirror('XF:07ID2-OP{Mir:M4CD-Ax:',name='SST 1 Mirror 4',kind='hinted')
mir3 = HexapodMirror('XF:07ID1-OP{Mir:M3ABC-Ax:',name='SST 1 Mirror 3',kind='hinted')
mir1 = HexapodMirror('XF:07IDA-OP{Mir:M1-Ax:',name='SST 1 Mirror 1',kind='hinted')

# sd.baseline.extend([mir3,mir4,mir2_type])
