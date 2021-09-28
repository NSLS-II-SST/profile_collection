from RSoXS.CommonFunctions.functions import run_report

run_report(__file__)

# SST devices  These all reference the base classes and instantiate the objects themselves into the current namespace
from RSoXS.SSTObjects.gatevalves import *
from RSoXS.SSTObjects.shutters import *
from RSoXS.SSTObjects.vacuum import *
from RSoXS.SSTObjects.motors import *
from RSoXS.SSTObjects.mirrors import *
from RSoXS.SSTObjects.diode import *
from RSoXS.SSTObjects.energy import *

# SST code  # Common code
from RSoXS.SSTBase.archiver import *

# RSoXS startup - bluesky RE / db / md definitions
from RSoXS.RSoXSBase.startup import *

# RSoXS specific devices
from RSoXS.RSoXSObjects.motors import *
from RSoXS.RSoXSObjects.cameras import *
from RSoXS.RSoXSObjects.signals import *
from RSoXS.RSoXSObjects.detectors import *
from RSoXS.RSoXSObjects.slits import *
from RSoXS.RSoXSObjects.syringepump import *
from RSoXS.RSoXSObjects.energy import *

# RSoXS specific code
from RSoXS.RSoXSBase.alignment import *
from RSoXS.RSoXSBase.common_procedures import *
from RSoXS.RSoXSBase.configurations import *
from RSoXS.RSoXSBase.schemas import *
from RSoXS.RSoXSBase.PVdictionary import *
from RSoXS.RSoXSBase.energyscancore import *
from RSoXS.RSoXSBase.energyscans import *
from RSoXS.RSoXSBase.NEXAFSscans import *
from RSoXS.RSoXSObjects.slackbot import rsoxs_bot
from RSoXS.RSoXSBase.acquisitions import *

try:
    from bluesky_queueserver import is_re_worker_active
except ImportError:
    # TODO: delete this when 'bluesky_queueserver' is distributed as part of collection environment
    def is_re_worker_active():
        return False


if not is_re_worker_active():
    from RSoXS.RSoXSBase.magics import *

    user()  # print out the current user metadata
    beamline_status()  # print out the current sample metadata, motor position and detector status


# from .RSoXSBase.startup import sd

sd.baseline.extend(
    [
        sam_viewer,
        sam_X,
        sam_Y,
        sam_Z,
        sam_Th,
        BeamStopS,
        BeamStopW,
        Det_S,
        Det_W,
        Shutter_Y,
        Izero_Y,
        Izero_ds,
        grating,
        mirror2,
        slits1,
        slits2,
        slits3,
        en,
        ring_current,
        Beamstop_WAXS,
        Beamstop_SAXS,
        Izero_Diode,
        Izero_Mesh,
        Slit1_Top_I,
        Slit1_IB_I,
        DM4_PD,
        mir1_pressure,
        rsoxs_ccg_izero,
        rsoxs_pg_izero,
        rsoxs_ccg_main,
        rsoxs_pg_main,
        rsoxs_ccg_ll,
        rsoxs_pg_ll,
        rsoxs_ll_gpwr,
        psh1,
        psh4,
        psh10,
        psh7,
        gv14,
        gv14a,
        gv15,
        gv26,
        gv27,
        gv27a,
        gv28,
        gvTEM,
        gvll,
        gvturbo,
        mir1,
        mir3,
        mir4,
        mir2_type,
    ]
)

# from .RSoXSBase.startup import sd

sd.monitors.extend(
    [
        Shutter_control,
        mono_en.readback,
        ring_current,
        Beamstop_WAXS,
        Beamstop_SAXS,
        Izero_Mesh,
        Sample_TEY,
    ]
)

# setup the preprocessors

RE.preprocessors.append(dark_frame_preprocessor_waxs)
RE.preprocessors.append(dark_frame_preprocessor_saxs)

# setup the contingencies

from RSoXS.RSoXSObjects.contingencies import *
