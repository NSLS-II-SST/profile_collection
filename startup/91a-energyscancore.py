import bluesky.plans as bp
import bluesky.plan_stubs as bps
from bluesky.plan_stubs import checkpoint, abs_set, sleep, trigger, read, wait, create, save
from bluesky.preprocessors import rewindable_wrapper
from bluesky.utils import short_uid, separate_devices, all_safe_rewind
from collections import defaultdict
from bluesky import preprocessors as bpp


run_report(__file__)


SLEEP_FOR_SHUTTER = 1


def one_trigger_nd_step(detectors, step, pos_cache):
    """
    Inner loop of an N-dimensional step scan

    This is the default function for ``per_step`` param in ND plans.

    Parameters
    ----------
    detectors : iterable
        devices to read
    step : dict
        mapping motors to positions in this step
    pos_cache : dict
        mapping motors to their last-set positions
    """

    def move():
        yield from checkpoint()
        grp = short_uid('set')
        for motor, pos in step.items():
            if pos == pos_cache[motor]:
                # This step does not move this motor.
                continue
            yield from abs_set(motor, pos, group=grp)
            pos_cache[motor] = pos
        yield from wait(group=grp)

    motors = step.keys()
    yield from move()
    detectors = separate_devices(detectors)  # remove redundant entries
    rewindable = all_safe_rewind(detectors)  # if devices can be re-triggered
    detector_with_shutter, *other_detectors = detectors
    grp = short_uid('trigger')

    def inner_trigger_and_read():
        """
        This was copied with local changes from the body of
        bluesky.plan_stubs.trigger_and_read.
        """
        no_wait = True
        for obj in other_detectors:
            if hasattr(obj, 'trigger'):
                no_wait = False
                yield from trigger(obj, group=grp)
        # Skip 'wait' if none of the devices implemented a trigger method.
        if not no_wait:
            yield from wait(group=grp)
        yield from create('primary')
        ret = {}  # collect and return readings to give plan access to them
        for obj in detectors:
            reading = (yield from read(obj))
            if reading is not None:
                ret.update(reading)
        yield from save()
        return ret

    yield from trigger(detector_with_shutter, group=grp)
    yield from sleep(SLEEP_FOR_SHUTTER)
    return (yield from rewindable_wrapper(inner_trigger_and_read(),
                                          rewindable))


# @dark_frames_enable
def en_scan_core(signals,dets, energy, energies,times,enscan_type=None,m3_pitch=7.94,diode_range=6,
                 pol=100,grating='no change'):
    saxs_det.cam.acquire_time.kind = 'hinted'
    # sw_det.waxs.cam.acquire_time.kind = 'normal'
    yield from bps.abs_set(mir3.Pitch,m3_pitch,wait=True)
    yield from bps.mv(DiodeRange,diode_range)

    if grating=='1200':
        print('Moving grating to 1200 l/mm...')
        if abs(grating.user_offset.get()-7.308) > .1:
            print('current grating offset is too far from known values, please update the procedure, grating will not move')
        elif abs(mirror2.user_offset.get()-8.1388) > .1:
            print('current Mirror 2 offset is too far from known values, please update the procedure, grating will not move')
        else:
            yield from grating_to_1200()
        print('done')
    elif grating=='250':
        print('Moving grating to 250 l/mm...')
        if abs(grating.user_offset.get()-7.308) > .1:
            print('current grating offset is too far from known values, please update the procedure, grating will not move')
        elif abs(mirror2.user_offset.get()-8.1388) > .1:
            print('current Mirror 2 offset is too far from known values, please update the procedure, grating will not move')
        else:
            yield from grating_to_250()
        print('done')

    yield from set_polarization(pol)

    # Hack in darkframes manually
    darktimes = np.unique(times)
    darkenergies = darktimes.copy()
    darkenergies[:] = energies[0]

    shutters = times.copy()
    darkshutters = darktimes.copy()
    shutters[:] = 1
    darkshutters[:] = 0

    times = np.concatenate((darktimes,times))
    energies = np.concatenate((darkenergies,energies))
    shutters = np.concatenate((darkshutters,shutters))



    sigcycler = cycler(Shutter_enable2, shutters)
    sigcycler += cycler(energy, energies)
  #  yield from bps.mv(saxs_det.cam.acquire_time,times[0])
    sigcycler += cycler(saxs_det.cam.acquire_time, times.copy())
    sigcycler += cycler(Shutter_open_time, times.copy())

    #sigcycler += cycler(sw_det.waxs.cam.acquire_time, times.copy()) #add extra exposure time for WAXS

   # yield from bps.abs_set(en, energies[0], timeout=180, wait=True)
   # for signal in signals:
   #     signal.kind = 'normal'
   # print(det
    yield from bp.scan_nd(dets + signals,sigcycler, md={'plan_name':enscan_type})

