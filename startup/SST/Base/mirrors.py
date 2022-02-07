from ophyd import (
    Device,
    Component as Cpt,
    EpicsSignal,
    PVPositioner,
    EpicsSignalRO,
)
from ophyd import FormattedComponent as FmtCpt
from ..CommonFunctions.functions import run_report
from ..Base.motors import DeadbandMixin


run_report(__file__)


class HexapodMirror(Device):
    X = Cpt(EpicsSignal, "X}Mtr_MON", write_pv="X}Mtr_SP", kind="hinted")
    Y = Cpt(EpicsSignal, "Y}Mtr_MON", write_pv="Y}Mtr_SP", kind="hinted")
    Z = Cpt(EpicsSignal, "Z}Mtr_MON", write_pv="Z}Mtr_SP", kind="hinted")
    Roll = Cpt(EpicsSignal, "R}Mtr_MON", write_pv="R}Mtr_SP", kind="hinted")
    Pitch = Cpt(EpicsSignal, "P}Mtr_MON", write_pv="P}Mtr_SP", kind="hinted")
    Yaw = Cpt(EpicsSignal, "Yaw}Mtr_MON", write_pv="Yaw}Mtr_SP", kind="hinted")


class FMBHexapodMirrorAxis(PVPositioner):
    readback = Cpt(EpicsSignalRO, "Mtr_MON")
    setpoint = Cpt(EpicsSignal, "Mtr_POS_SP")
    actuate = FmtCpt(EpicsSignal, "{self.parent.prefix}}}MOVE_CMD.PROC")
    actual_value = 1
    stop_signal = FmtCpt(EpicsSignal, "{self.parent.prefix}}}STOP_CMD.PROC")
    stop_value = 1
    done = FmtCpt(EpicsSignalRO, "{self.parent.prefix}}}BUSY_STS")
    done_value = 0


class FMBHexapodMirrorAxisStandAlonePitch(DeadbandMixin,PVPositioner):
    readback = Cpt(EpicsSignalRO, "-Ax:P}Mtr_MON")
    setpoint = Cpt(EpicsSignal, "-Ax:P}Mtr_POS_SP")
    actuate = Cpt(EpicsSignal, "}MOVE_CMD.PROC")
    actual_value = 1
    stop_signal = Cpt(EpicsSignal, "}STOP_CMD.PROC")
    stop_value = 1
    done = Cpt(EpicsSignalRO, "}BUSY_STS")
    done_value = 0



class FMBHexapodMirror(Device):
    Z = Cpt(FMBHexapodMirrorAxis, "-Ax:Z}")
    Y = Cpt(FMBHexapodMirrorAxis, "-Ax:Y}")
    X = Cpt(FMBHexapodMirrorAxis, "-Ax:X}")
    Pitch = Cpt(FMBHexapodMirrorAxis, "-Ax:P}")
    Yaw = Cpt(FMBHexapodMirrorAxis, "-Ax:Yaw}")
    Roll = Cpt(FMBHexapodMirrorAxis, "-Ax:R}")
