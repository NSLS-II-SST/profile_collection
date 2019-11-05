import numpy as np
import bluesky.plans as bp
import bluesky.plan_stubs as bps
import pandas as pd
import bluesky_darkframes
from IPython.core.magic import register_line_magic
from suitcase import tiff_series, csv
import datetime
from bluesky.preprocessors import make_decorator
import queue
from PIL import Image

run_report(__file__)


def set_exposure(exposure):
    if exposure > 0.001 and exposure < 1000 :
        sw_det.set_exposure(exposure)
        RSoXS_Diodes.set_exposure(exposure)
        RSoXS_DrainCurrent.set_exposure(exposure)
    else:
        print('Invalid time, exposure time not set')


def exposure():
    return (sw_det.exposure()+'\n'+
            RSoXS_Diodes.exposure()+'\n'+
            RSoXS_DrainCurrent.exposure()+'\n')


@register_line_magic
def exp(line):
    try:
        secs = float(line)
    except:
        boxed_text('Exposure times',exposure(),'lightgreen',shrink=True)
    else:
        if secs > 0.001 and secs < 1000:
            set_exposure(secs)
del exp


@register_line_magic
def binning(line):
    try:
        bins = int(line)
    except:
        boxed_text('Pixel Binning',sw_det.binning(),'lightpurple',shrink=True)
    else:
        if bins > 0 and bins < 100:
            sw_det.set_binning(bins)
del binning


@register_line_magic
def temp(line):
    boxed_text('Detector cooling',sw_det.cooling_state(),'blue',shrink=True,width=95)
del temp


@register_line_magic
def cool(line):
    sw_det.cooling_on()
del cool


@register_line_magic
def warm(line):
    sw_det.cooling_off()
del warm


@register_line_magic
def dark(line):
    sw_det.shutter_off()
del dark


@register_line_magic
def darkoff(line):
    sw_det.shutter_on()
del darkoff


def dark_plan():
    shutterstate = sw_det.saxs.cam.sync.setpoint
    yield from bps.mv(sw_det.saxs.cam.sync,0) # disable shutter
    yield from bps.trigger(sw_det, group='darkframe-trigger')
    yield from bps.wait('darkframe-trigger')
    snapshot = bluesky_darkframes.SnapshotDevice(sw_det)
    yield from bps.mv(sw_det.saxs.cam.sync,shutterstate)  # put shutter back in previous state
    return snapshot


dark_frame_preprocessor = bluesky_darkframes.DarkFramePreprocessor(
    dark_plan=dark_plan,
    detector=sw_det,
    max_age=300,
    locked_signals=[sw_det.saxs.cam.acquire_time,
                    Det_S.user_setpoint,
                    Det_W.user_setpoint,
                    sw_det.saxs.cam.bin_x,
                    sw_det.saxs.cam.bin_y,
                    sw_det.waxs.cam.bin_x,
                    sw_det.waxs.cam.bin_y,
                    sam_X.user_setpoint,
                    sam_Y.user_setpoint,
                    ],
    limit=50)


# possibly add a exposure time preprocessor to check beam exposure on CCD over exposure

# if some number of pixels are over exposured, repeat acquisition at .3 exposure time

# if there is no scatter, pause
dark_frames_enable = make_decorator(dark_frame_preprocessor)()
RE.preprocessors.append(dark_frame_preprocessor)
# not doing this because EVERYTHING that goes through RE will get a dark image - this is excessive - fixed now!



def buildeputable(start, stop, step, widfract, startinggap,name):
    ens = np.arange(start,stop,step)
    gaps = []
    ensout = []
    heights = []
    IzeroDiode.kind= 'hinted'
    #startinggap = epugap_from_energy(ens[0]) #get starting position from existing table

    count = 0
    for energy in ens:
        yield from bps.mv(mono_en,energy)
        yield from bps.mv(epu_gap,max(20000,startinggap-500*widfract))
        #yield from bp.scan([DM4_PD],epu_gap,
        #                   min(99500,max(20000,startinggap-1500*widfract)),
        #                   min(100000,max(21500,startinggap+1500*widfract)),
        #                   51)
        yield from tune_max([IzeroMesh],"Izero Mesh Current",epu_gap,
                                    min(99500,max(20000,startinggap-500*widfract)),
                                    min(100000,max(21500,startinggap+1000*widfract)),
                                    10*widfract,7,3,True)

        gaps.append(bec.peaks.max["Izero Mesh Current"][0])
        heights.append(bec.peaks.max["Izero Mesh Current"][1])
        ensout.append(mono_en.position)
        startinggap = bec.peaks.max["Izero Mesh Current"][0]
        #data = np.column_stack((ensout, gaps))
        data = {'Energies': ensout, 'EPUGaps': gaps, 'PeakCurrent': heights}
        dataframe = pd.DataFrame(data=data)
        dataframe.to_csv('/mnt/zdrive/EPUdata' + name + '.csv')
        count+=1
        if count > 50:
            count=0
            plt.close()
    #print(ens,gaps)