def NEXAFS_scan_core(signals,dets, energy, energies,enscan_type=None,
                     openshutter = False,open_each_step=False,m3_pitch=7.94,diode_range=6,pol=100,
                     exp_time=1,grating='no change',motorname='None',offset=0):



    yield from bps.abs_set(mir3.Pitch,m3_pitch,wait=True)
    yield from bps.mv(DiodeRange,diode_range)
    # if pol is 1:
    #     epu_mode.put(0)
    # else:
    #     epu_mode.put(2)
    # yield from bps.sleep(1)
    # yield from bps.mv(en.polarization,pol)
    set_exposure(exp_time)
    if grating=='1200':
        print('Moving grating to 1200 l/mm...')
        if abs(mono_en.grating.user_offset.get()-7.308) > .1:
            print('current grating offset is too far from known values, please update the procedure, grating will not move')
        elif abs(mono_en.mirror2.user_offset.get()-8.1388) > .1:
            print('current Mirror 2 offset is too far from known values, please update the procedure, grating will not move')
        else:
            yield from grating_to_1200()
        print('done')
    elif grating=='250':
        print('Moving grating to 250 l/mm...')
        if abs(mono_en.grating.user_offset.get()-7.308) > .1:
            print('current grating offset is too far from known values, please update the procedure, grating will not move')
        elif abs(mono_en.mirror2.user_offset.get()-8.1388) > .1:
            print('current Mirror 2 offset is too far from known values, please update the procedure, grating will not move')
        else:
            yield from grating_to_250()
        print('done')
    if motorname is not 'None':
        yield from bps.rel_set(eval(motorname),offset,wait=True)
    print('setting pol')
    yield from set_polarization(pol)
    en.read;

    sigcycler = cycler(energy, energies)


    yield from bps.mv(en, energies[0])
    for signal in signals:
        signal.kind = 'normal'
    if openshutter and not open_each_step:
        yield from bps.mv(Shutter_enable, 0)
        yield from bps.mv(Shutter_control, 1)
        yield from bp.scan_nd(dets + signals + [en.energy],
                              sigcycler,
                              md={'plan_name':enscan_type})
        yield from bps.mv(Shutter_control, 0)
    elif open_each_step:
        yield from bps.mv(Shutter_enable, 1)
        yield from bp.scan_nd(dets + signals + [en.energy],
                              sigcycler,
                              md={'plan_name':enscan_type},
                              per_step=one_shuttered_step)
    else:
        yield from bp.scan_nd(dets + signals + [en.energy],
                              sigcycler,
                              md={'plan_name':enscan_type})




## HACK HACK

