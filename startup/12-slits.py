run_report(__file__)

from .RSoXSObjects.slits import *

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