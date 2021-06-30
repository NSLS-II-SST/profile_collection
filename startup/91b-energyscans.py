run_report(__file__)

import numpy as np
import bluesky.plans as bp
import bluesky.plan_stubs as bps


def full_oxygen_scan_nd(multiple=1,diode_range=6,m3_pitch=7.99,grating='1200',master_plan=None,**kwargs):
    '''
    full_oxygen_scan_nd
    @param multiple: default exposure times is multipled by this
    @param diode_range: integer range for the dilde
    @param m3_pitch: pitch value for M3 for this energy range - check before scans
    @param grating: '1200' high energy or '250' low energy
    @param kwargs: all extra parameters for general scans - see the inputs for en_scan_core
    @return: Do a step scan and take images
    '''
    enscan_type = 'full_oxygen_scan_nd'
    if len(read_input("Starting a Oxygen energy scan hit enter in the next 3 seconds to abort", "abort", "", 3)) > 0:
        return
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
    yield from en_scan_core(energies=energies, times=times,enscan_type=enscan_type,master_plan=master_plan,
                            diode_range=diode_range,m3_pitch=m3_pitch, grating=grating,**kwargs)

def short_oxygen_scan_nd(multiple=1,diode_range=6,m3_pitch=7.98,grating='1200',master_plan=None,**kwargs):
    '''
    short_oxygen_scan_nd
    @param multiple: default exposure times is multipled by this
    @param diode_range: integer range for the dilde
    @param m3_pitch: pitch value for M3 for this energy range - check before scans
    @param grating: '1200' high energy or '250' low energy
    @param kwargs: all extra parameters for general scans - see the inputs for en_scan_core
    @return: Do a step scan and take images
    '''
    enscan_type = 'short_oxygen_scan_nd'
    if len(read_input("Starting a Oxygen energy scan hit enter in the next 3 seconds to abort", "abort", "", 3)) > 0:
        return
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
    yield from en_scan_core(energies=energies, times=times,enscan_type=enscan_type,master_plan=master_plan,
                            diode_range=diode_range,m3_pitch=m3_pitch, grating=grating,**kwargs)


def short_zincl_scan_nd(multiple=1,diode_range=6,m3_pitch=7.98,grating='1200',master_plan=None,**kwargs):
    '''
    short_zincl_scan_nd
    @param multiple: default exposure times is multipled by this
    @param diode_range: integer range for the dilde
    @param m3_pitch: pitch value for M3 for this energy range - check before scans
    @param grating: '1200' high energy or '250' low energy
    @param kwargs: all extra parameters for general scans - see the inputs for en_scan_core
    @return: Do a step scan and take images
    '''
    enscan_type = 'short_zincl_scan_nd'
    if len(read_input("Starting a Zinc energy scan hit enter in the next 3 seconds to abort", "abort", "", 3)) > 0:
        return
    # create a list of energies
    energies = np.arange(1015,1020,1)
    energies = np.append(energies,np.arange(1020,1027,0.5))
    energies = np.append(energies,np.arange(1027,1035,1))
    times = energies.copy()


    times[:] = 2
    times *= multiple

    # use these energies and exposure times to scan energy and record detectors and signals
    yield from en_scan_core(energies=energies, times=times,enscan_type=enscan_type,master_plan=master_plan,
                            diode_range=diode_range,m3_pitch=m3_pitch, grating=grating,**kwargs)



def very_short_oxygen_scan_nd(multiple=1,diode_range=6,m3_pitch=7.97,grating='1200',master_plan=None,**kwargs):
    '''
    very_short_oxygen_scan_nd
    @param multiple: default exposure times is multipled by this
    @param diode_range: integer range for the dilde
    @param m3_pitch: pitch value for M3 for this energy range - check before scans
    @param grating: '1200' high energy or '250' low energy
    @param kwargs: all extra parameters for general scans - see the inputs for en_scan_core
    @return: Do a step scan and take images
    '''
    enscan_type = 'very_short_oxygen_scan_nd'
    if len(read_input("Starting a Oxygen energy scan hit enter in the next 3 seconds to abort", "abort", "", 3)) > 0:
        return
    # create a list of energies
    energies = np.arange(510,525,5)
    energies = np.append(energies,np.arange(525,531,0.5))
    energies = np.append(energies,np.arange(531,535,2))
    energies = np.append(energies,np.arange(535,560,10))
    times = energies.copy()

    # Define exposures times for different energy ranges
    #times[energies<525] = 2
    #times[(energies < 540) & (energies >= 525)] = 5
    #times[energies >= 540] = 2
    times[:] = 2
    times *= multiple

    # use these energies and exposure times to scan energy and record detectors and signals
    yield from en_scan_core(energies=energies, times=times,enscan_type=enscan_type,master_plan=master_plan,
                            diode_range=diode_range,m3_pitch=m3_pitch, grating=grating,**kwargs)