def do_some_eputables():
    yield from buildeputable(150, 1500, 10, 1, 21000, 'Harmonic1Phase')
    #yield from buildeputable(850, 2500, 10, 1.5, 27650, 'H3v2')
    yield from buildeputable(750, 2500, 10, 2, 20500, 'H5v2')
    yield from buildeputable(1050, 2500, 10, 2, 20500, 'H7v1')
    yield from buildeputable(1350, 2500, 10, 2, 20500, 'H9v1')
    yield from buildeputable(1650, 2500, 10, 2, 20500, 'H11v1')




def tune_max(
        detectors, signal, motor,
        start, stop, min_step,
        num=10,
        step_factor=3.0,
        snake=False,
        *, md=None):
    r"""
    plan: tune a motor to the maximum of signal(motor)

    Initially, traverse the range from start to stop with
    the number of points specified.  Repeat with progressively
    smaller step size until the minimum step size is reached.
    Rescans will be centered on the signal maximum
    with original scan range reduced by ``step_factor``.

    Set ``snake=True`` if your positions are reproducible
    moving from either direction.  This will not
    decrease the number of traversals required to reach convergence.
    Snake motion reduces the total time spent on motion
    to reset the positioner.  For some positioners, such as
    those with hysteresis, snake scanning may not be appropriate.
    For such positioners, always approach the positions from the
    same direction.

    Note:  if there are multiple maxima, this function may find a smaller one
    unless the initial number of steps is large enough.

    Parameters
    ----------
    detectors : Signal
        list of 'readable' objects
    signal : string
        detector field whose output is to maximize
    motor : object
        any 'settable' object (motor, temp controller, etc.)
    start : float
        start of range
    stop : float
        end of range, note: start < stop
    min_step : float
        smallest step size to use.
    num : int, optional
        number of points with each traversal, default = 10
    step_factor : float, optional
        used in calculating new range after each pass

        note: step_factor > 1.0, default = 3
    snake : bool, optional
        if False (default), always scan from start to stop
    md : dict, optional
        metadata

    Examples
    --------
    Find the center of a peak using synthetic hardware.

     from ophyd.sim import SynAxis, SynGauss
     motor = SynAxis(name='motor')
     det = SynGauss(name='det', motor, 'motor',
                    center=-1.3, Imax=1e5, sigma=0.05)
     RE(tune_max([det], "det", motor, -1.5, -0.5, 0.01, 10))
    """
    if min_step <= 0:
        raise ValueError("min_step must be positive")
    if step_factor <= 1.0:
        raise ValueError("step_factor must be greater than 1.0")
    try:
        motor_name, = motor.hints['fields']
    except (AttributeError, ValueError):
        motor_name = motor.name
    _md = {'detectors': [det.name for det in detectors],
           'motors': [motor.name],
           'plan_args': {'detectors': list(map(repr, detectors)),
                         'motor': repr(motor),
                         'start': start,
                         'stop': stop,
                         'num': num,
                         'min_step': min_step, },
           'plan_name': 'tune_centroid',
           'hints': {},
           }
    _md.update(md or {})
    try:
        dimensions = [(motor.hints['fields'], 'primary')]
    except (AttributeError, KeyError):
        pass
    else:
        _md['hints'].setdefault('dimensions', dimensions)

    low_limit = min(start, stop)
    high_limit = max(start, stop)

    @bpp.stage_decorator(list(detectors) + [motor])
    @bpp.run_decorator(md=_md)
    def _tune_core(start, stop, num, signal):
        next_pos = start
        step = (stop - start) / (num - 1)
        peak_position = None
        cur_I = None
        max_I = -1e50  # for peak maximum finding (allow for negative values)
        max_xI = 0

        while abs(step) >= min_step and low_limit <= next_pos <= high_limit:
            yield Msg('checkpoint')
            yield from bps.mv(motor, next_pos)
            ret = (yield from bps.trigger_and_read(detectors + [motor]))
            cur_I = ret[signal]['value']
            position = ret[motor_name]['value']

            if cur_I > max_I:
                max_I = cur_I
                max_xI = position

            next_pos += step
            in_range = min(start, stop) <= next_pos <= max(start, stop)

            if not in_range:
                if max_I == -1e50:
                    return
                peak_position = max_xI  # centroid
                max_xI, max_I = 0, 0  # reset for next pass
                new_scan_range = (stop - start) / step_factor
                start = np.clip(peak_position - new_scan_range / 2,
                                low_limit, high_limit)
                stop = np.clip(peak_position + new_scan_range / 2,
                               low_limit, high_limit)
                if snake:
                    start, stop = stop, start
                step = (stop - start) / (num - 1)
                next_pos = start
                # print("peak position = {}".format(peak_position))
                # print("start = {}".format(start))
                # print("stop = {}".format(stop))

        # finally, move to peak position
        if peak_position is not None:
            # improvement: report final peak_position
            # print("final position = {}".format(peak_position))
            yield from bps.mv(motor, peak_position)

    return (yield from _tune_core(start, stop, num, signal))


