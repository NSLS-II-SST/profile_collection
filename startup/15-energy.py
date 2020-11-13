run_report(__file__)

from ophyd import PVPositioner, EpicsSignalRO, PseudoPositioner, PseudoSingle, EpicsMotor, EpicsSignal
from ophyd import Component as Cpt
from ophyd.pseudopos import (pseudo_position_argument,
                             real_position_argument)
from IPython.core.magic import register_line_magic

import pathlib
import xarray as xr
import numpy as np
import IPython

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
import xarray as xr

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
        return self.RealPosition(epugap=self.gap(pseudo_pos.energy, pseudo_pos.polarization),
                                 monoen=pseudo_pos.energy,
                                 epuphase=self.phase(pseudo_pos.energy, pseudo_pos.polarization),
                                 #epumode=self.mode(pseudo_pos.polarization)
                                 )

    @real_position_argument
    def inverse(self, real_pos):
        '''Run an inverse (real -> pseudo) calculation'''
        return self.PseudoPosition( energy=real_pos.monoen,
                                    polarization=self.pol(real_pos.epuphase,epu_mode.get()))

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
    # end class methods, begin internal methods
    
    # begin LUT functions
    
    def __init__(self,a,configpath=pathlib.Path(IPython.paths.get_ipython_dir())/'profile_collection'/'startup'/'config',**kwargs):
        super().__init__(a,**kwargs)
        self.C250_gap = xr.load_dataarray(configpath/'EPU_C_250_gap.nc')
        self.C250_intens = xr.load_dataarray(configpath/'EPU_C_250_intens.nc')
        self.C1200_gap = xr.load_dataarray(configpath/'EPU_C_1200_gap.nc')
        self.C1200_intens = xr.load_dataarray(configpath/'EPU_C_1200_intens.nc')
        self.L250_gap = xr.load_dataarray(configpath/'EPU_L_250_gap.nc')
        self.L250_intens = xr.load_dataarray(configpath/'EPU_L_250_intens.nc')
        self.L1200_gap = xr.load_dataarray(configpath/'EPU_L_1200_gap.nc')
        self.L1200_intens = xr.load_dataarray(configpath/'EPU_L_1200_intens.nc')
        self.polphase = xr.load_dataarray(configpath/'polphase.nc')
        self.phasepol = xr.DataArray(data=self.polphase.pol,coords={'phase':self.polphase.values},dims={'phase'})
        
    def gap(self,energy,pol,grating='best',verbose=False):
        
        if pol == -1:
            g250_gap = float(self.C250_gap.interp(Energies=energy))
            g250_intens = float(self.C250_intens.interp(Energies=energy))
            g1200_gap = float(self.C1200_gap.interp(Energies=energy))
            g1200_intens = float(self.C1200_intens.interp(Energies=energy))
        elif pol>=0 and pol<=90:
            phase = self.phase(energy,pol)/1000
            g250_gap = float(self.L250_gap.interp(Energies=energy,phase=phase))
            g250_intens = float(self.L250_intens.interp(Energies=energy,phase=phase))
            g1200_gap = float(self.L1200_gap.interp(Energies=energy,phase=phase))
            g1200_intens = float(self.L1200_intens.interp(Energies=energy,phase=phase))
        else:
            return np.nan
        
        if verbose:
            print(f'For pol {pol}, energy {energy} phase {phase}: ')
            print(f'  . 250 l/mm grating: gap = {g250_gap}, intensity {g250_intens}')
            print(f'  . 1200 l/mm grating: gap = {g1200_gap}, intensity {g1200_intens}')
        
        if grating=='250' or np.isnan(g1200_gap):
            return min(100000,max(0,g250_gap))
        elif grating=='1200' or np.isnan(g250_gap):
            return min(100000,max(0,g1200_gap))
        else:
            if g250_intens > g1200_intens:
                return min(100000,max(0,g250_gap))
            else:
                return min(100000,max(0,g1200_gap))

    def phase(self,en,pol):
        return min(29500,max(0,float(self.polphase.interp(pol=pol))))
    def pol(self,phase,mode):
        if mode == 2:
            return -1
        else:
            return float(self.phasepol.interp(phase=phase))
    def mode(self,pol):
        if pol == -1:
            return 2
        else:
            return 0

    



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
    if pol==-1:
        if(epu_mode.get() != 0):
            yield from bps.mv(epu_mode,0)
            yield from bps.sleep(1)
    elif 0 <= pol <=90 :
        if (epu_mode.get() != 2):
            yield from bps.mv(epu_mode, 2)
            yield from bps.sleep(1)
    else:
        print('need a valid polarization')
        return 1
    en.read();
    enval = en.energy.readback.get()
    phaseval = en.phase(enval,pol)
    gapval = en.gap(enval,pol)
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
    type =  mono_en.gratingtype.enum_strs.index(mono_en.gratingtype.get())
    if type == 2:
        return 0 # the grating is already here
    yield from bps.abs_set(mono_en.gratingtype, 2,wait=False)
    yield from bps.abs_set(mono_en.gratingtype_proc, 1,wait=True)
    yield from bps.sleep(60)
    yield from bps.mv(mirror2.user_offset, 8.1176)
    yield from bps.mv(grating.user_offset, 7.263)
    yield from bps.mv(mono_en.cff, 1.385)
    yield from bps.mv(mono_en,270)

def grating_to_1200():
    type =  mono_en.gratingtype.enum_strs.index(mono_en.gratingtype.get())
    if type == 9:
        return 0 # the grating is already here
    yield from bps.abs_set(mono_en.gratingtype,9,wait=False)
    yield from bps.abs_set(mono_en.gratingtype_proc, 1,wait=True)
    yield from bps.sleep(60)
    yield from bps.mv(mirror2.user_offset,8.1396)
    yield from bps.mv(grating.user_offset,7.3097)
    yield from bps.mv(mono_en.cff,1.7)
    yield from bps.mv(mono_en,270)


sd.monitors.extend([mono_en.readback])

# XF:07ID1-OP{Mono:PGM1-Ax::EVSTART_SP # start energy
# XF:07ID1-OP{Mono:PGM1-Ax::EVSTOP_SP # stop energy
# XF:07ID1-OP{Mono:PGM1-Ax::EVVELO_SP # Ev/sec
# XF:07ID1-OP{Mono:PGM1-Ax::START_CMD.PROC #start
# XF:07ID1-OP{Mono:PGM1-Ax::ENERGY_ST_CMD.PROC #stop

Mono_Scan_Start_ev = EpicsSignal('XF:07ID1-OP{Mono:PGM1-Ax::EVSTART_SP',
                        name='MONO scan start energy',kind='normal')
Mono_Scan_Stop_ev = EpicsSignal('XF:07ID1-OP{Mono:PGM1-Ax::EVSTOP_SP',
                        name='MONO scan stop energy',kind='normal')
Mono_Scan_Speed_ev = EpicsSignal('XF:07ID1-OP{Mono:PGM1-Ax::EVVELO_SP',
                        name='MONO scan speed',kind='normal')
Mono_Scan_Start = EpicsSignal('XF:07ID1-OP{Mono:PGM1-Ax::START_CMD.PROC',
                        name='MONO scan start command',kind='normal')
Mono_Scan_Stop = EpicsSignal('XF:07ID1-OP{Mono:PGM1-Ax::ENERGY_ST_CMD.PROC',
                        name='MONO scan start command',kind='normal')