from ..CommonFunctions.functions import run_report
from ..Base.valves_and_shutters import EPS_Shutter

run_report(__file__)


gv14 = EPS_Shutter(
    "XF:07IDA-VA:2{FS:6-GV:1}", name="Pre Mono Gate Valve", kind="hinted"
)
gv14.shutter_type = "GV"
gv14.openval = 0
gv14.closeval = 1

gv14a = EPS_Shutter("XF:07IDA-VA:2{FS:6-GV:2}", name="Mono Gate Valve", kind="hinted")
gv14a.shutter_type = "GV"
gv14a.openval = 0
gv14a.closeval = 1

gv15 = EPS_Shutter(
    "XF:07IDB-VA:2{Mono:PGM-GV:1}", name="Pre Shutter Gate Valve", kind="hinted"
)
gv15.shutter_type = "GV"
gv15.openval = 0
gv15.closeval = 1

gv26 = EPS_Shutter(
    "XF:07IDB-VA:2{Mir:M3C-GV:1}", name="Post Shutter Gate Valve", kind="hinted"
)
gv26.shutter_type = "GV"
gv26.openval = 1
gv26.closeval = 0

gv27 = EPS_Shutter(
    "XF:07IDB-VA:3{Slt:C-GV:1}", name="Upstream Gate Valve", kind="hinted"
)
gv27.shutter_type = "GV"
gv27.openval = 1
gv27.closeval = 0

gv27a = EPS_Shutter(
    "XF:07IDB-VA:2{RSoXS:Main-GV:1}", name="Izero-Main Gate Valve", kind="hinted"
)
gv27a.shutter_type = "GV"
gv27a.openval = 1
gv27a.closeval = 0

gv28 = EPS_Shutter(
    "XF:07IDB-VA:2{BT:1-GV:1}", name="Downstream Gate Valve", kind="hinted"
)
gv28.shutter_type = "GV"
gv28.openval = 1
gv28.closeval = 0

gvTEM = EPS_Shutter(
    "XF:07IDB-VA:2{RSoXS:Main-GV:2}", name="TEM Load Lock Gate Valve", kind="hinted"
)
gvTEM.shutter_type = "GV"
gvTEM.openval = 0
gvTEM.closeval = 1

gvll = EPS_Shutter(
    "XF:07IDB-VA:2{RSoXS:LL-GV:1}", name="Load Lock Gate Valve", kind="hinted"
)
gvll.shutter_type = "GV"
gvll.openval = 0
gvll.closeval = 1

gvturbo = EPS_Shutter(
    "XF:07IDB-VA:2{RSoXS:TP-GV:1}", name="Turbo Gate Valve", kind="hinted"
)
gvturbo.shutter_type = "GV"
gvturbo.openval = 0
gvturbo.closeval = 1
