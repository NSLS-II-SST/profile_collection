run_report(__file__)

from ophyd import PVPositioner, EpicsSignalRO, PseudoPositioner, PseudoSingle, EpicsMotor, EpicsSignal
from ophyd import Component as Cpt
from ophyd.pseudopos import (pseudo_position_argument,
                             real_position_argument)
from IPython.core.magic import register_line_magic


class UndulatorMotor(EpicsMotor):
    user_setpoint = Cpt(EpicsSignal, '-SP', limits=True)
class UndulatorMotorPhs(UndulatorMotor):
    user_readback = Cpt(EpicsSignal, '-RB', limits=True)

epu_gap = UndulatorMotor('SR:C07-ID:G1A{SST1:1-Ax:Gap}-Mtr', name='EPU 60 Gap',kind='normal')
epu_phase = UndulatorMotor('SR:C07-ID:G1A{SST1:1-Ax:Phase}-Mtr', name='EPU 60 Phase',kind='normal')

class Monochromator(PVPositioner):
    setpoint = Cpt(EpicsSignal,':ENERGY_SP', kind='normal')
    value = Cpt(EpicsSignalRO, ':ENERGY_MON',kind='hinted')
    readback = Cpt(EpicsSignalRO, ':ENERGY_MON',kind='hinted')

    grating = Cpt(prettymotor, 'GrtP}Mtr', name="Mono Grating", kind='normal')
    mirror2 = Cpt(prettymotor, 'MirP}Mtr', name="Mono Mirror", kind='normal')
    cff = Cpt(EpicsSignal, ':CFF_SP', name="Mono CFF", kind='normal')
    vls = Cpt(EpicsSignal, ':VLS_B2.A', name="Mono CFF", kind='normal')

    done = Cpt(EpicsSignalRO, ':ERDY_STS')
    done_value = 1
    stop_signal = Cpt(EpicsSignal, ':ENERGY_ST_CMD')

mono_en= Monochromator('XF:07ID1-OP{Mono:PGM1-Ax:', name='Monochromator Energy',kind='normal')

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
    '''
    this version is using values from April 27 valid from 150 eV through 1500 eV for First Harmonic
    '''
    if polarization is 100 and energy >= 1100:
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
    elif polarization == 190 and energy >= 385 and energy <= 930:
        gap = 13452 + 22.51 * energy
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

def epuphase_from_en_pol(polarization):
    if polarization is 190:
        return 29500
    else:
        return 0


def epumode_from_en_pol(polarization):
    return 2


def pol_from_mode_phase(phase):
    if abs(phase - 29500) <100:
        return 190
    else:
        return 100


