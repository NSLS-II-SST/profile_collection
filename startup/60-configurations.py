run_report(__file__)
import bluesky.plans as bp
import bluesky.plan_stubs as bps
import time
from IPython.core.magic import register_line_magic

def Shutter_in():
    yield from bps.mv(Shutter_Y, 3)
def Shutter_out():
    yield from bps.mv(Shutter_Y,44)

def Izero_screen():
    yield from bps.mv(Izero_Y, 2)
def Izero_mesh():
    yield from bps.mv(Izero_Y, -29)
def Izero_diode():
    yield from bps.mv(Izero_Y, 35)
def Izero_out():
    yield from bps.mv(Izero_Y, 145)

def DetS_edge():
    yield from bps.mv(Det_S,-50)
def DetS_out():
    yield from bps.mv(Det_S,-94)

def DetW_edge():
    yield from bps.mv(Det_W,-50)
def DetW_in():
    yield from bps.mv(Det_W,-35)
def DetW_out():
    yield from bps.mv(Det_W,-94)

def BSw_in():
    yield from bps.mv(BeamStopW,70.035)
def BSw_out():
    yield from bps.mv(BeamStopW,3)

def BSs_in():
    yield from bps.mv(BeamStopS,67.4)
def BSs_out():
    yield from bps.mv(BeamStopS,3)

def Detectors_out():
    yield from bps.mv(Det_S,-94,
                      Det_W,-94)

def Detectors_edge():
    yield from bps.mv(Det_S,-50,
                      Det_W,-50)

def BS_out():
    yield from bps.mv(BSw,3,
                      BSs,3)



def slits_in_SAXS():
    yield from bps.mv(slits1.vsize, .2,
                      slits1.hsize, .2,
                      slits2.vsize, .6,
                      slits2.hsize, .4,
                      slits3.vsize, 1.2,
                      slits3.hsize, 1,
                      slits1.vcenter, .15,
                      slits1.hcenter, .1,
                      slits2.vcenter, .15,
                      slits2.hcenter, .1,
                      slits3.vcenter, 0,
                      slits3.hcenter, 0)
def slits_out():
    yield from bps.mv(slits1.vsize, 10,
                      slits1.hsize, 10,
                      slits2.vsize, 10,
                      slits2.hsize, 10,
                      slits3.vsize, 10,
                      slits3.hsize, 10)
def slits_in_WAXS():
    yield from bps.mv(slits1.vsize, .3,
                      slits1.hsize, .5,
                      slits2.vsize, .5,
                      slits2.hsize, .8,
                      slits3.vsize, 1,
                      slits3.hsize, 1.2,
                      slits1.vcenter, 0.08,
                      slits1.hcenter, 0.04,
                      slits2.vcenter, .151,
                      slits2.hcenter, .111,
                      slits3.vcenter, 0.203,
                      slits3.hcenter, 0.2)

def mirror3_pos():
    yield from bps.mv(mir3.Pitch, 8.031)
    time.sleep(3)
    yield from bps.mv(mir3.X, 26.15)
    time.sleep(3)
    yield from bps.mv(mir3.Y, 18.05)
    time.sleep(3)
    yield from bps.mv(mir3.Z, 0)
    time.sleep(3)
    yield from bps.mv(mir3.Roll, 0)
    time.sleep(3)
    yield from bps.mv(mir3.Yaw, 0)
    time.sleep(3)

def mirror3_NEXAFSpos():
    yield from bps.mv(mir3.Pitch, 8.151)
    time.sleep(3)
    yield from bps.mv(mir3.X, 26.15)
    time.sleep(3)
    yield from bps.mv(mir3.Y, 18.05)
    time.sleep(3)
    yield from bps.mv(mir3.Z, 0)
    time.sleep(3)
    yield from bps.mv(mir3.Roll, 0)
    time.sleep(3)
    yield from bps.mv(mir3.Yaw, 0)
    time.sleep(3)

def mirror1_pos():
    yield from bps.mv(mir1.Pitch, 0.6702)
    time.sleep(3)
    yield from bps.mv(mir1.X, 0)
    time.sleep(3)
    yield from bps.mv(mir1.Y, -17.86)
    time.sleep(3)
    yield from bps.mv(mir1.Z, -0.01)
    time.sleep(3)
    yield from bps.mv(mir1.Roll, .2)
    time.sleep(3)
    yield from bps.mv(mir1.Pitch, 0.6702)
    time.sleep(3)
    yield from bps.mv(mir1.Yaw, .3)


def mirror1_NEXAFSpos():
    yield from bps.mv(mir1.Pitch, 0.691)
    time.sleep(3)
    yield from bps.mv(mir1.X, 0)
    time.sleep(3)
    yield from bps.mv(mir1.Y, -18)
    time.sleep(3)
    yield from bps.mv(mir1.Z, 0)
    time.sleep(3)
    yield from bps.mv(mir1.Roll, 0)
    time.sleep(3)
    yield from bps.mv(mir1.Yaw, 0)

def SAXSmode():
    yield from slits_in_SAXS()
    yield from bps.mv(Shutter_Y, 3,
                      Izero_Y, -29,
                      Det_W, -94,
                      BeamStopW, 3,
                      BeamStopS, 67.4,
                      sam_Y, -125)

def WAXSmode():
    yield from slits_in_WAXS()
    yield from bps.mv(Shutter_Y, 3,
                      Izero_Y, -29,
                      Det_W, -36,
                      Det_S, -94,
                      BeamStopW, 70.7035,
                      BeamStopS, 3,
                      sam_Y, -125)

def all_out():
    yield from psh10.close()
    print('Retracting Slits to 1 cm gap')
    yield from slits_out()
    print('Moving the rest of RSoXS components')
    yield from bps.mv(Shutter_Y, 44,
                      Izero_Y, 144,
                      Det_W, -94,
                      Det_S, -94,
                      BeamStopW, 3,
                      BeamStopS, 3,
                      sam_Y, 345,
                      sam_X, 0,
                      sam_Z, 0,
                      sam_Th, 0)
    print('All done - Happy NEXAFSing')


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

