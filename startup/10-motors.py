run_report(__file__)

from ..SSTObjects.diode import *
from ..SSTObjects.motors import *
from ..RSoXSObjects.motors import *
from ..CommonFunctions.functions import boxed_text

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
                        (sam_X.where()+'  x'+"\n"+
                         sam_Y.where()+'  y' + "\n"+
                         sam_Z.where()+'  z' + "\n"+
                         sam_Th.where()+'  th'+"\n"+
                         BeamStopW.where()+'  bsw'+"\n"+
                         BeamStopS.where()+'  bss'+"\n"+
                         Det_W.where()+'  dw'+"\n"+
                         Det_S.where()+'  ds'+"\n"+
                         Shutter_Y.where()+"\n"+
                         Izero_Y.where()+"\n"+
                         Izero_ds.where()+"\n"+
                         Exit_Slit.where()+"\n"+
                         sam_viewer.where()+"\n"),
               'lightgray',shrink=True)


del x,y,z,th,ds,dw,bss,bsw,motors

sd.monitors.extend([Shutter_control]) # this will give us a monitor to time the shutter opens and close

sd.baseline.extend([sam_viewer, sam_X, sam_Y, sam_Z, sam_Th, BeamStopS, BeamStopW, Det_S, Det_W,
                    Shutter_Y, Izero_Y, Izero_ds, grating, mirror2])
# s