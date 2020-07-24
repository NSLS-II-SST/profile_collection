run_report(__file__)

from ophyd.sim import SynSignalWithRegistry, SynSignal
from ophyd import Device, Component, Signal, DeviceStatus
import numpy as np
import threading

def make_random_array():
    # return numpy array
    return np.zeros([100,100])


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
#  test out the nxsas suitcase
#  (/home/xf07id1/conda_envs/nxsas-analysis-2019-3.0) xf07id1@xf07id1-ws19:~$ ipython --profile=collection
# In [1]: import suitcase.nxsas
# In [2]: h = db[-1]
# In [3]: suitcase.nxsas.export(h.documents(), directory=".")



class PatchedSynSignalWithRegistry(SynSignalWithRegistry, Device):
    def trigger(self):
        "Promptly return  a status object that will be marked 'done' after self.exposure_time seconds."
        super().trigger()  # returns NullStatus, which is "done" immediately -- let's do better
        status = DeviceStatus(self)
        # In the background, wait for `self.exposure_time` seconds and then mark the status as "done".
        threading.Timer(self.exposure_time, status._finished).start()
        return status


class SimGreatEyes(Device):
    image = Component(PatchedSynSignalWithRegistry,
                      func=make_random_array,
                      save_path='/DATA/images/data/%Y/%m/%d/',
                      exposure_time=2)
    cam= Component(SimGreatEyesCam)

    def stage(self):
        print("staging")
        return super().stage()

    def unstage(self):
        print("unstaging")
        return super().unstage()

    def trigger(self):
        print("trigger")
        return self.image.trigger()

    def collect_asset_docs(self):
        print('collecting documents')
        yield from self.image.collect_asset_docs()
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
        self.image.exposure_time = secs

    def exptime(self):
        return ("{} has an exposure time of {} seconds".format(
            colored(self.name, 'lightblue'),
            colored(str(self.image.exposure_time), 'lightgreen')))

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