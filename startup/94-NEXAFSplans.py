run_report(__file__)

import numpy as np


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
    yield from bps.mv(DiodeRange, 6)
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

def full_Nitrogen_NEXAFS(sigs=[],
                        dets=[Sample_TEY,Izero_Mesh,Beamstop_WAXS], energy=en):
    '''
    Full Carbon Scan runs an RSoXS sample set through the carbon edge, with particular emphasis in he pre edge region


    :param sigs: which other signals to use
    :param dets: which detector to use
    :param energy: what energy motor to scan
    :return: perform scan

    normal scan takes ~ 7 minutes to complete
    '''
    enscan_type = 'full_Nitrogen_NEXAFS'
    sample()
    if len(read_input("Starting a Nitrogen NEXAFS scan hit enter in the next 3 seconds to abort"
                      "\nYou remembered to hook up the shutter, right?", "abort", "", 3)) > 0:
        return
    yield from bps.abs_set(mir3.Pitch,7.92,wait=True)
    yield from bps.mv(DiodeRange,7)
    # create a list of energies
    energies = np.arange(385,397,1)
    energies = np.append(energies,np.arange(397,407,.2))
    energies = np.append(energies,np.arange(407,440,1))
    times = energies.copy()

    # Define exposures times for different energy ranges
    # use these energies and exposure times to scan energy and record detectors and signals


    yield from NEXAFS_scan_core(sigs, dets, energy, energies,enscan_type=enscan_type,openshutter=True)


def full_Oxygen_NEXAFS(sigs=[],
                        dets=[Sample_TEY,Izero_Mesh,Beamstop_WAXS], energy=en):
    '''
    Full Carbon Scan runs an RSoXS sample set through the carbon edge, with particular emphasis in he pre edge region


    :param sigs: which other signals to use
    :param dets: which detector to use
    :param energy: what energy motor to scan
    :return: perform scan

    normal scan takes ~ 7 minutes to complete
    '''
    enscan_type = 'full_Oxygen_NEXAFS'
    sample()
    if len(read_input("Starting a Oxygen NEXAFS scan hit enter in the next 3 seconds to abort"
                      "\nYou remembered to hook up the shutter, right?", "abort", "", 3)) > 0:
        return
    yield from bps.abs_set(mir3.Pitch,7.915,wait=True)
    yield from bps.mv(DiodeRange, 6)
    # create a list of energies
    energies = np.arange(510,525,1)
    energies = np.append(energies,np.arange(525,540,.2))
    energies = np.append(energies,np.arange(540,560,1))
    times = energies.copy()

    # Define exposures times for different energy ranges
    # use these energies and exposure times to scan energy and record detectors and signals


    yield from NEXAFS_scan_core(sigs, dets, energy, energies,enscan_type=enscan_type,openshutter=True)



def full_Al_NEXAFS(sigs=[],
                        dets=[Sample_TEY,Izero_Mesh,Beamstop_WAXS], energy=en):
    '''
    Full Carbon Scan runs an RSoXS sample set through the carbon edge, with particular emphasis in he pre edge region


    :param sigs: which other signals to use
    :param dets: which detector to use
    :param energy: what energy motor to scan
    :return: perform scan

    normal scan takes ~ 7 minutes to complete
    '''
    enscan_type = 'full_Al_NEXAFS'
    sample()
    if len(read_input("Starting a Aluminum NEXAFS scan hit enter in the next 3 seconds to abort"
                      "\nYou remembered to hook up the shutter, right?", "abort", "", 3)) > 0:
        return
    yield from bps.abs_set(mir3.Pitch,7.89,wait=True)
    yield from bps.mv(DiodeRange, 7)
    # create a list of energies
    energies = np.arange(1550,1620,.5)

    times = energies.copy()

    # Define exposures times for different energy ranges
    # use these energies and exposure times to scan energy and record detectors and signals


    yield from NEXAFS_scan_core(sigs, dets, energy, energies,enscan_type=enscan_type,openshutter=True)



def full_Zn_NEXAFS(sigs=[],
                        dets=[Sample_TEY,Izero_Mesh,Beamstop_WAXS], energy=en):
    '''
    Full Carbon Scan runs an RSoXS sample set through the carbon edge, with particular emphasis in he pre edge region


    :param sigs: which other signals to use
    :param dets: which detector to use
    :param energy: what energy motor to scan
    :return: perform scan

    normal scan takes ~ 7 minutes to complete
    '''
    enscan_type = 'full_Zn_NEXAFS'
    sample()
    if len(read_input("Starting a Zinc NEXAFS scan hit enter in the next 3 seconds to abort"
                      "\nYou remembered to hook up the shutter, right?", "abort", "", 3)) > 0:
        return
    yield from bps.abs_set(mir3.Pitch,7.9,wait=True)
    yield from bps.mv(DiodeRange, 7)
    # create a list of energies
    energies = np.arange(1000,1070,.5)
    times = energies.copy()

    # Define exposures times for different energy ranges
    # use these energies and exposure times to scan energy and record detectors and signals


    yield from NEXAFS_scan_core(sigs, dets, energy, energies,enscan_type=enscan_type,openshutter=True)