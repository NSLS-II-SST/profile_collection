run_report(__file__)
from ophyd import (EpicsMotor, Device, Component as Cpt, EpicsSignal)
from ophyd import FormattedComponent as FmtCpt

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


class FMBHexapodMirrorAxis(PVPositioner):
    readback = Cpt(EpicsSignalRO, 'Mtr_MON')
    setpoint = Cpt(EpicsSignal, 'Mtr_POS_SP')
    actuate = FmtCpt(EpicsSignal, '{self.parent.prefix}}}MOVE_CMD.PROC')
    actual_value = 1
    stop_signal = FmtCpt(EpicsSignal, '{self.parent.prefix}}}STOP_CMD.PROC')
    stop_value = 1
    done = FmtCpt(EpicsSignalRO, '{self.parent.prefix}}}BUSY_STS')
    done_value = 0


class FMBHexapodMirror(Device):
    z = Cpt(FMBHexapodMirrorAxis, '-Ax:Z}')
    y = Cpt(FMBHexapodMirrorAxis, '-Ax:Y}')
    x = Cpt(FMBHexapodMirrorAxis, '-Ax:X}')
    pit = Cpt(FMBHexapodMirrorAxis, '-Ax:P}')
    yaw = Cpt(FMBHexapodMirrorAxis, '-Ax:Yaw}')
    rol = Cpt(FMBHexapodMirrorAxis, '-Ax:R}')



mir4 = HexapodMirror('XF:07ID2-OP{Mir:M4CD-Ax:',name='SST 1 Mirror 4',kind='hinted')
mir3 = HexapodMirror('XF:07ID1-OP{Mir:M3ABC-Ax:',name='SST 1 Mirror 3',kind='hinted')
mir1 = HexapodMirror('XF:07IDA-OP{Mir:M1-Ax:',name='SST 1 Mirror 1',kind='hinted')

mir4f = FMBHexapodMirror('XF:07ID2-OP{Mir:M4CD',name='SST 1 Mirror 4 fmb',kind='hinted')
mir3f = FMBHexapodMirror('XF:07ID1-OP{Mir:M3ABC',name='SST 1 Mirror 3 fmb',kind='hinted')
mir1f = FMBHexapodMirror('XF:07IDA-OP{Mir:M1',name='SST 1 Mirror 1 fmb',kind='hinted')

sd.baseline.extend([mir3,mir4,mir2_type])
