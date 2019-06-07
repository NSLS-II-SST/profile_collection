run_report(__file__)

import numpy as np
from datetime import datetime
import bluesky.plans as bp
import bluesky.plan_stubs as bps
from suitcase import tiff_series, csv
import pandas as pd
from IPython.core.magic import register_line_magic

def set_exposure(exposure):
    if exposure > 0.001 and exposure < 1000 :
        sw_det.set_exposure(exposure)
        RSoXS_DM.set_exposure(exposure)
        RSoXS_Slits.set_exposure(exposure)
    else:
        print('Invalid time, exposure time not set')

def exposure():
    return (sw_det.exposure()+'\n'+
            RSoXS_DM.exposure()+'\n'+
            RSoXS_Slits.exposure()+'\n')

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
    boxed_text('Detector cooling',sw_det.cooling_state(),'blue',shrink=True)
del temp


@register_line_magic
def cool(line):
    sw_det.cooling_on()
del cool


@register_line_magic
def warm(line):
    sw_det.cooling_off()
del warm


def user():
    title = ("User metadata - stored in every scan:")
    text=''
    if len(RE.md["proposal_id"]) > 0 :
        text += '   proposal ID:         '+colored('{}'.format(RE.md["proposal_id"]).center(40,' '),'yellow')
    if len(RE.md["user_name"]) > 0 :
        text += '\n   User Name:           '+colored('{}'.format(RE.md["user_name"]).center(40,' '),'yellow')
    if len(RE.md["user_start_date"]) > 0 :
        text += '\n   User Start Date:     '+colored('{}'.format(RE.md["user_start_date"]).center(40,' '),'yellow')
    if len(RE.md["user_id"]) > 0 :
        text += '\n   User ID:             '+colored('{}'.format(RE.md["user_id"]).center(40,' '),'yellow')
    if len(RE.md["institution"]) > 0 :
        text += '\n   Institution:         '+colored('{}'.format(RE.md["institution"]).center(40,' '),'yellow')
    if len(RE.md["project_name"]) > 0 :
        text += '\n   project:             '+colored('{}'.format(RE.md["project_name"]).center(40,' '),'yellow')
    if len(RE.md["project_desc"]) > 0 :
        text += '\n   Project Description: '+colored('{}'.format(RE.md["project_desc"]).center(40,' '),'yellow')
    boxed_text(title, text, 'green',80,shrink=True)


def sample():
    title = "Sample metadata - stored in every scan:"
    text = ''
    if len(RE.md["proposal_id"]) > 0 :
        text += '   proposal ID:           '+colored('{}'.format(RE.md["proposal_id"]).center(38,' '),'cyan')
    if len(RE.md["user_name"]) > 0 :
        text += '\n   User Name:             '+colored('{}'.format(RE.md["user_name"]).center(38,' '),'cyan')
    if len(RE.md["institution"]) > 0 :
        text += '\n   Institution:           '+colored('{}'.format(RE.md["institution"]).center(38,' '),'cyan')
    if len(RE.md["sample_name"]) > 0 :
        text += '\n   Sample Name:           '+colored('{}'.format(RE.md["sample_name"]).center(38,' '),'cyan')
    if len(RE.md["sample_desc"]) > 0 :
        text += '\n   Sample Description:    '+colored('{}'.format(RE.md["sample_desc"]).center(38,' '),'cyan')
    if len(RE.md["sample_id"]) > 0 :
        text += '\n   Sample ID:             '+colored('{}'.format(RE.md["sample_id"]).center(38,' '),'cyan')
    if len(RE.md["sample_set"]) > 0 :
        text += '\n   Sample Set:            '+colored('{}'.format(RE.md["sample_set"]).center(38,' '),'cyan')
    if len(RE.md["sample_date"]) > 0 :
        text += '\n   Sample Creation Date:  '+colored('{}'.format(RE.md["sample_date"]).center(38,' '),'cyan')
    if len(RE.md["project_name"]) > 0 :
        text += '\n   Project name:          '+colored('{}'.format(RE.md["project_name"]).center(38,' '),'cyan')
    if len(RE.md["project_desc"]) > 0 :
        text += '\n   Project Description:   '+colored('{}'.format(RE.md["project_desc"]).center(38,' '),'cyan')
    if len(RE.md["samp_user_id"]) > 0 :
        text += '\n   Creator User ID:       '+colored('{}'.format(RE.md["samp_user_id"]).center(38,' '),'cyan')
    if len(RE.md["composition"]) > 0 :
        text += '\n   Composition(formula):  '+colored('{}'.format(RE.md["composition"]).center(38,' '),'cyan')
    if len(RE.md["density"]) > 0 :
        text += '\n   Density:               '+colored('{}'.format(RE.md["density"]).center(38,' '),'cyan')
    if len(RE.md["components"]) > 0 :
        text += '\n   List of Components:    '+colored('{}'.format(RE.md["components"]).center(38,' '),'cyan')
    if len(RE.md["thickness"]) > 0 :
        text += '\n   Thickness:             '+colored('{}'.format(RE.md["thickness"]).center(38,' '),'cyan')
    if len(RE.md["sample_state"]) > 0 :
        text += '\n   Sample state:          '+colored('{}'.format(RE.md["sample_state"]).center(38,' '),'cyan')
    if len(RE.md["notes"]) > 0 :
        text += '\n   Notes:                 '+colored('{}'.format(RE.md["notes"]).center(38,' '),'cyan')
    boxed_text(title, text, 'red',80,shrink=True)

