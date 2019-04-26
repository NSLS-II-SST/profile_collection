print(f'Loading {__file__}...')

from ophyd import (SingleTrigger, Component as Cpt, Device, PVPositioner, EpicsSignal, EpicsSignalRO)
import time

class EPS_Shutter(Device):
    state = Cpt(EpicsSignal, 'Pos-Sts')
    cls = Cpt(EpicsSignal, 'Cmd:Cls-Cmd')
    opn = Cpt(EpicsSignal, 'Cmd:Opn-Cmd')
    error = Cpt(EpicsSignal,'Err-Sts')
    maxcount = 3
    openval = 1                 # normal shutter values, FS1 is reversed
    closeval = 0


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.color = 'red'

    def status(self):
        if self.state.value == self.closeval:
            return 'closed'
        else:
            return 'open'

    def open_plan(self):
        #RE.msg_hook = None
        count = 0
        while self.state.value == self.openval:
            count += 1
            print(u'\u231b', end=' ', flush=True)
            yield from bps.mv(self.opn, 1)
            if count >= self.maxcount:
                print('tried %d times and failed to open %s %s' % (count, self.name, ':('))  # u'\u2639'  unicode frown
                return(yield from null())
            time.sleep(1.5)
        print('Opened {}'.format(self.name))
        #RE.msg_hook = BMM_msg_hook

    def close_plan(self):
        #RE.msg_hook = None
        count = 0
        while self.state.value != self.closeval:
            count += 1
            print(u'\u231b', end=' ', flush=True)
            yield from bps.mv(self.cls, 1)
            if count >= self.maxcount:
                print('tried %d times and failed to close %s %s' % (count, self.name, ':('))
                return(yield from null())
            time.sleep(1.5)
        print('Closed {}'.format(self.name))
        #RE.msg_hook = BMM_msg_hook

    def open(self):
        #RE.msg_hook = None
        self.read()
        if self.state.value != self.openval:
            count = 0
            while self.state.value != self.openval:
                count += 1
                print(u'\u231b', end=' ', flush=True)
                yield from bps.mv(self.opn, 1)
                if count >= self.maxcount:
                    print('tried %d times and failed to open %s %s' % (count, self.name, ':('))
                    return
                time.sleep(1.5)
                self.read()
            print(' Opened {}'.format(self.name))
        else:
            print('{} is open'.format(self.name))
       #RE.msg_hook = BMM_msg_hook

    def close(self):
        #RE.msg_hook = None
        self.read()
        if self.state.value != self.closeval:
            count = 0
            while self.state.value != self.closeval:
                count += 1
                print(u'\u231b', end=' ', flush=True)
                yield from bps.mv(self.cls, 1)
                if count >= self.maxcount:
                    print('tried %d times and failed to close %s %s' % (count, self.name, ':('))
                    return
                time.sleep(1.5)
                self.read()
            print(' Closed {}'.format(self.name))
        else:
            print('{} is closed'.format(self.name))
        #RE.msg_hook = BMM_msg_hook

psh1 = EPS_Shutter('XF:07ID-PPS{Sh:FE}', name = 'Front-End Shutter',kind='hinted')
psh1.shutter_type = 'FE'
psh1.openval  = 0
psh1.closeval = 1

psh4 = EPS_Shutter('XF:07IDA-PPS{PSh:4}', name = 'Hutch Photon Shutter',kind='hinted')
psh4.shutter_type = 'PH'
psh4.openval  = 0
psh4.closeval = 1

psh10 = EPS_Shutter('XF:07IDA-PPS{PSh:10}', name = 'Upstream Photon Shutter',kind='hinted')
psh10.shutter_type = 'PH'
psh10.openval  = 0
psh10.closeval = 1

psh7 = EPS_Shutter('XF:07IDA-PPS{PSh:7}', name = 'Downstream Photon Shutter',kind='hinted')
psh7.shutter_type = 'PH'
psh10.openval  = 0
psh10.closeval = 1


gv14 = EPS_Shutter('XF:07IDA-VA:2{FS:6-GV:1}', name = 'Pre Mono Gate Valve',kind='hinted')
psh10.shutter_type = 'GV'
psh10.openval  = 0
psh10.closeval = 1

gv14a = EPS_Shutter('XF:07IDA-VA:2{FS:6-GV:2}', name = 'Mono Gate Valve',kind='hinted')
psh10.shutter_type = 'GV'
psh10.openval  = 0
psh10.closeval = 1

