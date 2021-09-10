
from ..RSoXSBase.detectors import *


#saxs_det = RSOXSGreatEyesDetector('XF:07ID1-ES:1{GE:1}', name='Small Angle CCD Detector',
#                                  read_attrs=['tiff', 'stats1.total'])
#saxs_det.transform_type = 3
#saxs_det.cam.ensure_nonblocking()
#
waxs_det = RSOXSGreatEyesDetector('XF:07ID1-ES:1{GE:2}', name='Wide Angle CCD Detector',
                                   read_attrs=['tiff', 'stats1.total'])

waxs_det.transform_type = 1
waxs_det.cam.ensure_nonblocking()


#saxs_det.stats1.name = "SAXS fullframe"
waxs_det.stats1.name = "WAXS fullframe"
#saxs_det.stats1.kind = 'hinted'
waxs_det.stats1.kind = 'hinted'
#saxs_det.stats1.total.kind = 'hinted'
waxs_det.stats1.total.kind = 'hinted'


saxs_det = SimGreatEyes(name="Simulated SAXS camera")


def set_exposure(exposure):
    if exposure > 0.001 and exposure < 1000 :
        saxs_det.set_exptime_detonly(exposure)
        waxs_det.set_exptime(exposure)
    else:
        print('Invalid time, exposure time not set')


def exposure():
    return ('   '+saxs_det.exposure()+'\n   '+waxs_det.exposure())


def snapshot(secs=0, count=1, name=None, energy = None, det= saxs_det):
    '''
    snap of detectors to clear any charge from light hitting them - needed before starting scans or snapping images
    :return:
    '''

    if count==1:
        counts = ''
    elif count <=0 :
        count = 1
        counts = ''
    else:
        count = round(count)
        counts = 's'
    if secs <= 0:
        secs = det.cam.acquire_time.get()

    if secs == 1:
        secss = ''
    else:
        secss = 's'



    if isinstance(energy, float):
        yield from bps.mv(en,energy)

    boxed_text('Snapshot','Taking {} snapshot{} of {} second{} with {} named {} at {} eV'.format(count,
                                                                                                 counts,
                                                                                                 secs,
                                                                                                 secss,det.name,
                                                                                                 name,
                                                                                                 energy),'red')
    samsave = RE.md['sample_name']
    if secs:
        set_exposure(secs)
    if name is not None:
        RE.md['sample_name'] = name

    yield from bp.count([det,
                         en.energy],
                        num=count)

    if name is not None:
        RE.md['sample_name'] = samsave

