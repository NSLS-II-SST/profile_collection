print(f'Loading {__file__}...')

from ophyd import (EpicsMotor, PseudoPositioner, PseudoSingle, Component as Cpt, EpicsSignal, EpicsSignalRO)
from ophyd.pseudopos import (pseudo_position_argument,
                             real_position_argument)

class Slits(PseudoPositioner):
    def __init__(self, *args, **kwargs):
        #self.width = mirror_length
        #self.senter  = mirror_width
        super().__init__(*args, **kwargs)

    def where(self):
        #print("%s:" % self.name.upper())
        text = "      vertical   size   = %7.3f mm            Top      = %7.3f mm\n" % \
               (self.vsize.position,   self.top.user_readback.value)
        text += "      vertical   center = %7.3f mm            Bottom   = %7.3f mm\n" % \
                (self.vcenter.position, self.bottom.user_readback.value)
        text += "      horizontal size   = %7.3f mm            Outboard = %7.3f mm\n" % \
                (self.hsize.position,   self.outboard.user_readback.value)
        text += "      horizontal center = %7.3f mm            Inboard  = %7.3f mm" % \
                (self.hcenter.position, self.inboard.user_readback.value)
        return text
  #  def wh(self):
  #      boxedtext(self.name, self.where(), 'cyan') #bruce's

    # The pseudo positioner axes:
    vsize   = Cpt(PseudoSingle, limits=(-1, 20))
    vcenter = Cpt(PseudoSingle, limits=(-10, 10))
    hsize   = Cpt(PseudoSingle, limits=(-1, 20))
    hcenter = Cpt(PseudoSingle, limits=(-10, 10))

    # The real (or physical) positioners:
    top      = Cpt(EpicsMotor, 'T}Mtr')
    bottom   = Cpt(EpicsMotor, 'B}Mtr')
    inboard  = Cpt(EpicsMotor, 'I}Mtr')
    outboard = Cpt(EpicsMotor, 'O}Mtr')

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



slits1 = Slits('XF:07ID2-ES1{Slt1-Ax:',  name='slits1')
slits2 = Slits('XF:07ID2-ES1{Slt2-Ax:',  name='slits2')
slits3 = Slits('XF:07ID2-ES1{Slt3-Ax:',  name='slits3')
#slits2.top.user_offset.put(-0.038)
#slits2.bottom.user_offset.put(0.264)
sd.baseline.extend([slits1, slits2, slits3 ])