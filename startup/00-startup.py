import sys
from pathlib import Path

paths = [
    path
    for path in Path(
        "/nsls2/data/sst/rsoxs/shared/config/bluesky/collection_packages"
    ).glob("*")
    if path.is_dir()
]
for path in paths:
    sys.path.append(str(path))


from sst.CommonFunctions.functions import run_report

run_report(__file__)

# sst devices  These all reference the Base classes and instantiate the objects themselves into the current namespace
from sst.HW.gatevalves import *
from sst.HW.shutters import *
from sst.HW.vacuum import *
from sst.HW.motors import *
from sst.HW.mirrors import *
from sst.HW.diode import *
from sst.HW.energy import *

# sst code  # Common code
from sst.Base.archiver import *

# RSoXS startup - bluesky RE / db / md definitions
from rsoxs.startup import *

# RSoXS specific devices
from rsoxs.HW.motors import *
from rsoxs.HW.cameras import *
from rsoxs.HW.signals import *
from rsoxs.HW.detectors import *
from rsoxs.HW.slits import *
from rsoxs.HW.syringepump import *
from rsoxs.HW.energy import *

# RSoXS specific code
from rsoxs.Functions.alignment import *
from rsoxs.Functions.common_procedures import *
from rsoxs.Functions.configurations import *
from rsoxs.Functions.schemas import *
from rsoxs.Functions.PVdictionary import *
from rsoxs.Functions.energyscancore import *
from rsoxs.Functions.energyscans import *
from rsoxs.Functions.NEXAFSscans import *
from rsoxs.HW.slackbot import rsoxs_bot
from rsoxs.Functions.acquisitions import *
from rsoxs.Functions.sample_spreadsheets import *


try:
    from bluesky_queueserver import is_re_worker_active
except ImportError:
    # TODO: delete this when 'bluesky_queueserver' is distributed as part of collection environment
    def is_re_worker_active():
        return False


if not is_re_worker_active():
    from rsoxs.Functions.magics import *

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
        Shutter_delay,
        Shutter_trigger,
        Shutter_open_time,
        Light_control,
        Shutter_enable,
        Shutter_enable1,
        Shutter_enable2,
        Shutter_enable3,

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

from rsoxs.HW.contingencies import *
