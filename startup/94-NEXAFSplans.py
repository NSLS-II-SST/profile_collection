run_report(__file__)

import numpy as np

def full_Carbon_NEXAFS(sigs=[],
                       dets=[Sample_TEY, Izero_Mesh, Beamstop_WAXS], energy=en, pol=0, diode_range=7, m3_pitch=7.98,
                       open_each_step=True, exp_time=1, grating='no change', motorname='None', offset=0):
    '''
    Full Carbon Scan runs an RSoXS sample set through the carbon edge, with particular emphasis in he pre edge region
    typically this is not run anymore as of jan 2021.  fly scans are the preferred NEXAFS method
    I'm keeping this here just as a historical record / fallback in case flying stops working

    :param sigs: which other signals to use
    :param dets: which detector to use
    :param energy: what energy motor to scan
    :return: perform scan

    normal scan takes ~ 7 minutes to complete
    '''
    enscan_type = 'full_Carbon_NEXAFS'
    sample()
    if len(read_input("Starting a Carbon NEXAFS scan hit enter in the next 3 seconds to abort", "abort", "", 3)) > 0:
        return

    # create a list of energies
    energies = np.arange(270, 282, .5)
    energies = np.append(energies, np.arange(282, 286, .1))
    energies = np.append(energies, np.arange(286, 292, .1))
    energies = np.append(energies, np.arange(292, 310, .25))
    energies = np.append(energies, np.arange(310, 320, 1))
    energies = np.append(energies, np.arange(320, 350, 1))

    yield from NEXAFS_scan_core(sigs, dets, energy, energies, enscan_type=enscan_type,
                                openshutter=True, diode_range=diode_range, m3_pitch=m3_pitch, pol=pol,
                                open_each_step=open_each_step, exp_time=exp_time, grating=grating,
                                motorname=motorname, offset=offset)


def fly_Carbon_NEXAFS(speed=.1, pol=0, diode_range=7, m3_pitch=7.98, grating='250'):
    """

    @param speed: the speed in eV/second to fly the mono
    @param pol: the polarization of the EPU to set before run
    @param diode_range: sets the range of the SAXS and WAXS beamstop DIODEs for direct beam measurements
    @param m3_pitch: the pitch of the M3 mirror to use for this energy range
    @param grating: the grating of the mono to use for the scan (currently "1200" and "250" are only valid choices)
    @return: perform a flying NEXAFS scan
    """
    enscan_type = 'fly_Carbon_NEXAFS'
    sample()
    if len(read_input("Starting a Carbon NEXAFS fly scan hit enter in the next 3 seconds to abort", "abort", "",
                      3)) > 0:
        return
    yield from NEXAFS_fly_scan_core([(270, 282, speed * 3), (282, 297, speed), (297, 340, speed * 5)],
                                    enscan_type=enscan_type, openshutter=True, exp_time=.5,
                                    diode_range=diode_range, m3_pitch=m3_pitch, pol=pol, grating=grating)


def fly_Calcium_NEXAFS(speed=.15, pol=0, diode_range=7, m3_pitch=7.99, grating='250'):
    """

    @param speed: the speed in eV/second to fly the mono
    @param pol: the polarization of the EPU to set before run
    @param diode_range: sets the range of the SAXS and WAXS beamstop DIODEs for direct beam measurements
    @param m3_pitch: the pitch of the M3 mirror to use for this energy range
    @param grating: the grating of the mono to use for the scan (currently "1200" and "250" are only valid choices)
    @return: perform a flying NEXAFS scan
    """
    enscan_type = 'fly_Calcium_NEXAFS'
    sample()
    if len(read_input("Starting a Carbon NEXAFS fly scan hit enter in the next 3 seconds to abort", "abort", "",
                      3)) > 0:
        return
    yield from NEXAFS_fly_scan_core([(320, 340, speed * 3), (340, 355, speed)], enscan_type=enscan_type,
                                    openshutter=True, exp_time=.5,
                                    diode_range=diode_range, m3_pitch=m3_pitch, pol=pol, grating=grating)


def fly_SulfurL_NEXAFS(speed=.1, pol=0, diode_range=7, m3_pitch=7.97, grating='250'):
    """

    @param speed: the speed in eV/second to fly the mono
    @param pol: the polarization of the EPU to set before run
    @param diode_range: sets the range of the SAXS and WAXS beamstop DIODEs for direct beam measurements
    @param m3_pitch: the pitch of the M3 mirror to use for this energy range
    @param grating: the grating of the mono to use for the scan (currently "1200" and "250" are only valid choices)
    @return: perform a flying NEXAFS scan
    """
    enscan_type = 'fly_SulfurL_NEXAFS'
    sample()
    if len(read_input("Starting a Sulfur L-edge NEXAFS fly scan hit enter in the next 3 seconds to abort", "abort", "",
                      3)) > 0:
        return
    yield from NEXAFS_fly_scan_core([(180, 225, speed)], enscan_type=enscan_type, openshutter=True, exp_time=.5,
                                    diode_range=diode_range, m3_pitch=m3_pitch, pol=pol, grating=grating)


