
from ..RSoXSBase.detectors import *

    #sudo mount -t cifs //10.7.0.217/data/ /mnt/zdrive -o user=linuxuser,pass=greateyes
    #needs to be run on the server
    # sudo mount -t cifs //10.7.0.217/data/ /mnt/zdrive -o user=linuxuser,pass=greateyes

#saxs_det = RSOXSGreatEyesDetector('XF:07ID1-ES:1{GE:1}', name='Small Angle CCD Detector',
#                                  read_attrs=['tiff', 'stats1.total'])
#saxs_det.transform_type = 3
#saxs_det.cam.ensure_nonblocking()
#
#
#
waxs_det = RSOXSGreatEyesDetector('XF:07ID1-ES:1{GE:2}', name='Wide Angle CCD Detector',
                                   read_attrs=['tiff', 'stats1.total'])

waxs_det.transform_type = 1
waxs_det.cam.ensure_nonblocking()


# sw_det = SyncedDetectors('', name='Synced')
# sw_det.saxs.name = "SAXS"
# sw_det.waxs.name = "WAXS"
#saxs_det.stats1.name = "SAXS fullframe"
waxs_det.stats1.name = "WAXS fullframe"
#saxs_det.stats1.kind = 'hinted'
waxs_det.stats1.kind = 'hinted'
#saxs_det.stats1.total.kind = 'hinted'
waxs_det.stats1.total.kind = 'hinted'
#saxs_det.stats2.name = "SAXS ROI"
#waxs_det.stats2.name = "WAXS ROI"
#saxs_det.stats2.kind = 'hinted'
#waxs_det.stats2.kind = 'hinted'
#saxs_det.stats2.total.kind = 'hinted'
#waxs_det.stats2.total.kind = 'hinted'
# sw_det.saxs.cam.sync.set(1)
# sw_det.waxs.cam.sync.set(1)
#
# #change this to saxs or waxs to record what the shutter state is
# shutter_status_w = sw_det.waxs.cam.sync
# shutter_status_s = saxs_det.cam.sync
# ###shutter_status_s = saxs_det.cam.shutter_mode
# ###shutter_status_s.name = 'shutter mode saxs'
# sw_det.waxs.cam.acquire_time.name = 'WAXS Exposure'
# sw_det.saxs.cam.acquire_time.name = 'SAXS Exposure'
# sw_det.saxs.transform_type = 3
# sw_det.waxs.transform_type = 1
# #
# for det in [saxs_det,waxs_det]:#, waxs_det,sw_det.waxs,sw_det.saxs]:
#      det.kind = 'hinted'
#      det.stats1.kind = 'hinted'
#      det.stats1.total.kind = 'hinted'
#      det.cam.kind = 'hinted'
#      det.cam.temperature_actual.kind = 'normal'
#      det.cam.hot_side_temp.kind = 'normal'
#      det.cam.bin_y.kind = 'normal'
#      det.cam.bin_x.kind = 'normal'
#      det.cam.adc_speed.kind = 'normal'
#      det.cam.acquire_time.kind = 'normal'
#      det.cam.model.kind = 'normal'
#      det.cam.trigger_mode.kind = 'normal'
#      det.cam.sync.kind = 'normal'
#      det.cam.shutter_mode.kind = 'normal'
#      det.cam.shutter_open_delay.kind = 'normal'
#      det.cam.shutter_close_delay.kind = 'normal'
#      det.cam.min_x.kind = 'normal'
#      det.cam.temperature.kind = 'normal'
#      det.cam.min_y.kind = 'normal'
# #
#
# sw_det.kind = 'hinted'
#
# sw_det.read_attrs = ['saxs','waxs']

saxs_det = SimGreatEyes(name="Simulated SAXS camera")