run_report(__file__)

from ophyd import PVPositioner, EpicsSignalRO, PseudoPositioner, PseudoSingle, EpicsMotor, EpicsSignal
from ophyd import Component as Cpt
from ophyd.pseudopos import (pseudo_position_argument,
                             real_position_argument)
from IPython.core.magic import register_line_magic


class UndulatorMotor(EpicsMotor):
    user_setpoint = Cpt(EpicsSignal, '-SP', limits=True)

#epu_gap = UndulatorMotor('SR:C07-ID:G1A{SST1:1-Ax:Gap}-Mtr', name='EPU 60 Gap',kind='normal')
#epu_phase = UndulatorMotor('SR:C07-ID:G1A{SST1:1-Ax:Phase}-Mtr', name='EPU 60 Phase',kind='normal')



# epu_mode = EpicsSignal('SR:C07-ID:G1A{SST1:1-Ax:Phase}Phs:Mode-RB',
#                        write_pv='SR:C07-ID:G1A{SST1:1-Ax:Phase}Phs:Mode-SP',
#                        name='EPU 60 Mode',kind='normal')

epu_mode = EpicsSignal('SR:C07-ID:G1A{SST1:1-Ax:Phase}Phs:Mode-SP',
                        name='EPU 60 Mode',kind='normal')


class Monochromator(PVPositioner):
    setpoint = Cpt(EpicsSignal,':ENERGY_SP', kind='normal', write_timeout=180.)
    value = Cpt(EpicsSignalRO, ':ENERGY_MON',kind='hinted')
    readback = Cpt(EpicsSignalRO, ':ENERGY_MON',kind='hinted')

    grating = Cpt(prettymotor, 'GrtP}Mtr', name="Mono Grating", kind='normal')
    mirror2 = Cpt(prettymotor, 'MirP}Mtr', name="Mono Mirror", kind='normal')
    cff = Cpt(EpicsSignal, ':CFF_SP', name="Mono CFF", kind='normal')
    vls = Cpt(EpicsSignal, ':VLS_B2.A', name="Mono CFF", kind='normal')
    gratingtype = Cpt(EpicsSignal, 'GrtX}Mtr_TYPE_MON', string=True, write_pv='GrtX}Mtr_TYPE_SP',
                      name="Mono Grating Type", kind='normal')

    gratingtype_proc = Cpt(EpicsSignal, 'GrtX}Mtr_DCPL_CALC.PROC',name="Mono Grating Type_proc", kind='omitted')
    mirror2type = Cpt(EpicsSignal, 'MirX}Mtr_TYPE_MON', write_pv='MirX}Mtr_TYPE_SP', name="Mono Mirror Type",
                      kind='normal')
    gratingx = Cpt(prettymotor, 'GrtX}Mtr', name="Mono Grating X motor",
                      kind='normal')
    mirror2x = Cpt(prettymotor, 'MirX}Mtr', name="Mono Mirror X motor",
                      kind='normal')

    done = Cpt(EpicsSignalRO, ':ERDY_STS')
    done_value = 1
    stop_signal = Cpt(EpicsSignal, ':ENERGY_ST_CMD')

# mono_en= Monochromator('XF:07ID1-OP{Mono:PGM1-Ax:', name='Monochromator Energy',kind='normal')

from scipy import interpolate
#energies = {270,280,400}
#phases = {0,4000,20000}
#gaps = {20000,24000,50000}
#gapinterp = interpolate.interp2d(energies, phases, gaps, kind='cubic',bounds_error=True)

def epugap_from_energy_old(energy):
    '''
    this version is using values from April 27 valid from 150 eV through 1500 eV for First Harmonic
    '''
    if energy >= 1100:
        enoff = energy - 370.01
        gap = (enoff ** 0) * 22833.87619739154 + \
              (enoff ** 1) * 29.68655012463454 + \
              (enoff ** 2) * -0.03210984163384775 + \
              (enoff ** 3) * 4.980917046937771e-05 + \
              (enoff ** 4) * -6.396452510943625e-08 + \
              (enoff ** 5) * 5.991083149692317e-11 + \
              (enoff ** 6) * -3.812842880047685e-14 + \
              (enoff ** 7) * 1.623556090541289e-17 + \
              (enoff ** 8) * -4.365835230578085e-21 + \
              (enoff ** 9) * 5.739408834109368e-25

    else:
        enoff = energy - 150
        gap = (enoff ** 0) * 20569.54179105347 + \
              (enoff ** 1) * 65.67661627149975 + \
              (enoff ** 2) * -0.07680907134551485 + \
              (enoff ** 3) * -0.0003134086632392047 + \
              (enoff ** 4) * 2.407905301445676e-06 + \
              (enoff ** 5) * -6.827469033291375e-09 + \
              (enoff ** 6) * 1.045015423402126e-11 + \
              (enoff ** 7) * -9.027454042580941e-15 + \
              (enoff ** 8) * 4.135706733331245e-18 + \
              (enoff ** 9) * -7.796287724230847e-22
    return gap


