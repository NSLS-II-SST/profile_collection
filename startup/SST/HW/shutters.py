from ..CommonFunctions.functions import run_report
from ..Base.valves_and_shutters import EPS_Shutter

run_report(__file__)

psh1 = EPS_Shutter("XF:07ID-PPS{Sh:FE}", name="Front-End Shutter", kind="hinted")
psh1.shutter_type = "FE"
psh1.openval = 0
psh1.closeval = 1

psh4 = EPS_Shutter("XF:07IDA-PPS{PSh:4}", name="Hutch Photon Shutter", kind="hinted")
psh4.shutter_type = "PH"
psh4.openval = 0
psh4.closeval = 1

psh10 = EPS_Shutter(
    "XF:07IDA-PPS{PSh:10}", name="Upstream Photon Shutter", kind="hinted"
)
psh10.shutter_type = "PH"
psh10.openval = 0
psh10.closeval = 1

psh7 = EPS_Shutter(
    "XF:07IDA-PPS{PSh:7}", name="Downstream Photon Shutter", kind="hinted"
)
psh7.shutter_type = "PH"
psh7.openval = 0
psh7.closeval = 1
