run_report(__file__)

from ophyd import (EpicsMotor, PseudoPositioner, PseudoSingle, Component as Cpt)
from ophyd.pseudopos import (pseudo_position_argument,
                             real_position_argument)

class Slits(PseudoPositioner):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def where(self):
        print("%s:" % self.name)
        text1 = "      vertical   size   = %7.3f mm" % \
               (self.vsize.position) + "\n"
        text1 += "      vertical   center = %7.3f mm" % \
                (self.vcenter.position) + "\n"
        text2 = "      horizontal size   = %7.3f mm" % \
                (self.hsize.position) + "\n"
        text2 += "      horizontal center = %7.3f mm" % \
                (self.hcenter.position) + "\n"
        return text1 + text2
    def wh(self):
        boxed_text(self.name, self.where(), 'cyan') #bruce's

    # The pseudo positioner axes:
    vsize   = Cpt(PseudoSingle, limits=(-1, 20),kind='hinted')
    vcenter = Cpt(PseudoSingle, limits=(-10, 10),kind='normal')
    hsize   = Cpt(PseudoSingle, limits=(-1, 20),kind='hinted')
    hcenter = Cpt(PseudoSingle, limits=(-10, 10),kind='normal')

    # The real (or physical) positioners:
    top      = Cpt(EpicsMotor, 'T}Mtr',kind='normal')
    bottom   = Cpt(EpicsMotor, 'B}Mtr',kind='normal')
    inboard  = Cpt(EpicsMotor, 'I}Mtr',kind='normal')
    outboard = Cpt(EpicsMotor, 'O}Mtr',kind='normal')

    @pseudo_position_argument
    def forward(self, pseudo_pos):
        '''Run a forward (pseudo -> real) calculation'''
        return self.RealPosition(top      = pseudo_pos.vcenter + pseudo_pos.vsize/2,
                                 bottom   = pseudo_pos.vcenter - pseudo_pos.vsize/2,
                                 outboard = pseudo_pos.hcenter + pseudo_pos.hsize/2,
                                 inboard  = pseudo_pos.hcenter - pseudo_pos.hsize/2
            )

    @real_position_argument
    def inverse(self, real_pos):
        '''Run an inverse (real -> pseudo) calculation'''
        return self.PseudoPosition(hsize   =  real_pos.outboard - real_pos.inboard,
                                   hcenter = (real_pos.outboard + real_pos.inboard)/2,
                                   vsize   =  real_pos.top      - real_pos.bottom,
                                   vcenter = (real_pos.top      + real_pos.bottom )/2,

        )


slits1 = Slits('XF:07ID2-ES1{Slt1-Ax:',  name='Upstream Scatter Slits', kind='hinted',concurrent=1)
slits2 = Slits('XF:07ID2-ES1{Slt2-Ax:',  name='Middle Scatter Slits', kind='hinted',concurrent=1)
slits3 = Slits('XF:07ID2-ES1{Slt3-Ax:',  name='Final Scatter Slits', kind='hinted',concurrent=1)


def set_slit_offsets():
    yield from bps.mv(slits3.bottom.user_offset,-1.39,
                      slits3.top.user_offset,-1.546,
                      slits3.outboard.user_offset,-.651,
                      slits3.inboard.user_offset,.615,
                      slits2.inboard.user_offset,-0.84,
                      slits2.outboard.user_offset,-1.955,
                      slits2.bottom.user_offset,-1.548,
                      slits2.top.user_offset,-2.159,
                      slits1.inboard.user_offset,-.273,
                      slits1.outboard.user_offset,-2.2050,
                      slits1.top.user_offset,-1.54,
                      slits1.bottom.user_offset,-.86)

sd.baseline.extend([slits1, slits2, slits3 ])