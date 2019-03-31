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
MirrorType = EpicsSignal('XF:07ID1-OP{Mono:PGM1-Ax:MirX}Mtr_TYPE_MON',name='MirrorType')
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

# class undulatorgap(PVPositioner):
#     setpoint = Cpt(EpicsSignal,'-Ax:Gap}-Mtr-SP')
#     readback = Cpt(EpicsSignalRO, '-Ax:Gap}-Mtr.RBV')
#     done = Cpt(EpicsSignalRO, '-Ax:Gap}-Mtr.MOVN')
#     done_value = 0
#     stop_signal = Cpt(EpicsSignal, '-Ax:Gap}-Mtr.STOP')

class UndulatorMotor(EpicsMotor):
    user_setpoint = Cpt(EpicsSignal, '-SP', limits=True)

epu_gap = UndulatorMotor('SR:C07-ID:G1A{SST1:1-Ax:Gap}-Mtr', name='epu_gap')

class Monochromator(PVPositioner):
    setpoint = Cpt(EpicsSignal,'ENERGY_SP')
    readback = Cpt(EpicsSignalRO, 'ENERGY_MON')
    done = Cpt(EpicsSignalRO, 'ERDY_STS')
    done_value = 1
    stop_signal = Cpt(EpicsSignal, 'ENERGY_ST_CMD')

mono_en= Monochromator('XF:07ID1-OP{Mono:PGM1-Ax::', name='mono_en')

def epugap_from_energy(energy):
    gap = 6401.9 +\
          (energy ** 1) * 129.42        +\
          (energy ** 2) *  -2.8688e-01  +\
          (energy ** 3) *   3.9787e-04  +\
          (energy ** 4) *  -1.8176e-07  +\
          (energy ** 5) *  -1.9100e-10  +\
          (energy ** 6) *   2.5694e-13  +\
          (energy ** 7) *  -8.0657e-17
    return gap #add as many terms as needed


class EnPos(PseudoPositioner):
    """Energy pseudopositioner class.

    Parameters:
    -----------

    """
    # synthetic axis
    energy = Cpt(PseudoSingle, kind='hinted', limits=(150,500))

    # real motors
    # epugap = Cpt(UndulatorMotor, 'SR:C07-ID:G1A{SST1:1', read_attrs=['readback'],
    #                        configuration_attrs=[])
    # monoen = Cpt(monochromator, 'XF:07ID1-OP{Mono:PGM1-Ax::', read_attrs=['readback'],
    #                        configuration_attrs=[])

    epugap = Cpt(UndulatorMotor, 'SR:C07-ID:G1A{SST1:1-Ax:Gap}-Mtr')
    monoen = Cpt(Monochromator, 'XF:07ID1-OP{Mono:PGM1-Ax::')

    @pseudo_position_argument
    def forward(self, pseudo_pos):
        '''Run a forward (pseudo -> real) calculation'''
        return self.RealPosition(epugap=epugap_from_energy(pseudo_pos.energy),
                                 monoen=pseudo_pos.energy)

    @real_position_argument
    def inverse(self, real_pos):
        '''Run an inverse (real -> pseudo) calculation'''
        return self.PseudoPosition( energy = real_pos.monoen )

en = EnPos('', name='en')

sd.baseline.extend([en, sam_X, sam_Y, sam_Z, sam_Th, BeamStopS, BeamStopW, Det_S, Det_W, Shutter_Y, Izero_Y])

