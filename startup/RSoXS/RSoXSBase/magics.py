from ..CommonFunctions.functions import run_report, boxed_text

run_report(__file__)

# This file should only be run if ipython is being used ... put that check here!

from IPython.core.magic import register_line_magic

import bluesky.plan_stubs as bps
# motors

from ..RSoXSObjects.motors import (
    sam_Y,
    sam_Th,
    sam_Z,
    sam_X,
    BeamStopS,
    BeamStopW,
    Det_W,
    Det_S,
    Shutter_Y,
    Izero_ds,
    Izero_Y,
    sam_viewer,
)
from ..SSTObjects.motors import Exit_Slit
from .configurations import all_out, WAXSmode, SAXSmode
from ..RSoXSObjects.detectors import (
    set_exposure,
    saxs_det,
    waxs_det,
    snapshot,
    exposure,
)
from ..RSoXSBase.common_metadata import sample, user
from ..RSoXSBase.startup import RE
from ..RSoXSObjects.energy import en, set_polarization


@register_line_magic
def x(line):
    sam_X.status_or_rel_move(line)


@register_line_magic
def y(line):
    sam_Y.status_or_rel_move(line)


@register_line_magic
def z(line):
    sam_Z.status_or_rel_move(line)


@register_line_magic
def th(line):
    sam_Th.status_or_rel_move(line)


@register_line_magic
def bsw(line):
    BeamStopW.status_or_rel_move(line)


@register_line_magic
def bss(line):
    BeamStopS.status_or_rel_move(line)


@register_line_magic
def dw(line):
    Det_W.status_or_rel_move(line)


@register_line_magic
def ds(line):
    Det_S.status_or_rel_move(line)


@register_line_magic
def motors(line):
    boxed_text(
        "RSoXS Motor Locations",
        (
            sam_X.where()
            + "  x"
            + "\n"
            + sam_Y.where()
            + "  y"
            + "\n"
            + sam_Z.where()
            + "  z"
            + "\n"
            + sam_Th.where()
            + "  th"
            + "\n"
            + BeamStopW.where()
            + "  bsw"
            + "\n"
            + BeamStopS.where()
            + "  bss"
            + "\n"
            + Det_W.where()
            + "  dw"
            + "\n"
            + Det_S.where()
            + "  ds"
            + "\n"
            + Shutter_Y.where()
            + "\n"
            + Izero_Y.where()
            + "\n"
            + Izero_ds.where()
            + "\n"
            + Exit_Slit.where()
            + "\n"
            + sam_viewer.where()
            + "\n"
        ),
        "lightgray",
        shrink=True,
    )


del x, y, z, th, ds, dw, bss, bsw, motors


# Energy


@register_line_magic
def e(line):
    try:
        loc = float(line)
    except:
        boxed_text("Beamline Energy", en.where(), "lightpurple", shrink=True)
    else:
        RE(bps.mv(en, loc))
        boxed_text("Beamline Energy", en.where(), "lightpurple", shrink=True)


del e


@register_line_magic
def pol(line):
    try:
        loc = float(line)
    except:
        boxed_text("Beamline Polarization", en.where(), "lightpurple", shrink=True)
    else:
        RE(set_polarization(loc))
        boxed_text("Beamline Polarization", en.where(), "lightpurple", shrink=True)


del pol


### Configurations


@register_line_magic
def nmode(line):
    RE(all_out())


del nmode


@register_line_magic
def wmode(line):
    RE(WAXSmode())


del wmode


@register_line_magic
def smode(line):
    RE(SAXSmode())


del smode

# various


@register_line_magic
def exp(line):
    try:
        secs = float(line)
    except:
        boxed_text("Exposure times", exposure(), "lightgreen", shrink=True)
    else:
        if secs > 0.001 and secs < 1000:
            set_exposure(secs)


del exp


@register_line_magic
def binning(line):
    try:
        bins = int(line)
    except:
        boxed_text(
            "Pixel Binning",
            "   " + saxs_det.binning() + "\n   " + waxs_det.binning(),
            "lightpurple",
            shrink=True,
        )
    else:
        if bins > 0 and bins < 100:
            saxs_det.set_binning(bins, bins)
            waxs_det.set_binning(bins, bins)


del binning


@register_line_magic
def temp(line):
    boxed_text(
        "Detector cooling",
        "   " + saxs_det.cooling_state() + "\n   " + waxs_det.cooling_state(),
        "blue",
        shrink=True,
        width=95,
    )


del temp


@register_line_magic
def cool(line):
    saxs_det.cooling_on()
    waxs_det.cooling_on()


del cool


@register_line_magic
def warm(line):
    saxs_det.cooling_off()
    waxs_det.cooling_off()


del warm


# snapshots


@register_line_magic
def snap(line):
    try:
        secs = float(line)
    except:
        RE(snapshot())
    else:
        if secs > 0 and secs < 100:
            RE(snapshot(secs))


del snap


@register_line_magic
def snapsaxs(line):
    try:
        secs = float(line)
    except:
        RE(snapshot(det=saxs_det))
    else:
        if secs > 0 and secs < 100:
            RE(snapshot(secs, det=saxs_det))


del snapsaxs


@register_line_magic
def snapwaxs(line):
    try:
        secs = float(line)
    except:
        RE(snapshot(det=waxs_det))
    else:
        if secs > 0 and secs < 100:
            RE(snapshot(secs, det=waxs_det))


del snapwaxs


@register_line_magic
def snaps(line):
    try:
        num = int(line)
    except:
        RE(snapshot())
    else:
        if num > 0 and num < 100:
            RE(snapshot(count=num))


del snaps


# metadata (sample/user)


@register_line_magic
def md(line):
    sample()


@register_line_magic
def u(line):
    user()


del md, u

from IPython.terminal.prompts import Prompts, Token
import datetime


class RSoXSPrompt(Prompts):
    def in_prompt_tokens(self, cli=None):
        dt = datetime.datetime.now()
        formatted_date = dt.strftime("%Y-%m-%d")

        if (
            len(RE.md["proposal_id"]) > 0
            and len(RE.md["project_name"]) > 0
            and len(RE.md["cycle"]) > 0
        ):
            RSoXStoken = (
                Token.Prompt,
                "RSoXS "
                + "{}/{}/{}/auto/{}/ ".format(
                    RE.md["cycle"],
                    RE.md["proposal_id"],
                    RE.md["project_name"],
                    formatted_date,
                ),
            )
        else:
            RSoXStoken = (Token.OutPrompt, "RSoXS (define metadata before scanning)")
        return [
            RSoXStoken,
            (Token.Prompt, " ["),
            (Token.PromptNum, str(self.shell.execution_count)),
            (Token.Prompt, "]: "),
        ]


ip = get_ipython()
ip.prompts = RSoXSPrompt(ip)


def beamline_status():
    # user()
    sample()
    boxed_text(
        "Detector status",
        exposure()
        + "\n   "
        + saxs_det.binning()
        + "\n   "
        + waxs_det.binning()
        + "\n   "
        + saxs_det.cooling_state()
        + "\n   "
        + waxs_det.cooling_state()
        + "\n   WAXS "
        + waxs_det.shutter()
        + "\n   SAXS "
        + saxs_det.shutter(),
        "lightblue",
        80,
        shrink=False,
    )


@register_line_magic
def status(line):
    beamline_status()


del status
