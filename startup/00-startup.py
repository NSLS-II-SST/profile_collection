
from .CommonFunctions.functions import *
run_report(__file__)

# SST devices  These all reference the base classes and instantiate the objects themselves into the current namespace (I hope)
from .SSTObjects.gatevalves import *
from .SSTObjects.shutters import *
from .SSTObjects.vacuum import *
from startup.RSoXSObjects.energy import *
from .SSTObjects.motors import *
from .SSTObjects.mirrors import *
from .SSTObjects.diode import *

# SST code  # Common code
from .SSTBase.archiver import *

# RSoXS startup - bluesky RE / db / md definitions
from .RSoXSBase.startup import *

# RSoXS specific devices
from .RSoXSObjects.motors import *
from .RSoXSObjects.cameras import *
from .RSoXSObjects.signals import *
from .RSoXSObjects.detectors import *
from .RSoXSObjects.slits import *
from .RSoXSObjects.syringepump import *

# RSoXS specific code
from .RSoXSBase.configurations import *
from .RSoXSBase.schemas import *
from .RSoXSBase.PVdictionary import *
from .RSoXSBase.common_procedures import *
from .RSoXSBase.common_metadata import *
from .RSoXSBase.energyscancore import *
from .RSoXSBase.energyscans import *
from .RSoXSBase.NEXAFSscans import *
from .RSoXSBase.alignment import *
from .RSoXSObjects.slackbot import rsoxs_bot

try:
    from bluesky_queueserver import is_re_worker_active
except ImportError:
    # TODO: delete this when 'bluesky_queueserver' is distributed as part of collection environment
    def is_re_worker_active():
        return False

if not is_re_worker_active():
    from .RSoXSBase.magics import *


user() # print out the current user metadata
beamline_status() # print out the current sample metadata, motor position and detector status


#from .RSoXSBase.startup import sd

sd.baseline.extend([sam_viewer,
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
                    ccg_izero,
                    pg_izero,
                    ccg_main,
                    pg_main,
                    ccg_ll,
                    pg_ll,
                    ll_gpwr,
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
                    mir2_type])

#from .RSoXSBase.startup import sd

sd.monitors.extend([Shutter_control,
                    mono_en.readback,
                    ring_current,
                    Beamstop_WAXS,
                    Beamstop_SAXS,
                    Izero_Mesh,
                    Sample_TEY,
                    ])


RE.preprocessors.append(dark_frame_preprocessor_waxs)
RE.preprocessors.append(dark_frame_preprocessor_saxs)