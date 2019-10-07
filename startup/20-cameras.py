run_report(__file__)

import time as ttime  # tea time
from types import SimpleNamespace
from datetime import datetime
from ophyd import (ProsilicaDetector, SingleTrigger, TIFFPlugin,
                   ImagePlugin, StatsPlugin, DetectorBase, HDF5Plugin,
                   AreaDetector, EpicsSignal, EpicsSignalRO, ROIPlugin,
                   TransformPlugin, ProcessPlugin, Device, DeviceStatus,
                   OverlayPlugin, ProsilicaDetectorCam, ColorConvPlugin)

from ophyd.status import StatusBase
from ophyd.device import Staged
from ophyd.areadetector.cam import AreaDetectorCam
from ophyd.areadetector.base import ADComponent, EpicsSignalWithRBV
from ophyd.areadetector.filestore_mixins import (FileStoreTIFFIterativeWrite,
                                                 FileStoreHDF5IterativeWrite,
                                                 FileStoreBase, new_short_uid,
                                                 FileStoreIterativeWrite)
from ophyd import Component as Cpt, Signal
from ophyd.utils import set_and_wait
from pathlib import PurePath
from bluesky.plan_stubs import stage, unstage, open_run, close_run, trigger_and_read, pause
from collections import OrderedDict

from nslsii.ad33 import SingleTriggerV33, StatsPluginV33, CamV33Mixin


class TIFFPluginWithFileStore(TIFFPlugin, FileStoreTIFFIterativeWrite):
    """Add this as a component to detectors that write TIFFs."""
    pass


