import numpy as np
import bluesky.plans as bp
import bluesky.plan_stubs as bps
import pandas as pd
import bluesky_darkframes
from IPython.core.magic import register_line_magic
from suitcase import tiff_series, csv
from datetime import datetime
from bluesky.preprocessors import make_decorator
import queue

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

dark_frames_enable = make_decorator(dark_frame_preprocessor)()
RE.preprocessors.append(dark_frame_preprocessor)
# not doing this because EVERYTHING that goes through RE will get a dark image - this is excessive - fixed now!
from bluesky.suspenders import SuspendBoolHigh

suspend = SuspendBoolHigh(psh1.state,sleep = 10, tripped_message="Beam Shutter Closed, waiting for it to open")
RE.install_suspender(suspend)


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



def spiralsearch(radius=1, stepsize=.2):
    x_center = sam_X.user_setpoint.value
    y_center = sam_Y.user_setpoint.value
    num = round(radius / stepsize)

    yield from spiral_square([sw_det, en.energy, Beamstop_SAXS, IzeroMesh], sam_X, sam_Y, x_center=x_center, y_center=y_center,
                     x_range=radius, y_range=radius, x_num=num, y_num=num)


def spiralsearch_all(barin=[]):
    for sample in barin:
        yield from load_sample(sample)
        RE.md['project_name'] = 'spiral_searches'
        yield from spiralsearch()


def stability_scans(num):
    scans = np.arange(num)
    for scan in scans:
        yield from bps.mv(en, 200)
        yield from bp.scan([IzeroMesh],en,200,1400,1201)


def image_bar(bar):
    global loc_Q
    loc_Q = queue.Queue(1)
    ypos = np.arange(-100,110,25)
    images = []
    for pos in ypos:
        yield from bps.mv(sam_viewer,pos)
        imageuid = yield from bp.count([SampleViewer_cam],1)
        print(imageuid)
        images.append(next(db[imageuid].data('Sample Imager Detector Area Camera_image')))
    stich_sample(images, 25,5)
    update_bar(bar, loc_Q)


def bar_add_from_click(event):
    global bar
    #print(event.xdata, event.ydata)
    if(isinstance(bar,list)):
        barnum = int(input('Bar location : '))

        #print(event.xdata,event.ydata)
        if barnum >=0 and barnum < len(bar) :
            bar[barnum]['location'][0] = {'motor' : 'x','position': event.xdata}
            bar[barnum]['location'][1] = {'motor' : 'y','position': event.ydata}
            bar[barnum]['location'][2] = {'motor' : 'z','position': 0}
            bar[barnum]['location'][3] = {'motor' : 'th','position': 0}
            print('position added')
        else:
            print('Invalid bar location')
    else:
        print('invalid bar')


def update_bar(bar,loc_Q):
    from threading import Thread
    try:
        loc_Q.get_nowait()
    except Exception:
        ...

    def worker():
        global bar
        for sample in bar:
            print(f'Click on {sample["sample_name"]} location or press enter on plot to skip, space to end')
            # ipython input x,y or click in plt which outputs x, y location
            while True:
                try:
                    #print('trying')
                    item = loc_Q.get(timeout=1)
                except Exception:
                    #print('no item')
                    ...
                else:
                    #print('got something')
                    break
            if item is not 'enter' or ' ' and isinstance(item,list):
                sample['location'] = item
            elif item is ' ':
                print('aborting')
                break
            elif item is'enter':
                print(f'leaving this {sample["sample_name"]} unchanged')
        print("done")
    t = Thread(target=worker)
    t.start()

def stich_sample(images, step_size, y_off):
    pixel_step = int(step_size * (1760) / 25)
    pixel_overlap = 2464 - pixel_step
    result = images[0]
    i = 0
    for image in images[1:]:
        i += 1
        result = np.concatenate((image[(y_off * i):, :], result[:-(y_off), pixel_overlap:]), axis=1)
    fig, ax = plt.subplots()
    ax.imshow(result, extent=[0, 235, 0, 29])
    fig.canvas.mpl_connect('button_press_event', plot_click)
    fig.canvas.mpl_connect('key_press_event', plot_key_press)
    plt.show()
    return result


def print_click(event):
    #print(event.xdata, event.ydata)
    global bar, barloc
    item = []
    item.append({'motor': 'x', 'position': event.xdata})
    item.append({'motor': 'y', 'position': event.ydata})
    item.append({'motor': 'z', 'position': 0})
    item.append({'motor': 'th', 'position': 0})
    bar[loc]['location'] = item
    print(f'Setting location {barloc} on bar to clicked position')


def plot_click(event):
    #print(event.xdata, event.ydata)
    global loc_Q
    item = []
    item.append({'motor': 'x', 'position': event.xdata, 'order': 0})
    item.append({'motor': 'y', 'position': event.ydata, 'order': 0})
    item.append({'motor': 'z', 'position': 0, 'order': 0})
    item.append({'motor': 'th', 'position': 0, 'order': 0})
    if not loc_Q.full() and event.button == 3:
        loc_Q.put(item,block=False)


def plot_key_press(event):
    global loc_Q
    if not loc_Q.full() and event.key == 'enter':
        loc_Q.put(event.key,block=False)


def set_loc(bar_name,locnum):
    global bar, barloc
    bar = bar_name
    barloc = locnum


