run_report(__file__)

import numpy as np
import bluesky.plans as bp
import bluesky.plan_stubs as bps


def full_oxygen_scan_nd(multiple=1,sigs=[],
                        dets=[sw_det],energy=en):
    '''
    Full Oxygen Scan runs an RSoXS sample set through the O edge, with particular emphasis in he pre edge region
    this results in 110 exposures


    :param multiple: adjustment for exposure times
    :param mesh: which Izero channel to use
    :param det: which detector to use
    :param energy: what energy motor to scan
    :return: perform scan

    normal scan takes ~ 16 minutes to complete
    '''
    sample()
    enscan_type = 'full_oxygen_scan_nd'
    #beamline_status()
    if len(read_input("Starting a Oxygen energy scan hit enter in the next 3 seconds to abort", "abort", "", 3)) > 0:
        return
    yield from bps.abs_set(mir3.Pitch, 7.89, wait=True)
    # create a list of energies
    energies = np.arange(510,525,1)
    energies = np.append(energies,np.arange(525,540,.2))
    energies = np.append(energies,np.arange(540,560,1))
    times = energies.copy()

    # Define exposures times for different energy ranges
    times[energies<282] = 2
    times[(energies < 286) & (energies >= 282)] = 5
    times[energies >= 286] = 2
    times *= multiple

    # use these energies and exposure times to scan energy and record detectors and signals
    yield from en_scan_core(sigs, dets, energy, energies, times,enscan_type=enscan_type)

def short_oxygen_scan_nd(multiple=1,sigs=[],
                        dets=[sw_det],energy=en):
    '''
    Short Oxygen Scan runs an RSoXS sample set through the O edge, with particular emphasis in he pre edge region

    :param multiple: adjustment for exposure times
    :param mesh: which Izero channel to use
    :param det: which detector to use
    :param energy: what energy motor to scan
    :return: perform scan

    normal scan takes ~ 16 minutes to complete
    '''
    sample()
    enscan_type = 'short_oxygen_scan_nd'
    #beamline_status()
    if len(read_input("Starting a Oxygen energy scan hit enter in the next 3 seconds to abort", "abort", "", 3)) > 0:
        return
    yield from bps.abs_set(mir3.Pitch,7.89,wait=True)
    # create a list of energies
    energies = np.arange(510,525,2)
    energies = np.append(energies,np.arange(525,540,0.5))
    energies = np.append(energies,np.arange(540,560,2))
    times = energies.copy()

    # Define exposures times for different energy ranges
    #times[energies<525] = 2
    #times[(energies < 540) & (energies >= 525)] = 5
    #times[energies >= 540] = 2
    times[:] = 2
    times *= multiple

    # use these energies and exposure times to scan energy and record detectors and signals
    yield from en_scan_core(sigs, dets, energy, energies, times,enscan_type=enscan_type)



def short_fluorine_scan_nd(multiple=1,sigs=[],
                        dets=[sw_det],energy=en):
    '''
    Short Fluorine Scan runs an RSoXS sample set through the F edge, with particular emphasis in he pre edge region


    :param multiple: adjustment for exposure times
    :param mesh: which Izero channel to use
    :param det: which detector to use
    :param energy: what energy motor to scan
    :return: perform scan

    normal scan takes ~ 16 minutes to complete
    '''
    sample()
    enscan_type = 'short_fluorine_scan_nd'
    #beamline_status()
    if len(read_input("Starting a fluorine energy scan hit enter in the next 3 seconds to abort", "abort", "", 3)) > 0:
        return
    # mir3.Pitch.put(7.89)
    # create a list of energies
    energies = np.arange(670,710,1)
    #energies = np.append(energies,np.arange(525,540,0.5))
    #energies = np.append(energies,np.arange(540,560,2))
    times = energies.copy()

    # Define exposures times for different energy ranges
    #times[energies<525] = 2
    #times[(energies < 540) & (energies >= 525)] = 5
    #times[energies >= 540] = 2
    times[:] = 2
    times *= multiple
    # use these energies and exposure times to scan energy and record detectors and signals

    yield from en_scan_core(sigs, dets, energy, energies, times,enscan_type=enscan_type)