@register_line_magic
def md(line):
    sample()

@register_line_magic
def u(line):
    user()

del md, u


def beamline_status():
    user()
    sample()
    boxed_text('Detector status',
               exposure()+'\n'+sw_det.binning()+'\n'+sw_det.cooling_state(),
               'lightblue',80,shrink=True)


@register_line_magic
def status(line):
    beamline_status()
del status

def newuser():
    print("This information will tag future data until this changes, please be as thorough as possible/n"
          "current values in parentheses, leave blank for no change")

    proposal_id = input('Your proposal id ({}): '.format(RE.md['proposal_id']))
    if proposal_id is not '':
        RE.md['proposal_id'] = proposal_id

    institution = input('Your institution ({}): '.format(RE.md['institution']))
    if institution is not '':
        RE.md['institution'] = institution

    user_name = input('Your name ({}): '.format(RE.md['user_name']))
    if user_name is not '':
        RE.md['user_name'] = user_name

    project_name = input('Your project ({}): '.format(RE.md['project_name']))
    if project_name is not '':
        RE.md['project_name'] = project_name

    project_desc = input('Your project description ({}): '.format(RE.md['project_desc']))
    if project_desc is not '':
        RE.md['project_desc'] = project_desc
    # if new, add user to database get unique ID.

    dt = datetime.now()
    user_start_date = dt.strftime('%Y-%m-%d')
    RE.md['user_start_date'] = user_start_date
    user_id = '0'
    RE.md['user_id'] = user_id
    user()
    return user_dict()


def sample_dict(sample_name = RE.md['sample_name'],
                sample_desc = RE.md['sample_desc'],
                sample_id = RE.md['sample_id'],
                sample_set = RE.md['sample_set'],
                sample_date = RE.md['sample_date'],
                project_name = RE.md['project_name'],
                project_desc = RE.md['project_desc'],
                samp_user_id = RE.md['samp_user_id'],
                composition = RE.md['composition'],
                density = RE.md['density'],
                components = RE.md['components'],
                thickness = RE.md['thickness'],
                sample_state = RE.md['sample_state'],
                notes = RE.md['notes'],
                ):
    return {'sample_name': sample_name,
            'sample_desc': sample_desc,
            'sample_id': sample_id,
            'sample_set': sample_set,
            'sample_date': sample_date,
            'project_name': project_name,
            'project_desc': project_desc,
            'samp_user_id': samp_user_id,
            'composition': composition,
            'density': density,
            'components': components,
            'thickness': thickness,
            'sample_state': sample_state,
            'notes': notes}


def user_dict(user_id = RE.md['user_id'],
                proposal_id = RE.md['proposal_id'],
                institution = RE.md['institution'],
                user_name = RE.md['user_name'],
                user_start_date = RE.md['user_start_date'],
                project_name = RE.md['project_name'],
                project_desc = RE.md['project_desc'],
                ):
    return {'user_id': user_id,
            'proposal_id': proposal_id,
            'institution': institution,
            'user_name': user_name,
            'user_start_date': user_start_date,
            'project_name': project_name,
            'project_desc': project_desc}


