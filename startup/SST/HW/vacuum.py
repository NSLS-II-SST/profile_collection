from ophyd import EpicsSignalRO, EpicsSignal

from ..CommonFunctions.functions import run_report


run_report(__file__)


rsoxs_ccg_izero = EpicsSignalRO(
    "XF:07IDB-VA:2{RSoXS:DM-CCG:1}P:Raw-I",
    name="IZero Chamber Cold Cathode Gauge",
    kind="hinted",
)
rsoxs_pg_izero = EpicsSignalRO(
    "XF:07IDB-VA:2{RSoXS:DM-TCG:1}P:Raw-I",
    name="IZero Chamber Pirani Gauge",
    kind="hinted",
)
rsoxs_ccg_main = EpicsSignalRO(
    "XF:07IDB-VA:2{RSoXS:Main-CCG:1}P:Raw-I",
    name="Main Chamber Chamber Cold Cathode Gauge",
    kind="hinted",
)
rsoxs_pg_main = EpicsSignalRO(
    "XF:07IDB-VA:2{RSoXS:Main-TCG:1}P:Raw-I",
    name="Main Chamber Pirani Gauge",
    kind="hinted",
)
rsoxs_ccg_ll = EpicsSignalRO(
    "XF:07IDB-VA:2{RSoXS:LL-CCG:1}P:Raw-I",
    name="Load Lock Chamber Cold Cathode Gauge",
    kind="hinted",
)
rsoxs_pg_ll = EpicsSignalRO(
    "XF:07IDB-VA:2{RSoXS:LL-TCG:1}P:Raw-I", name="Load Lock Pirani Gauge", kind="hinted"
)
rsoxs_ll_gpwr = EpicsSignal(
    "XF:07IDB-VA:2{RSoXS:LL-CCG:1}Pwr-Cmd",
    name="Power to Load Lock Gauge",
    kind="hinted",
)