def rd(obj, *, default_value=0):
    """Reads a single-value non-triggered object
    This is a helper plan to get the scalar value out of a Device
    (such as an EpicsMotor or a single EpicsSignal).
    For devices that have more than one read key the following rules are used:
    - if exactly 1 field is hinted that value is used
    - if no fields are hinted and there is exactly 1 value in the
      reading that value is used
    - if more than one field is hinted an Exception is raised
    - if no fields are hinted and there is more than one key in the reading an
      Exception is raised
    The devices is not triggered and this plan does not create any Events
    Parameters
    ----------
    obj : Device
        The device to be read
    default_value : Any
        The value to return when not running in a "live" RunEngine.
        This come ups when ::
           ret = yield Msg('read', obj)
           assert ret is None
        the plan is passed to `list` or some other iterator that
        repeatedly sends `None` into the plan to advance the
        generator.
    Returns
    -------
    val : Any or None
        The "single" value of the device
    """
    hints = getattr(obj, 'hints', {}).get("fields", [])
    if len(hints) > 1:
        msg = (
            f"Your object {obj} ({obj.name}.{getattr(obj, 'dotted_name', '')}) "
            f"has {len(hints)} items hinted ({hints}).  We do not know how to "
            "pick out a single value.  Please adjust the hinting by setting the "
            "kind of the components of this device or by rd ing one of it's components"
        )
        raise ValueError(msg)
    elif len(hints) == 0:
        hint = None
        if hasattr(obj, "read_attrs"):
            if len(obj.read_attrs) != 1:
                msg = (
                    f"Your object {obj} ({obj.name}.{getattr(obj, 'dotted_name', '')}) "
                    f"and has {len(obj.read_attrs)} read attrs.  We do not know how to "
                    "pick out a single value.  Please adjust the hinting/read_attrs by "
                    "setting the kind of the components of this device or by rd ing one "
                    "of its components"
                )

                raise ValueError(msg)
    # len(hints) == 1
    else:
        (hint,) = hints

    ret = yield from read(obj)

    # list-ify mode
    if ret is None:
        return default_value

    if hint is not None:
        return ret[hint]["value"]

    # handle the no hint 1 field case
    try:
        (data,) = ret.values()
    except ValueError as er:
        msg = (
            f"Your object {obj} ({obj.name}.{getattr(obj, 'dotted_name', '')}) "
            f"and has {len(ret)} read values.  We do not know how to pick out a "
            "single value.  Please adjust the hinting/read_attrs by setting the "
            "kind of the components of this device or by rd ing one of its components"
        )

        raise ValueError(msg) from er
    else:
        return data["value"]






from cycler import cycler
from bluesky.utils import (Msg, short_uid as _short_uid)
import bluesky.utils as utils
from bluesky.plan_stubs import trigger_and_read
# monkey batch bluesky.plans_stubs to fix bug.
bps.rd = rd

def one_shuttered_step(detectors, step, pos_cache):
    """
    Inner loop of an N-dimensional step scan

    This is the default function for ``per_step`` param`` in ND plans.

    Parameters
    ----------
    detectors : iterable
        devices to read
    step : dict
        mapping motors to positions in this step
    pos_cache : dict
        mapping motors to their last-set positions
    """

    yield Msg('checkpoint')
    grp = _short_uid('set') #stolen from move per_step to break out the wait
    for motor, pos in step.items():
        if pos == pos_cache[motor]:
            # This step does not move this motor.
            continue
        yield Msg('set', motor, pos, group=grp)
        pos_cache[motor] = pos

    motors = step.keys() # start the acquisition now
    yield from bps.mv(Shutter_trigger, 1)
    yield from trigger_and_read(list(detectors) + list(motors))
    t = yield from bps.rd(Shutter_open_time)
    yield from bps.sleep((t / 1000)  + 0.5)
    yield Msg('wait', None, group=grp) # now wait for motors, before moving on to next step