def load_sample_dict_to_md(sam_dict):
    RE.md['sample_name'] = sam_dict['sample_name']
    RE.md['sample_desc'] = sam_dict['sample_desc']
    RE.md['sample_id'] = sam_dict['sample_id']
    RE.md['sample_set'] = sam_dict['sample_set']
    RE.md['sample_date'] = sam_dict['sample_date']
    RE.md['project_name'] = sam_dict['project_name']
    RE.md['project_desc'] = sam_dict['project_desc']
    RE.md['samp_user_id'] = sam_dict['samp_user_id']
    RE.md['composition'] = sam_dict['composition']
    RE.md['density'] = sam_dict['density']
    RE.md['components'] = sam_dict['components']
    RE.md['thickness'] = sam_dict['thickness']
    RE.md['sample_state'] = sam_dict['sample_state']
    RE.md['notes'] = sam_dict['notes']


def load_user_dict_to_md(user_dict):
    RE.md['user_id'] = user_dict['user_id']
    RE.md['proposal_id'] = user_dict['proposal_id']
    RE.md['institution'] = user_dict['institution']
    RE.md['user_name'] = user_dict['user_name']
    RE.md['project_name'] = user_dict['project_name']
    RE.md['project_desc'] = user_dict['project_desc']


def newsample():
    print("This information will tag future data until this changes, please be as thorough as possible\n"
          "current values in parentheses, leave blank for no change")
    sample_name = input('Your sample name  - be concise ({}): '.format(RE.md['sample_name']))
    if sample_name is not '':
        RE.md['sample_name'] = sample_name

    sample_desc = input('Describe your sample - be thorough ({}): '.format(RE.md['sample_desc']))
    if sample_desc is not '':
        RE.md['sample_desc'] = sample_desc

    sample_id = input('Your sample id - if you have one ({}): '.format(RE.md['sample_id']))
    if sample_id is not '':
        RE.md['sample_id'] = sample_id

    sample_set = input('What set does this sample belong to ({}): '.format(RE.md['sample_set']))
    if sample_set is not '':
        RE.md['sample_set'] = sample_set

    sample_date = input('Sample creation date ({}): '.format(RE.md['sample_date']))
    if sample_date is not '':
        RE.md['sample_date'] = sample_date

    project_name = input('Is there an associated project name ({}): '.format(RE.md['project_name']))
    if project_name is not '':
        RE.md['project_name'] = project_name

    project_desc = input('Describe the project ({}): '.format(RE.md['project_desc']))
    if project_desc is not '':
        RE.md['project_desc'] = project_desc

    samp_user_id = input('Associated User ID ({}): '.format(RE.md['samp_user_id']))
    if samp_user_id is not '':
        RE.md['samp_user_id'] = samp_user_id

    composition = input('Sample composition or chemical formula ({}): '.format(RE.md['composition']))
    if composition is not '':
        RE.md['composition'] = composition

    density = input('Sample density ({}): '.format(RE.md['density']))
    if density is not '':
        RE.md['density'] = density

    components = input('Sample components ({}): '.format(RE.md['components']))
    if components is not '':
        RE.md['components'] = components

    thickness = input('Sample thickness ({}): '.format(RE.md['thickness']))
    if thickness is not '':
        RE.md['thickness'] = thickness

    sample_state = input('Sample state "Broken/Fresh" ({}): '.format(RE.md['sample_state']))
    if sample_state is not '':
        RE.md['sample_state'] = sample_state

    notes = input('Sample notes ({}): '.format(RE.md['notes']))
    if notes is not '':
        RE.md['notes'] = notes
    sample()
    return sample_dict()


