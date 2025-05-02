## profile_collection is a "bootstrapping" mechanism that triggers the rsoxs package and other beamline codebase to be loaded into the beamline computers.
## profile_collection is located in .ipython, which is separate from the rest of the beamline codebase (e.g., the rsoxs package).  It isan IPython profile, not a normal "python package".
## The rsoxs package should not be placed in this same ~/.ipython directory, nor should the contents of profile_collection be consolidated into the rsoxs package.  This has been attempted before and does not work.
## Configuration files (e.g., devices.toml, regions.toml) belong in this codebase.  It is easier to find the location of an IPython Profile such as profile_collection, but harder to locate these configuration files from the rsoxs package.

## Goal is to keep this file and generally profile_collection package as minimal as possible such that main changes here would be made by NSLS II DSSI (e.g., changing Kafka), and DSSI would not have to edit rsoxs package.

import sys
from pathlib import Path
from tiled.client import from_profile
import os
import time as ttime

## 20250130 - adding in capabilities from configure_base that are no longer used after recent code upgrade
## Needs to be imported before alignment_local.py, I think
import matplotlib.pyplot as plt
import bluesky.callbacks as bc
from bluesky.callbacks import *
from bluesky.utils import ProgressBarManager



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

from rsoxs.startup import RE, sd, md # db
from nbs_bl.printing import run_report

run_report(__file__)

# sst code  # Common code
# from sst_base.archiver import *
from rsoxs.devices.cameras import configure_cameras
from rsoxs.plans.rsoxs import *
from rsoxs.plans.run_acquisitions import *
from rsoxs.configuration_setup.configuration_load_save import *
from rsoxs.configuration_setup.configurations_instrument import *
from rsoxs.alignment.fiducials import *
from rsoxs.alignment.energy_calibration import *

## Eliot's old code
from rsoxs.HW.cameras import * ## 20250131 - temporary solution to using crosshairs, need a better long-term solution
from rsoxs.Functions.alignment import *
from rsoxs.Functions.alignment_local import *



import nslsii
from nslsii import configure_kafka_publisher, configure_bluesky_logging, configure_ipython_logging
from nslsii.common.ipynb.logutils import log_exception

ipython = get_ipython()



class TiledInserter:
    def insert(self, name, doc):
        ATTEMPTS = 4
        error = None
        for attempt in range(ATTEMPTS):
            try:
                tiled_writing_client.post_document(name, doc)
            except Exception as exc:
                print(f"Tiled Insertion Failure for document {name}:", repr(exc))
                error = exc
            else:
                break
            ttime.sleep(2)
        else:
            # Out of attempts
            raise error

# Define tiled catalog
tiled_writing_client = from_profile("nsls2", api_key=os.environ["TILED_BLUESKY_WRITING_API_KEY_RSOXS"])["rsoxs"]["raw"]
#tiled_writing_client = from_profile("rsoxs")
# tiled_inserter = TiledInserter()
#c = tiled_reading_client = from_profile("nsls2")["rsoxs"]["raw"]
#db = Broker(c)

#nslsii.configure_base(get_ipython().user_ns, tiled_inserter, publish_documents_with_kafka=False, pbar=True)
configure_kafka_publisher(RE, beamline_name="rsoxs")

#RE.subscribe(tiled_inserter.insert)
RE.subscribe(tiled_writing_client.post_document)
configure_bluesky_logging(ipython=ipython)
configure_ipython_logging(exception_logger=log_exception, ipython=ipython)



try:
    from bluesky_queueserver import is_re_worker_active
except ImportError:
    # TODO: delete this when 'bluesky_queueserver' is distributed as part of collection environment
    def is_re_worker_active():
        return False


if not is_re_worker_active(): ## If not running queueserver, run these
    from rsoxs.Functions.magics import *
    pbar_manager = ProgressBarManager()
    RE.waiting_hook = pbar_manager

    beamline_status()  # print out the current sample metadata, motor position and detector status


## TODO: delete thee code below, but add the important devices to baseline in devices.toml

# setup the contingencies

from rsoxs.HW.contingencies import *


## TODO: make new profile_collection_local package.  Consider setting a global variable LOCAL = True such that hardware cannot be moved in rsoxs functions.
