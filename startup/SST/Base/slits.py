from ophyd import EpicsMotor, PseudoPositioner, PseudoSingle, Component as Cpt
from ophyd.pseudopos import pseudo_position_argument, real_position_argument
from ..CommonFunctions.functions import boxed_text, run_report


run_report(__file__)


class Slits(PseudoPositioner):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def where(self):
        print("%s:" % self.name)
        text1 = "      vertical   size   = %7.3f mm" % (self.vsize.position) + "\n"
        text1 += "      vertical   center = %7.3f mm" % (self.vcenter.position) + "\n"
        text2 = "      horizontal size   = %7.3f mm" % (self.hsize.position) + "\n"
        text2 += "      horizontal center = %7.3f mm" % (self.hcenter.position) + "\n"
        return text1 + text2

    def wh(self):
        boxed_text(self.name, self.where(), "cyan")  # bruce's

    # The pseudo positioner axes:
    vsize = Cpt(PseudoSingle, limits=(-1, 20), kind="hinted")
    vcenter = Cpt(PseudoSingle, limits=(-10, 10), kind="normal")
    hsize = Cpt(PseudoSingle, limits=(-1, 20), kind="hinted")
    hcenter = Cpt(PseudoSingle, limits=(-10, 10), kind="normal")

    # The real (or physical) positioners:
    top = Cpt(EpicsMotor, "T}Mtr", kind="normal")
    bottom = Cpt(EpicsMotor, "B}Mtr", kind="normal")
    inboard = Cpt(EpicsMotor, "I}Mtr", kind="normal")
    outboard = Cpt(EpicsMotor, "O}Mtr", kind="normal")

    @pseudo_position_argument
    def forward(self, pseudo_pos):
        """Run a forward (pseudo -> real) calculation"""
        return self.RealPosition(
            top=pseudo_pos.vcenter + pseudo_pos.vsize / 2,
            bottom=pseudo_pos.vcenter - pseudo_pos.vsize / 2,
            outboard=pseudo_pos.hcenter + pseudo_pos.hsize / 2,
            inboard=pseudo_pos.hcenter - pseudo_pos.hsize / 2,
        )

    @real_position_argument
    def inverse(self, real_pos):
        """Run an inverse (real -> pseudo) calculation"""
        return self.PseudoPosition(
            hsize=real_pos.outboard - real_pos.inboard,
            hcenter=(real_pos.outboard + real_pos.inboard) / 2,
            vsize=real_pos.top - real_pos.bottom,
            vcenter=(real_pos.top + real_pos.bottom) / 2,
        )