def short_fluorine_scan_nd(multiple=1,diode_range=7,m3_pitch=7.98,grating='1200',master_plan=None,**kwargs):
    '''
    short_fluorine_scan_nd
    @param multiple: default exposure times is multipled by this
    @param diode_range: integer range for the dilde
    @param m3_pitch: pitch value for M3 for this energy range - check before scans
    @param grating: '1200' high energy or '250' low energy
    @param kwargs: all extra parameters for general scans - see the inputs for en_scan_core
    @return: Do a step scan and take images
    '''
    enscan_type = 'short_fluorine_scan_nd'
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
    yield from en_scan_core(energies=energies, times=times,enscan_type=enscan_type,master_plan=master_plan,
                            diode_range=diode_range,m3_pitch=m3_pitch, grating=grating,**kwargs)



def full_nitrogen_scan_nd(multiple=1,diode_range=6,m3_pitch=7.93,grating='1200',master_plan=None,**kwargs):
    '''
    full_nitrogen_scan_nd
    @param multiple: default exposure times is multipled by this
    @param diode_range: integer range for the dilde
    @param m3_pitch: pitch value for M3 for this energy range - check before scans
    @param grating: '1200' high energy or '250' low energy
    @param kwargs: all extra parameters for general scans - see the inputs for en_scan_core
    @return: Do a step scan and take images
    '''
    enscan_type = 'full_nitrogen_scan_nd'
    if len(read_input("Starting a Nitrogen energy scan hit enter in the next 3 seconds to abort", "abort", "", 3)) > 0:
        return
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
    yield from en_scan_core(energies=energies, times=times,enscan_type=enscan_type,master_plan=master_plan,
                            diode_range=diode_range,m3_pitch=m3_pitch, grating=grating,**kwargs)


def short_nitrogen_scan_nd(multiple=1,diode_range=6,m3_pitch=8.00,grating='1200',master_plan=None,**kwargs):
    '''
    short_nitrogen_scan_nd
    @param multiple: default exposure times is multipled by this
    @param diode_range: integer range for the dilde
    @param m3_pitch: pitch value for M3 for this energy range - check before scans
    @param grating: '1200' high energy or '250' low energy
    @param kwargs: all extra parameters for general scans - see the inputs for en_scan_core
    @return: Do a step scan and take images
    '''
    enscan_type='short_nitrogen_scan_nd'
    if len(read_input("Starting a Short Nitrogen energy scan "
                      "hit enter in the next 3 seconds to abort", "abort", "", 3)) > 0:
        return

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
    yield from en_scan_core(energies=energies, times=times,enscan_type=enscan_type,master_plan=master_plan,
                            diode_range=diode_range,m3_pitch=m3_pitch, grating=grating,**kwargs)


def very_short_carbon_scan_nd(multiple=1,diode_range=6,m3_pitch=8.01,grating='1200',master_plan=None,**kwargs):
    '''
    very_short_carbon_scan_nd
    @param multiple: default exposure times is multipled by this
    @param diode_range: integer range for the dilde
    @param m3_pitch: pitch value for M3 for this energy range - check before scans
    @param grating: '1200' high energy or '250' low energy
    @param kwargs: all extra parameters for general scans - see the inputs for en_scan_core
    @return: Do a step scan and take images
    '''
    enscan_type = 'very_short_carbon_scan_nd'
    if len(read_input("Starting a very short Carbon energy scan hit "
                      "enter in the next 3 seconds to abort", "abort", "", 3)) > 0:
        return

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
    times[(energies < 286) & (energies >= 282)] = 2
    times[energies >= 286] = 2
    times *= multiple

    # use these energies and exposure times to scan energy and record detectors and signals
    yield from en_scan_core(energies=energies, times=times,enscan_type=enscan_type,master_plan=master_plan,
                            diode_range=diode_range,m3_pitch=m3_pitch, grating=grating,**kwargs)


