run_report(__file__)

import numpy as np
import bluesky.plans as bp
import bluesky.plan_stubs as bps
from cycler import cycler


def full_carbon_scan(multiple=1,sigs=[IzeroMesh],dets=[sw_det],energy=en):
    '''
    Full Carbon Scan runs an RSoXS sample set through the carbon edge, with particular emphasis in he pre edge region
    this results in 128 exposures


    :param multiple: adjustment for exposure times
    :param mesh: which Izero channel to use
    :param det: which detector to use
    :param energy: what energy motor to scan
    :return: perform scan

    normal scan takes ~ 18 minutes to complete
    '''
    sample()
    #beamline_status()
    #if len(read_input("Starting a Carbon energy scan hit any key in the next 3 seconds to abort", "abort", "", 3)) > 0:
    #    return

    # create a list of energies
    energies = np.arange(270,282,.5)
    energies = np.append(energies,np.arange(282,286,.1))
    energies = np.append(energies,np.arange(286,292,.2))
    energies = np.append(energies,np.arange(292,305,1))
    energies = np.append(energies,np.arange(305,320,1))
    energies = np.append(energies,np.arange(320,350,5))
    energies = np.insert(energies,0,270)
    energies = np.insert(energies,0,270)
    energies = np.insert(energies,0,270)
    times = energies.copy()

    # Define exposures times for different energy ranges
    times[energies<282] = 1
    times[(energies < 286) & (energies >= 282)] = 5
    times[energies >= 286] = 2
    times[0] = 1 #darks
    times[1] = 5
    times[2] = 2
    times *= multiple

    shuttervalue = energies.copy()
    shuttervalue[:3] = 0  # first 3 values are 0 (dark)
    shuttervalue[3:] = 2  # the rest of the values are shutter enabled (2)
    # use these energies and exposure times to scan energy and record detectors and signals
    yield from en_scan_core(sigs, dets, energy, energies, shuttervalue, times)


def full_oxygen_scan_nd(multiple=1,sigs=[IzeroMesh],dets=[sw_det],energy=en):
    '''
    Full Carbon Scan runs an RSoXS sample set through the carbon edge, with particular emphasis in he pre edge region
    this results in 110 exposures


    :param multiple: adjustment for exposure times
    :param mesh: which Izero channel to use
    :param det: which detector to use
    :param energy: what energy motor to scan
    :return: perform scan

    normal scan takes ~ 16 minutes to complete
    '''
    sample()
    #beamline_status()
    #if len(read_input("Starting a Carbon energy scan hit any key in the next 3 seconds to abort", "abort", "", 3)) > 0:
    #    return

    # create a list of energies
    energies = np.arange(510,525,1)
    energies = np.append(energies,np.arange(525,540,.2))
    energies = np.append(energies,np.arange(540,560,1))
    times = energies.copy()

    # Define exposures times for different energy ranges
    times[energies<282] = 1
    times[(energies < 286) & (energies >= 282)] = 5
    times[energies >= 286] = 2
    times *= multiple

    shuttervalue = energies.copy()
    shuttervalue[:] = 2  # the rest of the values are shutter enabled (2)
    # use these energies and exposure times to scan energy and record detectors and signals
    yield from en_scan_core(sigs, dets, energy, energies, shuttervalue, times)



def full_nitrogen_scan_nd(multiple=1,sigs=[IzeroMesh],dets=[sw_det],energy=en):
    '''
    Full Carbon Scan runs an RSoXS sample set through the carbon edge, with particular emphasis in he pre edge region
    this results in 95 exposures


    :param multiple: adjustment for exposure times
    :param mesh: which Izero channel to use
    :param det: which detector to use
    :param energy: what energy motor to scan
    :return: perform scan

    normal scan takes ~ 15 minutes to complete
    '''
    sample()
    #beamline_status()
    #if len(read_input("Starting a Carbon energy scan hit any key in the next 3 seconds to abort", "abort", "", 3)) > 0:
    #    return

    # create a list of energies
    energies = np.arange(385,397,1)
    energies = np.append(energies,np.arange(397,407,.2))
    energies = np.append(energies,np.arange(407,440,1))
    times = energies.copy()

    # Define exposures times for different energy ranges
    times[energies < 400] = 2
    # times[(energies < 286) & (energies >= 282)] = 5
    times[energies >= 400] = 2
    times *= multiple

    shuttervalue = energies.copy()
    shuttervalue[:] = 2  # the rest of the values are shutter enabled (2)
    # use these energies and exposure times to scan energy and record detectors and signals
    yield from en_scan_core(sigs, dets, energy, energies, shuttervalue, times)



