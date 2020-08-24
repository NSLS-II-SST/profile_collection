run_report(__file__)

import bluesky.plans as bp
import bluesky.plan_stubs as bps
from cycler import cycler
from bluesky.plan_stubs import checkpoint, abs_set, sleep, trigger, read, wait, create, save
from bluesky.preprocessors import rewindable_wrapper
from bluesky.utils import short_uid, separate_devices, all_safe_rewind

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
def en_scan_core(signals,dets, energy, energies,times,enscan_type=None,m3_pitch=7.94,diode_range=6,pol=100):
    saxs_det.cam.acquire_time.kind = 'hinted'
    # sw_det.waxs.cam.acquire_time.kind = 'normal'
    yield from bps.abs_set(mir3.Pitch,m3_pitch,wait=True)
    yield from bps.mv(DiodeRange,diode_range)

    # if pol is 1:
    #     epu_mode.put(0)
    # else:
    #     epu_mode.put(2)
    # yield from bps.sleep(1)
    # yield from bps.mv(en.polarization,pol)
    yield from set_polarization(pol)

    sigcycler = cycler(energy, energies)
  #  yield from bps.mv(saxs_det.cam.acquire_time,times[0])
    sigcycler += cycler(saxs_det.cam.acquire_time, times.copy())
    #sigcycler += cycler(sw_det.waxs.cam.acquire_time, times.copy()) #add extra exposure time for WAXS

   # yield from bps.abs_set(en, energies[0], timeout=180, wait=True)
   # for signal in signals:
   #     signal.kind = 'normal'
   # print(dets)
    yield from bp.scan_nd(dets + signals,sigcycler, md={'plan_name':enscan_type})

def NEXAFS_scan_core(signals,dets, energy, energies,enscan_type=None,
                     openshutter = False,m3_pitch=7.94,diode_range=6,pol=100):

    sigcycler = cycler(energy, energies)

   # yield from bps.abs_set(mir3.Pitch,m3_pitch,wait=True)
    yield from bps.mv(DiodeRange,diode_range)
    # if pol is 1:
    #     epu_mode.put(0)
    # else:
    #     epu_mode.put(2)
    # yield from bps.sleep(1)
    # yield from bps.mv(en.polarization,pol)
    yield from set_polarization(pol)
    print('setting pol')




    yield from bps.mv(en, energies[0])
    for signal in signals:
        signal.kind = 'normal'
    if openshutter:
        yield from bps.mv(Shutter_enable, 0)
        yield from bps.mv(Shutter_control, 1)

    yield from bp.scan_nd(dets + signals + [en.energy],
                          sigcycler,
                          md={'plan_name':enscan_type})
    if openshutter:
        yield from bps.mv(Shutter_control, 0)