class EnPos(PseudoPositioner):
    """Energy pseudopositioner class.

    Parameters:
    -----------

    """
    # synthetic axis
    energy = Cpt(PseudoSingle, kind='hinted', limits=(150,2500),name="Beamline Energy")
    polarization = Cpt(PseudoSingle, kind='hinted', limits=(99,200),name="X-ray Polarization")

    # real motors

    monoen = Cpt(Monochromator, 'XF:07ID1-OP{Mono:PGM1-Ax:',kind='hinted',name='Mono Energy')
    epugap = Cpt(UndulatorMotor, 'SR:C07-ID:G1A{SST1:1-Ax:Gap}-Mtr',kind='normal',name='EPU Gap')
    epuphase = Cpt(UndulatorMotor, 'SR:C07-ID:G1A{SST1:1-Ax:Phase}-Mtr',kind='normal',name='EPU Phase')

    @pseudo_position_argument
    def forward(self, pseudo_pos):
        '''Run a forward (pseudo -> real) calculation'''
        return self.RealPosition(epugap=epugap_from_en_pol(pseudo_pos.energy, pseudo_pos.polarization),
                                 monoen=pseudo_pos.energy,
                                 epuphase=epuphase_from_en_pol(pseudo_pos.polarization))

    @real_position_argument
    def inverse(self, real_pos):
        '''Run an inverse (real -> pseudo) calculation'''
        return self.PseudoPosition( energy=real_pos.monoen,
                                    polarization=pol_from_mode_phase(real_pos.epuphase))

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
            colored('{:.2f}'.format(self.monoen.setpoint.value).rstrip('0').rstrip('.'),'yellow'),
            colored('{:.2f}'.format(self.monoen.readback.value).rstrip('0').rstrip('.'),'yellow'),
            colored('{:.2f}'.format(self.epugap.user_setpoint.value).rstrip('0').rstrip('.'),'yellow'),
            colored('{:.2f}'.format(self.epugap.user_readback.value).rstrip('0').rstrip('.'),'yellow'),
            colored('{:.2f}'.format(self.epuphase.user_setpoint.value).rstrip('0').rstrip('.'),'yellow'),
            colored('{:.2f}'.format(self.epuphase.user_readback.value).rstrip('0').rstrip('.'),'yellow'),
            colored('{:.2f}'.format(self.epumode.user_setpoint.value).rstrip('0').rstrip('.'),'yellow'),
            colored('{:.2f}'.format(self.epumode.user_readback.value).rstrip('0').rstrip('.'),'yellow'),
            colored('{:.2f}'.format(self.monoen.grating.user_setpoint.value).rstrip('0').rstrip('.'),'yellow'),
            colored('{:.2f}'.format(self.monoen.grating.user_readback.value).rstrip('0').rstrip('.'),'yellow'),
            colored('{:.2f}'.format(self.monoen.mirror2.user_setpoint.value).rstrip('0').rstrip('.'),'yellow'),
            colored('{:.2f}'.format(self.monoen.mirror2.user_readback.value).rstrip('0').rstrip('.'),'yellow'),
            colored('{:.2f}'.format(self.monoen.cff.value).rstrip('0').rstrip('.'),'yellow'),
            colored('{:.2f}'.format(self.monoen.vls.value).rstrip('0').rstrip('.'),'yellow'))

    def where(self):
        return ('Beamline Energy : {}').format(
            colored('{:.2f}'.format(self.monoen.readback.value).rstrip('0').rstrip('.'), 'yellow'))

    def wh(self):
        boxed_text(self.name+" location", self.where_sp(), 'green',shrink=True)


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
            colored('{:.2f}'.format(self.monoen.setpoint.value).rstrip('0').rstrip('.'),'yellow'),
            colored('{:.2f}'.format(self.monoen.readback.value).rstrip('0').rstrip('.'),'yellow'),
            colored('{:.2f}'.format(self.epugap.user_setpoint.value).rstrip('0').rstrip('.'),'yellow'),
            colored('{:.2f}'.format(self.epugap.user_readback.value).rstrip('0').rstrip('.'),'yellow'),
            colored('{:.2f}'.format(self.monoen.grating.user_setpoint.value).rstrip('0').rstrip('.'),'yellow'),
            colored('{:.2f}'.format(self.monoen.grating.user_readback.value).rstrip('0').rstrip('.'),'yellow'),
            colored('{:.2f}'.format(self.monoen.mirror2.user_setpoint.value).rstrip('0').rstrip('.'),'yellow'),
            colored('{:.2f}'.format(self.monoen.mirror2.user_readback.value).rstrip('0').rstrip('.'),'yellow'),
            colored('{:.2f}'.format(self.monoen.cff.value).rstrip('0').rstrip('.'),'yellow'),
            colored('{:.2f}'.format(self.monoen.vls.value).rstrip('0').rstrip('.'),'yellow'))

    def where(self):
        return ('Beamline Energy : {}').format(
            colored('{:.2f}'.format(self.monoen.readback.value).rstrip('0').rstrip('.'), 'yellow'))

    def wh(self):
        boxed_text(self.name+" location", self.where_sp(), 'green',shrink=True)


    def set_mirror_grating_manually(self,eV,m,k,c):
        [grating,mirror] = get_mirror_grating_angles(eV, c, m, k)
        yield from bps.mv(self.monoen.mirror2,mirror,self.monoen.grating,grating)

