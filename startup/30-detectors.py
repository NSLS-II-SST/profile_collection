run_report(__file__)

import time
from ophyd import Component as C
from ophyd import EpicsSignalRO, Device
from ophyd.areadetector.trigger_mixins import SingleTrigger
from ophyd.areadetector import (GreatEyesDetector, GreatEyesDetectorCam,
                                ImagePlugin, TIFFPlugin, StatsPlugin,
                                ProcessPlugin, ROIPlugin, TransformPlugin)
from ophyd.areadetector.filestore_mixins import FileStoreTIFFIterativeWrite


class TIFFPluginWithFileStore(TIFFPlugin, FileStoreTIFFIterativeWrite):
    """Add this as a component to detectors that write TIFFs."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class GreatEyesDetCamWithVersions(GreatEyesDetectorCam):
    adcore_version = C(EpicsSignalRO, 'ADCoreVersion_RBV')
    driver_version = C(EpicsSignalRO, 'DriverVersion_RBV')


class RSOXSGreatEyesDetector(SingleTrigger, GreatEyesDetector):
    image = C(ImagePlugin, 'image1:')
    cam = C(GreatEyesDetCamWithVersions, 'cam1:')

    tiff = C(TIFFPluginWithFileStore, 'TIFF1:',
             write_path_template='/DATA/images/data/%Y/%m/%d/',
             read_path_template='/DATA/images/data/%Y/%m/%d/',
             read_attrs=[],
             root='/DATA/images/')
    stats1 = C(StatsPlugin, 'Stats1:')
    stats2 = C(StatsPlugin, 'Stats2:')
    stats3 = C(StatsPlugin, 'Stats3:')
    stats4 = C(StatsPlugin, 'Stats4:')
    stats5 = C(StatsPlugin, 'Stats5:')
    trans1 = C(TransformPlugin, 'Trans1:')
    roi1 = C(ROIPlugin, 'ROI1:')
    roi2 = C(ROIPlugin, 'ROI2:')
    roi3 = C(ROIPlugin, 'ROI3:')
    roi4 = C(ROIPlugin, 'ROI4:')
    proc1 = C(ProcessPlugin, 'Proc1:')

    def stage(self, *args, **kwargs):
        self.cam.temperature_actual.read()
        self.cam.temperature.read()
        if abs(self.cam.temperature_actual.value - self.cam.temperature.value) > 2.0:
            boxed_text("Temperature Warning!!!!",
                      self.cooling_state()+
                      "\nPlease wait until temperature has stabilized before collecting important data.",'yellow',85)
        return [self].append(super().stage(*args, **kwargs))

    def shutter(self):
        switch = {
            0:'disabled',
            1:'unknown',
            3:'unknown',
            4:'unknown',
            2:'enabled'
        }
        return ('Shutter is {}'.format(switch[self.cam.shutter_mode.value]))

    def shutter_on(self):
        self.cam.shutter_mode.set(2)

    def shutter_off(self):
        self.cam.shutter_mode.set(0)

    def unstage(self, *args, **kwargs):
        return [self].append(super().unstage(*args, **kwargs))

    def set_exptime(self,secs):
        self.cam.acquire_time.set(secs)

    def exptime(self):
        return ("{} has an exposure time of {} seconds".format(
            colored(self.name,'lightblue'),
            colored(str(self.cam.acquire_time.value),'lightgreen')))

    def set_temp(self,degc):
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
                    colored(self.name,'lightblue'),
                    colored(self.cam.temperature_actual.value,'red'),
                    colored(self.cam.temperature.value,'blue')))
            else:
                return ("\nTemperature of {} ({} °C) is at setpoint ({} °C) and cooling is on".format(
                    colored(self.name,'lightblue'),
                    colored(self.cam.temperature_actual.value,'green'),
                    colored(self.cam.temperature.value,'blue')))
        else:
            if self.cam.temperature_actual.value - self.cam.temperature.value > 1.0:
                return ("\nTemperature of {} ({} °C) is not at setpoint ({} °C) and cooling is off".format(
                     colored(self.name,'lightblue'),
                     colored(self.cam.temperature_actual.value,'red'),
                     colored(self.cam.temperature.value,'lightgray')))
            else:
                return ("\nTemperature of {} ({} °C) is at setpoint ({} °C), but cooling is off".format(
                    colored(self.name,'lightblue'),
                    colored(self.cam.temperature_actual.value,'green'),
                    colored(self.cam.temperature.value,'lightgray')))

    def set_binning(self,binx,biny):
        self.cam.bin_x.set(binx)
        self.cam.bin_y.set(biny)

    def binning(self):
        return ('Binning of {} is set to ({},{}) pixels'.format(
            colored(self.name,'lightblue'),
            colored(self.cam.bin_x.value,'lightpurple'),
            colored(self.cam.bin_y.value,'lightpurple')))

    #sudo mount -t cifs //10.7.0.217/data/ /mnt/zdrive -o user=linuxuser,pass=greateyes
    #needs to be run on the server
    # sudo mount -t cifs //10.7.0.217/data/ /mnt/zdrive -o user=linuxuser,pass=greateyes


saxs_det = RSOXSGreatEyesDetector('XF:07ID1-ES:1{GE:1}', name='Small Angle CCD Detector',
                                  read_attrs=['tiff', 'stats1.total'])
waxs_det = RSOXSGreatEyesDetector('XF:07ID1-ES:1{GE:2}', name='Wide Angle CCD Detector',
                                  read_attrs=['tiff', 'stats1.total'])



class SyncedDetectors(Device):
    saxs = C(RSOXSGreatEyesDetector, 'XF:07ID1-ES:1{GE:1}',read_attrs=['tiff', 'stats1.total'],name="Small Angle CCD Detector")
    waxs = C(RSOXSGreatEyesDetector, 'XF:07ID1-ES:1{GE:2}',read_attrs=['tiff', 'stats1.total'],name="Wide Angle CCD Detector")

    def __init__(self, *args, **kwargs):
        self.lightwason = None
        super().__init__(*args, **kwargs)

    def stage(self, *args, **kwargs):
        listout = []
        listout.append(self.saxs.stage())
        listout.append(self.waxs.stage())
        if light.get() is 1:
            light.off()
            self.lightwason=True
            time.sleep(3)
        else:
            self.lightwason=False
        listout.append(self)
        return listout

    def unstage(self, *args, **kwargs):
        listout = []
        listout.append(self.saxs.unstage())
        listout.append(self.waxs.unstage())
        if self.lightwason:
            time.sleep(3)
            light.on()
        listout.append(self)
        return listout

    def trigger(self):
        self.waxs.cam.trigger_mode.put(0)
        waxs_status = self.waxs.trigger()
        time.sleep(0.005)
        saxs_status = self.saxs.trigger()  # not sure this is needed?
        return saxs_status & waxs_status

    def collect_asset_docs(self, *args, **kwargs):
        yield from self.saxs.collect_asset_docs(*args, **kwargs)
        yield from self.waxs.collect_asset_docs(*args, **kwargs)

    def set_exposure(self,seconds):
        self.waxs.set_exptime(seconds)
        self.saxs.set_exptime(seconds)

    def exposure(self):
        return (self.waxs.exptime() +'\n'+ self.saxs.exptime())

    def set_binning(self,pixels):
        self.saxs.set_binning(pixels,pixels)
        self.waxs.set_binning(pixels,pixels)

    def binning(self):
        return (self.saxs.binning() +'\n'+ self.waxs.binning())

    def cooling_on(self):
        self.saxs.set_temp(-80)
        self.waxs.set_temp(-80)

    def shutter_status(self):
        return self.saxs.shutter()

    def shutter_on(self):
        self.saxs.shutter_on()

    def shutter_off(self):
        self.saxs.shutter_off()

    def cooling_state(self):
        return (self.saxs.cooling_state()+ self.waxs.cooling_state())

    def cooling_off(self):
        self.saxs.cooling_off()
        self.waxs.cooling_off()
        time.sleep(2)
        self.cooling_state()

    def open_shutter(self):
        self.saxs.cam.shutter_control.set(1)

    def close_shutter(self):
        self.saxs.cam.shutter_control.set(0)

    def shutter(self):
        return self.saxs.cam.shutter_control.get()


sw_det = SyncedDetectors('', name='Synced')
sw_det.saxs.name = "SAXS"
sw_det.waxs.name = "WAXS"
sw_det.saxs.stats1.name = "SAXS ROI1"
sw_det.waxs.stats1.name = "WAXS ROI1"
shutter_status = sw_det.saxs.cam.shutter_mode
shutter_status.name = 'shutter mode'
sw_det.waxs.cam.acquire_time.name = 'WAXS Exposure'
sw_det.saxs.cam.acquire_time.name = 'SAXS Exposure'

for det in [saxs_det, waxs_det,sw_det.waxs,sw_det.saxs]:
    det.kind = 'normal'
    det.stats1.kind = 'hinted'
    det.stats1.total.kind = 'hinted'
    det.cam.kind = 'normal'
    det.cam.temperature_actual.kind = 'normal'
    det.cam.hot_side_temp.kind = 'normal'
    det.cam.bin_y.kind = 'normal'
    det.cam.bin_x.kind = 'normal'
    det.cam.adc_speed.kind = 'normal'
    det.cam.acquire_time.kind = 'hinted'
    det.cam.model.kind = 'normal'
    det.cam.trigger_mode.kind = 'normal'
    det.cam.shutter_mode.kind = 'hinted'
    det.cam.shutter_open_delay.kind = 'normal'
    det.cam.shutter_close_delay.kind = 'normal'
    det.cam.min_x.kind = 'normal'
    det.cam.temperature.kind = 'normal'
    det.cam.min_y.kind = 'normal'
sw_det.kind = 'hinted'
sw_det.waxs.cam.shutter_mode.kind='normal'

sd.baseline.extend([waxs_det.cam.temperature_actual, saxs_det.cam.temperature_actual, waxs_det.cam.hot_side_temp, saxs_det.cam.hot_side_temp , waxs_det.cam.bin_y , saxs_det.cam.bin_y ])
sd.baseline.extend([waxs_det.cam.bin_x, saxs_det.cam.bin_x, waxs_det.cam.adc_speed, saxs_det.cam.adc_speed , waxs_det.cam.acquire_time , saxs_det.cam.acquire_time ])
sd.baseline.extend([waxs_det.cam.model, saxs_det.cam.model, waxs_det.cam.trigger_mode, saxs_det.cam.trigger_mode , waxs_det.cam.shutter_mode , saxs_det.cam.shutter_mode ])
sd.baseline.extend([waxs_det.cam.shutter_open_delay, saxs_det.cam.shutter_open_delay, waxs_det.cam.shutter_close_delay, saxs_det.cam.shutter_close_delay , waxs_det.cam.min_x , saxs_det.cam.min_x ])
sd.baseline.extend([waxs_det.cam.temperature, saxs_det.cam.temperature, waxs_det.cam.min_y, saxs_det.cam.min_y  ])