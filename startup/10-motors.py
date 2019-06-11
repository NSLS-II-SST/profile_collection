from IPython.core.magic import register_line_magic
from ophyd import EpicsMotor


run_report(__file__)

class prettymotor(EpicsMotor):

    def where(self):
        return ('{} : {}').format(
            colored(self.name, 'lightblue'),
            colored('{:.2f}'.format(self.user_readback.value).rstrip('0').rstrip('.'), 'yellow'))

    def where_sp(self):
        return ('{} Setpoint : {}\n{} Readback : {}').format(
            colored(self.name, 'lightblue'),
            colored('{:.2f}'.format(self.user_readback.value).rstrip('0').rstrip('.'), 'yellow'),
            colored(self.name, 'lightblue'),
            colored('{:.2f}'.format(self.user_setpoint.value).rstrip('0').rstrip('.'), 'yellow'))

    def wh(self):
        boxed_text(self.name+" location", self.where_sp(), 'green',shrink=True)

    def status_or_rel_move(self,line):
        try:
            loc = float(line)
        except:
            boxed_text(self.name, self.where_sp(), 'lightgray', shrink=True)
        else:
            RE(bps.mvr(self, loc))
            boxed_text(self.name, self.where(), 'lightgray', shrink=True)


sam_X = prettymotor('XF:07ID2-ES1{Stg-Ax:X}Mtr', name='RSoXS Sample Outboard-Inboard',kind='hinted')
sam_Y = prettymotor('XF:07ID2-ES1{Stg-Ax:Y}Mtr', name='RSoXS Sample Up-Down',kind='hinted')
sam_Z = prettymotor('XF:07ID2-ES1{Stg-Ax:Z}Mtr', name='RSoXS Sample Downstream-Upstream',kind='hinted')
sam_Th = prettymotor('XF:07ID2-ES1{Stg-Ax:Yaw}Mtr', name='RSoXS Sample Rotation',kind='hinted')
BeamStopW = prettymotor('XF:07ID2-ES1{BS-Ax:1}Mtr', name='Beam Stop WAXS',kind='hinted')
BeamStopS = prettymotor('XF:07ID2-ES1{BS-Ax:2}Mtr', name='Beam Stop SAXS',kind='hinted')
Det_W = prettymotor('XF:07ID2-ES1{Det-Ax:1}Mtr', name='Detector WAXS Translation',kind='hinted')
Det_S = prettymotor('XF:07ID2-ES1{Det-Ax:2}Mtr', name='Detector SAXS Translation',kind='hinted')
Shutter_Y = prettymotor('XF:07ID2-ES1{FSh-Ax:1}Mtr', name='Shutter Vertical Translation',kind='hinted')
Izero_Y = prettymotor('XF:07ID2-ES1{Scr-Ax:1}Mtr', name='Izero Assembly Vertical Translation',kind='hinted')
Izero_ds = prettymotor('XF:07ID2-BI{Diag:07-Ax:Y}Mtr', name='Downstream Izero DM7 Vertical Translation',kind='hinted')
Exit_Slit = prettymotor('XF:07ID2-BI{Slt:11-Ax:YGap}Mtr', name='Exit Slit of Mono Vertical Gap',kind='hinted')

sd.baseline.extend([sam_X, sam_Y, sam_Z, sam_Th, BeamStopS, BeamStopW, Det_S, Det_W, Shutter_Y, Izero_Y, Izero_ds])


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
    boxed_text('RSoXS Motor Locations',
                        (sam_X.where()+"\n"+
                         sam_Y.where()+"\n"+
                         sam_Z.where()+"\n"+
                         sam_Th.where()+"\n"+
                         BeamStopW.where()+"\n"+
                         BeamStopS.where()+"\n"+
                         Det_W.where()+"\n"+
                         Det_S.where()+"\n"+
                         Shutter_Y.where()+"\n"+
                         Izero_Y.where()+"\n"+
                         Izero_ds.where()+"\n"+
                         Exit_Slit.where()+"\n"),
               'lightgray',shrink=True)


del x,y,z,th,ds,dw,bss,bsw,motors
