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
    bin_x = Component(Signal, value=3)
    bin_y = Component(Signal, value=3)
    temperature = Component(Signal, value=-80)
    temperature_actual = Component(Signal, value=-80)
    enable_cooling = Component(Signal, value=1)

    def collect_asset_docs(self):
        yield from []






class SimGreatEyes(Device):
    image = Component(SynSignalWithRegistry, func=make_random_array, save_path='/tmp/sim_detector_storage/')
    cam= Component(SimGreatEyesCam)

    def collect_asset_docs(self):
        yield from []
    def shutter(self):
        switch = {
            0: 'disabled',
            1: 'enabled',
            3: 'unknown',
            4: 'unknown',
            2: 'enabled'
        }
        # return ('Shutter is {}'.format(switch[self.cam.sync.value]))
        return ('Shutter is {}'.format(switch[self.cam.shutter_mode.value]))

    def shutter_on(self):
        # self.cam.sync.set(1)
        self.cam.shutter_mode.set(2)

    def shutter_off(self):
        # self.cam.sync.set(0)
        self.cam.shutter_mode.set(0)

    def set_exptime(self, secs):
        self.cam.acquire_time.set(secs)

    def exptime(self):
        return ("{} has an exposure time of {} seconds".format(
            colored(self.name, 'lightblue'),
            colored(str(self.cam.acquire_time.value), 'lightgreen')))

    def set_temp(self, degc):
        self.cam.temperature.set(degc)
        self.cam.enable_cooling.set(1)

    def cooling_off(self):
        self.cam.enable_cooling.set(0)

    #    def setROI(self,):
    #        self.cam.

    def cooling_state(self):
        if self.cam.enable_cooling.value:
            self.cam.temperature_actual.read()
            if self.cam.temperature_actual.value - self.cam.temperature.value > 1.0:
                return ("\nTemperature of {} ({} °C) is not at setpoint ({} °C) but cooling is on".format(
                    colored(self.name, 'lightblue'),
                    colored(self.cam.temperature_actual.value, 'red'),
                    colored(self.cam.temperature.value, 'blue')))
            else:
                return ("\nTemperature of {} ({} °C) is at setpoint ({} °C) and cooling is on".format(
                    colored(self.name, 'lightblue'),
                    colored(self.cam.temperature_actual.value, 'green'),
                    colored(self.cam.temperature.value, 'blue')))
        else:
            if self.cam.temperature_actual.value - self.cam.temperature.value > 1.0:
                return ("\nTemperature of {} ({} °C) is not at setpoint ({} °C) and cooling is off".format(
                    colored(self.name, 'lightblue'),
                    colored(self.cam.temperature_actual.value, 'red'),
                    colored(self.cam.temperature.value, 'lightgray')))
            else:
                return ("\nTemperature of {} ({} °C) is at setpoint ({} °C), but cooling is off".format(
                    colored(self.name, 'lightblue'),
                    colored(self.cam.temperature_actual.value, 'green'),
                    colored(self.cam.temperature.value, 'lightgray')))

    def set_binning(self, binx, biny):
        self.cam.bin_x.set(binx)
        self.cam.bin_y.set(biny)

    def binning(self):
        return ('Binning of {} is set to ({},{}) pixels'.format(
            colored(self.name, 'lightblue'),
            colored(self.cam.bin_x.value, 'lightpurple'),
            colored(self.cam.bin_y.value, 'lightpurple')))

    def exposure(self):
        return self.exptime()

    def set_exposure(self, seconds):
        self.set_exptime(seconds)


saxs_det = SimGreatEyes(name="Simulated SAXS camera")