def scan_eliot(detectors, cycler, exp_time,*, md=None):
    """
    Scan over an arbitrary N-dimensional trajectory.
    1.) begin movement as soon as photon part of detection ends
            wait for shutter to close, not for detector readout
    2.) do not wait for motor movement to finish before beginnning detection step

    NOTE this may result in small smearing of data by one point backwards,
        but this is usually worth it for the speed up

    Parameters
    ----------
    detectors : list
    cycler : Cycler
        list of dictionaries mapping motors to positions
    exp_time : EpicsSignal
        signal to read to get the exposure time (in ms)
    **shutter_sig : Signal to wait for it to go to 0 before ending step
        this signals the end of photons, not the end of the detector trigger
        it is safe to move to the next step once this signal is 0
    ***per_step : not used here, all is hard coded in
    md : dict, optional
        metadata

    """
    _md = {'detectors': [det.name for det in detectors],
           'motors': [motor.name for motor in cycler.keys],
           'num_points': len(cycler),
           'num_intervals': len(cycler) - 1,
           'plan_args': {'detectors': list(map(repr, detectors)),
                         'cycler': repr(cycler)},
           'plan_name': 'scan_eliot',
           'hints': {},
           }
    _md.update(md or {})
    try:
        dimensions = [(motor.hints['fields'], 'primary')
                      for motor in cycler.keys]
    except (AttributeError, KeyError):
        # Not all motors provide a 'fields' hint, so we have to skip it.
        pass
    else:
        _md['hints'].setdefault('dimensions', dimensions)

    pos_cache = defaultdict(lambda: None)  # where last position is stashed
    cycler = utils.merge_cycler(cycler)
    motors = list(cycler.keys)

    @bpp.stage_decorator(list(detectors) + motors)
    @bpp.run_decorator(md=_md)
    def inner_scan_eliot():
        # this makes the reading step easier (usually done by trigger_and_read)
        devices = separate_devices(list(detectors) + motors)  # remove redundant entries

        # go to first motor position
        yield Msg('checkpoint')
        motorgrp = _short_uid('set')  # stolen from move per_step to break out the wait
        for motor, pos in list(cycler)[0].items():
            if pos == pos_cache[motor]:
                # This step does not move this motor.
                continue
            yield Msg('set', motor, pos, group=motorgrp)
            pos_cache[motor] = pos
        # wait for motors this time
        yield Msg('wait', None, group=motorgrp)  # now wait for motors, before moving on to next step

        # trigger detectors
        detgrp = _short_uid('trigger')
        no_wait = True
        for obj in devices:
            if hasattr(obj, 'trigger'):
                no_wait = False
                yield from trigger(obj, group=detgrp)

        # step through the list
        for step in list(cycler): # this is repeating the first step
            # wait for motor movement to end
            yield Msg('wait', None, group=motorgrp)  # now wait for motors, before moving on to next step
            # do we need to wait at all? - I guess the previous set might be active?

            # move to next position - detectors might still be triggering at this point
            yield Msg('checkpoint')
            motorgrp = _short_uid('set')  # stolen from move per_step to break out the wait
            for motor, pos in step.items():
                if pos == pos_cache[motor]:
                    # This step does not move this motor.
                    continue
                yield Msg('set', motor, pos, group=motorgrp)
                pos_cache[motor] = pos

            # wait for detector trigger from last step to finish
            if not no_wait:
                yield from wait(group=detgrp)

            # read detectors
            yield from create('primary')
            for obj in devices:
                yield from read(obj)
            yield from save()

            #trigger next detector step
            detgrp = _short_uid('trigger')
            no_wait = True
            for obj in list(detectors): # changing this from devices, I don't want to trigger motors while they
                        # may still be in a set() - I will just read them without a trigger
                if hasattr(obj, 'trigger'):
                    no_wait = False
                    yield from trigger(obj, group=detgrp)

            # wait enough time for the shutter to close

            t = yield from bps.rd(exp_time)
            yield from bps.sleep(t / 1000)

            # how do I wait for an EpicsSignal instead?
            # for now, I will just wait for the exposure time

            # NOTE: the darkframes preprocessor will sometimes delay this significantly, I would like to
            # find a way to notice that and wait more time accordingly


        #wait for detectors to finish the final time
        if not no_wait:
            yield from wait(group=detgrp)

        #read detectors the final time
        yield from create('primary')
        for obj in devices:
            yield from read(obj)
        yield from save()

        # wait for the final motor movement
        yield Msg('wait', None, group=motorgrp)

    return (yield from inner_scan_eliot())


