print(f'Loading {__file__}...')

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
             write_path_template='/mnt/zdrive/data/%Y/%m/%d/',
             read_path_template='Z:\\images\\data\\%Y\\%m\\%d\\',
             read_attrs=[],
             root='Z:\\images\\data\\')

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
    def set_temp(self,degc):
        self.cam.temperature.set(degc)
        self.cam.enable_cooling.set(1)
    def cooling_off(self):
        self.cam.enable_cooling.set(0)
#    def setROI(self,):
#        self.cam.
    def setbinning(self,binx,biny):
        self.cam.bin_x.set(binx)
        self.cam.bin_y.set(biny)
    def stage(self):
        if self.cam.temperature_actual.value - self.cam.temperature.value > 1.0:
            print("Warning! temperature of {} ({:.2f} °C) is not at setpoint ({:.2f} °C)".format(
                    self.name, self.cam.temperature_actual.value, self.cam.temperature.value))
        return [self]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    #sudo mount -t cifs //10.7.0.217/data/ /mnt/zdrive -o user=linuxuser,pass=greateyes
    #needs to be run on the server


saxs_det = RSOXSGreatEyesDetector('XF:07ID1-ES:1{GE:1}', name='Small Angle CCD Detector',
                                  read_attrs=['tiff', 'stats1.total'])
waxs_det = RSOXSGreatEyesDetector('XF:07ID1-ES:1{GE:2}', name='Wide Angle CCD Detector',
                                  read_attrs=['tiff', 'stats1.total'])


class SyncedDetectors(Device):
    saxs = C(RSOXSGreatEyesDetector, 'XF:07ID1-ES:1{GE:1}',read_attrs=['tiff', 'stats1.total'])
    waxs = C(RSOXSGreatEyesDetector, 'XF:07ID1-ES:1{GE:2}',read_attrs=['tiff', 'stats1.total'])

    def trigger(self):
        self.waxs.cam.trigger_mode.put(0)
        waxs_status = self.waxs.trigger()
        time.sleep(0.005)
        saxs_status = self.saxs.trigger()  # not sure this is needed?
        return saxs_status & waxs_status

    def collect_asset_docs(self, *args, **kwargs):
        yield from self.saxs.collect_asset_docs(*args, **kwargs)
        yield from self.waxs.collect_asset_docs(*args, **kwargs)

    def setexp(self,seconds):
        self.waxs.cam.acquire_time.set(seconds)
        self.saxs.cam.acquire_time.set(seconds)

    def setbinning(self,pixels):
        self.saxs.setbinning(pixels,pixels)
        self.waxs.setbinning(pixels,pixels)

    def cooling_on(self):
        self.saxs.set_temp(-40)  #temporary until the power supply is fixed
        self.waxs.set_temp(-80)

    def open_shutter(self):
        self.saxs.cam.shutter_control.set(1)

    def close_shutter(self):
        self.saxs.cam.shutter_control.set(0)

    def shutter(self):
        return self.saxs.cam.shutter_control.get()
    def stage(self):
        listout = self.saxs.stage()
        listout.append(self.waxs.stage())
        if light.setpoint:
            light.off()
            self.lightwason=True
            sleep(1)
        else:
            self.lightwason=False
        return listout.append(self)
    def unstage(self):
        listout = self.saxs.unstage()
        listout.append(self.waxs.unstage())
        if self.lightwason:
            light.on()
        return listout.append(self)

sw_det = SyncedDetectors('', name='Small and Wide Angle Synced CCD Detectors')

for det in [saxs_det, waxs_det,sw_det.waxs,sw_det.saxs]:
    det.kind = 'hinted'
    det.stats1.kind = 'hinted'
    det.stats1.total.kind = 'hinted'
    #det.cam.kind = 'hinted'
    det.cam.temperature_actual.kind = 'hinted'
    det.cam.hot_side_temp.kind = 'hinted'
    det.cam.bin_y.kind = 'hinted'
    det.cam.bin_x.kind = 'hinted'
    det.cam.adc_speed.kind = 'hinted'
    det.cam.acquire_time.kind = 'hinted'
    det.cam.model.kind = 'hinted'
    det.cam.trigger_mode.kind = 'hinted'
    det.cam.shutter_mode.kind = 'hinted'
    det.cam.shutter_open_delay.kind = 'hinted'
    det.cam.shutter_close_delay.kind = 'hinted'
    det.cam.min_x.kind = 'hinted'
    det.cam.temperature.kind = 'hinted'
    det.cam.min_y.kind = 'hinted'
sw_det.kind = 'hinted'

sd.baseline.extend([waxs_det.cam.temperature_actual, saxs_det.cam.temperature_actual, waxs_det.cam.hot_side_temp, saxs_det.cam.hot_side_temp , waxs_det.cam.bin_y , saxs_det.cam.bin_y ])
sd.baseline.extend([waxs_det.cam.bin_x, saxs_det.cam.bin_x, waxs_det.cam.adc_speed, saxs_det.cam.adc_speed , waxs_det.cam.acquire_time , saxs_det.cam.acquire_time ])
sd.baseline.extend([waxs_det.cam.model, saxs_det.cam.model, waxs_det.cam.trigger_mode, saxs_det.cam.trigger_mode , waxs_det.cam.shutter_mode , saxs_det.cam.shutter_mode ])
sd.baseline.extend([waxs_det.cam.shutter_open_delay, saxs_det.cam.shutter_open_delay, waxs_det.cam.shutter_close_delay, saxs_det.cam.shutter_close_delay , waxs_det.cam.min_x , saxs_det.cam.min_x ])
sd.baseline.extend([waxs_det.cam.temperature, saxs_det.cam.temperature, waxs_det.cam.min_y, saxs_det.cam.min_y  ])