def snapsw(seconds,samplename='',sampleid='', num_images=1,dark=0):

    '''
    this procedure is old and should not be used, suitcasing is fixed, and does this better
    :param seconds:
    :param samplename:
    :param sampleid:
    :param num_images:
    :param dark:
    :return:
    '''
    # TODO: do it more generally
    # yield from bps.mv(sw_det.setexp, seconds)
    yield from bps.mv(sw_det.waxs.cam.acquire_time, seconds)
    yield from bps.mv(sw_det.saxs.cam.acquire_time, seconds)
    yield from bps.mv(sw_det.waxs.cam.shutter_close_delay,200)
    yield from bps.mv(sw_det.saxs.cam.shutter_close_delay,200)
    yield from bps.mv(sw_det.waxs.cam.shutter_open_delay,200)
    yield from bps.mv(sw_det.saxs.cam.shutter_open_delay,200)
    if(dark):
        yield from bps.mv(sw_det.saxs.cam.shutter_mode, 0)
        if samplename is "":
            samplename = "dark"
    else:
        yield from bps.mv(sw_det.saxs.cam.shutter_mode, 2)
        if samplename is "":
            samplename = "snap"
    md=RE.md
    md['sample'] = samplename
    md['sampleid'] = sampleid
    md['exptime'] = seconds
    uid = (yield from bp.count([sw_det], num=num_images, md=md))
    hdr = db[uid]
    quick_view(hdr)
    dt = datetime.fromtimestamp(hdr.start['time'])
    formatted_date = dt.strftime('%Y-%m-%d')
    energy = hdr.table(stream_name='baseline')['Beamline Energy_energy'][1]
    tiff_series.export(hdr.documents(fill=True),
        file_prefix=('{start[institution]}/'
                    '{start[user]}/'
                    '{start[project]}/'
                    f'{formatted_date}/'
                    '{start[scan_id]}-'
                    '{start[sample]}-'
                    f'{energy:.2f}eV-'),
        directory='Z:/images/users/')
    csv.export(hdr.documents(stream_name='baseline'),
        file_prefix=('{institution}/'
                     '{user}/'
                     '{project}/'
                     f'{formatted_date}/'
                     '{scan_id}-'
                     '{sample}-'
                     f'{energy:.2f}eV-'),
        directory='Z:/images/users/')
    csv.export(hdr.documents(stream_name='Izero Mesh Drain Current_monitor'),
        file_prefix=('{institution}/'
                     '{user}/'
                     '{project}/'
                     f'{formatted_date}/'
                     '{scan_id}-'
                     '{sample}-'
                     f'{energy:.2f}eV-'),
        directory='Z:/images/users/')

def enscansw(seconds, enstart, enstop, steps,samplename='enscan',sampleid=''):
    '''
    This is old and should not be used.  Suitcasing has made the normal scans work well
    :param seconds:
    :param enstart:
    :param enstop:
    :param steps:
    :param samplename:
    :param sampleid:
    :return:
    '''
    # TODO: do it more generally
    # yield from bps.mv(sw_det.setexp, seconds)
    yield from bps.mv(sw_det.waxs.cam.acquire_time, seconds)
    yield from bps.mv(sw_det.saxs.cam.acquire_time, seconds)
    md = RE.md
    md['sample'] = samplename
    md['sampleid'] = sampleid
    first_scan_id = None
    dt = datetime.now()
    formatted_date = dt.strftime('%Y-%m-%d')
    for i, pos in enumerate(np.linspace(enstart, enstop, steps)):
        yield from bps.mv(en, pos)
        uid = (yield from bp.count([sw_det], md=md))
        hdr = db[uid]
        quick_view(hdr)
        if i == 0:
            first_scan_id = hdr.start['scan_id']
            dt = datetime.fromtimestamp(hdr.start['time'])
            formatted_date = dt.strftime('%Y-%m-%d')
        tiff_series.export(hdr.documents(fill=True),
            file_prefix=('{start[institution]}/'
                         '{start[user]}/'
                         '{start[project]}/'
                         f'{formatted_date}/'
                         f'{first_scan_id}-'
                         '-{start[scan_id]}-'
                         '-{start[sample]}-'
                         f'{pos:.2f}eV-'),
            directory='Z:/images/users/')
        csv.export(hdr.documents(stream_name='baseline'),
            file_prefix=('{institution}/'
                         '{user}/'
                         '{project}/'
                         f'{formatted_date}/'
                         f'{first_scan_id}-'
                         '{scan_id}-'
                         '{sample}-'
                         f'{pos:.2f}eV-'),
            directory='Z:/images/users/')
        csv.export(hdr.documents(stream_name='Izero Mesh Drain Current_monitor'),
            file_prefix=('{institution}/'
                         '{user}/'
                         '{project}/'
                         f'{formatted_date}/'
                         f'{first_scan_id}-'
                         '{scan_id}-'
                         '{sample}-'
                         f'{pos:.2f}eV-'),
            directory='Z:/images/users/')

    # uid = (yield from bp.scan([sw_det], en, enstart, enstop,steps, md=md))
    # hdr = db[uid]
    # dt = datetime.datetime.fromtimestamp(hdr.start['time'])
    # formatted_date = dt.strftime('%Y-%m-%d')
    # tiff_series.export(hdr.documents(fill=True),
    #     file_prefix=('{start[institution]}/'
    #                 '{start[user]}/'
    #                 '{start[project]}/'
    #                 f'{formatted_date}/'
    #                 '{start[scan_id]}-{start[sample]}-{event[data][en_energy]:.2f}eV-'), # not working, need energy in each filename
    #     directory='Z:/images/users/')