def epugap_from_en_pol(energy,polarization):
    gap=None
    if polarization == 190: # vertical polarization (29500 phase)
        if 145.212 <= energy < 1100:
            enoff = energy - 145.212
            gap = (enoff ** 0) * 14012.9679723399 + \
                  (enoff ** 1) * 50.90077784479197 + \
                  (enoff ** 2) * -0.151128059295173 + \
                  (enoff ** 3) * 0.0007380466942855418 + \
                  (enoff ** 4) * -2.88796126025716e-06 + \
                  (enoff ** 5) * 7.334088791503296e-09 + \
                  (enoff ** 6) * -1.138174337292876e-11 + \
                  (enoff ** 7) * 1.043317214147193e-14 + \
                  (enoff ** 8) * -5.190019656736424e-18 + \
                  (enoff ** 9) * 1.081963010325867e-21
        elif 1100 <= energy < 2200: # third harmonic
            enoff = (energy/3) - 145.212
            gap = (enoff ** 0) * 14012.9679723399 + \
                  (enoff ** 1) * 50.90077784479197 + \
                  (enoff ** 2) * -0.151128059295173 + \
                  (enoff ** 3) * 0.0007380466942855418 + \
                  (enoff ** 4) * -2.88796126025716e-06 + \
                  (enoff ** 5) * 7.334088791503296e-09 + \
                  (enoff ** 6) * -1.138174337292876e-11 + \
                  (enoff ** 7) * 1.043317214147193e-14 + \
                  (enoff ** 8) * -5.190019656736424e-18 + \
                  (enoff ** 9) * 1.081963010325867e-21
        else:
            gap= None

    elif polarization == 126: # 26000 phase

        if 159.381 <= energy < 1100:
            enoff = energy - 159.381
            gap = (enoff ** 0) * 14016.21086765142 + \
                  (enoff ** 1) * 47.07181476458327 + \
                  (enoff ** 2) * -0.1300551161025656 + \
                  (enoff ** 3) * 0.0006150285348211382 + \
                  (enoff ** 4) * -2.293881944658508e-06 + \
                  (enoff ** 5) * 5.587375098889097e-09 + \
                  (enoff ** 6) * -8.43630153398218e-12 + \
                  (enoff ** 7) * 7.633856981759912e-15 + \
                  (enoff ** 8) * -3.794296038862279e-18 + \
                  (enoff ** 9) * 7.983637046811202e-22
        elif 1100 <= energy < 2200: # third harmonic
            enoff = (energy/3) - 159.381
            gap = (enoff ** 0) * 14016.21086765142 + \
                  (enoff ** 1) * 47.07181476458327 + \
                  (enoff ** 2) * -0.1300551161025656 + \
                  (enoff ** 3) * 0.0006150285348211382 + \
                  (enoff ** 4) * -2.293881944658508e-06 + \
                  (enoff ** 5) * 5.587375098889097e-09 + \
                  (enoff ** 6) * -8.43630153398218e-12 + \
                  (enoff ** 7) * 7.633856981759912e-15 + \
                  (enoff ** 8) * -3.794296038862279e-18 + \
                  (enoff ** 9) * 7.983637046811202e-22
        else:
            gap= None
    elif polarization == 123: # 23000 phase

        if 182.5 <= energy < 1100:
            enoff = energy - 182.5
            gap = (enoff ** 0) * 14003.31346237464 + \
                  (enoff ** 1) * 40.94577604418467 + \
                  (enoff ** 2) * -0.06267710555062726 + \
                  (enoff ** 3) * 0.0001737842192174001 + \
                  (enoff ** 4) * -7.357701847539232e-07 + \
                  (enoff ** 5) * 2.558819479531793e-09 + \
                  (enoff ** 6) * -5.240182651164082e-12 + \
                  (enoff ** 7) * 6.024494955600835e-15 + \
                  (enoff ** 8) * -3.616738308743303e-18 + \
                  (enoff ** 9) * 8.848652101678885e-22
        elif 1100 <= energy < 2200: # third harmonic
            enoff = (energy/3) - 182.5
            gap = (enoff ** 0) * 14003.31346237464 + \
                  (enoff ** 1) * 40.94577604418467 + \
                  (enoff ** 2) * -0.06267710555062726 + \
                  (enoff ** 3) * 0.0001737842192174001 + \
                  (enoff ** 4) * -7.357701847539232e-07 + \
                  (enoff ** 5) * 2.558819479531793e-09 + \
                  (enoff ** 6) * -5.240182651164082e-12 + \
                  (enoff ** 7) * 6.024494955600835e-15 + \
                  (enoff ** 8) * -3.616738308743303e-18 + \
                  (enoff ** 9) * 8.848652101678885e-22
        else:
            gap= None
    elif polarization == 121: # 21000 phase

        if 198.751 <= energy < 1100:
            enoff = energy - 198.751
            gap = (enoff ** 0) * 14036.87876588605 + \
                  (enoff ** 1) * 36.26534721487319 + \
                  (enoff ** 2) * -0.02493769623114209 + \
                  (enoff ** 3) * 7.394536103134409e-05 + \
                  (enoff ** 4) * -7.431387500375352e-07 + \
                  (enoff ** 5) * 3.111643242754014e-09 + \
                  (enoff ** 6) * -6.397457929818655e-12 + \
                  (enoff ** 7) * 7.103146460443289e-15 + \
                  (enoff ** 8) * -4.1024632494443e-18 + \
                  (enoff ** 9) * 9.715673261754361e-22
        elif 1100 <= energy < 2200: # third harmonic
            enoff = (energy/3) - 198.751
            gap = (enoff ** 0) * 14036.87876588605 + \
                  (enoff ** 1) * 36.26534721487319 + \
                  (enoff ** 2) * -0.02493769623114209 + \
                  (enoff ** 3) * 7.394536103134409e-05 + \
                  (enoff ** 4) * -7.431387500375352e-07 + \
                  (enoff ** 5) * 3.111643242754014e-09 + \
                  (enoff ** 6) * -6.397457929818655e-12 + \
                  (enoff ** 7) * 7.103146460443289e-15 + \
                  (enoff ** 8) * -4.1024632494443e-18 + \
                  (enoff ** 9) * 9.715673261754361e-22
        else:
            gap= None
    elif polarization == 118: # 18000 phase
        if 207.503 <= energy < 1100:
            enoff = energy - 207.503
            gap = (enoff ** 0) * 14026.99244058688 + \
                  (enoff ** 1) * 41.45793369967348 + \
                  (enoff ** 2) * -0.05393526187293287 + \
                  (enoff ** 3) * 0.000143951535786684 + \
                  (enoff ** 4) * -3.934262835746608e-07 + \
                  (enoff ** 5) * 6.627045869131144e-10 + \
                  (enoff ** 6) * -4.544338541442881e-13 + \
                  (enoff ** 7) * -8.922084434570775e-17 + \
                  (enoff ** 8) * 2.598052818031009e-19 + \
                  (enoff ** 9) * -8.57226301371417e-23
        elif 1100 <= energy < 2200: # third harmonic
            enoff = (energy/3) - 207.503
            gap = (enoff ** 0) * 14026.99244058688 + \
                  (enoff ** 1) * 41.45793369967348 + \
                  (enoff ** 2) * -0.05393526187293287 + \
                  (enoff ** 3) * 0.000143951535786684 + \
                  (enoff ** 4) * -3.934262835746608e-07 + \
                  (enoff ** 5) * 6.627045869131144e-10 + \
                  (enoff ** 6) * -4.544338541442881e-13 + \
                  (enoff ** 7) * -8.922084434570775e-17 + \
                  (enoff ** 8) * 2.598052818031009e-19 + \
                  (enoff ** 9) * -8.57226301371417e-23
        else:
            gap= None
    elif polarization == 115: # 15000 phase
        if 182.504 <= energy < 1100:
            enoff = energy - 182.504
            gap = (enoff ** 0) * 13992.18828384784 + \
                  (enoff ** 1) * 53.60817055119084 + \
                  (enoff ** 2) * -0.1051753524422272 + \
                  (enoff ** 3) * 0.0003593146854690839 + \
                  (enoff ** 4) * -1.31756627781552e-06 + \
                  (enoff ** 5) * 3.797812404620049e-09 + \
                  (enoff ** 6) * -7.051992603620334e-12 + \
                  (enoff ** 7) * 7.780656762625199e-15 + \
                  (enoff ** 8) * -4.613775121707344e-18 + \
                  (enoff ** 9) * 1.130384721733557e-21
        elif 1100 <= energy < 2200: # third harmonic
            enoff = (energy/3) - 182.504
            gap = (enoff ** 0) * 13992.18828384784 + \
                  (enoff ** 1) * 53.60817055119084 + \
                  (enoff ** 2) * -0.1051753524422272 + \
                  (enoff ** 3) * 0.0003593146854690839 + \
                  (enoff ** 4) * -1.31756627781552e-06 + \
                  (enoff ** 5) * 3.797812404620049e-09 + \
                  (enoff ** 6) * -7.051992603620334e-12 + \
                  (enoff ** 7) * 7.780656762625199e-15 + \
                  (enoff ** 8) * -4.613775121707344e-18 + \
                  (enoff ** 9) * 1.130384721733557e-21
        else:
            gap= None
    elif polarization == 112: # 12000 phase
        if 144.997 <= energy < 1100:
            enoff = energy - 144.997
            gap = (enoff ** 0) * 13989.91908871217 + \
                  (enoff ** 1) * 79.52996467926575 + \
                  (enoff ** 2) * -0.397042588553584 + \
                  (enoff ** 3) * 0.002410883165646499 + \
                  (enoff ** 4) * -9.116960991617411e-06 + \
                  (enoff ** 5) * 2.050737514265884e-08 + \
                  (enoff ** 6) * -2.757338309663122e-11 + \
                  (enoff ** 7) * 2.170984724060052e-14 + \
                  (enoff ** 8) * -9.195312153413385e-18 + \
                  (enoff ** 9) * 1.610241510211877e-21
        elif 1100 <= energy < 2200: # third harmonic
            enoff = (energy/3) - 144.997
            gap = (enoff ** 0) * 13989.91908871217 + \
                  (enoff ** 1) * 79.52996467926575 + \
                  (enoff ** 2) * -0.397042588553584 + \
                  (enoff ** 3) * 0.002410883165646499 + \
                  (enoff ** 4) * -9.116960991617411e-06 + \
                  (enoff ** 5) * 2.050737514265884e-08 + \
                  (enoff ** 6) * -2.757338309663122e-11 + \
                  (enoff ** 7) * 2.170984724060052e-14 + \
                  (enoff ** 8) * -9.195312153413385e-18 + \
                  (enoff ** 9) * 1.610241510211877e-21
        else:
            gap= None
    elif polarization == 108: # 8000 phase

        if 130.875 <= energy < 1040:
            enoff = energy - 130.875
            gap = (enoff ** 0) * 16104.67059771744 + \
                  (enoff ** 1) * 98.54001020289179 + \
                  (enoff ** 2) * -0.5947064552024715 + \
                  (enoff ** 3) * 0.004033533429002568 + \
                  (enoff ** 4) * -1.782124825808961e-05 + \
                  (enoff ** 5) * 4.847183095095359e-08 + \
                  (enoff ** 6) * -8.068283751628014e-11 + \
                  (enoff ** 7) * 8.010337241397708e-14 + \
                  (enoff ** 8) * -4.353748003371495e-17 + \
                  (enoff ** 9) * 9.967428321189753e-21
        elif 1040 <= energy < 2200: # third harmonic
            enoff = (energy/3) - 130.875
            gap = (enoff ** 0) * 16104.67059771744 + \
                  (enoff ** 1) * 98.54001020289179 + \
                  (enoff ** 2) * -0.5947064552024715 + \
                  (enoff ** 3) * 0.004033533429002568 + \
                  (enoff ** 4) * -1.782124825808961e-05 + \
                  (enoff ** 5) * 4.847183095095359e-08 + \
                  (enoff ** 6) * -8.068283751628014e-11 + \
                  (enoff ** 7) * 8.010337241397708e-14 + \
                  (enoff ** 8) * -4.353748003371495e-17 + \
                  (enoff ** 9) * 9.967428321189753e-21
        else:
            gap= None
    elif polarization == 104: # 4000 phase

        if 129.248 <= energy < 986:
            enoff = energy - 129.248
            gap = (enoff ** 0) * 18071.42451568721 + \
                  (enoff ** 1) * 105.3373080773754 + \
                  (enoff ** 2) * -0.6939864876005439 + \
                  (enoff ** 3) * 0.004579806360258253 + \
                  (enoff ** 4) * -1.899845179678045e-05 + \
                  (enoff ** 5) * 4.885880764915016e-08 + \
                  (enoff ** 6) * -7.850671908438762e-11 + \
                  (enoff ** 7) * 7.704987833035725e-14 + \
                  (enoff ** 8) * -4.23491772565011e-17 + \
                  (enoff ** 9) * 1.000126057875859e-20
        elif 986 <= energy < 2200: # third harmonic
            enoff = (energy/3) - 129.248
            gap = (enoff ** 0) * 18071.42451568721 + \
                  (enoff ** 1) * 105.3373080773754 + \
                  (enoff ** 2) * -0.6939864876005439 + \
                  (enoff ** 3) * 0.004579806360258253 + \
                  (enoff ** 4) * -1.899845179678045e-05 + \
                  (enoff ** 5) * 4.885880764915016e-08 + \
                  (enoff ** 6) * -7.850671908438762e-11 + \
                  (enoff ** 7) * 7.704987833035725e-14 + \
                  (enoff ** 8) * -4.23491772565011e-17 + \
                  (enoff ** 9) * 1.000126057875859e-20
        else:
            gap= None
    elif polarization == 1: # circular polarization

        if 233.736 <= energy < 1800:
            enoff = energy - 233.736
            gap = (enoff ** 0) * 15007.3400729319 + \
                (enoff ** 1) * 40.66671812653791 + \
                      (enoff ** 2) * -0.07652786157391561 + \
                      (enoff ** 3) * 0.0002182211302350642 + \
                      (enoff ** 4) * -5.623344130428556e-07 + \
                      (enoff ** 5) * 1.006174849255388e-09 + \
                      (enoff ** 6) * -1.118133612192828e-12 + \
                      (enoff ** 7) * 7.294270087002236e-16 + \
                      (enoff ** 8) * -2.546331275323855e-19 + \
                      (enoff ** 9) * 3.661307542366029e-23
    else:
        # polarization is 100: # horizontal polarization - default

        if 80.0586 <= energy < 1100:
            enoff = energy - 80.0586
            gap = (enoff ** 0) * 13999.72137152461 + \
                  (enoff ** 1) * 123.5660983013199 + \
                  (enoff ** 2) * -0.5357230317064841 + \
                  (enoff ** 3) * 0.00207025419625126 + \
                  (enoff ** 4) * -5.279184665398675e-06 + \
                  (enoff ** 5) * 8.561167840842576e-09 + \
                  (enoff ** 6) * -8.648473125484471e-12 + \
                  (enoff ** 7) * 5.239890404156463e-15 + \
                  (enoff ** 8) * -1.734402937759189e-18 + \
                  (enoff ** 9) * 2.419654287110562e-22
        elif 1100 <= energy < 2200:  # third harmonic
            enoff = (energy/3) - 80.0586
            gap = (enoff ** 0) * 13999.72137152461 + \
                  (enoff ** 1) * 123.5660983013199 + \
                  (enoff ** 2) * -0.5357230317064841 + \
                  (enoff ** 3) * 0.00207025419625126 + \
                  (enoff ** 4) * -5.279184665398675e-06 + \
                  (enoff ** 5) * 8.561167840842576e-09 + \
                  (enoff ** 6) * -8.648473125484471e-12 + \
                  (enoff ** 7) * 5.239890404156463e-15 + \
                  (enoff ** 8) * -1.734402937759189e-18 + \
                  (enoff ** 9) * 2.419654287110562e-22
        else:
            gap = None
    return gap


