from ophyd import EpicsMotor, EpicsSignal, PositionerBase, Device, Signal
from ophyd import Component as Cpt
from ophyd.status import wait as status_wait
import bluesky.plan_stubs as bps
from ..CommonFunctions.functions import boxed_text, colored, whisper
from ..CommonFunctions.functions import run_report


run_report(__file__)


class FMBOEpicsMotor(EpicsMotor):
    resolution = Cpt(EpicsSignal, ".MRES")
    encoder = Cpt(EpicsSignal, ".REP")
    clr_enc_lss = Cpt(EpicsSignal, "_ENC_LSS_CLR_CMD.PROC")
    home_cmd = Cpt(EpicsSignal, "_HOME_CMD.PROC")
    enable = Cpt(EpicsSignal, "_ENA_CMD.PROC")
    kill = Cpt(EpicsSignal, "_KILL_CMD.PROC")

    status_list = (
        "MTACT",
        "MLIM",
        "PLIM",
        "AMPEN",
        "LOOPM",
        "TIACT",
        "INTMO",
        "DWPRO",
        "DAERR",
        "DVZER",
        "ABDEC",
        "UWPEN",
        "UWSEN",
        "ERRTAG",
        "SWPOC",
        "ASSCS",
        "FRPOS",
        "HSRCH",
        "SODPL",
        "SOPL",
        "HOCPL",
        "PHSRA",
        "PREFE",
        "TRMOV",
        "IFFE",
        "AMFAE",
        "AMFE",
        "FAFOE",
        "WFOER",
        "INPOS",
        "ENC_LSS",
    )

    ###################################################################
    # this is the complete list of status signals defined in the FMBO #
    # IOC for thier MCS8 motor controllers                            #
    ###################################################################
    mtact = Cpt(EpicsSignal, "_MTACT_STS")
    mtact_desc = Cpt(EpicsSignal, "_MTACT_STS.DESC")
    mlim = Cpt(EpicsSignal, "_MLIM_STS")
    mlim_desc = Cpt(EpicsSignal, "_MLIM_STS.DESC")
    plim = Cpt(EpicsSignal, "_PLIM_STS")
    plim_desc = Cpt(EpicsSignal, "_PLIM_STS.DESC")
    ampen = Cpt(EpicsSignal, "_AMPEN_STS")
    ampen_desc = Cpt(EpicsSignal, "_AMPEN_STS.DESC")
    loopm = Cpt(EpicsSignal, "_LOOPM_STS")
    loopm_desc = Cpt(EpicsSignal, "_LOOPM_STS.DESC")
    tiact = Cpt(EpicsSignal, "_TIACT_STS")
    tiact_desc = Cpt(EpicsSignal, "_TIACT_STS.DESC")
    intmo = Cpt(EpicsSignal, "_INTMO_STS")
    intmo_desc = Cpt(EpicsSignal, "_INTMO_STS.DESC")
    dwpro = Cpt(EpicsSignal, "_DWPRO_STS")
    dwpro_desc = Cpt(EpicsSignal, "_DWPRO_STS.DESC")
    daerr = Cpt(EpicsSignal, "_DAERR_STS")
    daerr_desc = Cpt(EpicsSignal, "_DAERR_STS.DESC")
    dvzer = Cpt(EpicsSignal, "_DVZER_STS")
    dvzer_desc = Cpt(EpicsSignal, "_DVZER_STS.DESC")
    abdec = Cpt(EpicsSignal, "_ABDEC_STS")
    abdec_desc = Cpt(EpicsSignal, "_ABDEC_STS.DESC")
    uwpen = Cpt(EpicsSignal, "_UWPEN_STS")
    uwpen_desc = Cpt(EpicsSignal, "_UWPEN_STS.DESC")
    uwsen = Cpt(EpicsSignal, "_UWSEN_STS")
    uwsen_desc = Cpt(EpicsSignal, "_UWSEN_STS.DESC")
    errtg = Cpt(EpicsSignal, "_ERRTG_STS")
    errtg_desc = Cpt(EpicsSignal, "_ERRTG_STS.DESC")
    swpoc = Cpt(EpicsSignal, "_SWPOC_STS")
    swpoc_desc = Cpt(EpicsSignal, "_SWPOC_STS.DESC")
    asscs = Cpt(EpicsSignal, "_ASSCS_STS")
    asscs_desc = Cpt(EpicsSignal, "_ASSCS_STS.DESC")
    frpos = Cpt(EpicsSignal, "_FRPOS_STS")
    frpos_desc = Cpt(EpicsSignal, "_FRPOS_STS.DESC")
    hsrch = Cpt(EpicsSignal, "_HSRCH_STS")
    hsrch_desc = Cpt(EpicsSignal, "_HSRCH_STS.DESC")
    sodpl = Cpt(EpicsSignal, "_SODPL_STS")
    sodpl_desc = Cpt(EpicsSignal, "_SODPL_STS.DESC")
    sopl = Cpt(EpicsSignal, "_SOPL_STS")
    sopl_desc = Cpt(EpicsSignal, "_SOPL_STS.DESC")
    hocpl = Cpt(EpicsSignal, "_HOCPL_STS")
    hocpl_desc = Cpt(EpicsSignal, "_HOCPL_STS.DESC")
    phsra = Cpt(EpicsSignal, "_PHSRA_STS")
    phsra_desc = Cpt(EpicsSignal, "_PHSRA_STS.DESC")
    prefe = Cpt(EpicsSignal, "_PREFE_STS")
    prefe_desc = Cpt(EpicsSignal, "_PREFE_STS.DESC")
    trmov = Cpt(EpicsSignal, "_TRMOV_STS")
    trmov_desc = Cpt(EpicsSignal, "_TRMOV_STS.DESC")
    iffe = Cpt(EpicsSignal, "_IFFE_STS")
    iffe_desc = Cpt(EpicsSignal, "_IFFE_STS.DESC")
    amfae = Cpt(EpicsSignal, "_AMFAE_STS")
    amfae_desc = Cpt(EpicsSignal, "_AMFAE_STS.2ESC")
    amfe = Cpt(EpicsSignal, "_AMFE_STS")
    amfe_desc = Cpt(EpicsSignal, "_AMFE_STS.DESC")
    fafoe = Cpt(EpicsSignal, "_FAFOE_STS")
    fafoe_desc = Cpt(EpicsSignal, "_FAFOE_STS.DESC")
    wfoer = Cpt(EpicsSignal, "_WFOER_STS")
    wfoer_desc = Cpt(EpicsSignal, "_WFOER_STS.DESC")
    inpos = Cpt(EpicsSignal, "_INPOS_STS")
    inpos_desc = Cpt(EpicsSignal, "_INPOS_STS.DESC")
    enc_lss = Cpt(EpicsSignal, "_ENC_LSS_STS")
    enc_lss_desc = Cpt(EpicsSignal, "_ENC_LSS_STS.DESC")

    def home(self, *args, **kwargs):
        yield from bps.mv(self.home_cmd, 1)

    def clear_encoder_loss(self):
        yield from bps.mv(self.clr_enc_lss, 1)

    def status(self):
        text = "\n  EPICS PV Base : %s\n\n" % (self.prefix)
        for signal in self.status_list:
            if signal.upper() not in self.status_list:
                continue
            suffix = getattr(self, signal).pvname.replace(self.prefix, "")
            if getattr(self, signal).get():
                value_color = "lightgreen"
            else:
                value_color = "lightred"

            text += "  %-26s : %-35s  %s   %s \n" % (
                getattr(self, signal + "_desc").get(),
                colored(
                    getattr(self, signal).enum_strs[getattr(self, signal).get()],
                    value_color,
                ),
                colored(getattr(self, signal).get(), value_color),
                whisper(suffix),
            )
        boxed_text("%s status signals" % self.name, text, "green", shrink=True)


