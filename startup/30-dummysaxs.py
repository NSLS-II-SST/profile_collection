run_report(__file__)

from ophyd.sim import SynSignalWithRegistry, SynSignal
from ophyd import Device, Component, Signal
import numpy as np

def make_random_array():
    # return numpy array
    return np.zeros(1000,1000)

class SimGreatEyes(Device):
    image = Component(SynSignalWithRegistry, func=make_random_array, save_path='/tmp/sim_detector_stroage/')
    some_other_thing = Component(Signal, value=3)
    a_dynamic_thing = Component(SynSignal, func=lambda: 3 + random.random())

saxs_det = SimGreatEyes(name="Simulated SAXS camera")