def epuphase_from_en_pol(polarization):
    if polarization == 190:
        return 29500
    elif polarization == 126:
        return 26000
    elif polarization == 123:
        return 23000
    elif polarization == 121:
        return 21000
    elif polarization == 118:
        return 18000
    elif polarization == 115:
        return 15000
    elif polarization == 112:
        return 12000
    elif polarization == 108:
        return 8000
    elif polarization == 104:
        return 4000
    elif polarization == 1:
        return 15000
    else:
        return 0


def epumode_from_en_pol(polarization):
    if polarization is 1:
        return 0
    else:
        return 2


def pol_from_mode_phase(phase, mode):
    if abs(phase - 29500) < 100 and mode is 2:
        return 190
    elif abs(phase - 26000) < 100 and mode is 2:
        return 126
    elif abs(phase - 23000) < 100 and mode is 2:
        return 123
    elif abs(phase - 21000) < 100 and mode is 2:
        return 121
    elif abs(phase - 18000) < 100 and mode is 2:
        return 118
    elif abs(phase - 15000) < 100 and mode is 2:
        return 115
    elif abs(phase - 12000) < 100 and mode is 2:
        return 112
    elif abs(phase - 8000) < 100 and mode is 2:
        return 108
    elif abs(phase - 4000) < 100 and mode is 2:
        return 104
    elif abs(phase - 15000) < 100 and mode is 0:
        return 1
    else:
        return 100


