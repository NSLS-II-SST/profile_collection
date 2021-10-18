from ophyd import (
    Component as Cpt,
    Device,
    EpicsSignal,
)
import time
import bluesky.plan_stubs as bps
import bluesky.plans as bp
from ..CommonFunctions.functions import run_report


run_report(__file__)


class EPS_Shutter(Device):
    state = Cpt(EpicsSignal, "Pos-Sts")
    cls = Cpt(EpicsSignal, "Cmd:Cls-Cmd")
    opn = Cpt(EpicsSignal, "Cmd:Opn-Cmd")
    error = Cpt(EpicsSignal, "Err-Sts")
    maxcount = 3
    openval = 1  # normal shutter values, FS1 is reversed
    closeval = 0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def status(self):
        if self.state.get() == self.closeval:
            return "closed"
        else:
            return "open"

    def open_plan(self):
        count = 0
        while self.state.get() != self.openval:
            count += 1
            print(u"\u231b", end=" ", flush=True)
            yield from bps.mv(self.opn, 1)
            if count >= self.maxcount:
                print(
                    "tried %d times and failed to open %s %s" % (count, self.name, ":(")
                )  # u'\u2639'  unicode frown
                return (yield from bps.null())
            yield from bps.sleep(1.5)
        print("Opened {}".format(self.name))

    def close_plan(self):
        count = 0
        while self.state.get() != self.closeval:
            count += 1
            print(u"\u231b", end=" ", flush=True)
            yield from bps.mv(self.cls, 1)
            if count >= self.maxcount:
                print(
                    "tried %d times and failed to close %s %s"
                    % (count, self.name, ":(")
                )
                return (yield from bps.null())
            yield from bps.sleep(1.5)
        print("Closed {}".format(self.name))

    def open(self):
        self.read()
        if self.state.get() != self.openval:
            count = 0
            while self.state.get() != self.openval:
                count += 1
                print(u"\u231b", end=" ", flush=True)
                self.opn.set(1)
                if count >= self.maxcount:
                    print(
                        "tried %d times and failed to open %s %s"
                        % (count, self.name, ":(")
                    )
                    return
                time.sleep(1.5)
                self.read()
            print(" Opened {}".format(self.name))
        else:
            print("{} is open".format(self.name))

    def close(self):
        self.read()
        if self.state.get() != self.closeval:
            count = 0
            while self.state.get() != self.closeval:
                count += 1
                print(u"\u231b", end=" ", flush=True)
                self.cls.set(1)
                if count >= self.maxcount:
                    print(
                        "tried %d times and failed to close %s %s"
                        % (count, self.name, ":(")
                    )
                    return
                time.sleep(1.5)
                self.read()
            print(" Closed {}".format(self.name))
        else:
            print("{} is closed".format(self.name))
