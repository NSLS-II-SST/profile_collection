run_report(__file__)

import time
from ophyd import (EpicsSignal, EpicsSignalRO, EpicsSignalWithRBV, Device, Component, DeviceStatus,
                   Staged, Signal)
from ophyd.areadetector import (ADComponent as ADCpt, EpicsSignalWithRBV, ImagePlugin, StatsPlugin, DetectorBase,
                                SingleTrigger, ADBase)
from ophyd.status import DeviceStatus

# These might need/make more sense to be split up into separate files later on.
# But while we have so few, I'm just putting them in this single file.

bpm13_sum = EpicsSignalRO('XF:07ID-BI{BPM:13}Stats5:Total_RBV', name='Downstream Izero Phosphor Intensity')

ring_current = EpicsSignalRO('SR:OPS-BI{DCCT:1}I:Real-I', name='NSLS-II Ring Current', kind='normal')


class I400(SingleTrigger, DetectorBase):
    _default_read_attrs = None
    _default_configuration_attrs = None

    _status_type = DeviceStatus
    gain = Component(Signal, ':RANGE_BP')
    exposure_time = Component(Signal, ':PERIOD_SP',put_complete=True)
    acquisition_mode = Component(Signal, ':GETCS.SCAN')
    acquisition_mode1 = Component(Signal, ':GETCS2.SCAN')
    acquire = Component(Signal, ':GETCS',put_complete=True)  # Rely on the IOC to signal done-ness.
    enabled = Component(Signal, ':ENABLE_IC_UPDATES')
    exptime_save = .5
    gain_save = 7
    ignore_triggers = 0
    trigger_count = 0

    def trigger(self):
        """
        Trigger the detector and return a Status object.
        """
        if not self._staged == Staged.yes:
            raise RuntimeError("Device must be staged before triggering.")

        if self.trigger_count > 0:
            if self.trigger_count >= self.ignore_triggers:
                self.trigger_count = 0
            else:
                self.trigger_count += 1
        if self.trigger_count == 0:
            self.trigger_count += 1
            self.status = DeviceStatus(self)
            self.acquire.put(1, callback= self.status._finished)
        return self.status

    def set_exposure(self, exptime):
        exptimeset = min(exptime,20)
        print('setting ',self.name,' exposure to ',exptimeset)
        self.exptime_save = exptimeset

    def exposure(self):
        return ('{} exposure time is set to {} seconds'.format(
            colored(self.name,'lightblue'),
            colored(self.exptime_save,'lightgreen')
        ))

    def stage(self):
        self.kind = 'hinted'
        output = [super().stage()]
        self.acquisition_mode.set(0)
        self.acquisition_mode1.set(0)
        self.exposure_time.set(self.exptime_save)
        self.gain.set(self.gain_save)
        return output.append(self)

    def unstage(self):
        self.kind = 'normal'
        self.acquisition_mode.set(7)
        self.acquisition_mode1.set(7)
        self.exposure_time.set(.4)
        return [self].append(super().unstage())



    Channel_1 = Component(StatsPlugin, ':IC1_MON', kind='hinted')
    Channel_2 = Component(StatsPlugin, ':IC2_MON', kind='hinted')
    Channel_3 = Component(StatsPlugin, ':IC3_MON', kind='hinted')
    Channel_4 = Component(StatsPlugin, ':IC4_MON', kind='hinted')


RSoXS_Diodes = I400('XF:07ID-ES1{DMR:I400-1}', name='I400 diode')
RSoXS_Diodes.gain_save = 6
RSoXS_DrainCurrent = I400('XF:07ID-ES1{Slt1:I400-1}', name='I400 drain')
RSoXS_DrainCurrent.gain_save = 4

Beamstop_WAXS = RSoXS_Diodes.Channel_1
Beamstop_WAXS.name = 'WAXS Beamstop'
Beamstop_SAXS = RSoXS_Diodes.Channel_2
Beamstop_SAXS.name = 'SAXS Beamstop'
IzeroMesh = RSoXS_DrainCurrent.Channel_4 # previously DM channel 3
IzeroMesh.name = 'Izero Mesh'
IzeroDiode = RSoXS_Diodes.Channel_4
IzeroDiode.name = 'Izero Photodiode'



SlitOut_I = RSoXS_DrainCurrent.Channel_1
SlitOut_I.name = 'Slit Outboard'
SlitBottom_I = RSoXS_DrainCurrent.Channel_2
SlitBottom_I.name = 'Slit Bottom'
SlitTop_I = RSoXS_DrainCurrent.Channel_3
SlitTop_I.name = 'Slit Top'
#SlitInboard_I = RSoXS_Slits.Channel_4
#SlitInboard_I.name = 'RSoXS Slit Inboard Current'


Downstream_I400 = I400('XF:07ID-BI{DM7:I400-1}', name='Downstream Diagnostic')
TransmissionDiode = Downstream_I400.Channel_4
TransmissionDiode.name = 'RSoXS Transmission Photodiode'




DM4_PD = EpicsSignal('XF:07ID-BI{DM5:F4}Cur:I3-I', name='DM4 Current', kind='hinted')


sd.monitors.extend([ring_current])
sd.baseline.extend([ring_current])
# Not sure how best to do this image yet... 

#BPM13 Image:
#XF:07ID-BI{BPM:13}image1:ArrayData
