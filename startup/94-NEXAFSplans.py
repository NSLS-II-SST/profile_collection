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
    yield from bps.abs_set(mir3.Pitch,7.958,wait=True)
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