class PrettyMotor(EpicsMotor):
    def __init__(self, *args, **kwargs):
        super(PrettyMotor, self).__init__(*args, **kwargs)
        self.read_attrs = ["user_readback", "user_setpoint"]

    def where(self):
        return ("{} : {}").format(
            colored(self.name, "lightblue"),
            colored(
                "{:.2f}".format(self.user_readback.get()).rstrip("0").rstrip("."),
                "yellow",
            ),
        )

    def where_sp(self):
        return ("{} Setpoint : {}\n{} Readback : {}").format(
            colored(self.name, "lightblue"),
            colored(
                "{:.2f}".format(self.user_readback.get()).rstrip("0").rstrip("."),
                "yellow",
            ),
            colored(self.name, "lightblue"),
            colored(
                "{:.2f}".format(self.user_setpoint.get()).rstrip("0").rstrip("."),
                "yellow",
            ),
        )

    def wh(self):
        boxed_text(self.name + " location", self.where_sp(), "green", shrink=True)

    def status_or_rel_move(self, line):
        try:
            loc = float(line)
        except:
            if len(line) > 0:
                if line[0] == "s":
                    self.status()  # followed by an s, display status
                elif line[0] == "a":
                    try:
                        loc = float(line[1:])
                    except:
                        # followed by an a but not a number, just display location
                        boxed_text(self.name, self.where_sp(), "lightgray", shrink=True)
                    else:
                        # followed by an a and a number, do absolute move
                        yield from bps.mv(self, loc)
                        boxed_text(self.name, self.where_sp(), "lightgray", shrink=True)
                else:
                    # followed by something besides a number, a or s, just show location
                    boxed_text(self.name, self.where_sp(), "lightgray", shrink=True)
            else:
                # followed by something besides a number, a or s, just show location
                boxed_text(self.name, self.where_sp(), "lightgray", shrink=True)
        else:
            # followed by a number - relative move
            yield from bps.mvr(self, loc)
            boxed_text(self.name, self.where(), "lightgray", shrink=True)


