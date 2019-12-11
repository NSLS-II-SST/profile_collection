run_report(__file__)

from ophyd import PVPositioner, EpicsSignalRO, PseudoPositioner, PseudoSingle, EpicsMotor, EpicsSignal
from ophyd import Component as Cpt
from ophyd.pseudopos import (pseudo_position_argument,
                             real_position_argument)
from IPython.core.magic import register_line_magic


class UndulatorMotor(EpicsMotor):
    user_setpoint = Cpt(EpicsSignal, '-SP', limits=True)

epu_gap = UndulatorMotor('SR:C07-ID:G1A{SST1:1-Ax:Gap}-Mtr', name='EPU 60 Gap',kind='normal')

class Monochromator(PVPositioner):
    setpoint = Cpt(EpicsSignal,':ENERGY_SP', kind='normal')
    readback = Cpt(EpicsSignalRO, ':ENERGY_MON',kind='hinted')

    grating = Cpt(prettymotor, 'GrtP}Mtr', name="Mono Grating", kind='normal')
    mirror2 = Cpt(prettymotor, 'MirP}Mtr', name="Mono Mirror", kind='normal')
    cff = Cpt(EpicsSignal, ':CFF_SP', name="Mono CFF", kind='normal')
    vls = Cpt(EpicsSignal, ':VLS_B2.A', name="Mono CFF", kind='normal')

    done = Cpt(EpicsSignalRO, ':ERDY_STS')
    done_value = 1
    stop_signal = Cpt(EpicsSignal, ':ENERGY_ST_CMD')

mono_en= Monochromator('XF:07ID1-OP{Mono:PGM1-Ax:', name='Monochromator Energy',kind='normal')

def epugap_from_energy(energy, harmonic = 1, polarization = 0):
    ''' this calculation was from Cherno's notebook data'''
#    gap = 6401.9 +\
#          (energy ** 1) * 129.42        +\
#          (energy ** 2) *  -2.8688e-01  +\
#          (energy ** 3) *   3.9787e-04  +\
#          (energy ** 4) *  -1.8176e-07  +\
#          (energy ** 5) *  -1.9100e-10  +\
#         (energy ** 6) *   2.5694e-13  +\
#         (energy ** 7) *  -8.0657e-17

    ''' this calculation was from earlier scan from 250-800 eV '''
#    gap = 7290.9 +\
#          (energy ** 1) * 120.6        +\
#          (energy ** 2) *  -0.24858  +\
#          (energy ** 3) *   3.512e-04  +\
#          (energy ** 4) *  -2.7821e-07  +\
#          (energy ** 5) *   1.1596e-10  +\
#          (energy ** 6) *  -1.8848e-14



    '''
    the following calculation was made April 26, 2019 from data from 150eV through 1050eV 5 eV steps
    at DM4 phoodiode with M3 pushing the beam down the transfer line
    grating 1200 l/mm, gold #2 stripe, Exit SlitAB
    hese settings may very well not be applicable for RSoXS or NEXAFS
    '''

    '''
    enoff = energy-150
    gap = (enoff ** 0) * 20495 +\
          (enoff ** 1) * 72.263 +\
          (enoff ** 2) * -0.20964 +\
          (enoff ** 3) * 0.000809 +\
          (enoff ** 4) * -2.549e-06 +\
          (enoff ** 5) * 5.8329e-09 +\
          (enoff ** 6) * -9.011e-12 +\
          (enoff ** 7) * 8.8072e-15 +\
          (enoff ** 8) * -4.8768e-18 +\
          (enoff ** 9) * 1.1606e-21
          
    '''
    '''
    this version is using values from April 27
    valid from 150eV through 1500eV for First Harmonic
    
    '''
    if harmonic is 3 or energy >= 1100:
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
        gap = (enoff ** 0) * 20569.54179105347 +\
              (enoff ** 1) * 65.67661627149975 +\
              (enoff ** 2) * -0.07680907134551485 +\
              (enoff ** 3) * -0.0003134086632392047 +\
              (enoff ** 4) * 2.407905301445676e-06 +\
              (enoff ** 5) * -6.827469033291375e-09 +\
              (enoff ** 6) * 1.045015423402126e-11 +\
              (enoff ** 7) * -9.027454042580941e-15 +\
              (enoff ** 8) * 4.135706733331245e-18 +\
              (enoff ** 9) * -7.796287724230847e-22

    return gap


class EnPos(PseudoPositioner):
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
        return self.RealPosition(epugap=epugap_from_energy(pseudo_pos.energy),
                                 monoen=pseudo_pos.energy)

    @real_position_argument
    def inverse(self, real_pos):
        '''Run an inverse (real -> pseudo) calculation'''
        return self.PseudoPosition( energy = real_pos.monoen )

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
en.epugap.kind = 'normal'

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