def short_carbon_scan_nd(multiple=1,diode_range=6,m3_pitch=8.00,grating='1200',master_plan=None,**kwargs):
    '''
    short_carbon_scan_nd
    @param multiple: default exposure times is multipled by this
    @param diode_range: integer range for the dilde
    @param m3_pitch: pitch value for M3 for this energy range - check before scans
    @param grating: '1200' high energy or '250' low energy
    @param kwargs: all extra parameters for general scans - see the inputs for en_scan_core
    @return: Do a step scan and take images
    '''
    enscan_type = 'short_carbon_scan_nd'
    if len(read_input("Starting a short Carbon energy scan hit enter in "
                      "the next 3 seconds to abort", "abort", "", 3)) > 0:
        return

    # create a list of energies
    energies = np.arange(270,282,2)
    energies = np.append(energies,np.arange(282,286,.25))
    energies = np.append(energies,np.arange(286,292,.5))
    energies = np.append(energies,np.arange(292,306,1))
    energies = np.append(energies,np.arange(306,320,4))
    energies = np.append(energies,np.arange(320,350,10))
    times = energies.copy()

    # Define exposures times for different energy ranges
    times[energies<282] = 2
    times[(energies < 286) & (energies >= 282)] = 2
    times[energies >= 286] = 2
    times *= multiple

    # use these energies and exposure times to scan energy and record detectors and signals
    yield from en_scan_core(energies=energies, times=times,enscan_type=enscan_type,master_plan=master_plan,
                            diode_range=diode_range,m3_pitch=m3_pitch, grating=grating,**kwargs)

def short_carbon_scan_nonaromatic(multiple=1,diode_range=6,m3_pitch=8.00,grating='1200',master_plan=None,**kwargs):
    '''
    short_carbon_scan_nonaromatic
    @param multiple: default exposure times is multipled by this
    @param diode_range: integer range for the dilde
    @param m3_pitch: pitch value for M3 for this energy range - check before scans
    @param grating: '1200' high energy or '250' low energy
    @param kwargs: all extra parameters for general scans - see the inputs for en_scan_core
    @return: Do a step scan and take images
    '''
    enscan_type = 'short_carbon_scan_nonaromatic'
    if len(read_input("Starting a short Carbon energy scan hit enter in "
                      "the next 3 seconds to abort", "abort", "", 3)) > 0:
        return

    # create a list of energies
    energies = np.arange(270,282,2)
    energies = np.append(energies,np.arange(282,286,.5))
    energies = np.append(energies,np.arange(286,290,.25))
    energies = np.append(energies,np.arange(290,292,.5))
    energies = np.append(energies,np.arange(292,306,1))
    energies = np.append(energies,np.arange(306,320,4))
    energies = np.append(energies,np.arange(320,350,10))
    times = energies.copy()

    # Define exposures times for different energy ranges
    times[energies<282] = 2
    times[(energies < 286) & (energies >= 282)] = 2
    times[energies >= 286] = 2
    times *= multiple

    # use these energies and exposure times to scan energy and record detectors and signals
    yield from en_scan_core(energies=energies, times=times,enscan_type=enscan_type,master_plan=master_plan,
                            diode_range=diode_range,m3_pitch=m3_pitch, grating=grating,**kwargs)


def custom_rsoxs_scan(energies=[((270,340,1),2)],plan_name='custom_rsoxs_scan',master_plan=None,
                      diode_range=6,m3_pitch=8.00,grating='1200',**kwargs):
    '''
    custom_rsoxs_scan
    @param multiple: default exposure times is multipled by this
    @param diode_range: integer range for the dilde
    @param m3_pitch: pitch value for M3 for this energy range - check before scans
    @param grating: '1200' high energy or '250' low energy
    @param kwargs: all extra parameters for general scans - see the inputs for en_scan_core
    @return: Do a step scan and take images
    '''

    
    enscan_type = plan_name
    newenergies = []
    newtimes = []
    if len(read_input("Starting a specified energy scan hit enter in "
                      "the next 3 seconds to abort", "abort", "", 3)) > 0:
        return
    for ((start,stop,step),exp) in energies:
        tempenergies =  np.arange(start, stop, step)
        newenergies = np.append(newenergies, tempenergies)
        temptimes =  tempenergies.copy()
        temptimes[:] = exp
        newtimes = np.append(newtimes,temptimes)
        

    yield from en_scan_core(energies=newenergies,times=newtimes,enscan_type=enscan_type,master_plan=master_plan,
                            diode_range=diode_range,m3_pitch=m3_pitch, grating=grating,**kwargs)