def very_short_carbon_scan_nd(multiple=1,sigs=[IzeroMesh],dets=[sw_det],energy=en):
    '''
    Full Carbon Scan runs an RSoXS sample set through the carbon edge, with particular emphasis in he pre edge region
    this results in 40 exposures


    :param multiple: adjustment for exposure times
    :param mesh: which Izero channel to use
    :param det: which detector to use
    :param energy: what energy motor to scan
    :return: perform scan

    normal scan takes ~ 6 minutes to complete
    '''
    sample()
    #beamline_status()
    #if len(read_input("Starting a Carbon energy scan hit any key in the next 3 seconds to abort", "abort", "", 3)) > 0:
    #    return

    # create a list of energies
    energies = np.arange(270,282,2)
    energies = np.append(energies,np.arange(282,286,.5))
    energies = np.append(energies,np.arange(286,292,.5))
    energies = np.append(energies,np.arange(292,306,2))
    energies = np.append(energies,np.arange(306,320,4))
    energies = np.append(energies,np.arange(320,350,10))
    times = energies.copy()

    # Define exposures times for different energy ranges
    times[energies<282] = 1
    times[(energies < 286) & (energies >= 282)] = 5
    times[energies >= 286] = 2
    times *= multiple

    shuttervalue = energies.copy()
    shuttervalue[:] = 2 # the rest of the values are shutter enabled (2)
    # use these energies and exposure times to scan energy and record detectors and signals
    yield from en_scan_core(sigs, dets,energy,energies,shuttervalue,times)


def short_carbon_scan_nd(multiple=1,sigs=[IzeroMesh],dets=[sw_det],energy=en):
    '''
    Full Carbon Scan runs an RSoXS sample set through the carbon edge, with particular emphasis in he pre edge region
    this results in 61 exposures


    :param multiple: adjustment for exposure times
    :param mesh: which Izero channel to use
    :param det: which detector to use
    :param energy: what energy motor to scan
    :return: perform scan

    normal scan takes ~ 10 minutes to complete
    '''
    sample()
    #if len(read_input("Starting a Carbon energy scan hit any key in the next 3 seconds to abort", "abort", "", 3)) > 0:
    #    return

    # create a list of energies
    energies = np.arange(270,282,1)
    energies = np.append(energies,np.arange(282,286,.25))
    energies = np.append(energies,np.arange(286,292,.5))
    energies = np.append(energies,np.arange(292,306,1))
    energies = np.append(energies,np.arange(306,320,4))
    energies = np.append(energies,np.arange(320,350,10))
    times = energies.copy()

    # Define exposures times for different energy ranges
    times[energies<282] = 1
    times[(energies < 286) & (energies >= 282)] = 5
    times[energies >= 286] = 2
    times *= multiple

    shuttervalue = energies.copy()
    shuttervalue[:] = 2 # the rest of the values are shutter enabled (2)
    # use these energies and exposure times to scan energy and record detectors and signals
    yield from en_scan_core(sigs, dets,energy,energies,shuttervalue,times)


def full_carbon_scan_nd(multiple=1, sigs=[IzeroMesh], dets=[sw_det], energy=en, once_mot= None, once_rstep = 0):
    '''
    Full Carbon Scan runs an RSoXS sample set through the carbon edge, with particular emphasis in he pre edge region
    this results in 128 exposures


    :param multiple: adjustment for exposure times
    :param mesh: which Izero channel to use
    :param det: which detector to use
    :param energy: what energy motor to scan
    :return: perform scan

    normal scan takes ~ 18 minutes to complete
    '''
    sample()
    #if len(read_input("Starting a Carbon energy scan hit any key in the next 3 seconds to abort", "abort", "", 3)) > 0:
    #    return

    # create a list of energies
    energies = np.arange(270,282,.5)
    energies = np.append(energies,np.arange(282,286,.1))
    energies = np.append(energies,np.arange(286,292,.2))
    energies = np.append(energies,np.arange(292,305,1))
    energies = np.append(energies,np.arange(305,320,1))
    energies = np.append(energies,np.arange(320,350,5))
    times = energies.copy()

    # Define exposures times for different energy ranges
    times[energies<282] = 1
    times[(energies < 286) & (energies >= 282)] = 5
    times[energies >= 286] = 2
    times *= multiple

    shutter_values = energies.copy()
    shutter_values[:] = 2  # all the values are shutter enabled (2)
    # this is because darks are now taken in the preprocessor automatically as needed

    if isinstance(once_mot,EpicsMotor):
        yield from bps.mvr(once_mot,once_rstep)


    # print(times.size)
    # print(energies.size)
    # print(shutter_values.size)
    # print(sigs)
    # print(dets)
    # use these energies and exposure times to scan energy and record detectors and signals
    yield from en_scan_core(sigs, dets, energy, energies, shutter_values, times)


# @dark_frames_enable
def en_scan_core(I400sigs, dets, energy, energies, shuttervalues, times):
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
    sigcycler += cycler(sw_det.waxs.cam.acquire_time, times.copy())
    sigcycler += cycler(sw_det.saxs.cam.shutter_mode, shuttervalues.astype(int))

    # light_was_on = False
    # if samplelight.value is 1:
    #     samplelight.off()
    #     sw_det.shutter_off()
    #     light_was_on = True
    #     boxed_text('Warning', 'light was on, taking a quick snapshot to clear CCDs', 'yellow', shrink=True)
    #     yield from quicksnap()

    yield from bp.scan_nd(I400sigs+ dets+ [en,sw_det.saxs.cam.shutter_mode],sigcycler)

    # if light_was_on:
    #     samplelight.on()    # leaving light off now - this just slows everything down if there are multiple scans