def full_nitrogen_scan_nd(multiple=1,sigs=[],
                          dets=[sw_det],energy=en):
    '''
    Full Nitrogen Scan runs an RSoXS sample set through the N edge, with particular emphasis in he pre edge region
    this results in 95 exposures


    :param multiple: adjustment for exposure times
    :param mesh: which Izero channel to use
    :param det: which detector to use
    :param energy: what energy motor to scan
    :return: perform scan

    normal scan takes ~ 15 minutes to complete
    '''
    enscan_type = 'full_nitrogen_scan_nd'
    sample()
    #beamline_status()
    if len(read_input("Starting a Nitrogen energy scan hit enter in the next 3 seconds to abort", "abort", "", 3)) > 0:
        return
    yield from bps.abs_set(mir3.Pitch, 7.94, wait=True)
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

    # use these energies and exposure times to scan energy and record detectors and signals
    yield from en_scan_core(sigs, dets, energy, energies, times,enscan_type=enscan_type)


def short_nitrogen_scan_nd(multiple=1,sigs=[],
                          dets=[sw_det],energy=en):
    '''
    Short Nitrogen Scan runs an RSoXS sample set through the N edge, with particular emphasis in he pre edge region


    :param multiple: adjustment for exposure times
    :param mesh: which Izero channel to use
    :param det: which detector to use
    :param energy: what energy motor to scan
    :return: perform scan

    normal scan takes ~ 15 minutes to complete
    '''
    enscan_type='short_nitrogen_scan_nd'
    sample()
    #beamline_status()
    if len(read_input("Starting a Short Nitrogen energy scan "
                      "hit enter in the next 3 seconds to abort", "abort", "", 3)) > 0:
        return
    yield from bps.abs_set(mir3.Pitch, 7.94, wait=True)
    # create a list of energies
    energies = np.arange(385,397,1)
    energies = np.append(energies,np.arange(397,401,.2))
    energies = np.append(energies,np.arange(401,410,1))
    energies = np.append(energies,np.arange(410,430,2))
    times = energies.copy()

    # Define exposures times for different energy ranges
    times[energies < 400] = 2
    # times[(energies < 286) & (energies >= 282)] = 5
    times[energies >= 400] = 2
    times *= multiple

    # use these energies and exposure times to scan energy and record detectors and signals
    yield from en_scan_core(sigs, dets, energy, energies, times,enscan_type=enscan_type)


def very_short_carbon_scan_nd(multiple=1,sigs=[],
                              dets=[sw_det],energy=en):
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
    enscan_type = 'very_short_carbon_scan_nd'
    sample()
    #beamline_status()
    if len(read_input("Starting a very short Carbon energy scan hit "
                      "enter in the next 3 seconds to abort", "abort", "", 3)) > 0:
        return
    yield from bps.abs_set(mir3.Pitch, 7.94, wait=True)
    # create a list of energies
    energies = np.arange(270,282,2)
    energies = np.append(energies,np.arange(282,286,.5))
    energies = np.append(energies,np.arange(286,292,.5))
    energies = np.append(energies,np.arange(292,306,2))
    energies = np.append(energies,np.arange(306,320,4))
    energies = np.append(energies,np.arange(320,350,10))
    times = energies.copy()

    # Define exposures times for different energy ranges
    times[energies<282] = 2
    times[(energies < 286) & (energies >= 282)] = 5
    times[energies >= 286] = 2
    times *= multiple

    # use these energies and exposure times to scan energy and record detectors and signals
    yield from en_scan_core(sigs, dets,energy,energies,times,enscan_type=enscan_type)


def short_carbon_scan_nd(multiple=1,sigs=[],
                         dets=[sw_det],energy=en):
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
    enscan_type = 'short_carbon_scan_nd'
    if len(read_input("Starting a short Carbon energy scan hit enter in "
                      "the next 3 seconds to abort", "abort", "", 3)) > 0:
        return

    #Oct 2019, this pitch value seems to be optimal for carbon
    yield from bps.abs_set(mir3.Pitch,7.94,wait=True)

    # create a list of energies
    energies = np.arange(270,282,1)
    energies = np.append(energies,np.arange(282,286,.25))
    energies = np.append(energies,np.arange(286,292,.5))
    energies = np.append(energies,np.arange(292,306,1))
    energies = np.append(energies,np.arange(306,320,4))
    energies = np.append(energies,np.arange(320,350,10))
    times = energies.copy()

    # Define exposures times for different energy ranges
    times[energies<282] = 2
    times[(energies < 286) & (energies >= 282)] = 5
    times[energies >= 286] = 2
    times *= multiple

    # use these energies and exposure times to scan energy and record detectors and signals
    yield from en_scan_core(sigs, dets,energy,energies,times,enscan_type=enscan_type)