def short_sulfurl_scan_nd(multiple=1,diode_range=6,m3_pitch=8.02,grating='1200',master_plan=None,**kwargs):
    '''
    short_sulfurl_scan_nd
    @param multiple: default exposure times is multipled by this
    @param diode_range: integer range for the dilde
    @param m3_pitch: pitch value for M3 for this energy range - check before scans
    @param grating: '1200' high energy or '250' low energy
    @param kwargs: all extra parameters for general scans - see the inputs for en_scan_core
    @return: Do a step scan and take images
    '''
    enscan_type = 'short_sulfurl_scan_nd'
    if len(read_input("Starting a short Sulfur L energy scan hit enter in "
                      "the next 3 seconds to abort", "abort", "", 3)) > 0:
        return

    #Oct 2019, this pitch value seems to be optimal for carbon

    # create a list of energies
    energies = np.arange(150,160,1)
    energies = np.append(energies,np.arange(160,170,.25))
    energies = np.append(energies,np.arange(170,200,1))
    times = energies.copy()

    # Define exposures times for different energy ranges
    times[energies < 170] = 2
    times[energies >= 170] = 2
    times *= multiple

    # use these energies and exposure times to scan energy and record detectors and signals
    yield from en_scan_core(energies=energies, times=times,enscan_type=enscan_type,master_plan=master_plan,
                            diode_range=diode_range,m3_pitch=m3_pitch, grating=grating,**kwargs)



def focused_carbon_scan_nd(multiple=1,diode_range=6,m3_pitch=7.93,grating='1200',master_plan=None,**kwargs):
    '''
    focused_carbon_scan_nd
    @param multiple: default exposure times is multipled by this
    @param diode_range: integer range for the dilde
    @param m3_pitch: pitch value for M3 for this energy range - check before scans
    @param grating: '1200' high energy or '250' low energy
    @param kwargs: all extra parameters for general scans - see the inputs for en_scan_core
    @return: Do a step scan and take images
    '''
    enscan_type = 'focused_carbon_scan_nd'
    if len(read_input("Starting a short Carbon energy scan hit enter in "
                      "the next 3 seconds to abort", "abort", "", 3)) > 0:
        return


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
    yield from en_scan_core(energies=energies, times=times,enscan_type=enscan_type,master_plan=master_plan,
                            diode_range=diode_range,m3_pitch=m3_pitch, grating=grating,**kwargs)


def g_carbon_scan_nd(multiple=1,diode_range=6,m3_pitch=7.93,grating='1200',master_plan=None,**kwargs):
    '''
    g_carbon_scan_nd
    @param multiple: default exposure times is multipled by this
    @param diode_range: integer range for the dilde
    @param m3_pitch: pitch value for M3 for this energy range - check before scans
    @param grating: '1200' high energy or '250' low energy
    @param kwargs: all extra parameters for general scans - see the inputs for en_scan_core
    @return: Do a step scan and take images
    '''
    enscan_type = 'g_carbon_scan_nd'
    if len(read_input("Starting a Carbon energy scan hit enter in the next 3 seconds to abort", "abort", "", 3)) > 0:
        return
    # create a list of energies
    energies = np.array([270,283.5,284.75,285.2,286.5])
    times = energies.copy()

    # Define exposures times for different energy ranges
    times[energies<2820] = 5
    times *= multiple

    # use these energies and exposure times to scan energy and record detectors and signals
    yield from en_scan_core(energies=energies, times=times,enscan_type=enscan_type,master_plan=master_plan,
                            diode_range=diode_range,m3_pitch=m3_pitch, grating=grating,**kwargs)


def t_carbon_scan_nd(multiple=1,diode_range=6,m3_pitch=7.93,grating='1200',master_plan=None,**kwargs):
    '''
    t_carbon_scan_nd
    @param multiple: default exposure times is multipled by this
    @param diode_range: integer range for the dilde
    @param m3_pitch: pitch value for M3 for this energy range - check before scans
    @param grating: '1200' high energy or '250' low energy
    @param kwargs: all extra parameters for general scans - see the inputs for en_scan_core
    @return: Do a step scan and take images
    '''
    enscan_type = 't_carbon_scan_nd'
    if len(read_input("Starting a Carbon energy scan hit enter in the next 3 seconds to abort", "abort", "", 3)) > 0:
        return
    # create a list of energies
    energies = np.array([270,283,284.3,284.9,285.5,286,286.5,287])
    times = energies.copy()

    # Define exposures times for different energy ranges
    times[energies<2820] = 5
    times *= multiple

    # use these energies and exposure times to scan energy and record detectors and signals
    yield from en_scan_core(energies=energies, times=times,enscan_type=enscan_type,master_plan=master_plan,
                            diode_range=diode_range,m3_pitch=m3_pitch, grating=grating,**kwargs)


