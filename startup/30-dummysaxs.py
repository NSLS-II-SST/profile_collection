run_report(__file__)

from ophyd.sim import SynSignalWithRegistry, SynSignal
from ophyd import Device, Component, Signal
import numpy as np

def make_random_array():
    # return numpy array
    return np.zeros([1000,1000])
class SimGreatEyesCam(Device):
    shutter_mode = Component(Signal, value=3)
    acquire_time = Component(SynSignal, func=lambda: 3 + np.random.rand())


class SimGreatEyes(Device):
    image = Component(SynSignalWithRegistry, func=make_random_array, save_path='/tmp/sim_detector_stroage/')
    cam= Component(SimGreatEyesCam)


saxs_det = SimGreatEyes(name="Simulated SAXS camera")