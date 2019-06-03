print(f'Loading {__file__}...')

import numpy as np
import bluesky.plans as bp
import bluesky.plan_stubs as bps
from cycler import cycler


def SWCarbon_acq(multiple,mesh,det,energy):
    energies = np.arange(270,282,.5)
    energies = np.append(energies,np.arange(282,286,.1))
    energies = np.append(energies,np.arange(286,292,.2))
    energies = np.append(energies,np.arange(292,305,1))
    energies = np.append(energies,np.arange(305,320,1))
    energies = np.append(energies,np.arange(320,350,5))
    times = energies.copy()
    times[energies<282] = 1
    times[(energies < 286) & (energies >= 282)] = 5
    times[energies >= 286] = 2
    times *= multiple
    times2 = times.copy()
    times3 = times.copy()

    yield from bp.scan_nd(
        [mesh,det],
        cycler(sw_det.saxs.cam.acquire_time, times) +
        cycler(sw_det.waxs.cam.acquire_time, times3) +
        cycler(mesh.parent.exposure_time, times3) +
        cycler(energy, energies))
