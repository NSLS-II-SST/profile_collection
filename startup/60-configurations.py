run_report(__file__)
import bluesky.plans as bp
import bluesky.plan_stubs as bps
import time
from IPython.core.magic import register_line_magic

def Shutter_in():
    yield from bps.mv(Shutter_Y, 2.2)
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

def DetS_in():
    yield from bps.mv(Det_S,0)
def DetS_edge():
    yield from bps.mv(Det_S,-50)
def DetS_out():
    yield from bps.mv(Det_S,-94)

def DetW_edge():
    yield from bps.mv(Det_W,-50)
def DetW_in():
    yield from bps.mv(Det_W,-10)
def DetW_out():
    yield from bps.mv(Det_W,-94)

def BSw_in():
    yield from bps.mv(BeamStopW,66.1)
def BSw_out():
    yield from bps.mv(BeamStopW,3)

def BSs_in():
    yield from bps.mv(BeamStopS,68.7)
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
    yield from bps.mv(slits1.vsize, 0.2,
                      slits1.vcenter, -0.55,
                      slits1.hsize, 0.2,
                      slits1.hcenter, 0.3,
                      slits2.vsize, 0.4,
                      slits2.vcenter, -0.85,
                      slits2.hsize, 0.35,
                      slits2.hcenter, 0.2,
                      slits3.vsize, 0.85,
                      slits3.vcenter, -0.5,
                      slits3.hsize, 0.7,
                      slits3.hcenter, 0.3)
def slits_out():
    yield from bps.mv(slits1.vsize, 10,
                      slits1.hsize, 10,
                      slits2.vsize, 10,
                      slits2.hsize, 10,
                      slits3.vsize, 10,
                      slits3.hsize, 10)
def slits_in_WAXS():
    yield from bps.mv(slits1.vsize, 0.5,
                      slits1.vcenter, -0.55,
                      slits1.hsize, 0.4,
                      slits1.hcenter, 0.3,
                      slits2.vsize, 0.8,
                      slits2.vcenter, -0.9,
                      slits2.hsize, 0.7,
                      slits2.hcenter, 0.2,
                      slits3.vsize, 1.15,
                      slits3.vcenter, -0.55,
                      slits3.hsize, 1.1,
                      slits3.hcenter, 0.3)

def mirror3_pos():
    yield from bps.mv(mir3.Pitch, 7.91)
    time.sleep(3)
    yield from bps.mv(mir3.X, 27)
    time.sleep(3)
    yield from bps.mv(mir3.Y, 18)
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
    yield from bps.mv(mir1.Pitch, 0.7)
    time.sleep(3)
    yield from bps.mv(mir1.X, 0)
    time.sleep(3)
    yield from bps.mv(mir1.Y, -18)
    time.sleep(3)
    yield from bps.mv(mir1.Z, 0)
    time.sleep(3)
    yield from bps.mv(mir1.Roll, 0)
    time.sleep(3)
    yield from bps.mv(mir1.Pitch, 0.7)
    time.sleep(3)
    yield from bps.mv(mir1.Yaw, 0)


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
    yield from bps.mv(Shutter_Y, 2.2,
                      Izero_Y, -29,
                      Det_S, 0,
                      Det_W, -94,
                      BeamStopW, 3,
                      BeamStopS, 68.7)
def SAXS():
    return [{
        'motor':    slits1.vsize,
        'position': 0.2,
        'order': 0},
        {
        'motor':    slits1.vcenter,
        'position': -0.55,
        'order': 0},
        {
        'motor':    slits1.hsize,
        'position': 0.2,
        'order': 0},
        {
        'motor':    slits1.hcenter,
        'position': 0.3,
        'order': 0},
        {
        'motor':    slits2.vsize,
        'position': 0.4,
        'order': 0},
        {
        'motor':    slits2.vcenter,
        'position': -0.85,
        'order': 0},
        {
        'motor':    slits2.hsize,
        'position': 0.35,
        'order': 0},
        {
        'motor':    slits2.hcenter,
        'position': 0.2,
        'order': 0},
        {
        'motor':    slits3.vsize,
        'position': 0.85,
        'order': 0},
        {
        'motor':    slits3.vcenter,
        'position': -0.5,
        'order': 0},
        {
        'motor':    slits3.hsize,
        'position': 0.7,
        'order': 0},
        {
        'motor':    slits3.hcenter,
        'position': 0.3,
        'order': 0},
        {
        'motor':    Shutter_Y,
        'position': 2.2,
        'order': 0},
        {
        'motor':    Izero_Y,
        'position': -29,
        'order': 0},
        {
        'motor':    Det_W,
        'position': -94,
        'order': 0},
        {
        'motor':    Det_S,
        'position': 0,
        'order': 0},
        {
        'motor':    BeamStopS,
        'position': 68.7,
        'order': 0},
        {
        'motor':    BeamStopW,
        'position': 3,
        'order': 0},
    ]

def WAXSmode():
    yield from slits_in_WAXS()
    yield from bps.mv(Shutter_Y, 2.2,
                      Izero_Y, -29,
                      Det_W, -10,
                      Det_S, -94,
                      BeamStopW, 66.1,
                      BeamStopS, 3,
                      sam_Y, -125)

def WAXS():
    return [{
        'motor':    slits1.vsize,
        'position': .5,
        'order': 0},
        {
        'motor':    slits1.vcenter,
        'position': -0.55,
        'order': 0},
        {
        'motor':    slits1.hsize,
        'position': 0.4,
        'order': 0},
        {
        'motor':    slits1.hcenter,
        'position': 0.3,
        'order': 0},
        {
        'motor':    slits2.vsize,
        'position': 0.8,
        'order': 0},
        {
        'motor':    slits2.vcenter,
        'position': -0.9,
        'order': 0},
        {
        'motor':    slits2.hsize,
        'position': 0.7,
        'order': 0},
        {
        'motor':    slits2.hcenter,
        'position': 0.2,
        'order': 0},
        {
        'motor':    slits3.vsize,
        'position': 1.15,
        'order': 0},
        {
        'motor':    slits3.vcenter,
        'position': -0.55,
        'order': 0},
        {
        'motor':    slits3.hsize,
        'position': 1.1,
        'order': 0},
        {
        'motor':    slits3.hcenter,
        'position': 0.3,
        'order': 0},
        {
        'motor':    Shutter_Y,
        'position': 2.2,
        'order': 0},
        {
        'motor':    Izero_Y,
        'position': -29,
        'order': 0},
        {
        'motor':    Det_W,
        'position': -10,
        'order': 0},
        {
        'motor':    Det_S,
        'position':-94,
        'order': 0},
        {
        'motor':    BeamStopW,
        'position': 66.1,
        'order': 0},
        {
        'motor':    BeamStopS,
        'position': 3,
        'order': 0},
    ]

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

