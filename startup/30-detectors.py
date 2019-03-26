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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    #sudo mount -t cifs //10.7.0.217/data/ /mnt/zdrive -o user=linuxuser,pass=greateyes
    #needs to be run on the server


saxs_det = RSOXSGreatEyesDetector('XF:07ID1-ES:1{GE:1}', name='saxs_det',
                                  read_attrs=['tiff', 'stats1.total'])
waxs_det = RSOXSGreatEyesDetector('XF:07ID1-ES:1{GE:2}', name='waxs_det',
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

sw_det = SyncedDetectors('', name='sw_det')

for det in [saxs_det, waxs_det,sw_det.waxs,sw_det.saxs]:
    det.kind = 'hinted'
    det.stats1.kind = 'hinted'
    det.stats1.total.kind = 'hinted'
sw_det.kind = 'hinted'