class EnPos(PseudoPositioner):
    """Energy pseudopositioner class.

    Parameters:
    -----------

    """
    # synthetic axis
    energy = Cpt(PseudoSingle, kind='hinted', limits=(91,2040),name="Beamline Energy")
    polarization = Cpt(PseudoSingle, kind='hinted', limits=(1,190),name="X-ray Polarization")

    # real motors

    monoen = Cpt(Monochromator, 'XF:07ID1-OP{Mono:PGM1-Ax:',kind='hinted',name='Mono Energy')
    epugap = Cpt(UndulatorMotor, 'SR:C07-ID:G1A{SST1:1-Ax:Gap}-Mtr',kind='normal',name='EPU Gap')
    epuphase = Cpt(UndulatorMotor, 'SR:C07-ID:G1A{SST1:1-Ax:Phase}-Mtr',kind='normal',name='EPU Phase')
   # epumode = Cpt(EpicsSignal,'SR:C07-ID:G1A{SST1:1-Ax:Phase}Phs:Mode-SP',
   #                        name='EPU Mode', kind='normal')

    @pseudo_position_argument
    def forward(self, pseudo_pos):
        '''Run a forward (pseudo -> real) calculation'''
        return self.RealPosition(epugap=epugap_from_en_pol(pseudo_pos.energy, pseudo_pos.polarization),
                                 monoen=pseudo_pos.energy,
                                 epuphase=epuphase_from_en_pol(pseudo_pos.polarization),
                                 #epumode=epumode_from_en_pol(pseudo_pos.polarization)
                                 )

    @real_position_argument
    def inverse(self, real_pos):
        '''Run an inverse (real -> pseudo) calculation'''
        return self.PseudoPosition( energy=real_pos.monoen,
                                    polarization=pol_from_mode_phase(real_pos.epuphase,epu_mode.get()))

    def where_sp(self):
        return ('Beamline Energy Setpoint : {}'
                '\nMonochromator Readback : {}'
                '\nEPU Gap Setpoint : {}'
                '\nEPU Gap Readback : {}'
                '\nEPU Phase Setpoint : {}'
                '\nEPU Phase Readback : {}'
                '\nEPU Mode Setpoint : {}'
                '\nEPU Mode Readback : {}'
                '\nGrating Setpoint : {}'
                '\nGrating Readback : {}'
                '\nMirror2 Setpoint : {}'
                '\nMirror2 Readback : {}'
                '\nCFF : {}'
                '\nVLS : {}').format(
            colored('{:.2f}'.format(self.monoen.setpoint.get()).rstrip('0').rstrip('.'),'yellow'),
            colored('{:.2f}'.format(self.monoen.readback.get()).rstrip('0').rstrip('.'),'yellow'),
            colored('{:.2f}'.format(self.epugap.user_setpoint.get()).rstrip('0').rstrip('.'),'yellow'),
            colored('{:.2f}'.format(self.epugap.user_readback.get()).rstrip('0').rstrip('.'),'yellow'),
            colored('{:.2f}'.format(self.epuphase.user_setpoint.get()).rstrip('0').rstrip('.'),'yellow'),
            colored('{:.2f}'.format(self.epuphase.user_readback.get()).rstrip('0').rstrip('.'),'yellow'),
            colored('{:.2f}'.format(self.epumode.user_setpoint.get()).rstrip('0').rstrip('.'),'yellow'),
            colored('{:.2f}'.format(self.epumode.user_readback.get()).rstrip('0').rstrip('.'),'yellow'),
            colored('{:.2f}'.format(self.monoen.grating.user_setpoint.get()).rstrip('0').rstrip('.'),'yellow'),
            colored('{:.2f}'.format(self.monoen.grating.user_readback.get()).rstrip('0').rstrip('.'),'yellow'),
            colored('{:.2f}'.format(self.monoen.mirror2.user_setpoint.get()).rstrip('0').rstrip('.'),'yellow'),
            colored('{:.2f}'.format(self.monoen.mirror2.user_readback.get()).rstrip('0').rstrip('.'),'yellow'),
            colored('{:.2f}'.format(self.monoen.cff.get()).rstrip('0').rstrip('.'),'yellow'),
            colored('{:.2f}'.format(self.monoen.vls.get()).rstrip('0').rstrip('.'),'yellow'))

    def where(self):
        return ('Beamline Energy : {}\nPolarization : {}').format(
            colored('{:.2f}'.format(self.monoen.readback.get()).rstrip('0').rstrip('.'), 'yellow'),
            colored('{:.2f}'.format(self.polarization.readback.get()).rstrip('0').rstrip('.'), 'yellow'))

    def wh(self):
        boxed_text(self.name+" location", self.where_sp(), 'green',shrink=True)

    def _sequential_move(self, real_pos, timeout=None, **kwargs):
        raise Exception('nope')


