run_report(__file__)

import numpy as np


def epu_angle_from_grazing(real_incident_angle,grazing_angle=20):
    print(
        f'Angle for Polarization = {np.arccos(np.cos(real_incident_angle * np.pi / 180) * 1 / (np.cos(grazing_angle * np.pi / 180))) * 180 / np.pi}')
    return np.arccos(
        np.cos(real_incident_angle * np.pi / 180) * 1 / (np.cos(grazing_angle * np.pi / 180))) * 180 / np.pi


def Carbon_angle_NEXAFS(grazing_angle=20,speed=.1,diode_range=7,angles = [20,40,55,70,90]):
    for angle in angles:
        yield from fly_Carbon_NEXAFS(speed=speed,
                                     pol=epu_angle_from_grazing(angle,grazing_angle),
                                     diode_range=diode_range,
                                     grating='250',
                                     m3_pitch=7.93)
def Oxygen_angle_NEXAFS(grazing_angle=20,speed=.2,diode_range=7,angles = [20,40,55,70,90]):
    for angle in angles:
        yield from fly_Oxygen_NEXAFS(speed=speed,
                                     pol=epu_angle_from_grazing(angle,grazing_angle),
                                     diode_range=diode_range,
                                     grating='250',
                                     m3_pitch=7.95)
def Nitrogen_angle_NEXAFS(grazing_angle=20,speed=.1,diode_range=7,angles = [20,40,55,70,90]):
    for angle in angles:
        yield from fly_Nitrogen_NEXAFS(speed=speed,
                                     pol=epu_angle_from_grazing(angle,grazing_angle),
                                     diode_range=diode_range,
                                     grating='250',
                                     m3_pitch=7.95)
def Fluorine_angle_NEXAFS(grazing_angle=20,speed=.3,diode_range=7,angles = [20,40,55,70,90]):
    for angle in angles:
        yield from fly_Fluorine_NEXAFS(speed=speed,
                                     pol=epu_angle_from_grazing(angle,grazing_angle),
                                     diode_range=diode_range,
                                     grating='1200',
                                     m3_pitch=7.97)