def focused_carbon_scan_nd(multiple=1,sigs=[],
                         dets=[sw_det],energy=en):
    '''
    Full Carbon Scan runs an RSoXS sample set through the carbon edge, with particular emphasis in he pre edge region
    this results in 61 exposures


    :param multiple: adjustment for exposure times
    :param mesh: which Izero channel to use
    :param det: which detector to use
    :param energy: what energy motor to scan
    :return: perform scan

    normal scan takes ~ 11 minutes to complete
    '''
    sample()
    enscan_type = 'focused_carbon_scan_nd'
    if len(read_input("Starting a short Carbon energy scan hit enter in "
                      "the next 3 seconds to abort", "abort", "", 3)) > 0:
        return

    #Oct 2019, this pitch value seems to be optimal for carbon
    yield from bps.abs_set(mir3.Pitch,7.94,wait=True)

    # create a list of energies
    energies = np.arange(270,282,5)
    energies = np.append(energies,np.arange(282,286,.2))
    energies = np.append(energies,np.arange(286,292,.5))
    energies = np.append(energies,np.arange(292,306,1))
    energies = np.append(energies,np.arange(306,320,4))
    energies = np.append(energies,np.arange(320,350,10))
    times = energies.copy()

    # Define exposures times for different energy ranges
    times[energies<282] = 2
    times[(energies < 286) & (energies >= 282)] = 5
    times[energies >= 286] = 2
    times *= multiple

    # use these energies and exposure times to scan energy and record detectors and signals
    yield from en_scan_core(sigs, dets,energy,energies,times,enscan_type=enscan_type)


def g_carbon_scan_nd(multiple=1,sigs=[],
                        dets=[sw_det], energy=en):
    '''
    G Carbon Scan runs an RSoXS sample set through the carbon edge, with a targeted 5 exposures


    :param multiple: adjustment for exposure times
    :param mesh: which Izero channel to use
    :param det: which detector to use
    :param energy: what energy motor to scan
    :return: perform scan

    normal scan takes ~ 18 minutes to complete
    '''
    enscan_type = 'g_carbon_scan_nd'
    sample()
    if len(read_input("Starting a Carbon energy scan hit enter in the next 3 seconds to abort", "abort", "", 3)) > 0:
        return
    yield from bps.abs_set(mir3.Pitch,7.94,wait=True)
    # create a list of energies
    energies = np.array([270,283.5,284.75,285.2,286.5])
    times = energies.copy()

    # Define exposures times for different energy ranges
    times[energies<2820] = 5
    times *= multiple

    # use these energies and exposure times to scan energy and record detectors and signals
    yield from en_scan_core(sigs, dets, energy, energies, times,enscan_type=enscan_type)


def t_carbon_scan_nd(multiple=1,sigs=[],
                        dets=[sw_det], energy=en):
    '''
    T Carbon Scan runs an RSoXS sample set through the carbon edge, with a targeted 6 exposures


    :param multiple: adjustment for exposure times
    :param mesh: which Izero channel to use
    :param det: which detector to use
    :param energy: what energy motor to scan
    :return: perform scan

    normal scan takes ~ 2 minutes to complete
    '''
    enscan_type = 't_carbon_scan_nd'
    sample()
    if len(read_input("Starting a Carbon energy scan hit enter in the next 3 seconds to abort", "abort", "", 3)) > 0:
        return
    yield from bps.abs_set(mir3.Pitch,7.94,wait=True)
    # create a list of energies
    energies = np.array([270,283,284.3,284.9,285.5,286,286.5,287])
    times = energies.copy()

    # Define exposures times for different energy ranges
    times[energies<2820] = 5
    times *= multiple

    # use these energies and exposure times to scan energy and record detectors and signals
    yield from en_scan_core(sigs, dets, energy, energies, times,enscan_type=enscan_type)


