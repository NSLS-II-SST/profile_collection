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

class Monochromator(PVPositioner):
    setpoint = Cpt(EpicsSignal,':ENERGY_SP', kind='normal', write_timeout=180.)
    value = Cpt(EpicsSignalRO, ':ENERGY_MON',kind='hinted')
    readback = Cpt(EpicsSignalRO, ':ENERGY_MON',kind='hinted')

    grating = Cpt(prettymotor, 'GrtP}Mtr', name="Mono Grating", kind='normal')
    mirror2 = Cpt(prettymotor, 'MirP}Mtr', name="Mono Mirror", kind='normal')
    cff = Cpt(EpicsSignal, ':CFF_SP', name="Mono CFF", kind='normal')
    vls = Cpt(EpicsSignal, ':VLS_B2.A', name="Mono CFF", kind='normal')

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
    '''
    this version is using values from April 27 valid from 150 eV through 1500 eV for First Harmonic
    '''
    # if polarization is 100 and energy >= 1100:
    #     enoff = energy - 370.01
    #     gap = (enoff ** 0) * 22833.87619739154 + \
    #           (enoff ** 1) * 29.68655012463454 + \
    #           (enoff ** 2) * -0.03210984163384775 + \
    #           (enoff ** 3) * 4.980917046937771e-05 + \
    #           (enoff ** 4) * -6.396452510943625e-08 + \
    #           (enoff ** 5) * 5.991083149692317e-11 + \
    #           (enoff ** 6) * -3.812842880047685e-14 + \
    #           (enoff ** 7) * 1.623556090541289e-17 + \
    #           (enoff ** 8) * -4.365835230578085e-21 + \
    #           (enoff ** 9) * 5.739408834109368e-25
    # elif polarization == 190 and energy >= 385 and energy <= 930:
    #     gap = 13452 + 22.51 * energy
    # else:
    #     enoff = energy - 150
    #     gap = (enoff ** 0) * 20569.54179105347 + \
    #           (enoff ** 1) * 65.67661627149975 + \
    #           (enoff ** 2) * -0.07680907134551485 + \
    #           (enoff ** 3) * -0.0003134086632392047 + \
    #           (enoff ** 4) * 2.407905301445676e-06 + \
    #           (enoff ** 5) * -6.827469033291375e-09 + \
    #           (enoff ** 6) * 1.045015423402126e-11 + \
    #           (enoff ** 7) * -9.027454042580941e-15 + \
    #           (enoff ** 8) * 4.135706733331245e-18 + \
    #           (enoff ** 9) * -7.796287724230847e-22
    # return gap
    gap = None

    if polarization is 190: # vertical polarization
        if 168 <= energy < 1100:
            enoff = energy - 167.50006507
            gap = (enoff ** 0) * 14622.35886091497          + \
                  (enoff ** 1) * 79.45356871349468          + \
                  (enoff ** 2) * -0.8727196924302836        + \
                  (enoff ** 3) * 0.007153735346301802       + \
                  (enoff ** 4) * -3.139219674602493e-05     + \
                  (enoff ** 5) * 7.865183870383904e-08      + \
                  (enoff ** 6) * -1.163807191257357e-10     + \
                  (enoff ** 7) * 1.005851882527788e-13      + \
                  (enoff ** 8) * -4.69241419016422e-17      + \
                  (enoff ** 9) * 9.126543545094467e-21

        elif 1100 <= energy < 2054: # third harmonic
            enoff = energy - 503.3203871
            gap = (enoff ** 0) * 15008.30898562484           + \
                  (enoff ** 1) * 15.53586640720786           + \
                  (enoff ** 2) * -0.022536487722764          + \
                  (enoff ** 3) * 8.228725309031966e-05       + \
                  (enoff ** 4) * -2.197534586531886e-07      + \
                  (enoff ** 5) * 3.555024066841478e-10       + \
                  (enoff ** 6) * -3.454252474185978e-13      + \
                  (enoff ** 7) * 1.97676836943378e-16        + \
                  (enoff ** 8) * -6.141418522304618e-20      + \
                  (enoff ** 9) * 7.993082265756972e-24

    elif polarization is 125: # vertical polarization
        if 212 <= energy < 1100:
            enoff = energy - 211.25467563
            gap = (enoff ** 0) * 14584.35660394691       + \
                  (enoff ** 1) * 81.46681437020771       + \
                  (enoff ** 2) * -1.063712849739659      + \
                  (enoff ** 3) * 0.009275638121170167    + \
                  (enoff ** 4) * -4.234975106446957e-05  + \
                  (enoff ** 5) * 1.098234371966891e-07   + \
                  (enoff ** 6) * -1.679207518873966e-10  + \
                  (enoff ** 7) * 1.498714839417041e-13   + \
                  (enoff ** 8) * -7.218373220487733e-17  + \
                  (enoff ** 9) * 1.449351930191205e-20

    elif polarization is 120: # vertical polarization
        if 235 <= energy < 1100:
            enoff = energy - 234.98519652
            gap = (enoff ** 0) * 14798.07731572243       + \
                  (enoff ** 1) * 56.16228122162846       + \
                  (enoff ** 2) * -0.4692082546739633     + \
                  (enoff ** 3) * 0.004164088423443679    + \
                  (enoff ** 4) * -1.999386443826096e-05  + \
                  (enoff ** 5) * 5.462418311398194e-08   + \
                  (enoff ** 6) * -8.785971602778833e-11  + \
                  (enoff ** 7) * 8.239422829429386e-14   + \
                  (enoff ** 8) * -4.166699208229707e-17  + \
                  (enoff ** 9) * 8.781955126316585e-21

    elif polarization is 116: # vertical polarization
        if 206 <= energy < 1100:
            enoff = energy - 205.00412715
            gap = (enoff ** 0) * 14916.98034273721       + \
                  (enoff ** 1) * 54.29503098264628       + \
                  (enoff ** 2) * -0.2491173385663503     + \
                  (enoff ** 3) * 0.001948412336737997    + \
                  (enoff ** 4) * -9.171645432305396e-06  + \
                  (enoff ** 5) * 2.487974365193833e-08   + \
                  (enoff ** 6) * -3.971806672617338e-11  + \
                  (enoff ** 7) * 3.692565191146745e-14   + \
                  (enoff ** 8) * -1.850015483152694e-17  + \
                  (enoff ** 9) * 3.863574657261709e-21

    elif polarization is 104: # vertical polarization
        if 100 <= energy < 1100:
            enoff = energy - 99.18637273
            gap = (enoff ** 0) * 15296.49505904854      + \
                  (enoff ** 1) * 111.6935238502345      + \
                  (enoff ** 2) * -0.5318452040149829    + \
                  (enoff ** 3) * 0.002522472412655326   + \
                  (enoff ** 4) * -8.139971173054056e-06 + \
                  (enoff ** 5) * 1.691909898011538e-08  + \
                  (enoff ** 6) * -2.21552389677964e-11  + \
                  (enoff ** 7) * 1.761177450482788e-14  + \
                  (enoff ** 8) * -7.745630380250356e-18 + \
                  (enoff ** 9) * 1.444917025851466e-21

    elif polarization is 112: # vertical polarization
        if 162 <= energy < 1100:
            enoff = energy - 161.66065884
            gap = (enoff ** 0) * 14970.74161247973      + \
                  (enoff ** 1) * 71.63595646171082      + \
                  (enoff ** 2) * -0.3333372852527692    + \
                  (enoff ** 3) * 0.002109066742806884   + \
                  (enoff ** 4) * -8.572917697871371e-06 + \
                  (enoff ** 5) * 2.095792129907114e-08  + \
                  (enoff ** 6) * -3.084391159303237e-11 + \
                  (enoff ** 7) * 2.678469462872999e-14  + \
                  (enoff ** 8) * -1.264020972655732e-17 + \
                  (enoff ** 9) * 2.501258335889735e-21

    elif polarization is 1: # circular polarization
        if 238 <= energy < 1800:
            enoff = energy - 237.37682344
            gap = (enoff ** 0) * 15013.34794532079           + \
                  (enoff ** 1) * 39.8763637325271            + \
                  (enoff ** 2) * -0.07794302832262227        + \
                  (enoff ** 3) * 0.0002096214175929367       + \
                  (enoff ** 4) * -4.460761960094444e-07      + \
                  (enoff ** 5) * 6.348684432599568e-10       + \
                  (enoff ** 6) * -5.617174609319205e-13      + \
                  (enoff ** 7) * 2.920241694418002e-16       + \
                  (enoff ** 8) * -8.037658719820455e-20      + \
                  (enoff ** 9) * 8.847705328400634e-24
    else:
        # polarization is 100: # horizontal polarization - default
        if 100 <= energy < 1100:
            enoff = energy - 99.08496564000001
            gap = (enoff ** 0) * 15879.88627763909       + \
              (enoff ** 1) *     110.0836448991598       + \
              (enoff ** 2) *     -0.5017899213674649     + \
              (enoff ** 3) *     0.002244632997626055    + \
              (enoff ** 4) *     -6.778863779803541e-06  + \
              (enoff ** 5) *     1.318236985628506e-08   + \
              (enoff ** 6) *     -1.622642480718214e-11  + \
              (enoff ** 7) *     1.222342409851351e-14   + \
              (enoff ** 8) *     -5.14422560200779e-18   + \
              (enoff ** 9) *     9.280241963159906e-22
        elif 1100 <= energy < 2043: # third harmonic
            enoff = energy - 270.0339431
            gap = (enoff ** 0) * 14980.14097989457        + \
                  (enoff ** 1) * 39.30125265144509        + \
                  (enoff ** 2) * -0.0674108834353197      + \
                  (enoff ** 3) * 0.000132989043933298     + \
                  (enoff ** 4) * -2.047601585681656e-07   + \
                  (enoff ** 5) * 2.208539436185439e-10    + \
                  (enoff ** 6) * -1.582405111796854e-13   + \
                  (enoff ** 7) * 7.140749578708601e-17    + \
                  (enoff ** 8) * -1.832598427725348e-20   + \
                  (enoff ** 9) * 2.037204560871964e-24
    return gap