en = EnPos('', name='en',concurrent=1)
en.energy.kind = 'hinted'
en.monoen.kind = 'normal'
en.monoen.readback.kind = 'normal'
mono_en.read_attrs = ['readback']
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


def cff_to_13():
    energy = en.monoen.setpoint.value
    yield from bps.mv(en.monoen.grating.user_offset,-0.3511242679026303,
                      en.monoen.mirror2.user_offset,-3.4610179934346594,
                      en.monoen.cff,1.3)
    yield from bps.mv(en,energy)


def cff_to_199():
    energy = en.monoen.setpoint.value
    yield from bps.mv(en.monoen.grating.user_offset,-0.098373,
                      en.monoen.mirror2.user_offset,-3.237992,
                      en.monoen.cff,1.99)
    yield from bps.mv(en,energy)

def cff_to_19():
    energy = en.monoen.setpoint.value
    yield from bps.mv(en.monoen.grating.user_offset, -0.3511,
                      en.monoen.mirror2.user_offset, -3.461,
                      en.monoen.cff, 1.9)
    yield from bps.mv(en, energy)


cffs = [[1.8,7.94,-0.1667,-0.1295],
        [1.75,7.915,-0.1847,-0.144],
        [1.7,7.92,-0.1163,-0.0896],
        [1.6,7.93,-0.2646,-0.2392],
        [1.5,7.93,0.021,0.144],
        [1.4,7.94,0.021,0.144],
        [1.3,7.95,0.021,0.144]]


def cffscan(cffs):
    for [cff, m3p, goff, m2off] in cffs:
        mir3.Pitch.put(m3p)
        RE(bps.mv(en.monoen.cff, cff,
                  en.monoen.grating.user_offset, goff,
                  en.monoen.mirror2.user_offset, m2off))
        RE(bp.scan([Izero_Mesh, Beamstop_WAXS], en, 280, 300, 201))


def mono_scan(energy = None,width = 20, pnts = 51):
    if energy is None:
        energy = en.energy.setpoint.value
    yield from bps.mv(en, energy)
    yield from bp.rel_scan([Izero_Mesh,Beamstop_WAXS],mono_en,-width/2,width/2,pnts)


def correct_mono(calibrated_eV,apply=False,current_eV=None, k=1200):
    '''

    :param calibrated_eV:  This is the "real" energy, what you want the readout to be
    :param apply:          Whether to apply the correction or not
    :param current_eV:     if None, the current value for energy will be set to the calibrated value
                           if not None, the value entered here will be set to the calibrated value
    :param k:              the grating line spacing

    :return:
    '''
    if current_eV is None:
        current_eV = en.energy.setpoint.value
    cff = en.monoen.cff.value
    [mirror_cur, grating_cur] = get_mirror_grating_angles(current_eV, cff, 1, k)
    [mirror_cal, grating_cal] = get_mirror_grating_angles(calibrated_eV, cff, 1, k)
    d_mir = mirror_cur-mirror_cal
    d_grat = grating_cur-grating_cal


    grat_off = mono_en.grating.user_offset.value
    mir_off = mono_en.mirror2.user_offset.value


    print(f'grating offset is {d_grat} from ideal, mirror offset is {d_mir} from ideal'
          f'\nGrating offset will be changed from {grat_off} to {grat_off + d_grat} and '
          f'\nMirror2 offset will be changed from {mir_off} to {mir_off + d_mir}')
    if apply:
        yield from bps.mv(mono_en.grating.user_offset, grat_off + d_grat)
        yield from bps.mv(mono_en.mirror2.user_offset, mir_off + d_mir)