def sufficient_carbon_scan_nd(multiple=1,sigs=[],
                        dets=[sw_det], energy=en):
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
    enscan_type = 'sufficient_carbon_scan_nd'
    sample()
    if len(read_input("Starting a Carbon energy scan hit enter in the next 3 seconds to abort", "abort", "", 3)) > 0:
        return
    yield from bps.abs_set(mir3.Pitch,7.94,wait=True)
    # create a list of energies
    energies = np.arange(270,282,1)
    energies = np.append(energies,np.arange(282,286,.1))
    energies = np.append(energies,np.arange(286,292,.25))
    energies = np.append(energies,np.arange(292,305,1))
    energies = np.append(energies,np.arange(305,320,5))
    energies = np.append(energies,np.arange(320,350,10))
    times = energies.copy()

    # Define exposures times for different energy ranges
    times[energies<282] = 2
    times[(energies < 286) & (energies >= 282)] = 5
    times[energies >= 286] = 2
    times *= multiple

    # use these energies and exposure times to scan energy and record detectors and signals
    yield from en_scan_core(sigs, dets, energy, energies, times,enscan_type=enscan_type)



def picky_carbon_scan_nd(multiple=1,sigs=[],
                        dets=[sw_det], energy=en):
    '''
    Subh's picky Carbon Scan runs an RSoXS sample set through the useless energies before the carbon edge
    this results in 15 exposures


    :param multiple: adjustment for exposure times
    :param mesh: which Izero channel to use
    :param det: which detector to use
    :param energy: what energy motor to scan
    :return: perform scan

    normal scan takes ~ 18 minutes to complete
    '''
    enscan_type = 'sufficient_carbon_scan_nd'
    sample()
    if len(read_input("Starting a Carbon energy scan hit enter in the next 3 seconds to abort", "abort", "", 3)) > 0:
        return
    yield from bps.abs_set(mir3.Pitch,7.94,wait=True)
    # create a list of energies
    energies = np.arange(270,285,1)
    times = energies.copy()

    # Define exposures times for different energy ranges
    times[energies<2820] = 1
    times *= multiple

    # use these energies and exposure times to scan energy and record detectors and signals
    yield from en_scan_core(sigs, dets, energy, energies, times,enscan_type=enscan_type)



def full_carbon_scan_nd(multiple=1,sigs=[],
                        dets=[sw_det], energy=en):
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
    enscan_type = 'full_carbon_scan_nd'
    sample()
    if len(read_input("Starting a Carbon energy scan hit enter in the next 3 seconds to abort", "abort", "", 3)) > 0:
        return
    yield from bps.abs_set(mir3.Pitch,7.94,wait=True)
    # create a list of energies
    energies = np.arange(270,282,.5)
    energies = np.append(energies,np.arange(282,286,.1))
    energies = np.append(energies,np.arange(286,292,.2))
    energies = np.append(energies,np.arange(292,305,1))
    energies = np.append(energies,np.arange(305,320,1))
    energies = np.append(energies,np.arange(320,350,5))
    times = energies.copy()

    # Define exposures times for different energy ranges
    times[energies<282] = 2
    times[(energies < 286) & (energies >= 282)] = 5
    times[energies >= 286] = 2
    times *= multiple

    # use these energies and exposure times to scan energy and record detectors and signals
    yield from en_scan_core(sigs, dets, energy, energies, times,enscan_type=enscan_type)



def full_carbon_NEXAFS(sigs=[],
                        dets=[Sample_TEY,Izero_Mesh,Beamstop_WAXS], energy=en):
    '''
    Full Carbon Scan runs an RSoXS sample set through the carbon edge, with particular emphasis in he pre edge region


    :param sigs: which other signals to use
    :param dets: which detector to use
    :param energy: what energy motor to scan
    :return: perform scan

    normal scan takes ~ 7 minutes to complete
    '''
    enscan_type = 'full_carbon_NEXAFS'
    sample()
    if len(read_input("Starting a Carbon NEXAFS scan hit enter in the next 3 seconds to abort"
                      "\nYou remembered to hook up the shutter, right?", "abort", "", 3)) > 0:
        return
    yield from bps.abs_set(mir3.Pitch,7.94,wait=True)
    # create a list of energies
    energies = np.arange(270,282,.5)
    energies = np.append(energies,np.arange(282,286,.1))
    energies = np.append(energies,np.arange(286,292,.1))
    energies = np.append(energies,np.arange(292,310,.25))
    energies = np.append(energies,np.arange(310,320,1))
    energies = np.append(energies,np.arange(320,350,1))
    times = energies.copy()

    # Define exposures times for different energy ranges
    # use these energies and exposure times to scan energy and record detectors and signals


    yield from NEXAFS_scan_core(sigs, dets, energy, energies,enscan_type=enscan_type,openshutter=True)