def short_carbon_scan(multiple=1,sigs=[IzeroMesh],dets=[sw_det],energy=en):
    '''
    Short Carbon Scan runs an RSoXS sample set through the carbon edge, with particular emphasis in he pre edge region
    this results in 128 exposures


    :param multiple: adjustment for exposure times
    :param mesh: which Izero channel to use
    :param det: which detector to use
    :param energy: what energy motor to scan
    :return: perform scan

    normal scan takes ~ 12 minutes to complete
    '''
    beamline_status()
    if len(read_input("Starting a Carbon energy scan hit any key in the next 3 seconds to abort", "abort", "", 3)) > 0:
        return

    # create a list of energies
    energies = np.arange(270,282,1)
    energies = np.append(energies,np.arange(282,286,.25))
    energies = np.append(energies,np.arange(286,292,.5))
    energies = np.append(energies,np.arange(292,306,1))
    energies = np.append(energies,np.arange(306,320,4))
    energies = np.append(energies,np.arange(320,350,10))
    energies = np.insert(energies,0,270)
    energies = np.insert(energies,0,270)
    energies = np.insert(energies,0,270)
    times = energies.copy()

    # Define exposures times for different energy ranges
    times[energies<282] = 1
    times[(energies < 286) & (energies >= 282)] = 5
    times[energies >= 286] = 2
    times[0] = 1 #darks
    times[1] = 5
    times[2] = 2
    times *= multiple

    shuttervalue = energies.copy()
    shuttervalue[:3] = 0 # first 3 values are 0 (dark)
    shuttervalue[3:] = 2 # the rest of the values are shutter enabled (2)
    # use these energies and exposure times to scan energy and record detectors and signals
    yield from en_scan_core(sigs, dets,energy,energies,shuttervalue,times)


def full_ca_scan(multiple=1,sigs=[IzeroMesh],dets=[sw_det],energy=en):
    '''
    Full Carbon Scan runs an RSoXS sample set through the carbon edge, with particular emphasis in he pre edge region
    this results in 128 exposures


    :param multiple: adjustment for exposure times
    :param mesh: which Izero channel to use
    :param det: which detector to use
    :param energy: what energy motor to scan
    :return: perform scan

    normal scan takes ~ 12 minutes to complete
    '''
    beamline_status()
    if len(read_input("Starting a short Calcium energy scan hit any key in the next 3 seconds to abort", "abort", "", 3)) > 0:
        return

    # create a list of energies
    energies = np.arange(345,355,1)
    energies = np.insert(energies,0,345)
    energies = np.insert(energies,0,345)
    energies = np.insert(energies,0,345)
    times = energies.copy()

    # Define exposures times for different energy ranges
    times[energies<400] = 20

    times[0] = 20 #darks
    times[1] = 20
    times[2] = 20

    times *= multiple


    shuttervalue = energies.copy()
    shuttervalue[:3] = 0  # first 3 values are 0 (dark)
    shuttervalue[3:] = 2  # the rest of the values are shutter enabled (2)
    # use these energies and exposure times to scan energy and record detectors and signals
    yield from en_scan_core(sigs, dets, energy, energies, shuttervalue, times)


def very_short_carbon_scan(multiple=1,sigs=[IzeroMesh],dets=[sw_det],energy=en):
    '''
    Full Carbon Scan runs an RSoXS sample set through the carbon edge, with particular emphasis in he pre edge region
    this results in 128 exposures


    :param multiple: adjustment for exposure times
    :param mesh: which Izero channel to use
    :param det: which detector to use
    :param energy: what energy motor to scan
    :return: perform scan

    normal scan takes ~ 12 minutes to complete
    '''
    beamline_status()
    if len(read_input("Starting a Carbon energy scan hit any key in the next 3 seconds to abort", "abort", "", 3)) > 0:
        return

    # create a list of energies
    energies = np.arange(270,282,1)
    energies = np.append(energies,np.arange(282,286,.25))
    energies = np.append(energies,np.arange(286,292,.5))
    energies = np.append(energies,np.arange(292,306,1))
    energies = np.append(energies,np.arange(306,320,4))
    energies = np.append(energies,np.arange(320,350,10))
    energies = np.insert(energies,0,270)
    energies = np.insert(energies,0,270)
    energies = np.insert(energies,0,270)
    times = energies.copy()

    # Define exposures times for different energy ranges
    times[energies<282] = 1
    times[(energies < 286) & (energies >= 282)] = 5
    times[energies >= 286] = 2
    times[0] = 1 #darks
    times[1] = 5
    times[2] = 2
    times *= multiple

    shuttervalue = energies.copy()
    shuttervalue[:3] = 0 # first 3 values are 0 (dark)
    shuttervalue[3:] = 2 # the rest of the values are shutter enabled (2)
    # use these energies and exposure times to scan energy and record detectors and signals
    yield from en_scan_core(sigs, dets,energy,energies,shuttervalue,times)