def sufficient_carbon_scan_nd(multiple=1,diode_range=6,m3_pitch=7.96,grating='1200',master_plan=None,**kwargs):
    '''
    sufficient_carbon_scan_nd
    @param multiple: default exposure times is multipled by this
    @param diode_range: integer range for the dilde
    @param m3_pitch: pitch value for M3 for this energy range - check before scans
    @param grating: '1200' high energy or '250' low energy
    @param kwargs: all extra parameters for general scans - see the inputs for en_scan_core
    @return: Do a step scan and take images
    '''
    enscan_type = 'sufficient_carbon_scan_nd'
    if len(read_input("Starting a Carbon energy scan hit enter in the next 3 seconds to abort", "abort", "", 3)) > 0:
        return
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
    yield from en_scan_core(energies=energies, times=times,enscan_type=enscan_type,master_plan=master_plan,
                            diode_range=diode_range,m3_pitch=m3_pitch, grating=grating,**kwargs)



def picky_carbon_scan_nd(multiple=1,diode_range=6,m3_pitch=7.93,grating='1200',master_plan=None,**kwargs):
    '''
    picky_carbon_scan_nd
    @param multiple: default exposure times is multipled by this
    @param diode_range: integer range for the dilde
    @param m3_pitch: pitch value for M3 for this energy range - check before scans
    @param grating: '1200' high energy or '250' low energy
    @param kwargs: all extra parameters for general scans - see the inputs for en_scan_core
    @return: Do a step scan and take images
    '''
    enscan_type = 'picky_carbon_scan_nd'
    if len(read_input("Starting a Carbon energy scan hit enter in the next 3 seconds to abort", "abort", "", 3)) > 0:
        return
    yield from bps.abs_set(mir3.Pitch,7.96,wait=True)
    # create a list of energies
    energies = np.arange(270,285,1)
    times = energies.copy()

    # Define exposures times for different energy ranges
    times[energies<2820] = 1
    times *= multiple

    # use these energies and exposure times to scan energy and record detectors and signals
    yield from en_scan_core(energies=energies, times=times,enscan_type=enscan_type,master_plan=master_plan,
                            diode_range=diode_range,m3_pitch=m3_pitch, grating=grating,**kwargs)



def full_carbon_scan_nd(multiple=1,diode_range=6,m3_pitch=8.00,grating='1200',master_plan=None,**kwargs):
    '''
    full_carbon_scan_nd
    @param multiple: default exposure times is multipled by this
    @param diode_range: integer range for the dilde
    @param m3_pitch: pitch value for M3 for this energy range - check before scans
    @param grating: '1200' high energy or '250' low energy
    @param kwargs: all extra parameters for general scans - see the inputs for en_scan_core
    @return: Do a step scan and take images
    '''
    enscan_type = 'full_carbon_scan_nd'
    if len(read_input("Starting a Carbon energy scan hit enter in the next 3 seconds to abort", "abort", "", 3)) > 0:
        return
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
    times[(energies < 286) & (energies >= 282)] = 2
    times[energies >= 286] = 2
    times *= multiple

    # use these energies and exposure times to scan energy and record detectors and signals
    yield from en_scan_core(energies=energies, times=times,enscan_type=enscan_type,master_plan=master_plan,
                            diode_range=diode_range,m3_pitch=m3_pitch, grating=grating,**kwargs)


