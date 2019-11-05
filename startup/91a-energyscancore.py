run_report(__file__)

import bluesky.plans as bp
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
def en_scan_core(I400sigs, dets, energy, energies,times,enscan_type=None):
    sw_det.saxs.cam.acquire_time.kind = 'hinted'
    sw_det.waxs.cam.acquire_time.kind = 'hinted'

    sigcycler = cycler(energy, energies)
    for i400channel in I400sigs:
        i400channel.parent.exposure_time.kind = 'hinted'
        try:
            sigcycler += cycler(i400channel.parent.exposure_time,times.copy())
        except ValueError:
            print('same i400 detected')
            i400channel.kind = 'hinted'
    sigcycler += cycler(sw_det.saxs.cam.acquire_time, times.copy())
    sigcycler += cycler(sw_det.waxs.cam.acquire_time, times.copy()) #add extra exposure time for WAXS
    #sigcycler += cycler(sw_det.saxs.cam.sync, shuttervalues.astype(int))

    Beamstop_SAXS.kind = "hinted"
    #Beamstop_WAXS.kind = "hinted"
    IzeroMesh.kind = "hinted"
    #SlitTop_I.kind = "hinted"
    #SlitBottom_I.kind = "hinted"
    #SlitOut_I.kind = "hinted"
    # light_was_on = False
    # if samplelight.value is 1:
    #     samplelight.off()
    #     sw_det.shutter_off()
    #     light_was_on = True
    #     boxed_text('Warning', 'light was on, taking a quick snapshot to clear CCDs', 'yellow', shrink=True)
    #     yield from quicksnap()
    print(sigcycler)

    yield from bp.scan_nd(dets + I400sigs+[en.energy],
                          sigcycler,
                          md={'plan_name':enscan_type},
                          per_step=one_trigger_nd_step)

    # if light_was_on:
    #     samplelight.on()    # leaving light off now - this just slows everything down if there are multiple scans