def full_Carbon_NEXAFS(sigs=[],
                        dets=[Sample_TEY,Izero_Mesh,Beamstop_WAXS], energy=en,pol=0,diode_range=7,m3_pitch=7.95,
                       open_each_step=True,exp_time=1,grating='no change', motorname='None',offset=0):
    '''
    Full Carbon Scan runs an RSoXS sample set through the carbon edge, with particular emphasis in he pre edge region


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
    energies = np.arange(270,282,.5)
    energies = np.append(energies,np.arange(282,286,.1))
    energies = np.append(energies,np.arange(286,292,.1))
    energies = np.append(energies,np.arange(292,310,.25))
    energies = np.append(energies,np.arange(310,320,1))
    energies = np.append(energies,np.arange(320,350,1))
    times = energies.copy()

    # Define exposures times for different energy ranges
    # use these energies and exposure times to scan energy and record detectors and signals


    yield from NEXAFS_scan_core(sigs, dets, energy, energies,enscan_type=enscan_type,
                                openshutter=True,diode_range=diode_range,m3_pitch=m3_pitch, pol=pol,
                                open_each_step=open_each_step,exp_time=exp_time,grating=grating,
                                motorname=motorname,offset=offset)

def fly_Carbon_NEXAFS(speed=.1,pol=0,diode_range=7,m3_pitch=7.95,grating='250'):
    '''
    Full Carbon Scan runs an RSoXS sample set through the carbon edge, with particular emphasis in he pre edge region


    :param sigs: which other signals to use
    :param dets: which detector to use
    :param energy: what energy motor to scan
    :return: perform scan

    normal scan takes ~ 7 minutes to complete
    '''
    enscan_type = 'fly_Carbon_NEXAFS'
    sample()
    if len(read_input("Starting a Carbon NEXAFS fly scan hit enter in the next 3 seconds to abort", "abort", "", 3)) > 0:
        return
    yield from NEXAFS_fly_scan_core([(270, 282, speed*3),(282, 297, speed),(297, 340, speed*5)], enscan_type=enscan_type,openshutter=True,exp_time=.5,
                                    diode_range=diode_range,m3_pitch=m3_pitch, pol=pol,grating=grating)

def fly_Calcium_NEXAFS(speed=.15,pol=0,diode_range=7,m3_pitch=7.99,grating='250'):
    '''
    Full Carbon Scan runs an RSoXS sample set through the carbon edge, with particular emphasis in he pre edge region


    :param sigs: which other signals to use
    :param dets: which detector to use
    :param energy: what energy motor to scan
    :return: perform scan

    normal scan takes ~ 7 minutes to complete
    '''
    enscan_type = 'fly_Calcium_NEXAFS'
    sample()
    if len(read_input("Starting a Carbon NEXAFS fly scan hit enter in the next 3 seconds to abort", "abort", "", 3)) > 0:
        return
    yield from NEXAFS_fly_scan_core([(320,340, speed*3),(340, 355, speed)], enscan_type=enscan_type,openshutter=True,exp_time=.5,
                                    diode_range=diode_range,m3_pitch=m3_pitch, pol=pol,grating=grating)

def fly_SulfurL_NEXAFS(speed=.1,pol=0,diode_range=7,m3_pitch=7.97,grating='250'):
    '''
    Full Carbon Scan runs an RSoXS sample set through the carbon edge, with particular emphasis in he pre edge region


    :param sigs: which other signals to use
    :param dets: which detector to use
    :param energy: what energy motor to scan
    :return: perform scan

    normal scan takes ~ 7 minutes to complete
    '''
    enscan_type = 'fly_SulfurL_NEXAFS'
    sample()
    if len(read_input("Starting a Carbon NEXAFS fly scan hit enter in the next 3 seconds to abort", "abort", "", 3)) > 0:
        return
    yield from NEXAFS_fly_scan_core([(180,225, speed)], enscan_type=enscan_type,openshutter=True,exp_time=.5,
                                    diode_range=diode_range,m3_pitch=m3_pitch, pol=pol,grating=grating)

def fly_Nitrogen_NEXAFS(speed=.1,pol=0,diode_range=7,m3_pitch=7.95,grating='250'):
    '''
    Full Carbon Scan runs an RSoXS sample set through the carbon edge, with particular emphasis in he pre edge region


    :param sigs: which other signals to use
    :param dets: which detector to use
    :param energy: what energy motor to scan
    :return: perform scan

    normal scan takes ~ 7 minutes to complete
    '''
    enscan_type = 'fly_Nitrogen_NEXAFS'
    sample()
    if len(read_input("Starting a Nitrogen NEXAFS fly scan hit enter in the next 3 seconds to abort", "abort", "", 3)) > 0:
        return
    yield from NEXAFS_fly_scan_core([(385, 397, speed*3),(397, 407, speed),(407, 440, speed*5)], enscan_type=enscan_type,openshutter=True,exp_time=.5,
                                    diode_range=diode_range,m3_pitch=m3_pitch, pol=pol,grating=grating)


def fly_Oxygen_NEXAFS(speed=.1,pol=0,diode_range=7,m3_pitch=7.95,grating='250'):
    '''
    Full Carbon Scan runs an RSoXS sample set through the carbon edge, with particular emphasis in he pre edge region


    :param sigs: which other signals to use
    :param dets: which detector to use
    :param energy: what energy motor to scan
    :return: perform scan

    normal scan takes ~ 7 minutes to complete
    '''
    enscan_type = 'fly_Oxygen_NEXAFS'
    sample()
    if len(read_input("Starting a Oxygen NEXAFS fly scan hit enter in the next 3 seconds to abort", "abort", "", 3)) > 0:
        return
    yield from NEXAFS_fly_scan_core([(510, 525, speed*3),(525, 540, speed),(540, 560, speed*5)], enscan_type=enscan_type,openshutter=True,exp_time=.5,
                                    diode_range=diode_range,m3_pitch=m3_pitch, pol=pol,grating=grating)

def fly_Fluorine_NEXAFS(speed=.1,pol=0,diode_range=7,m3_pitch=7.95,grating='1200'):
    '''
    Full Carbon Scan runs an RSoXS sample set through the carbon edge, with particular emphasis in he pre edge region


    :param sigs: which other signals to use
    :param dets: which detector to use
    :param energy: what energy motor to scan
    :return: perform scan

    normal scan takes ~ 7 minutes to complete
    '''
    enscan_type = 'fly_Fluorine_NEXAFS'
    sample()
    if len(read_input("Starting a Fluorine NEXAFS fly scan hit enter in the next 3 seconds to abort", "abort", "", 3)) > 0:
        return
    yield from NEXAFS_fly_scan_core([(680, 720, speed)], enscan_type=enscan_type,openshutter=True,exp_time=.5,
                                    diode_range=diode_range,m3_pitch=m3_pitch, pol=pol,grating=grating)

def short_Carbon_NEXAFS(sigs=[],
                        dets=[Sample_TEY,Izero_Mesh,Beamstop_WAXS], energy=en,pol=0,diode_range=7,m3_pitch=7.92,
                       open_each_step=True,exp_time=1,grating='no change', motorname='None',offset=0):
    '''
    Full Carbon Scan runs an RSoXS sample set through the carbon edge, with particular emphasis in he pre edge region


    :param sigs: which other signals to use
    :param dets: which detector to use
    :param energy: what energy motor to scan
    :return: perform scan

    normal scan takes ~ 7 minutes to complete
    '''
    enscan_type = 'short_Carbon_NEXAFS'
    sample()
    if len(read_input("Starting a short Carbon NEXAFS scan hit enter in the next 3 seconds to abort", "abort", "", 3)) > 0:
        return


    # create a list of energies
    energies = np.arange(270,282,.5)
    energies = np.append(energies,np.arange(282,286,.2))
    energies = np.append(energies,np.arange(286,292,.2))
    energies = np.append(energies,np.arange(292,310,.5))
    energies = np.append(energies,np.arange(310,320,1))
    energies = np.append(energies,np.arange(320,350,2))
    times = energies.copy()

    # Define exposures times for different energy ranges
    # use these energies and exposure times to scan energy and record detectors and signals


    yield from NEXAFS_scan_core(sigs, dets, energy, energies,enscan_type=enscan_type,
                                openshutter=True,diode_range=diode_range,m3_pitch=m3_pitch, pol=pol,
                                open_each_step=open_each_step,exp_time=exp_time,grating=grating,
                                motorname=motorname,offset=offset)


def full_SulfurL_NEXAFS(sigs=[],
                        dets=[Sample_TEY,Izero_Mesh,Beamstop_WAXS], energy=en,pol=0,diode_range=7,m3_pitch=7.94,
                       open_each_step=True,exp_time=1,grating='no change', motorname='None',offset=0):
    '''
    Full Carbon Scan runs an RSoXS sample set through the carbon edge, with particular emphasis in he pre edge region


    :param sigs: which other signals to use
    :param dets: which detector to use
    :param energy: what energy motor to scan
    :return: perform scan

    normal scan takes ~ 7 minutes to complete
    '''
    enscan_type = 'full_SulfurL_NEXAFS'
    sample()
    if len(read_input("Starting a Sulfur L edge NEXAFS scan hit enter in the next 3 seconds to abort", "abort", "", 3)) > 0:
        return


    # create a list of energies
    energies = np.arange(180,225,.5)
    times = energies.copy()

    # Define exposures times for different energy ranges
    # use these energies and exposure times to scan energy and record detectors and signals


    yield from NEXAFS_scan_core(sigs, dets, energy, energies,enscan_type=enscan_type,
                                openshutter=True,diode_range=diode_range,m3_pitch=m3_pitch, pol=pol,
                                open_each_step=open_each_step,exp_time=exp_time,grating=grating,
                                motorname=motorname,offset=offset)
def full_Nitrogen_NEXAFS(sigs=[],
                        dets=[Sample_TEY,Izero_Mesh,Beamstop_WAXS], energy=en,pol=0,m3_pitch=7.90,diode_range=6,
                       open_each_step=True,exp_time=1,grating='no change', motorname='None',offset=0):
    '''
    Full Nitrogen Scan runs an RSoXS sample set through the carbon edge, with particular emphasis in he pre edge region


    :param sigs: which other signals to use
    :param dets: which detector to use
    :param energy: what energy motor to scan
    :return: perform scan

    normal scan takes ~ 7 minutes to complete
    '''
    enscan_type = 'full_Nitrogen_NEXAFS'
    sample()
    if len(read_input("Starting a Nitrogen NEXAFS scan hit enter in the next 3 seconds to abort", "abort", "", 3)) > 0:
        return

    # create a list of energies
    energies = np.arange(385,397,1)
    energies = np.append(energies,np.arange(397,407,.2))
    energies = np.append(energies,np.arange(407,440,1))
    times = energies.copy()

    # Define exposures times for different energy ranges
    # use these energies and exposure times to scan energy and record detectors and signals


    yield from NEXAFS_scan_core(sigs, dets, energy, energies,enscan_type=enscan_type,
                                openshutter=True,diode_range=diode_range,m3_pitch=m3_pitch, pol=pol,
                                open_each_step=open_each_step,exp_time=exp_time,grating=grating,
                                motorname=motorname,offset=offset)
def full_Fluorine_NEXAFS(sigs=[],
                        dets=[Sample_TEY,Izero_Mesh,Beamstop_WAXS], energy=en,pol=0,m3_pitch=7.90,diode_range=7,
                       open_each_step=True,exp_time=1,grating='no change', motorname='None',offset=0):
    '''
    Full Nitrogen Scan runs an RSoXS sample set through the carbon edge, with particular emphasis in he pre edge region


    :param sigs: which other signals to use
    :param dets: which detector to use
    :param energy: what energy motor to scan
    :return: perform scan

    normal scan takes ~ 7 minutes to complete
    '''
    enscan_type = 'full_Fluorine_NEXAFS'
    sample()
    if len(read_input("Starting a Fluorine NEXAFS scan hit enter in the next 3 seconds to abort", "abort", "", 3)) > 0:
        return
    # create a list of energies
    energies = np.arange(680,720,.25)
    times = energies.copy()

    # Define exposures times for different energy ranges
    # use these energies and exposure times to scan energy and record detectors and signals


    yield from NEXAFS_scan_core(sigs, dets, energy, energies,enscan_type=enscan_type,
                                openshutter=True,diode_range=diode_range,m3_pitch=m3_pitch, pol=pol,
                                open_each_step=open_each_step,exp_time=exp_time,grating=grating,
                                motorname=motorname,offset=offset)
def short_Fluorine_NEXAFS(sigs=[],
                        dets=[Sample_TEY,Izero_Mesh,Beamstop_WAXS], energy=en,pol=0,m3_pitch=7.90,diode_range=7,
                       open_each_step=True,exp_time=1,grating='no change', motorname='None',offset=0):
    '''
    Full Nitrogen Scan runs an RSoXS sample set through the carbon edge, with particular emphasis in he pre edge region


    :param sigs: which other signals to use
    :param dets: which detector to use
    :param energy: what energy motor to scan
    :return: perform scan

    normal scan takes ~ 7 minutes to complete
    '''
    enscan_type = 'short_Fluorine_NEXAFS'
    sample()
    if len(read_input("Starting a short Fluorine NEXAFS scan hit enter in the next 3 seconds to abort", "abort", "", 3)) > 0:
        return
    # create a list of energies
    energies = np.arange(680,720,.5)
    times = energies.copy()

    # Define exposures times for different energy ranges
    # use these energies and exposure times to scan energy and record detectors and signals


    yield from NEXAFS_scan_core(sigs, dets, energy, energies,enscan_type=enscan_type,
                                openshutter=True,diode_range=diode_range,m3_pitch=m3_pitch, pol=pol,
                                open_each_step=open_each_step,exp_time=exp_time,grating=grating,
                                motorname=motorname,offset=offset)


def full_Oxygen_NEXAFS(sigs=[],
                        dets=[Sample_TEY,Izero_Mesh,Beamstop_WAXS], energy=en,pol=0,m3_pitch=7.90,diode_range=6,
                       open_each_step=True,exp_time=1,grating='no change', motorname='None',offset=0):
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
    if len(read_input("Starting a Oxygen NEXAFS scan hit enter in the next 3 seconds to abort", "abort", "", 3)) > 0:
        return
    # create a list of energies
    energies = np.arange(510,525,1)
    energies = np.append(energies,np.arange(525,540,.2))
    energies = np.append(energies,np.arange(540,560,1))
    times = energies.copy()

    # Define exposures times for different energy ranges
    # use these energies and exposure times to scan energy and record detectors and signals


    yield from NEXAFS_scan_core(sigs, dets, energy, energies,enscan_type=enscan_type,
                                openshutter=True,diode_range=diode_range,m3_pitch=m3_pitch, pol=pol,
                                open_each_step=open_each_step,exp_time=exp_time,grating=grating,
                                motorname=motorname,offset=offset)

def short_Oxygen_NEXAFS(sigs=[],
                        dets=[Sample_TEY,Izero_Mesh,Beamstop_WAXS], energy=en,pol=0,m3_pitch=7.90,diode_range=6,
                       open_each_step=True,exp_time=1,grating='no change', motorname='None',offset=0):
    '''
    Full Carbon Scan runs an RSoXS sample set through the carbon edge, with particular emphasis in he pre edge region


    :param sigs: which other signals to use
    :param dets: which detector to use
    :param energy: what energy motor to scan
    :return: perform scan

    normal scan takes ~ 7 minutes to complete
    '''
    enscan_type = 'short_Oxygen_NEXAFS'
    sample()
    if len(read_input("Starting a short Oxygen NEXAFS scan hit enter in the next 3 seconds to abort", "abort", "", 3)) > 0:
        return
    # create a list of energies
    energies = np.arange(510,525,1)
    energies = np.append(energies,np.arange(525,540,.4))
    energies = np.append(energies,np.arange(540,560,1))
    times = energies.copy()

    # Define exposures times for different energy ranges
    # use these energies and exposure times to scan energy and record detectors and signals


    yield from NEXAFS_scan_core(sigs, dets, energy, energies,enscan_type=enscan_type,
                                openshutter=True,diode_range=diode_range,m3_pitch=m3_pitch, pol=pol,
                                open_each_step=open_each_step,exp_time=exp_time,grating=grating,
                                motorname=motorname,offset=offset)


def full_Al_NEXAFS(sigs=[],
                        dets=[Sample_TEY,Izero_Mesh,Beamstop_WAXS], energy=en,pol=0,m3_pitch=7.90,diode_range=6,
                       open_each_step=True,exp_time=1,grating='no change', motorname='None',offset=0):
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
    if len(read_input("Starting an Aluminum NEXAFS scan hit enter in the next 3 seconds to abort", "abort", "", 3)) > 0:
        return

    # create a list of energies
    energies = np.arange(1550,1620,.5)

    times = energies.copy()

    # Define exposures times for different energy ranges
    # use these energies and exposure times to scan energy and record detectors and signals


    yield from NEXAFS_scan_core(sigs, dets, energy, energies,enscan_type=enscan_type,
                                openshutter=True,diode_range=diode_range,m3_pitch=m3_pitch, pol=pol,
                                open_each_step=open_each_step,exp_time=exp_time,grating=grating,
                                motorname=motorname,offset=offset)


def full_Zn_NEXAFS(sigs=[],
                        dets=[Sample_TEY,Izero_Mesh,Beamstop_WAXS], energy=en,pol=0,m3_pitch=7.9,diode_range=7,
                       open_each_step=True,exp_time=1,grating='no change', motorname='None',offset=0):
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
    if len(read_input("Starting a Zinc NEXAFS scan hit enter in the next 3 seconds to abort", "abort", "", 3)) > 0:
        return

    # create a list of energies
    energies = np.arange(1000,1070,.5)
    times = energies.copy()

    # Define exposures times for different energy ranges
    # use these energies and exposure times to scan energy and record detectors and signals


    yield from NEXAFS_scan_core(sigs, dets, energy, energies,enscan_type=enscan_type,
                                openshutter=True,diode_range=diode_range,m3_pitch=m3_pitch, pol=pol,
                                open_each_step=open_each_step,exp_time=exp_time,grating=grating,
                                motorname=motorname,offset=offset)


def do_HOPGscans_epu():
    pols = [0,20,40,55,70,90,-1]
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