def full_carbon_scan_nonaromatic(multiple=1,diode_range=6,m3_pitch=7.97,grating='1200',master_plan=None,**kwargs):
    '''
    full_carbon_scan_nonaromatic
    @param multiple: default exposure times is multipled by this
    @param diode_range: integer range for the dilde
    @param m3_pitch: pitch value for M3 for this energy range - check before scans
    @param grating: '1200' high energy or '250' low energy
    @param kwargs: all extra parameters for general scans - see the inputs for en_scan_core
    @return: Do a step scan and take images
    '''
    enscan_type = 'full_carbon_scan_nonaromatic'
    if len(read_input("Starting a Carbon energy scan hit enter in the next 3 seconds to abort", "abort", "", 3)) > 0:
        return
    # create a list of energies
    energies = np.arange(270,282,.5)
    energies = np.append(energies,np.arange(282,286,.2))
    energies = np.append(energies,np.arange(286,292,.1))
    energies = np.append(energies,np.arange(292,305,1))
    energies = np.append(energies,np.arange(305,320,2))
    energies = np.append(energies,np.arange(320,350,5))
    times = energies.copy()

    # Define exposures times for different energy ranges
    times[energies<282] = 2
    times[(energies < 286) & (energies >= 282)] = 2
    times[energies >= 286] = 2
    times *= multiple

    # use these energies and exposure times to scan energy and record detectors and signals
    yield from en_scan_core(energies=energies, times=times,enscan_type=enscan_type,master_plan=master_plan,
                            diode_range=diode_range,m3_pitch=m3_pitch, grating=grating,**kwargs)


def full_fluorine_scan_nd(multiple=1,diode_range=7,m3_pitch=7.89,grating='1200',master_plan=None,**kwargs):
    '''
    full_fluorine_scan_nd
    @param multiple: default exposure times is multipled by this
    @param diode_range: integer range for the dilde
    @param m3_pitch: pitch value for M3 for this energy range - check before scans
    @param grating: '1200' high energy or '250' low energy
    @param kwargs: all extra parameters for general scans - see the inputs for en_scan_core
    @return: Do a step scan and take images
    '''
    enscan_type = 'full_fluorine_scan_nd'
    if len(read_input("Starting a Fluorine energy scan hit enter in the next 3 seconds to abort", "abort", "", 3)) > 0:
        return
    # create a list of energies
    energies = np.arange(680,720.25,.25)
    times = energies.copy()

    # Define exposures times for different energy ranges
    times[energies<282] = 2
    times[(energies < 286) & (energies >= 282)] = 2
    times[energies >= 286] = 2
    times *= multiple

    # use these energies and exposure times to scan energy and record detectors and signals
    yield from en_scan_core(energies=energies, times=times,enscan_type=enscan_type,master_plan=master_plan,
                            diode_range=diode_range,m3_pitch=m3_pitch, grating=grating,**kwargs)

def veryshort_fluorine_scan_nd(multiple=1,diode_range=7,m3_pitch=7.99,grating='1200',master_plan=None,**kwargs):
    '''
    veryshort_fluorine_scan_nd
    @param multiple: default exposure times is multipled by this
    @param diode_range: integer range for the dilde
    @param m3_pitch: pitch value for M3 for this energy range - check before scans
    @param grating: '1200' high energy or '250' low energy
    @param kwargs: all extra parameters for general scans - see the inputs for en_scan_core
    @return: Do a step scan and take images
    '''
    enscan_type = 'veryshort_fluorine_scan_nd'
    if len(read_input("Starting a Fluorine energy scan hit enter in the next 3 seconds to abort", "abort", "", 3)) > 0:
        return
    # create a list of energies
    energies = np.arange(680,700,1)
    energies = np.append(energies,np.arange(700,720.5,5))
    times = energies.copy()

    # Define exposures times for different energy ranges
    times[energies<282] = 2
    times[(energies < 286) & (energies >= 282)] = 2
    times[energies >= 286] = 2
    times *= multiple

    # use these energies and exposure times to scan energy and record detectors and signals
    yield from en_scan_core(energies=energies, times=times,enscan_type=enscan_type,master_plan=master_plan,
                            diode_range=diode_range,m3_pitch=m3_pitch, grating=grating,**kwargs)


def full_ca_scan_nd(multiple=1,diode_range=6,m3_pitch=8.00,grating='1200',master_plan=None,**kwargs):
    '''
    full_ca_scan_nd
    @param multiple: default exposure times is multipled by this
    @param diode_range: integer range for the dilde
    @param m3_pitch: pitch value for M3 for this energy range - check before scans
    @param grating: '1200' high energy or '250' low energy
    @param kwargs: all extra parameters for general scans - see the inputs for en_scan_core
    @return: Do a step scan and take images
    '''
    if len(read_input("Starting a Calcium energy scan hit enter in the next 3 seconds to abort", "abort", "", 3)) > 0:
        return
    enscan_type = 'full_ca_scan_nd'
    # create a list of energies
    energies = np.arange(320,340,5)
    energies = np.append(energies,np.arange(340,345,1))
    energies = np.append(energies,np.arange(345,355,.5))
    energies = np.append(energies,np.arange(355,360,1))
    times = energies.copy()

    # Define exposures times for different energy ranges
    times[energies<400] = 3
    times *= multiple

    # use these energies and exposure times to scan energy and record detectors and signals
    yield from en_scan_core(energies=energies, times=times,enscan_type=enscan_type,master_plan=master_plan,
                            diode_range=diode_range,m3_pitch=m3_pitch, grating=grating,**kwargs)