gv15 = EPS_Shutter('XF:07IDB-VA:2{Mono:PGM-GV:1}', name = 'Pre Shutter Gate Valve',kind='hinted')
psh10.shutter_type = 'GV'
psh10.openval  = 0
psh10.closeval = 1

gv26 = EPS_Shutter('XF:07IDB-VA:2{Mir:M3C-GV:1}', name = 'Post Shutter Gate Valve',kind='hinted')
psh10.shutter_type = 'GV'
psh10.openval  = 0
psh10.closeval = 1

gv27 = EPS_Shutter('XF:07IDB-VA:3{Slt:C-GV:1}', name = 'Upstream Gate Valve',kind='hinted')
psh10.shutter_type = 'GV'
psh10.openval  = 0
psh10.closeval = 1

gv27a = EPS_Shutter('XF:07IDB-VA:2{RSoXS:Main-GV:1}', name = 'Izero-Main Gate Valve',kind='hinted')
psh10.shutter_type = 'GV'
psh10.openval  = 0
psh10.closeval = 1

gv28 = EPS_Shutter('XF:07IDB-VA:2{BT:1-GV:1}', name = 'Downstream Gate Valve',kind='hinted')
psh10.shutter_type = 'GV'
psh10.openval  = 0
psh10.closeval = 1

gvTEM = EPS_Shutter('XF:07IDB-VA:2{RSoXS:Main-GV:2}', name = 'TEM Load Lock Gate Valve',kind='hinted')
psh10.shutter_type = 'GV'
psh10.openval  = 0
psh10.closeval = 1

gvll = EPS_Shutter('XF:07IDB-VA:2{RSoXS:LL-GV:1}', name = 'Load Lock Gate Valve',kind='hinted')
psh10.shutter_type = 'GV'
psh10.openval  = 0
psh10.closeval = 1

gvturbo = EPS_Shutter('XF:07IDB-VA:2{RSoXS:TP-GV:1}', name = 'Turbo Gate Valve',kind='hinted')
psh10.shutter_type = 'GV'
psh10.openval  = 0
psh10.closeval = 1

ccg_izero = EpicsSignalRO('XF:07IDB-VA:2{RSoXS:DM-CCG:1}P:Raw-I',
                          name="IZero Chamber Cold Cathode Gauge",
                          kind='hinted')
pg_izero  = EpicsSignalRO('XF:07IDB-VA:2{RSoXS:DM-TCG:1}P:Raw-I',
                          name='IZero Chamber Pirani Gauge',
                          kind='hinted')
ccg_main  = EpicsSignalRO('XF:07IDB-VA:2{RSoXS:Main-CCG:1}P:Raw-I',
                          name="Main Chamber Chamber Cold Cathode Gauge",
                          kind='hinted')
pg_main   = EpicsSignalRO('XF:07IDB-VA:2{RSoXS:Main-TCG:1}P:Raw-I',
                          name='Main Chamber Pirani Gauge',
                          kind='hinted')
ccg_ll    = EpicsSignalRO('XF:07IDB-VA:2{RSoXS:LL-CCG:1}P:Raw-I',
                          name="Load Lock Chamber Cold Cathode Gauge",
                          kind='hinted')
pg_ll     = EpicsSignalRO('XF:07IDB-VA:2{RSoXS:LL-TCG:1}P:Raw-I',
                          name='Load Lock Pirani Gauge',
                          kind='hinted')
ll_gpwr   = EpicsSignal('XF:07IDB-VA:2{RSoXS:LL-CCG:1}Pwr-Cmd',
                        name='Power to Load Lock Gauge',
                        kind='hinted')


class PDU(EpicsSignal):

    def on(self):
        self.set(1,timeout=2,settle_time=1)

    def off(self):
        self.set(0,timeout=2,settle_time=1)


light = PDU('XF:07ID-CT{RG:C1-PDU:1}Sw:8-SP',write_pv='XF:07ID-CT{RG:C1-PDU:1}Sw:8-Sel')


sd.baseline.extend([ccg_izero,pg_izero,ccg_main,pg_main,ccg_ll,pg_ll,ll_gpwr,psh1,psh4,psh10,psh7,gv14,gv14a,gv15,gv26,gv27,gv27a,gv28,gvTEM,gvll,gvturbo,light])