class EnPosold(PseudoPositioner):
    """Energy pseudopositioner class.

    Parameters:
    -----------

    """
    # synthetic axis
    energy = Cpt(PseudoSingle, kind='hinted', limits=(150,2500),name="Beamline Energy")

    # real motors

    monoen = Cpt(Monochromator, 'XF:07ID1-OP{Mono:PGM1-Ax:',kind='hinted',name='Mono Energy')
    epugap = Cpt(UndulatorMotor, 'SR:C07-ID:G1A{SST1:1-Ax:Gap}-Mtr',kind='normal',name='EPU Gap')

    @pseudo_position_argument
    def forward(self, pseudo_pos):
        '''Run a forward (pseudo -> real) calculation'''
        return self.RealPosition(epugap=epugap_from_energy_old(pseudo_pos.energy),
                                 monoen=pseudo_pos.energy,)

    @real_position_argument
    def inverse(self, real_pos):
        '''Run an inverse (real -> pseudo) calculation'''
        return self.PseudoPosition( energy=real_pos.monoen)

    def where_sp(self):
        return ('Beamline Energy Setpoint : {}'
                '\nMonochromator Readback : {}'
                '\nEPU Gap Setpoint : {}'
                '\nEPU Gap Readback : {}'
                '\nGrating Setpoint : {}'
                '\nGrating Readback : {}'
                '\nMirror2 Setpoint : {}'
                '\nMirror2 Readback : {}'
                '\nCFF : {}'
                '\nVLS : {}').format(
            colored('{:.2f}'.format(self.monoen.setpoint.get()).rstrip('0').rstrip('.'),'yellow'),
            colored('{:.2f}'.format(self.monoen.readback.get()).rstrip('0').rstrip('.'),'yellow'),
            colored('{:.2f}'.format(self.epugap.user_setpoint.get()).rstrip('0').rstrip('.'),'yellow'),
            colored('{:.2f}'.format(self.epugap.user_readback.get()).rstrip('0').rstrip('.'),'yellow'),
            colored('{:.2f}'.format(self.monoen.grating.user_setpoint.get()).rstrip('0').rstrip('.'),'yellow'),
            colored('{:.2f}'.format(self.monoen.grating.user_readback.get()).rstrip('0').rstrip('.'),'yellow'),
            colored('{:.2f}'.format(self.monoen.mirror2.user_setpoint.get()).rstrip('0').rstrip('.'),'yellow'),
            colored('{:.2f}'.format(self.monoen.mirror2.user_readback.get()).rstrip('0').rstrip('.'),'yellow'),
            colored('{:.2f}'.format(self.monoen.cff.get()).rstrip('0').rstrip('.'),'yellow'),
            colored('{:.2f}'.format(self.monoen.vls.get()).rstrip('0').rstrip('.'),'yellow'))

    def where(self):
        return ('Beamline Energy : {}').format(
            colored('{:.2f}'.format(self.monoen.readback.get()).rstrip('0').rstrip('.'), 'yellow'))

    def wh(self):
        boxed_text(self.name+" location", self.where_sp(), 'green',shrink=True)


    def set_mirror_grating_manually(self,eV,m,k,c):
        [grating,mirror] = get_mirror_grating_angles(eV, c, m, k)
        yield from bps.mv(self.monoen.mirror2,mirror,self.monoen.grating,grating)