def short_calcium_scan_nd(multiple=1,diode_range=6,m3_pitch=8.00,grating='1200',master_plan=None,**kwargs):
    '''
    short_calcium_scan_nd
    @param multiple: default exposure times is multipled by this
    @param diode_range: integer range for the dilde
    @param m3_pitch: pitch value for M3 for this energy range - check before scans
    @param grating: '1200' high energy or '250' low energy
    @param kwargs: all extra parameters for general scans - see the inputs for en_scan_core
    @return: Do a step scan and take images
    '''
    if len(read_input("Starting a Calcium energy scan hit enter in the next 3 seconds to abort", "abort", "", 3)) > 0:
        return
    enscan_type = 'short_calcium_scan_nd'
    # create a list of energies
    energies = np.arange(320,340,5)
    energies = np.append(energies,np.arange(340,345,1))
    energies = np.append(energies,np.arange(345,355,.5))
    times = energies.copy()

    # Define exposures times for different energy ranges
    times[energies<400] = 2
    times *= multiple

    # use these energies and exposure times to scan energy and record detectors and signals
    yield from en_scan_core(energies=energies, times=times,enscan_type=enscan_type,master_plan=master_plan,
                            diode_range=diode_range,m3_pitch=m3_pitch, grating=grating,**kwargs)



def full_carbon_calcium_scan_nd(multiple=1,diode_range=6,m3_pitch=7.96,grating='1200',master_plan=None,**kwargs):
    '''
    full_carbon_calcium_scan_nd
    @param multiple: default exposure times is multipled by this
    @param diode_range: integer range for the dilde
    @param m3_pitch: pitch value for M3 for this energy range - check before scans
    @param grating: '1200' high energy or '250' low energy
    @param kwargs: all extra parameters for general scans - see the inputs for en_scan_core
    @return: Do a step scan and take images
    '''
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
    yield from en_scan_core(energies=energies, times=times,enscan_type=enscan_type,master_plan=master_plan,
                            diode_range=diode_range,m3_pitch=m3_pitch, grating=grating,**kwargs)

def survey_scan_verylowenergy(multiple=1,diode_range=7,m3_pitch=7.93,grating='250',master_plan=None,**kwargs):
    '''
    survey_scan_verylowenergy
    @param multiple: default exposure times is multipled by this
    @param diode_range: integer range for the dilde
    @param m3_pitch: pitch value for M3 for this energy range - check before scans
    @param grating: '1200' high energy or '250' low energy
    @param kwargs: all extra parameters for general scans - see the inputs for en_scan_core
    @return: Do a step scan and take images
    '''
    enscan_type = 'survey_scan_verylowenergy'
    if len(read_input("Starting a low energy survey scan hit enter in the next 3 seconds to abort", "abort", "", 3)) > 0:
        return
    # create a list of energies
    energies = np.arange(70.0,260.0,1.0)
    times = energies.copy()

    # Define exposures times for different energy ranges
    times[:] = 2.0
    times *= multiple

    # use these energies and exposure times to scan energy and record detectors and signals
    yield from en_scan_core(energies=energies, times=times,enscan_type=enscan_type,master_plan=master_plan,
                            diode_range=diode_range,m3_pitch=m3_pitch, grating=grating,**kwargs)