class PrettyMotorFMBO(FMBOEpicsMotor, PrettyMotor):
    pass

class DeadbandMixin(Device, PositionerBase):
    """
    Should be the leftmost class in the inheritance list so that it grabs move first!
    Must be combined with either EpicsMotor or PVPositioner, or some other class
    that has a done_value attribute
    An EpicsMotor subclass that has an absolute tolerance for moves.
    If the readback is within tolerance of the setpoint, the MoveStatus
    is marked as finished, even if the motor is still settling.
    This prevents motors with long, but irrelevant, settling times from
    adding overhead to scans.
    """
    tolerance = Cpt(Signal, value=-1, kind='config')
    move_latch = Cpt(Signal, value=0, kind="omitted")

    def _done_moving(self, success=True, timestamp=None, value=None, **kwargs):
        '''Call when motion has completed.  Runs ``SUB_DONE`` subscription.'''
        if self.move_latch.get():
            # print(f"{timestamp}: {self.name} marked done")
            if success:
                self._run_subs(sub_type=self.SUB_DONE, timestamp=timestamp,
                               value=value)

            self._run_subs(sub_type=self._SUB_REQ_DONE, success=success,
                           timestamp=timestamp)
            self._reset_sub(self._SUB_REQ_DONE)
            self.move_latch.put(0)

    def move(self, position, wait=True, **kwargs):
        tolerance = self.tolerance.get()

        if tolerance < 0:
            self.move_latch.put(1)
            return super().move(position, wait=wait, **kwargs)
        else:
            status = super().move(position, wait=False, **kwargs)
            setpoint = position
            done_value = getattr(self, "done_value", 1)
            def check_deadband(value, timestamp, **kwargs):
                if abs(value - setpoint) < tolerance:
                    self._done_moving(timestamp=timestamp,
                                      success=True,
                                      value=done_value)
                else:
                    pass
                    # print(f"{timestamp}: {self.name}, {value} not within {tolerance} of {setpoint}")

            def clear_deadband(*args, timestamp, **kwargs):
                # print(f"{timestamp}: Ran deadband clear for {self.name}")
                self.clear_sub(check_deadband, event_type=self.SUB_READBACK)

            self.subscribe(clear_deadband, event_type=self._SUB_REQ_DONE, run=False)
            self.move_latch.put(1)
            self.subscribe(check_deadband, event_type=self.SUB_READBACK, run=True)

            try:
                if wait:
                    status_wait(status)
            except KeyboardInterrupt:
                self.stop()
                raise

            return status
