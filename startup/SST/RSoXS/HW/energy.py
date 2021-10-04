from ...HW.energy import (
    EnPos,
    base_grating_to_250,
    base_grating_to_1200,
    base_set_polarization,
)
from ..HW.motors import sam_Th
from ...CommonFunctions.functions import run_report


run_report(__file__)


# epu_mode = EpicsSignal('SR:C07-ID:G1A{SST1:1-Ax:Phase}Phs:Mode-RB',
#                        write_pv='SR:C07-ID:G1A{SST1:1-Ax:Phase}Phs:Mode-SP',
#                        name='EPU 60 Mode',kind='normal')


# enold = EnPosold('', name='enold',concurrent=1)
# enold.energy.kind = 'hinted'
# enold.monoen.kind = 'normal'
# enold.monoen.readback.kind = 'normal'
# enold.epugap.kind = 'normal'


en = EnPos("", rotation_motor=sam_Th, name="en")
en.energy.kind = "hinted"
en.monoen.kind = "normal"
# en.monoen.readback.kind = 'hinted'
mono_en = en.monoen
epu_gap = en.epugap
epu_phase = en.epuphase
# epu_mode = en.epumode
# epu_mode = en.epumode
# mono_en.read_attrs = ['readback']
mono_en.readback.kind = "normal"
en.epugap.kind = "normal"
en.epuphase.kind = "normal"
en.polarization.kind = "normal"
en.sample_polarization.kind = "normal"
en.read_attrs = ["energy", "polarization", "sample_polarization"]
en.epugap.read_attrs = ["user_readback", "user_setpoint"]
en.monoen.read_attrs = [
    "readback",
    "grating",
    "grating.user_readback",
    "grating.user_setpoint",
    "grating.user_offset",
    "mirror2",
    "mirror2.user_readback",
    "mirror2.user_offset",
    "mirror2.user_setpoint",
    "cff",
]
en.monoen.grating.kind = "normal"
en.monoen.mirror2.kind = "normal"
en.monoen.gratingx.kind = "normal"
en.monoen.mirror2x.kind = "normal"
en.epugap.kind = "normal"
en.epugap.kind = "normal"


def set_polarization(pol):
    base_set_polarization(pol, en)


def grating_to_1200():
    base_grating_to_1200(mono_en, en)


def grating_to_250():
    base_grating_to_250(mono_en, en)