def epuphase_from_en_pol(polarization):
    if polarization is 190:
        return 29500
    elif polarization is 125:
        return 25000
    elif polarization is 120:
        return 20000
    elif polarization is 116:
        return 16000
    elif polarization is 112:
        return 12000
    elif polarization is 104:
        return 4000
    elif polarization is 1:
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
    elif abs(phase - 25000) < 100 and mode is 2:
        return 125
    elif abs(phase - 20000) < 100 and mode is 2:
        return 120
    elif abs(phase - 16000) < 100 and mode is 2:
        return 116
    elif abs(phase - 12000) < 100 and mode is 2:
        return 112
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
    epumode = Cpt(EpicsSignal,'SR:C07-ID:G1A{SST1:1-Ax:Phase}Phs:Mode-RB',
                           write_pv='SR:C07-ID:G1A{SST1:1-Ax:Phase}Phs:Mode-SP',
                           name='EPU 60 Mode', kind='normal')

    @pseudo_position_argument
    def forward(self, pseudo_pos):
        '''Run a forward (pseudo -> real) calculation'''
        return self.RealPosition(epugap=epugap_from_en_pol(pseudo_pos.energy, pseudo_pos.polarization),
                                 monoen=pseudo_pos.energy,
                                 epuphase=epuphase_from_en_pol(pseudo_pos.polarization),
                                 epumode=epumode_from_en_pol(pseudo_pos.polarization))

    @real_position_argument
    def inverse(self, real_pos):
        '''Run an inverse (real -> pseudo) calculation'''
        return self.PseudoPosition( energy=real_pos.monoen,
                                    polarization=pol_from_mode_phase(real_pos.epuphase,real_pos.epumode))

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

en = EnPos('', name='en')
en.energy.kind = 'hinted'
en.monoen.kind = 'normal'
en.monoen.readback.kind = 'normal'
mono_en = en.monoen
epu_gap = en.epugap
epu_phase = en.epuphase
epu_mode = en.epumode
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
        yield from bps.amv(mono_en.grating.user_offset, grat_off + d_grat)
        yield from bps.mv(mono_en.mirror2.user_offset, mir_off + d_mir)


