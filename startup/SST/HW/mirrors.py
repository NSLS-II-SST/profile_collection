from ophyd import EpicsSignal

from ..CommonFunctions.functions import run_report
from ..Base.mirrors import HexapodMirror, FMBHexapodMirror


run_report(__file__)

mir2_type = EpicsSignal(
    "XF:07ID1-OP{Mono:PGM1-Ax:MirX}Mtr_TYPE_MON", name="SST 1 Mirror 2 Stripe"
)

mir4OLD = HexapodMirror(
    "XF:07ID2-OP{Mir:M4CD-Ax:", name="SST 1 Mirror 4", kind="hinted"
)
mir3OLD = HexapodMirror(
    "XF:07ID1-OP{Mir:M3ABC-Ax:", name="SST 1 Mirror 3", kind="hinted"
)
mir1OLD = HexapodMirror("XF:07IDA-OP{Mir:M1-Ax:", name="SST 1 Mirror 1", kind="hinted")

mir4 = FMBHexapodMirror(
    "XF:07ID2-OP{Mir:M4CD", name="SST 1 Mirror 4 fmb", kind="hinted"
)
mir3 = FMBHexapodMirror(
    "XF:07ID1-OP{Mir:M3ABC", name="SST 1 Mirror 3 fmb", kind="hinted"
)
mir1 = FMBHexapodMirror("XF:07IDA-OP{Mir:M1", name="SST 1 Mirror 1 fmb", kind="hinted")