en = EnPos('', name='en')
en.energy.kind = 'hinted'
en.monoen.kind = 'normal'
en.monoen.readback.kind = 'normal'
mono_en = en.monoen
epu_gap = en.epugap
epu_phase = en.epuphase
#epu_mode = en.epumode
#mono_en.read_attrs = ['readback']
en.epugap.kind = 'normal'
# en.read_attrs = ['energy',
#                  'energy.readback',
#                  'energy.setpoint',
#                  'monoen',
#                  'epugap']
# en.epugap.read_attrs = ['user_readback', 'user_setpoint']
# en.monoen.read_attrs = ['grating',
#                         'grating.user_readback',
#                         'grating.user_setpoint',
#                         'grating.user_offset',
#                         'mirror2',
#                         'mirror2.user_readback',
#                         'mirror2.user_offset',
#                         'mirror2.user_setpoint',
#                         'cff']

#enold = EnPosold('', name='enold',concurrent=1)
#enold.energy.kind = 'hinted'
#enold.monoen.kind = 'normal'
#enold.monoen.readback.kind = 'normal'
#enold.epugap.kind = 'normal'

sd.baseline.extend([en])


def set_polarization(pol):
    if pol==1:
        if(epu_mode.get() != 0):
            yield from bps.mv(epu_mode,0)
            yield from bps.sleep(1)
    elif pol in [100,104,108,112,115,118,121,123,126,190]:
        if (epu_mode.get() != 2):
            yield from bps.mv(epu_mode, 2)
            yield from bps.sleep(1)
    else:
        print('need a valid polarization')
        return 1
    en.read();
    enval = en.energy.readback.get()
    phaseval = epuphase_from_en_pol(pol)
    gapval = epugap_from_en_pol(enval,pol)
    #print(enval)
    #print(pol)
    #print(phaseval)
    #print(gapval)
    yield from bps.mv(epu_phase, phaseval,epu_gap,gapval)
    yield from bps.mv(en.polarization, pol)
    en.read();
    return 0