def fly_SiliconL_NEXAFS(speed=.1, pol=0, diode_range=6, m3_pitch=8.01, grating='250'):
    """

    @param speed: the speed in eV/second to fly the mono
    @param pol: the polarization of the EPU to set before run
    @param diode_range: sets the range of the SAXS and WAXS beamstop DIODEs for direct beam measurements
    @param m3_pitch: the pitch of the M3 mirror to use for this energy range
    @param grating: the grating of the mono to use for the scan (currently "1200" and "250" are only valid choices)
    @return: perform a flying NEXAFS scan
    """
    enscan_type = 'fly_SiliconL_NEXAFS'
    sample()
    if len(read_input("Starting a Silicon L-edge NEXAFS fly scan hit enter in the next 3 seconds to abort", "abort", "",
                      3)) > 0:
        return
    yield from NEXAFS_fly_scan_core([(100, 140, speed)], enscan_type=enscan_type, openshutter=True, exp_time=.5,
                                    diode_range=diode_range, m3_pitch=m3_pitch, pol=pol, grating=grating)


def fly_SiliconK_NEXAFS(speed=.2, pol=0, diode_range=6, m3_pitch=7.97, grating='1200'):
    """

    @param speed: the speed in eV/second to fly the mono
    @param pol: the polarization of the EPU to set before run
    @param diode_range: sets the range of the SAXS and WAXS beamstop DIODEs for direct beam measurements
    @param m3_pitch: the pitch of the M3 mirror to use for this energy range
    @param grating: the grating of the mono to use for the scan (currently "1200" and "250" are only valid choices)
    @return: perform a flying NEXAFS scan
    """
    enscan_type = 'fly_SiliconK_NEXAFS'
    sample()
    if len(read_input("Starting a Silicon K-edge NEXAFS fly scan hit enter in the next 3 seconds to abort", "abort", "",
                      3)) > 0:
        return
    yield from NEXAFS_fly_scan_core([(1830, 1870, speed)], enscan_type=enscan_type, openshutter=True, exp_time=.5,
                                    diode_range=diode_range, m3_pitch=m3_pitch, pol=pol, grating=grating)


def fly_Nitrogen_NEXAFS(speed=.1, pol=0, diode_range=7, m3_pitch=7.96, grating='250'):
    """

    @param speed: the speed in eV/second to fly the mono
    @param pol: the polarization of the EPU to set before run
    @param diode_range: sets the range of the SAXS and WAXS beamstop DIODEs for direct beam measurements
    @param m3_pitch: the pitch of the M3 mirror to use for this energy range
    @param grating: the grating of the mono to use for the scan (currently "1200" and "250" are only valid choices)
    @return: perform a flying NEXAFS scan
    """
    enscan_type = 'fly_Nitrogen_NEXAFS'
    sample()
    if len(read_input("Starting a Nitrogen NEXAFS fly scan hit enter in the next 3 seconds to abort", "abort", "",
                      3)) > 0:
        return
    yield from NEXAFS_fly_scan_core([(385, 397, speed * 3), (397, 407, speed), (407, 440, speed * 5)],
                                    enscan_type=enscan_type, openshutter=True, exp_time=.5,
                                    diode_range=diode_range, m3_pitch=m3_pitch, pol=pol, grating=grating)


def fly_Oxygen_NEXAFS(speed=.1, pol=0, diode_range=7, m3_pitch=7.96, grating='250'):
    """

    @param speed: the speed in eV/second to fly the mono
    @param pol: the polarization of the EPU to set before run
    @param diode_range: sets the range of the SAXS and WAXS beamstop DIODEs for direct beam measurements
    @param m3_pitch: the pitch of the M3 mirror to use for this energy range
    @param grating: the grating of the mono to use for the scan (currently "1200" and "250" are only valid choices)
    @return: perform a flying NEXAFS scan
    """
    enscan_type = 'fly_Oxygen_NEXAFS'
    sample()
    if len(read_input("Starting a Oxygen NEXAFS fly scan hit enter in the next 3 seconds to abort", "abort", "",
                      3)) > 0:
        return
    yield from NEXAFS_fly_scan_core([(510, 525, speed * 3), (525, 540, speed), (540, 560, speed * 5)],
                                    enscan_type=enscan_type, openshutter=True, exp_time=.5,
                                    diode_range=diode_range, m3_pitch=m3_pitch, pol=pol, grating=grating)


