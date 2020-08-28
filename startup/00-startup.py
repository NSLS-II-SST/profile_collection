from IPython.utils.coloransi import TermColors as color

import os

import nslsii


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