@register_line_magic
def e(line):
    try:
        loc = float(line)
    except:
        boxed_text('Beamline Energy',en.where(),'lightpurple',shrink=True)
    else:
        RE(bps.mv(en,loc))
        boxed_text('Beamline Energy', en.where(), 'lightpurple', shrink=True)
del e



@register_line_magic
def pol(line):
    try:
        loc = float(line)
    except:
        boxed_text('Beamline Polarization',en.where(),'lightpurple',shrink=True)
    else:
        RE(set_polarization(loc))
        boxed_text('Beamline Polarization', en.where(), 'lightpurple', shrink=True)
del pol



def grating_to_250():
    yield from bps.abs_set(mono_en.gratingtype, 2,wait=False)
    yield from bps.abs_set(mono_en.gratingtype_proc, 1,wait=True)
    yield from bps.sleep(60)
    yield from bps.mv(mirror2.user_offset, 8.1388)
    yield from bps.mv(grating.user_offset, 7.308-.031725)
    yield from bps.mv(mono_en.cff, 1.385)

def grating_to_1200():
    yield from bps.abs_set(mono_en.gratingtype,9,wait=False)
    yield from bps.abs_set(mono_en.gratingtype_proc, 1,wait=True)
    yield from bps.sleep(60)
    yield from bps.mv(mirror2.user_offset,8.1388)
    yield from bps.mv(grating.user_offset,7.308)
    yield from bps.mv(mono_en.cff,1.7)
