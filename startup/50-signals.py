print(f'Loading {__file__}...')

import time
from ophyd import (EpicsSignal, EpicsSignalRO, Device, Component, DeviceStatus,
                   Staged)

# These might need/make more sense to be split up into separate files later on.
# But while we have so few, I'm just putting them in this single file.

bpm13_sum = EpicsSignalRO('XF:07ID-BI{BPM:13}Stats5:Total_RBV', name='Downstream Izero Phosphor Intensity')

ring_current = EpicsSignalRO('SR:OPS-BI{DCCT:1}I:Real-I', name='NSLS-II Ring Current', kind='normal')





class I400(Device):
    gain = Component(EpicsSignal, ':RANGE_BP')
    exposure_time = Component(EpicsSignal, ':PERIOD_SP')
    acquisition_mode = Component(EpicsSignal, ':GETCS.SCAN')
    acquisition_mode1 = Component(EpicsSignal, ':GETCS2.SCAN')
    acquire = Component(EpicsSignal, ':GETCS', put_complete=True)  # Rely on the IOC to signal done-ness.
    enabled = Component(EpicsSignal, ':ENABLE_IC_UPDATES')
    exptime_save = .5

    def trigger(self):
        """
        Trigger the detector and return a Status object.
        """
        if not self._staged == Staged.yes:
            raise RuntimeError("Device must be staged before triggering.")
        status = DeviceStatus(self)
        self.acquire.put(1, callback= status._finished)
        return status

    def set_exposure(self, exptime):
        print('setting exposure to ',exptime)
        self.exptime_save = exptime

    def stage(self):
        # print('staging')
        self.kind = 'hinted'
        self.acquisition_mode.set(0)
        self.acquisition_mode1.set(0)
        self.exposure_time.set(self.exptime_save)
        return [self]

    def unstage(self):
        # print('unstaging')
        self.kind = 'normal'
        self.acquisition_mode.set(7)
        self.acquisition_mode1.set(7)
        self.exposure_time.set(.4)
        return [self]

    class I400Channel(EpicsSignal):
        # readback = Component(EpicsSignalRO, '', kind='hinted')

        # def read(self):
        #     value = self.get().readback
        #     return{self.name: {'value': value,'timestamp': time.time()}}

        def trigger(self):
            """
            Trigger the detector and return a Status object.
            """
            self.kind = 'hinted'
            st = self.parent.trigger()
            self.kind = 'normal'
            return st

        def set_exposure(self, exptime):
            self.parent.set_exposure(exptime)

        def stage(self):
            self.parent.stage()
            print('staging channel')
            self.parent.acquisition_mode.set(0)
            self.parent.acquisition_mode1.set(0)
            self.parent.exposure_time.set(self.exptime_save)
            self.kind = 'hinted'
            return [self].append(super().stage())

        def unstage(self):
            print('unstaging channel')
            self.kind = 'normal'
            self.parent.acquisition_mode.set(7)
            self.parent.acquisition_mode1.set(7)
            self.parent.exposure_time.set(.4)
            return [self].append(super().unstage())

    Channel_1 = Component(I400Channel, ':IC1_MON', kind='normal')
    Channel_2 = Component(I400Channel, ':IC2_MON', kind='normal')
    Channel_3 = Component(I400Channel, ':IC3_MON', kind='normal')
    Channel_4 = Component(I400Channel, ':IC4_MON', kind='normal')


RSoXS_DM = I400('XF:07ID-ES1{DMR:I400-1}', name='RSoXS Diagnostic Picoammeter')
BSW_I = RSoXS_DM.Channel_1
BSW_I.name = 'RSoXS WAXS Beamstop Current'
BSS_I = RSoXS_DM.Channel_2
BSS_I.name = 'RSoXS SAXS Beamstop Current'
IzeroMesh = RSoXS_DM.Channel_3
IzeroMesh.name = 'Izero Mesh Drain Current'
IzeroDiode = RSoXS_DM.Channel_4
IzeroDiode.name = 'Izero Diode Current'


RSoXS_Slits = I400('XF:07ID-ES1{Slt1:I400-1}', name='RSoXS Slits Picoammeter')
SlitOut_I = RSoXS_Slits.Channel_1
SlitOut_I.name = 'RSoXS Slit Outboard Current'
SlitBottom_I = RSoXS_Slits.Channel_2
SlitBottom_I.name = 'RSoXS Slit Bottom Current'
SlitTop_I = RSoXS_Slits.Channel_3
SlitTop_I.name = 'RSoXS Slit Top Current'
SlitInboard_I = RSoXS_Slits.Channel_4
SlitInboard_I.name = 'RSoXS Slit Inboard Current'


Downstream_I400 = I400('XF:07ID-BI{DM7:I400-1}', name='RSoXS Downstream Picoammeter')
TransmissionDiode = Downstream_I400.Channel_4
TransmissionDiode.name = 'RSoXS Transmission Photodiode'




# dm3_c1 = EpicsSignalRO('XF:07ID-BI{DM3:I400-1}:IC1_MON', name='Diagnostic Module 3 Current')
# BeamstopW_I = EpicsSignal('XF:07ID-ES1{DMR:I400-1}:IC1_MON', name='WAXS Beamstop Current', kind='normal')
# BeamstopS_I = EpicsSignal('XF:07ID-ES1{DMR:I400-1}:IC2_MON', name='SAXS Beamstop Current', kind='normal')
# IzeroMesh   = EpicsSignal('XF:07ID-ES1{DMR:I400-1}:IC3_MON', name='Izero Mesh Drain Current', kind='normal')
# IzeroDiode  = EpicsSignal('XF:07ID-ES1{DMR:I400-1}:IC4_MON', name='Izero Diode Current', kind='normal')
DM4_PD = EpicsSignal('XF:07ID-BI{DM5:F4}Cur:I1-I', name='DM4 Current', kind='hinted')


sd.monitors.extend([IzeroMesh, ring_current])
sd.baseline.extend([IzeroMesh, ring_current, IzeroDiode, BSW_I, BSS_I])
# Not sure how best to do this image yet... 

#BPM13 Image:
#XF:07ID-BI{BPM:13}image1:ArrayData
