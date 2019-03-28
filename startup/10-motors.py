print(f'Loading {__file__}...')

from ophyd import EpicsMotor, EpicsSignal
sam_X = EpicsMotor('XF:07ID2-ES1{Stg-Ax:X}Mtr', name='sam_X')
sam_Y = EpicsMotor('XF:07ID2-ES1{Stg-Ax:Y}Mtr', name='sam_Y')
sam_Z = EpicsMotor('XF:07ID2-ES1{Stg-Ax:Z}Mtr', name='sam_Z')
sam_Th = EpicsMotor('XF:07ID2-ES1{Stg-Ax:Yaw}Mtr', name='sam_Th')
sam_Th.kind = 'hinted'
BSw = BeamStopW = EpicsMotor('XF:07ID2-ES1{BS-Ax:1}Mtr', name='BeamStopW')
BSs = BeamStopS = EpicsMotor('XF:07ID2-ES1{BS-Ax:2}Mtr', name='BeamStopS')
Det_W = EpicsMotor('XF:07ID2-ES1{Det-Ax:1}Mtr', name='Det_W')
Det_S = EpicsMotor('XF:07ID2-ES1{Det-Ax:2}Mtr', name='Det_S')
Shutter_Y = EpicsMotor('XF:07ID2-ES1{FSh-Ax:1}Mtr', name='Shutter_Y')
Izero_Y = EpicsMotor('XF:07ID2-ES1{Scr-Ax:1}Mtr', name='Izero_Y')
#epu_gap = EpicsMotor('SR:C07-ID:G1A{SST1:1-Ax:Gap}-Mtr', name='epu_gap')

## monochromator
# dcm_bragg = BraggEpicsMotor('XF:07ID6-OP{Mono:DCM1-Ax:Bragg}Mtr', name='dcm_bragg')
#mono_en = EpicsSignal(read_pv='XF:07ID1-OP{Mono:PGM1-Ax::ENERGY_MON',
#                     write_pv='XF:07ID1-OP{Mono:PGM1-Ax::ENERGY_SP',
#                     name='mono_en')

from ophyd import PVPositioner, EpicsSignalRO, PseudoPositioner, PseudoSingle
from ophyd import Component as Cpt
from ophyd.pseudopos import (pseudo_position_argument,
                             real_position_argument)

class undulatorgap(PVPositioner):
    setpoint = Cpt(EpicsSignal,'-Ax:Gap}-Mtr-SP')
    readback = Cpt(EpicsSignalRO, '-Ax:Gap}-Mtr.RBV')
    done = Cpt(EpicsSignalRO, '-Ax:Gap}-Mtr.MOVN')
    done_value = 0
    stop_signal = Cpt(EpicsSignal, '-Ax:Gap}-Mtr.STOP')

epu_gap = undulatorgap('SR:C07-ID:G1A{SST1:1',name='epu_gap', read_attrs=['readback'],
                configuration_attrs=[])

class monochromator(PVPositioner):
    setpoint = Cpt(EpicsSignal,'ENERGY_SP')
    readback = Cpt(EpicsSignalRO, 'ENERGY_MON')
    done = Cpt(EpicsSignalRO, 'ERDY_STS')
    done_value = 1
    stop_signal = Cpt(EpicsSignal, 'ENERGY_ST_CMD')

mono_en= monochromator('XF:07ID1-OP{Mono:PGM1-Ax::',name='mono_en')

def epugap_from_energy(energy):
    return energy*36 + 18509 #add as many terms as needed

class enpos(PseudoPositioner):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._hints = None
    # synthetic axis

    energy = Cpt(PseudoSingle, kind='hinted', limits=(150,500))

    # real motors

    epugap = Cpt(undulatorgap,'SR:C07-ID:G1A{SST1:1', read_attrs=['readback'],
                           configuration_attrs=[])

    monoen = Cpt(monochromator, 'XF:07ID1-OP{Mono:PGM1-Ax::', read_attrs=['readback'],
                           configuration_attrs=[])

    @pseudo_position_argument
    def forward(self, pseudo_pos):
        '''Run a forward (pseudo -> real) calculation'''
        return self.RealPosition(
                                    epugap = epugap_from_energy(pseudo_pos.energy) ,
                                    monoen = pseudo_pos.energy
                                 )

    @real_position_argument
    def inverse(self, real_pos):
        '''Run an inverse (real -> pseudo) calculation'''
        return self.PseudoPosition( energy = real_pos.monoen )

en = enpos('',name='en')

