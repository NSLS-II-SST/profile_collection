from ophyd import EpicsSignal, PVPositionerPC, Signal, Component
from ophyd.status import SubscriptionStatus
from ..CommonFunctions.functions import run_report


run_report(__file__)


Shutter_enable = EpicsSignal(
    "XF:07IDB-CT{DIODE-MTO:1}OutMaskBit:2-Sel",
    name="RSoXS Shutter Toggle Enable",
    kind="normal",
)
Shutter_enable1 = EpicsSignal(
    "XF:07IDB-CT{DIODE-MTO:1}InMaskBit:1-Sel",
    name="RSoXS Shutter Toggle Enable In",
    kind="normal",
)
Shutter_enable2 = EpicsSignal(
    "XF:07IDB-CT{DIODE-MTO:1}InMaskBit:2-Sel",
    name="RSoXS Shutter Toggle Enable In2",
    kind="normal",
    put_complete=False,
    auto_monitor=False,
)
Shutter_enable3 = EpicsSignal(
    "XF:07IDB-CT{DIODE-MTO:1}InMaskBit:3-Sel",
    name="RSoXS Shutter Toggle Enable In3",
    kind="normal",
)
Shutter_control = EpicsSignal(
    "XF:07IDB-CT{DIODE-Local:1}OutPt01:Data-Sel",
    name="RSoXS Shutter Toggle",
    kind="normal",
)
Shutter_delay = EpicsSignal(
    "XF:07IDB-CT{DIODE-MTO:1}OutDelaySet:2-SP",
    name="RSoXS Shutter Delay (ms)",
    kind="normal",
)
Shutter_open_time = EpicsSignal(
    "XF:07IDB-CT{DIODE-MTO:1}OutWidthSet:2-SP",
    name="RSoXS Shutter Opening Time (ms)",
    kind="normal",
)
Shutter_trigger = EpicsSignal(
    "XF:07IDB-CT{DIODE-MTO:1}Trigger:PV-Cmd",
    name="RSoXS Shutter Trigger",
    kind="normal",
)
Light_control = EpicsSignal(
    "XF:07IDB-CT{DIODE-Local:1}OutPt05:Data-Sel",
    name="RSoXS Light Toggle",
    kind="normal",
)

class ShutterSet(PVPositionerPC):
    readback = Component(EpicsSignal,'-RB')
    setpoint = Component(EpicsSignal,'-SP')

    def set(self, value,*args,**kwargs):
        if value is None:
            saw_rise = False

            def watcher(*,old_value,value,**kwargs):
                nonlocal saw_rise
                if value == 1:
                    saw_rise = True
                    return False
                if value == 0 and saw_rise:
                    return True
            return SubscriptionStatus(self.readback, watcher)
        else:
            return super().set(value, *args, **kwargs)



shutter_open_set = ShutterSet('XF:07IDB-CT{DIODE-MTO:1}Output:2',name = "Shutter Open with Watcher")
