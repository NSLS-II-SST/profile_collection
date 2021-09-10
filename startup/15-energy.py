run_report(__file__)


from .SSTObjects.energy import *

sd.baseline.extend([en])

@register_line_magic
def e(line):
    try:
        loc = float(line)
    except:
        boxed_text('Beamline Energy',en.where(),'lightpurple',shrink=True)
    else:
        RE(bps.mv(en,loc))
        boxed_text('Beamline Energy', en.where(), 'lightpurple', shrink=True)
del e



@register_line_magic
def pol(line):
    try:
        loc = float(line)
    except:
        boxed_text('Beamline Polarization',en.where(),'lightpurple',shrink=True)
    else:
        RE(set_polarization(loc))
        boxed_text('Beamline Polarization', en.where(), 'lightpurple', shrink=True)
del pol




sd.monitors.extend([mono_en.readback])

# XF:07ID1-OP{Mono:PGM1-Ax::EVSTART_SP # start energy
# XF:07ID1-OP{Mono:PGM1-Ax::EVSTOP_SP # stop energy
# XF:07ID1-OP{Mono:PGM1-Ax::EVVELO_SP # Ev/sec
# XF:07ID1-OP{Mono:PGM1-Ax::START_CMD.PROC #start
# XF:07ID1-OP{Mono:PGM1-Ax::ENERGY_ST_CMD.PROC #stop