def motscansw(seconds,motor, start, stop, steps,samplename='motscan',sampleid=''):
    # TODO: do it more generally
    # yield from bps.mv(sw_det.setexp, seconds)
    yield from bps.mv(sw_det.waxs.cam.acquire_time, seconds)
    yield from bps.mv(sw_det.saxs.cam.acquire_time, seconds)
    md = RE.md
    md['sample'] = samplename
    md['sampleid'] = sampleid
    first_scan_id = None
    dt = datetime.now()
    formatted_date = dt.strftime('%Y-%m-%d')
    for i, pos in enumerate(np.linspace(start, stop, steps)):
        yield from bps.mv(motor, pos)
        uid = (yield from bp.count([sw_det], md=md))
        hdr = db[uid]
        quick_view(hdr)
        if i == 0:
            first_scan_id = hdr.start['scan_id']
            dt = datetime.fromtimestamp(hdr.start['time'])
            formatted_date = dt.strftime('%Y-%m-%d')
        tiff_series.export(hdr.documents(fill=True),
            file_prefix=('{start[institution]}/'
                         '{start[user]}/'
                         '{start[project]}/'
                         f'{formatted_date}/'
                         f'{first_scan_id}-'
                         '{start[scan_id]}'
                         '-{start[sample]}-'
                         f'{pos:.2f}-'),
            directory='Z:/images/users/')
        csv.export(hdr.documents(stream_name='baseline'),
            file_prefix=('{institution}/'
                         '{user}/'
                         '{project}/'
                         f'{formatted_date}/'
                         f'{first_scan_id}-'
                         '{scan_id}-{sample}-'
                         f'{pos:.2f}-'),
            directory='Z:/images/users/')
        csv.export(hdr.documents(stream_name='Izero Mesh Drain Current_monitor'),
            file_prefix=('{institution}/'
                         '{user}/'
                         '{project}/'
                         f'{formatted_date}/'
                         f'{first_scan_id}-'
                         '{scan_id}-{sample}-'
                         f'{pos:.2f}-'),
            directory='Z:/images/users/')
def myplan(dets, motor, start, stop, num):
    yield from bp.scan(dets, motor, start, stop, num)



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
        yield from tune_max([IzeroDiode],"Izero Diode Current",epu_gap,
                                    min(99500,max(20000,startinggap-500*widfract)),
                                    min(100000,max(21500,startinggap+1000*widfract)),
                                    10*widfract,7,3,True)

        gaps.append(bec.peaks.max["Izero Diode Current"][0])
        heights.append(bec.peaks.max["Izero Diode Current"][1])
        ensout.append(mono_en.position)
        startinggap = bec.peaks.max["Izero Diode Current"][0]
        #data = np.column_stack((ensout, gaps))
        data = {'Energies': ensout, 'EPUGaps': gaps, 'PeakCurrent': heights}
        dataframe = pd.DataFrame(data=data)
        dataframe.to_csv('EPUdata' + name + '.csv')
        count+=1
        if count > 50:
            count=0
            plt.close()
    #print(ens,gaps)


def do_some_eputables():
    #yield from buildeputable(150, 1500, 10, 1, 21000, 'H1v1p1')
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


@register_line_magic
def snap(line):
    RE(bp.count([sw_det,en,IzeroMesh], num=1))

del snap