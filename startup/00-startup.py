from IPython.utils.coloransi import TermColors as color

import os

import nslsii

from pathlib import Path

import appdirs

# Use caproto not pyepics.
os.environ['OPHYD_CONTROL_LAYER'] = 'caproto'


def colored(text, tint='white', attrs=[]):
    '''
    A simple wrapper around IPython's interface to TermColors
    '''
    tint = tint.lower()
    if 'dark' in tint:
        tint = 'Dark' + tint[4:].capitalize()
    elif 'light' in tint:
        tint = 'Light' + tint[5:].capitalize()
    elif 'blink' in tint:
        tint = 'Blink' + tint[5:].capitalize()
    elif 'no' in tint:
        tint = 'Normal'
    else:
        tint = tint.capitalize()
    return '{0}{1}{2}'.format(getattr(color, tint), str(text), color.Normal)


def run_report(thisfile):
    '''
    Noisily proclaim to be importing a file of python code.
    '''
    print(colored('Importing %s ...' % thisfile.split('/')[-1], 'lightcyan'))


run_report(__file__)

# Very important, the databroker config lives in C:\Users\greateyes\AppData\Roaming\databroker\rsoxs.yml,
# not in ~/.config/databroker/rsoxs.yml
nslsii.configure_base(
    get_ipython().user_ns,
    'rsoxs',
    publish_documents_to_kafka=True
)

# After the above call, you will now have the following in your namespace:
# 
#	RE : RunEngine 
#	db : databroker 
#	sd : SupplementalData
#	pbar_manager : ProgressBarManager
#	bec : BestEffortCallback
#	peaks : bec.peaks
#	plt : matplotlib.pyplot
#	np : numpy
#	bc : bluesky.callbacks
#	bp : bluesky.plans
#	bps : bluesky.plan_stubs
#	mv : bluesky.plan_stubs.mv
#	mvr : bluesky.plan_stubs.mvr
#	mov : bluesky.plan_stubs.mov
#	movr : bluesky.plan_stubs.movr
#	bpp : bluesky.preprocessors





from databroker.v0 import Broker

try:
    from bluesky.utils import PersistentDict
except ImportError:
    import msgpack
    import msgpack_numpy
    import zict

    class PersistentDict(zict.Func):
        def __init__(self, directory):
            self._directory = directory
            self._file = zict.File(directory)
            super().__init__(self._dump, self._load, self._file)

        @property
        def directory(self):
            return self._directory

        def __repr__(self):
            return f"<{self.__class__.__name__} {dict(self)!r}>"

        @staticmethod
        def _dump(obj):
            "Encode as msgpack using numpy-aware encoder."
            # See https://github.com/msgpack/msgpack-python#string-and-binary-type
            # for more on use_bin_type.
            return msgpack.packb(
                obj,
                default=msgpack_numpy.encode,
                use_bin_type=True)

        @staticmethod
        def _load(file):
            return msgpack.unpackb(
                file,
                object_hook=msgpack_numpy.decode,
                raw=False)

runengine_metadata_dir = appdirs.user_data_dir(appname="bluesky") / Path("runengine-metadata")

# PersistentDict will create the directory if it does not exist
RE.md = PersistentDict(runengine_metadata_dir)

# Optional: set any metadata that rarely changes.
RE.md['beamline_id'] = 'SST-1 RSoXS'

# Add a callback that prints scan IDs at the start of each scan.
def print_scan_ids(name, start_doc):
    print("Transient Scan ID: {0} @ {1}".format(start_doc['scan_id'],time.strftime("%Y/%m/%d %H:%M:%S")))
    print("Persistent Unique Scan ID: '{0}'".format(start_doc['uid']))

RE.subscribe(print_scan_ids, 'start')

control_layer = os.getenv('OPHYD_CONTROL_LAYER')

#print(f'You are using the "{control_layer}" control layer')

# getting rid of the warnings
import logging
logging.getLogger('caproto').setLevel('ERROR')
bec.disable_baseline()

from bluesky.callbacks.zmq import Publisher
publisher = Publisher('localhost:5577')
RE.subscribe(publisher)

logging.getLogger('ophyd').setLevel('WARNING')