def full_ca_scan_nd(multiple=1,sigs=[],
                    dets=[sw_det],energy=en):
    '''
    Calcium Scan runs an RSoXS sample set through the Ca edge, with particular emphasis in he pre edge region


    :param multiple: adjustment for exposure times
    :param mesh: which Izero channel to use
    :param det: which detector to use
    :param energy: what energy motor to scan
    :return: perform scan

    normal scan takes ~ 12 minutes to complete
    '''
    beamline_status()
    if len(read_input("Starting a Calcium energy scan hit enter in the next 3 seconds to abort", "abort", "", 3)) > 0:
        return
    enscan_type = 'full_ca_scan_nd'
    # create a list of energies
    energies = np.arange(320,340,5)
    energies = np.append(energies,np.arange(340,345,1))
    energies = np.append(energies,np.arange(345,355,.5))
    times = energies.copy()

    # Define exposures times for different energy ranges
    times[energies<400] = 20
    times *= multiple

    # use these energies and exposure times to scan energy and record detectors and signals
    yield from en_scan_core(sigs, dets, energy, energies, times,enscan_type=enscan_type)


def full_carbon_calcium_scan_nd(multiple=1,sigs=[],
                        dets=[sw_det], energy=en):
    '''
    Full Carbon and Calcium Scan runs an RSoXS sample set through the carbon and calcium edges,
    with particular emphasis in he pre edge region

    :param multiple: adjustment for exposure times
    :param mesh: which Izero channel to use
    :param det: which detector to use
    :param energy: what energy motor to scan
    :return: perform scan

    normal scan takes ~ 18 minutes to complete
    '''
    sample()
    enscan_type = 'full_carbon_calcium_scan_nd'
    if len(read_input("Starting a full carbon and calcium energy scan hit "
                      "enter in the next 3 seconds to abort", "abort", "", 3)) > 0:
        return

    # create a list of energies
    energies = np.arange(270,282,.5)
    energies = np.append(energies,np.arange(282,286,.1))
    energies = np.append(energies,np.arange(286,292,.2))
    energies = np.append(energies,np.arange(292,305,1))
    energies = np.append(energies,np.arange(305,320,5))
    energies = np.append(energies,np.arange(320,340,5))
    energies = np.append(energies,np.arange(340,345,1))
    energies = np.append(energies,np.arange(345,360,.5))
    times = energies.copy()

    # Define exposures times for different energy ranges
    times[energies<282] = 2
    times[(energies < 286) & (energies >= 282)] = 5
    times[energies >= 286] = 2
    times[energies >= 320] = 10
    times *= multiple

    # use these energies and exposure times to scan energy and record detectors and signals
    yield from en_scan_core(sigs, dets, energy, energies, times,enscan_type=enscan_type)

from ophyd.sim import det_with_count_time
from cycler import cycler

def fluorine_SAXS(exp_time=1):
    enscan_type = 'fluorine_SAXS'
    #Oct 2019, this pitch value seems to be optimal for carbon
    yield from bps.abs_set(mir3.Pitch,7.89)
    set_exposure(exp_time)
    yield from bps.abs_set(en, 680, timeout=180, wait=True)
    yield from bp.scan([sw_det, en.energy],en,680,700,41,md={'plan_name':enscan_type})


def Si_SAXS(exp_time=1):
    enscan_type = 'Si_SAXS'
    # Oct 2019, this pitch value seems to be optimal for carbon
    yield from bps.abs_set(mir3.Pitch,7.87)
    set_exposure(exp_time)
    yield from bps.abs_set(en, 1830, timeout=180, wait=True)
    yield from bp.scan([sw_det, en.energy], en, 1830, 1870, 41, md={'plan_name': enscan_type})


def fluorine_WAXS(exp_time=2):

    enscan_type = 'fluorine_WAXS'
    #Oct 2019, this pitch value seems to be optimal for carbon

    yield from bps.mv(en,680)
    yield from bps.abs_set(mir3.Pitch,7.89)
    yield from bp.scan([sw_det, en.energy],en,680,700,41,md={'plan_name':enscan_type})