def fly_Fluorine_NEXAFS(speed=.5, pol=0, diode_range=7, m3_pitch=7.98, grating='1200'):
    """

    @param speed: the speed in eV/second to fly the mono
    @param pol: the polarization of the EPU to set before run
    @param diode_range: sets the range of the SAXS and WAXS beamstop DIODEs for direct beam measurements
    @param m3_pitch: the pitch of the M3 mirror to use for this energy range
    @param grating: the grating of the mono to use for the scan (currently "1200" and "250" are only valid choices)
    @return: perform a flying NEXAFS scan
    """
    enscan_type = 'fly_Fluorine_NEXAFS'
    sample()
    if len(read_input("Starting a Fluorine NEXAFS fly scan hit enter in the next 3 seconds to abort", "abort", "",
                      3)) > 0:
        return
    yield from NEXAFS_fly_scan_core([(680, 720, speed)], enscan_type=enscan_type, openshutter=True, exp_time=.5,
                                    diode_range=diode_range, m3_pitch=m3_pitch, pol=pol, grating=grating)


def fly_Boron_NEXAFS(speed=.1, pol=0, diode_range=6, m3_pitch=8.0, grating='250'):
    """

    @param speed: the speed in eV/second to fly the mono
    @param pol: the polarization of the EPU to set before run
    @param diode_range: sets the range of the SAXS and WAXS beamstop DIODEs for direct beam measurements
    @param m3_pitch: the pitch of the M3 mirror to use for this energy range
    @param grating: the grating of the mono to use for the scan (currently "1200" and "250" are only valid choices)
    @return: perform a flying NEXAFS scan
    """
    enscan_type = 'fly_Fluorine_NEXAFS'
    sample()
    if len(read_input("Starting a Fluorine NEXAFS fly scan hit enter in the next 3 seconds to abort", "abort", "",
                      3)) > 0:
        return
    yield from NEXAFS_fly_scan_core([(190, 215, speed)], enscan_type=enscan_type, openshutter=True, exp_time=.5,
                                    diode_range=diode_range, m3_pitch=m3_pitch, pol=pol, grating=grating)



def do_HOPGscans_epu():
    pols = [0, 20, 40, 55, 70, 90, -1]
    yield from load_sample(hopggrazing)
    for polarization in pols:
        yield from full_Carbon_NEXAFS(dets=[Sample_TEY, IzeroMesh], pol=polarization)
    yield from load_sample(hopgnormal)
    for polarization in pols:
        yield from full_Carbon_NEXAFS(dets=[Sample_TEY, IzeroMesh], pol=polarization)
    yield from load_sample(hopggrazing)
    for polarization in pols:
        yield from full_Carbon_NEXAFS(dets=[Sample_TEY, IzeroMesh], pol=polarization)
    yield from load_sample(hopgnormal)
    for polarization in pols:
        yield from full_Carbon_NEXAFS(dets=[Sample_TEY, IzeroMesh], pol=polarization)
    yield from load_sample(hopggrazing)
    for polarization in pols:
        yield from full_Carbon_NEXAFS(dets=[Sample_TEY, IzeroMesh], pol=polarization)
    yield from load_sample(hopgnormal)
    for polarization in pols:
        yield from full_Carbon_NEXAFS(dets=[Sample_TEY, IzeroMesh], pol=polarization)


def normal_incidence_rotate_pol_nexafs(nexafs_plan=fly_Carbon_NEXAFS,
                                       polarizations=[0, 20, 45, 70, 90],
                                       **kwargs):
    """
    At normal incidence, rotate the polarization of the X-ray beam and conduct a NEXAFS scan at each polarization
    """
    yield from rotate_now(90)
    for pol in polarizations:
        yield from nexafs_plan(pol=pol, **kwargs)


def fixed_pol_rotate_sample_nexafs(nexafs_plan=fly_Carbon_NEXAFS,
                                   angles=[20, 40, 55, 70, 90],
                                   polarization=0,
                                   **kwargs):
    """
    At fixed polarization, rotate the sample to do a traditional angle dependant NEXAFS measurement
    """
    for angle in angles:
        yield from rotate_now(angle)
        yield from nexafs_plan(pol=polarization, **kwargs)


def epu_angle_from_grazing(real_incident_angle, grazing_angle=20):
    return np.arccos(
        np.cos(real_incident_angle * np.pi / 180) * 1 / (np.cos(grazing_angle * np.pi / 180))) * 180 / np.pi


def fixed_sample_rotate_pol_nexafs(nexafs_plan=fly_Carbon_NEXAFS,
                                   grazing_angle=20,
                                   angles=[20, 40, 55, 70, 90],
                                   **kwargs):
    """
    At fixed incident angle, rotate the polarization angle of the X-rays and take NEXAFS at each step
    polarization is calculated relative to the sample normal
    angles less than the grazing angle are not allowed and are ignored
    """
    yield from rotate_now(grazing_angle)
    for angle in angles:
        if angle < grazing_angle:
            continue
        yield from nexafs_plan(pol=epu_angle_from_grazing(angle, grazing_angle), **kwargs)