def survey_scan_lowenergy(multiple=1,diode_range=7,m3_pitch=7.91,grating='1200',master_plan=None,**kwargs):
    '''
    survey_scan_lowenergy
    @param multiple: default exposure times is multipled by this
    @param diode_range: integer range for the dilde
    @param m3_pitch: pitch value for M3 for this energy range - check before scans
    @param grating: '1200' high energy or '250' low energy
    @param kwargs: all extra parameters for general scans - see the inputs for en_scan_core
    @return: Do a step scan and take images
    '''
    enscan_type = 'survey_scan_lowenergy'
    if len(read_input("Starting a Low energy survey scan hit enter in the next 3 seconds to abort", "abort", "", 3)) > 0:
        return
    # create a list of energies
    energies = np.arange(240.0,500,2.0)
    times = energies.copy()

    # Define exposures times for different energy ranges
    times[:] = 2.0
    times *= multiple

    # use these energies and exposure times to scan energy and record detectors and signals
    yield from en_scan_core(energies=energies, times=times,enscan_type=enscan_type,master_plan=master_plan,
                            diode_range=diode_range,m3_pitch=m3_pitch, grating=grating,**kwargs)



def survey_scan_highenergy(multiple=1,diode_range=7,m3_pitch=7.89,grating='1200',master_plan=None,**kwargs):
    '''
    survey_scan_highenergy
    @param multiple: default exposure times is multipled by this
    @param diode_range: integer range for the dilde
    @param m3_pitch: pitch value for M3 for this energy range - check before scans
    @param grating: '1200' high energy or '250' low energy
    @param kwargs: all extra parameters for general scans - see the inputs for en_scan_core
    @return: Do a step scan and take images
    '''
    enscan_type = 'survey_scan_highenergy'
    if len(read_input("Starting a High energy survey scan hit enter in the next 3 seconds to abort", "abort", "", 3)) > 0:
        return
    # create a list of energies
    energies = np.arange(400.0,1200,5.0)
    times = energies.copy()

    # Define exposures times for different energy ranges
    times[:] = 2.0
    times *= multiple

    # use these energies and exposure times to scan energy and record detectors and signals
    yield from en_scan_core(energies=energies, times=times,enscan_type=enscan_type,master_plan=master_plan,
                            diode_range=diode_range,m3_pitch=m3_pitch, grating=grating,**kwargs)


def survey_scan_veryhighenergy(multiple=1,diode_range=7,m3_pitch=7.89,grating='1200',master_plan=None,**kwargs):
    '''
    survey_scan_veryhighenergy
    @param multiple: default exposure times is multipled by this
    @param diode_range: integer range for the dilde
    @param m3_pitch: pitch value for M3 for this energy range - check before scans
    @param grating: '1200' high energy or '250' low energy
    @param kwargs: all extra parameters for general scans - see the inputs for en_scan_core
    @return: Do a step scan and take images
    '''
    enscan_type = 'survey_scan_veryhighenergy'
    if len(read_input("Starting a Very High energy survey scan hit enter in the next 3 seconds to abort", "abort", "", 3)) > 0:
        return
    # create a list of energies
    energies = np.arange(1200.0,2030,10.0)
    times = energies.copy()

    # Define exposures times for different energy ranges
    times[:] = 2.0
    times *= multiple

    # use these energies and exposure times to scan energy and record detectors and signals
    yield from en_scan_core(energies=energies, times=times,enscan_type=enscan_type,master_plan=master_plan,
                            diode_range=diode_range,m3_pitch=m3_pitch, grating=grating,**kwargs)



def cdsaxs_scan(energies=[(250,2),(270,2),(280,2),(285,2),(300,2)],
                angles=(-60,61,2),plan_name='cdsaxs_single',master_plan='cdsaxs_scan',
                diode_range=6,m3_pitch=8.00,grating='1200',**kwargs):
    '''
    custom_rsoxs_scan
    @param multiple: default exposure times is multipled by this
    @param energies: list of touples of energy, exposure time
    @param angles: list of angles.  at each angle, the energy list will be collected
    @param diode_range: integer range for the dilde
    @param m3_pitch: pitch value for M3 for this energy range - check before scans
    @param grating: '1200' high energy or '250' low energy
    @param kwargs: all extra parameters for general scans - see the inputs for en_scan_core
    @return: Do a step scan and take images
    '''

    enscan_type = plan_name
    newenergies = []
    newtimes = []
    if len(read_input("Starting a CD-SAXS energy,angle scan hit enter in "
                      "the next 3 seconds to abort", "abort", "", 3)) > 0:
        return
    for (energy,exp) in energies:
        newenergies.append(energy)
        newtimes.append(exp)

    for angle in np.arange(*angles):
        yield from rotate_now(angle,force=True)
        yield from en_scan_core(energies=newenergies,times=newtimes,enscan_type=enscan_type,master_plan=master_plan,
                                diode_range=diode_range,m3_pitch=m3_pitch, grating=grating,**kwargs)