class TIFFPluginEnsuredOff(TIFFPlugin):
    """Add this as a component to detectors that do not write TIFFs."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stage_sigs.update([('auto_save', 'No')])


class ProsilicaDetectorCamV33(ProsilicaDetectorCam):
    '''This is used to update the Standard Prosilica to AD33. It adds the
process
    '''
    wait_for_plugins = Cpt(EpicsSignal, 'WaitForPlugins',
                           string=True, kind='hinted')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stage_sigs['wait_for_plugins'] = 'Yes'

    def ensure_nonblocking(self):
        self.stage_sigs['wait_for_plugins'] = 'Yes'
        for c in self.parent.component_names:
            cpt = getattr(self.parent, c)
            if cpt is self:
                continue
            if hasattr(cpt, 'ensure_nonblocking'):
                cpt.ensure_nonblocking()


class StandardProsilica(SingleTrigger, ProsilicaDetector):
    image = Cpt(ImagePlugin, 'image1:')
    stats1 = Cpt(StatsPlugin, 'Stats1:')
    stats2 = Cpt(StatsPlugin, 'Stats2:')
    stats3 = Cpt(StatsPlugin, 'Stats3:')
    stats4 = Cpt(StatsPlugin, 'Stats4:')
    stats5 = Cpt(StatsPlugin, 'Stats5:')
    trans1 = Cpt(TransformPlugin, 'Trans1:')
    roi1 = Cpt(ROIPlugin, 'ROI1:')
    roi2 = Cpt(ROIPlugin, 'ROI2:')
    roi3 = Cpt(ROIPlugin, 'ROI3:')
    roi4 = Cpt(ROIPlugin, 'ROI4:')
    proc1 = Cpt(ProcessPlugin, 'Proc1:')
    over1 = Cpt(OverlayPlugin, 'Over1:')
    cc1 = Cpt(ColorConvPlugin, 'CC1:')

    # This class does not save TIFFs. We make it aware of the TIFF plugin
    # only so that it can ensure that the plugin is not auto-saving.
    tiff = Cpt(TIFFPluginEnsuredOff, suffix='TIFF1:')

    @property
    def hints(self):
        return {'fields': [self.stats1.total.name]}


class StandardProsilicaV33(SingleTriggerV33, ProsilicaDetector):
    cam = Cpt(ProsilicaDetectorCamV33, 'cam1:')
    image = Cpt(ImagePlugin, 'image1:')
    stats1 = Cpt(StatsPluginV33, 'Stats1:')
    stats2 = Cpt(StatsPluginV33, 'Stats2:')
    stats3 = Cpt(StatsPluginV33, 'Stats3:')
    stats4 = Cpt(StatsPluginV33, 'Stats4:')
    stats5 = Cpt(StatsPluginV33, 'Stats5:')
    trans1 = Cpt(TransformPlugin, 'Trans1:')
    roi1 = Cpt(ROIPlugin, 'ROI1:')
    roi2 = Cpt(ROIPlugin, 'ROI2:')
    roi3 = Cpt(ROIPlugin, 'ROI3:')
    roi4 = Cpt(ROIPlugin, 'ROI4:')
    proc1 = Cpt(ProcessPlugin, 'Proc1:')
    over1 = Cpt(OverlayPlugin, 'Over1:')

    # This class does not save TIFFs. We make it aware of the TIFF plugin
    # only so that it can ensure that the plugin is not auto-saving.
    tiff = Cpt(TIFFPluginEnsuredOff, suffix='TIFF1:')

    @property
    def hints(self):
        return {'fields': [self.stats1.total.name]}


class StandardProsilicaWithTIFF(StandardProsilica):
    tiff = Cpt(TIFFPluginWithFileStore,
               suffix='TIFF1:',
               write_path_template='/DATA/images/data/%Y/%m/%d/',
               root='/DATA/images/data',
               reg=db.reg)


class StandardProsilicaWithTIFFV33(StandardProsilicaV33):
    tiff = Cpt(TIFFPluginWithFileStore,
               suffix='TIFF1:',
               write_path_template='/XF11ID/data/%Y/%m/%d/',
               root='/XF11ID/data',
               reg=db.reg)


Side_cam = StandardProsilica('XF:07ID1-ES:1{Scr:2}', name='RSoXS Sample Area Camera')
DetS_cam = StandardProsilica('XF:07ID1-ES:1{Scr:3}', name='WAXS Detector Area Camera')
Izero_cam = StandardProsilica('XF:07ID1-ES:1{Scr:1}', name='Izero YAG Camera')
Sample_cam = StandardProsilica('XF:07ID1-ES:1{Scr:4}', name='RSoXS Sample Area Camera')
SampleViewer_cam = StandardProsilicaWithTIFF('XF:07ID1-ES:1{Scr:5}', name='Sample Imager Detector Area Camera')

crosshair = Sample_cam.over1.overlay_1
Sample_cam.over1.overlay_1.position_y.kind='hinted'
Sample_cam.over1.overlay_1.position_x.kind='hinted'
crosshair.x = crosshair.position_x
crosshair.y = crosshair.position_y

crosshair_side = Side_cam.over1.overlay_1
crosshair_side.x = crosshair_side.position_x
crosshair_side.y = crosshair_side.position_y
crosshair_side.x.kind='hinted'
crosshair_side.y.kind='hinted'

crosshair_saxs = DetS_cam.over1.overlay_1
crosshair_saxs.x = crosshair_saxs.position_x
crosshair_saxs.y = crosshair_saxs.position_y
crosshair_saxs.x.kind='hinted'
crosshair_saxs.y.kind='hinted'


def crosshair_on():crosshair.use.set(1)


def crosshair_off():crosshair.use.set(0)


all_standard_pros = [Sample_cam, DetS_cam, Izero_cam, SampleViewer_cam]
for camera in all_standard_pros:
    camera.read_attrs = ['stats1', 'stats2', 'stats3', 'stats4', 'stats5']
    # camera.tiff.read_attrs = []  # leaving just the 'image'
    for stats_name in ['stats1', 'stats2', 'stats3', 'stats4', 'stats5']:
        stats_plugin = getattr(camera, stats_name)
        stats_plugin.read_attrs = ['total']
        #camera.stage_sigs[stats_plugin.blocking_callbacks] = 1

    #The following 2 lines should be used when not running AD V33
    #camera.stage_sigs[camera.roi1.blocking_callbacks] = 1
    #camera.stage_sigs[camera.trans1.blocking_callbacks] = 1

    #The following line should only be used when running AD V33
    # camera.cam.ensure_nonblocking()

    camera.stage_sigs[camera.cam.trigger_mode] = 'Fixed Rate'
