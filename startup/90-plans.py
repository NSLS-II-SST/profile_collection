print(f'Loading {__file__}...')

import bluesky.plans as bp
import bluesky.plan_stubs as bps
import bluesky.preprocessors as bpp


def myplan(dets, motor, start, stop, num):
    yield from bp.scan(dets, motor, start, stop, num)