def quicksnap():
    '''
    snap of detectors to clear any charge from light hitting them - needed before starting scans or snapping images
    :return:
    '''
    set_exposure(1)
    binsave = sw_det.saxs.cam.bin_x.value
    sw_det.saxs.cam.bin_x.set(16)
    sw_det.saxs.cam.bin_y.set(16)
    sw_det.waxs.cam.bin_x.set(16)
    sw_det.waxs.cam.bin_y.set(16)
    samsave = RE.md['sample_name']
    samidsave = RE.md['sample_id']
    RE.md['sample_name'] = 'CCDClear'
    RE.md['sample_id'] = '000'
    yield from bp.count([sw_det, en, Beamstop_SAXS, Beamstop_SAXS, IzeroMesh], num=2)
    RE.md['sample_name'] = samsave
    RE.md['sample_id'] = samidsave
    sw_det.set_binning(binsave)


# @dark_frames_enable
def snapshot(secs=0, count=1, name='snap', energy = None):
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
        secs = sw_det.saxs.cam.acquire_time.value

    if secs == 1:
        secss = ''
    else:
        secss = 's'

    if isinstance(energy, float):
        yield from bps.mv(en,energy)

    boxed_text('Snapshot','Taking {} snapshot{} of {} second{} named {} at {} eV'.format(count,
                                                                                         counts,
                                                                                         secs,
                                                                                         secss,
                                                                                         name,
                                                                                         energy),'red')
    samsave = RE.md['sample_name']
    samidsave = RE.md['sample_id']
    light_was_on = False
    # if samplelight.value is 1:
    #     samplelight.off()
    #     light_was_on = True
    #     boxed_text('Warning','light was on, taking a quick snapshot to clear CCDs','yellow',shrink=True)
    #     sw_det.shutter_off()
    #     yield from quicksnap()
    #     sw_det.shutter_on()
    if secs:
        set_exposure(secs)
    RE.md['sample_name'] = name
    RE.md['sample_id'] = '000'
    Beamstop_SAXS.kind = "hinted"
    Beamstop_WAXS.kind = "hinted"
    IzeroMesh.kind = "hinted"
    SlitTop_I.kind = "hinted"
    SlitBottom_I.kind = "hinted"
    SlitOut_I.kind = "hinted"
    yield from bp.count([sw_det,
                         en.energy,
                         Beamstop_WAXS,
                         IzeroMesh],
                        num=count)
    # if light_was_on:
    #     samplelight.on()

    RE.md['sample_name'] = samsave
    RE.md['sample_id'] = samidsave


@register_line_magic
def snap(line):
    try:
        secs = float(line)
    except:
        RE(snapshot())
    else:
        if secs > 0 and secs < 100:
            RE(snapshot(secs))
del snap

@register_line_magic
def snaps(line):
    try:
        num = int(line)
    except:
        RE(snapshot())
    else:
        if num > 0 and num < 100:
            RE(snapshot(count=num))
del snaps

def stability_scans(num):
    scans = np.arange(num)
    for scan in scans:
        yield from bps.mv(en, 200)
        yield from bp.scan([IzeroMesh],en,200,1400,1201)


def vent():
    yield from psh10.close()
    yield from gv28.close()
    yield from gv27a.close()
    yield from bps.mv(sam_Y,349)

    print('waiting for you to close the load lock gate valve')
    print('Please also close the small manual black valve on the back of the load lock now')
    while gvll.state.value is 1:
        gvll.read() # attempt at a fix for problem where macro hangs here.
        bps.sleep(1)
    print('TEM load lock closed - turning off loadlock gauge')
    yield from bps.mv(ll_gpwr,0)
    print('Should be safe to begin vent by pressing right most button of BOTTOM turbo controller once')
    print('')
