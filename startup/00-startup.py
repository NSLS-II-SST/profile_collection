## profile_collection is a "bootstrapping" mechanism that triggers the rsoxs package and other beamline codebase to be loaded into the beamline computers.
## profile_collection is located in .ipython, which is separate from the rest of the beamline codebase (e.g., the rsoxs package).  It isan IPython profile, not a normal "python package".
## The rsoxs package should not be placed in this same ~/.ipython directory, nor should the contents of profile_collection be consolidated into the rsoxs package.  This has been attempted before and does not work.
## Configuration files (e.g., devices.toml, regions.toml) belong in this codebase.  It is easier to find the location of an IPython Profile such as profile_collection, but harder to locate these configuration files from the rsoxs package.

## Goal is to keep this file and generally profile_collection package as minimal as possible such that main changes here would be made by NSLS II DSSI (e.g., changing Kafka), and DSSI would not have to edit rsoxs package.

import sys
from pathlib import Path

## 20250130 - adding in capabilities from configure_base that are no longer used after recent code upgrade
## Needs to be imported before alignment_local.py, I think
import matplotlib.pyplot as plt
import bluesky.callbacks as bc
from bluesky.callbacks import *
plt.ion()

paths = [
    path
    for path in Path(
        "/nsls2/data/sst/rsoxs/shared/config/bluesky/collection_packages"
    ).glob("*")
    if path.is_dir()
]
for path in paths:
    sys.path.append(str(path))

## Uses this package: https://github.com/xraygui/nbs-bl
## Gives the path to profile_collection directory and looks for devices.toml file
## This should replace any hardware imports from sst_hw, sst_base, and rsoxs.  rsoxs.Functions imports may have to stay until some of the functions are rewritten to become compliant with data security upgrades.
from nbs_bl.configuration import load_and_configure_everything
load_and_configure_everything()

from rsoxs.startup import RE, db, sd, md
from nbs_bl.printing import run_report

run_report(__file__)

# sst code  # Common code
# from sst_base.archiver import *
from rsoxs.devices.cameras import configure_cameras
from rsoxs.plans.rsoxs import *
from rsoxs.plans.runAcquisitions import *
from rsoxs.configurationSetup.configurationLoadSave import *
from rsoxs.alignment.fiducials import *

from rsoxs.Functions.alignment import *
from rsoxs.Functions.alignment_local import *
from rsoxs.Functions.common_procedures import *
from rsoxs.Functions.configurations import *
from rsoxs.Functions.schemas import *
from rsoxs.Functions.PVdictionary import *  ## TODO: probably delete, not actually used
from rsoxs.Functions.energyscancore import *
from rsoxs.Functions.rsoxs_plans import *
from rsoxs.Functions.fly_alignment import *
#from rsoxs.Functions.spreadsheets import *
from rsoxs.HW.slackbot import rsoxs_bot
#from rsoxs_scans.spreadsheets import *
from rsoxs_scans.acquisition import *

from rsoxs.HW.cameras import * ## 20250131 - temporary solution to using crosshairs, need a better long-term solution

import nslsii
from nslsii import configure_kafka_publisher, configure_bluesky_logging, configure_ipython_logging
from nslsii.common.ipynb.logutils import log_exception

ipython = get_ipython()


#nslsii.configure_base(get_ipython().user_ns, "rsoxs", bec=False, configure_logging=True, publish_documents_with_kafka=False) ## 20250130 - Adding this back to ensure we did not lose anything from before, but it set up a PersistentDict and 
configure_kafka_publisher(RE, beamline_name="rsoxs")
RE.subscribe(db.insert)
configure_bluesky_logging(ipython=ipython)
configure_ipython_logging(exception_logger=log_exception, ipython=ipython)

try:
    from bluesky_queueserver import is_re_worker_active
except ImportError:
    # TODO: delete this when 'bluesky_queueserver' is distributed as part of collection environment
    def is_re_worker_active():
        return False


if not is_re_worker_active():
    from rsoxs.Functions.magics import *

    beamline_status()  # print out the current sample metadata, motor position and detector status

print("Extending Baseline")
# from .Functions.startup import sd
#

## TODO: delete thee code below, but add the important devices to baseline in devices.toml
"""
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
        mono_en.readback,
        mono_en.setpoint,
        mono_en.grating,
        mono_en.grating.user_offset,
        mono_en.gratingx,
        mono_en.mirror2,
        mono_en.mirror2.user_offset,
        mono_en.mirror2x,
        mono_en.readback,
        mono_en.cff,
        en.epugap,
        en.epuphase,
        en.epumode,
        en.polarization,
        en.sample_polarization,
        slits1,
        slits2,
        slits3,
        ring_current,
        Beamstop_WAXS,
        Beamstop_SAXS,
        Slit1_Current_Top,
        Slit1_Current_Bottom,
        Slit1_Current_Inboard,
        Slit1_Current_Outboard,
        Izero_Diode,
        Izero_Mesh, #
        mir1_pressure,
        rsoxs_ccg_izero,
        rsoxs_pg_izero,
        rsoxs_ccg_main,
        rsoxs_pg_main,
        rsoxs_ccg_ll,
        rsoxs_pg_ll,
        rsoxs_ll_gpwr,
        FEsh1,
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
        Shutter_SAXS_count,
        Shutter_WAXS_count,
        tem_tempstage
    ]
)
"""
# from .Functions.startup import sd
#
# sd.monitors.extend(
#     [
#         Shutter_control,
#         Shutter_open_time,
#         #tem_tempstage.readback,
#         #mono_en_int,
#         #mono_en.readback,
#         #epu_gap.user_readback,
#         #mono_en.en_mon,
#         ring_current,
#         #Beamstop_WAXS,
#         #Beamstop_SAXS,
#         #Shutter_SAXS_count,
#         Shutter_WAXS_count,
#         #Slit1_Current_Top,
#         #Slit1_Current_Bottom,
#         #Slit1_Current_Inboard,
#         #Slit1_Current_Outboard,
#         #Izero_Mesh,
#         #Sample_TEY,
#     ]
# )




# setup the contingencies

from rsoxs.HW.contingencies import *
