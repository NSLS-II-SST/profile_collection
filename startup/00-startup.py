from SST.CommonFunctions.functions import run_report

run_report(__file__)

# SST devices  These all reference the Base classes and instantiate the objects themselves into the current namespace
from SST.HW.gatevalves import *
from SST.HW.shutters import *
from SST.HW.vacuum import *
from SST.HW.motors import *
from SST.HW.mirrors import *
from SST.HW.diode import *
from SST.HW.energy import *

# SST code  # Common code
from SST.Base.archiver import *

# RSoXS startup - bluesky RE / db / md definitions
from SST.RSoXS.startup import *

# RSoXS specific devices
from SST.RSoXS.HW.motors import *
from SST.RSoXS.HW.cameras import *
from SST.RSoXS.HW.signals import *
from SST.RSoXS.HW.detectors import *
from SST.RSoXS.HW.slits import *
from SST.RSoXS.HW.syringepump import *
from SST.RSoXS.HW.energy import *

# RSoXS specific code
from SST.RSoXS.Functions.alignment import *
from SST.RSoXS.Functions.common_procedures import *
from SST.RSoXS.Functions.configurations import *
from SST.RSoXS.Functions.schemas import *
from SST.RSoXS.Functions.PVdictionary import *
from SST.RSoXS.Functions.energyscancore import *
from SST.RSoXS.Functions.energyscans import *
from SST.RSoXS.Functions.NEXAFSscans import *
from SST.RSoXS.HW.slackbot import rsoxs_bot
from SST.RSoXS.Functions.acquisitions import *
from SST.RSoXS.Functions.sample_spreadsheets import *


try:
    from bluesky_queueserver import is_re_worker_active
except ImportError:
    # TODO: delete this when 'bluesky_queueserver' is distributed as part of collection environment
    def is_re_worker_active():
        return False


if not is_re_worker_active():
    from SST.RSoXS.Functions.magics import *

    user()  # print out the current user metadata
    beamline_status()  # print out the current sample metadata, motor position and detector status


# from .Functions.startup import sd
#
sd.baseline.extend(
     [
        sam_viewer,
        sam_X,
        sam_Y,
        sam_Z,
        sam_Th,
        TEMZ,
        TEMY,
        TEMX,
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
        Slit1_Current_Top,
        Slit1_Current_Bottom,
        Slit1_Current_Inboard,
        Slit1_Current_Outboard,
        Izero_Diode,
        Izero_Mesh,
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

# from .Functions.startup import sd
#
sd.monitors.extend(
    [
        Shutter_control,
        mono_en.readback,
        ring_current,
        Beamstop_WAXS,
        Beamstop_SAXS,
        Slit1_Current_Top,
        Slit1_Current_Bottom,
        Slit1_Current_Inboard,
        Slit1_Current_Outboard,
        Izero_Mesh,
        Sample_TEY,
    ]
)



def waxs_spiral_mode():
    try:
        RE.preprocessors.remove(dark_frame_preprocessor_waxs_spirals)
    except ValueError:
        pass
    try:
        RE.preprocessors.remove(dark_frame_preprocessor_waxs)
    except ValueError:
        pass
    RE.preprocessors.append(dark_frame_preprocessor_waxs_spirals)

def waxs_normal_mode():
    try:
        RE.preprocessors.remove(dark_frame_preprocessor_waxs_spirals)
    except ValueError:
        pass
    try:
        RE.preprocessors.remove(dark_frame_preprocessor_waxs)
    except ValueError:
        pass
    RE.preprocessors.append(dark_frame_preprocessor_waxs)


waxs_normal_mode()
RE.preprocessors.append(dark_frame_preprocessor_saxs)
# setup the contingencies

from SST.RSoXS.HW.contingencies import *
