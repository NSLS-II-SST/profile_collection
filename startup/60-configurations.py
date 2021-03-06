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
    yield from bps.mv(BeamStopW,71.4)
def BSw_out():
    yield from bps.mv(BeamStopW,3)

def BSs_in():
    yield from bps.mv(BeamStopS,67)
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
    yield from bps.mv(slits1.vsize, 0.025,
                      slits1.vcenter, -0.55,
                      slits1.hsize, 0.153,
                      slits1.hcenter, 0.7,
                      slits2.vsize, 0.4,
                      slits2.vcenter, -0.9,
                      slits2.hsize, 0.5,
                      slits2.hcenter, 0.7,
                      slits3.vsize, 1,
                      slits3.vcenter, -0.5,
                      slits3.hsize, 1,
                      slits3.hcenter, 0.9)
def slits_out():
    yield from bps.mv(slits1.vsize, 10,
                      slits1.hsize, 10,
                      slits2.vsize, 10,
                      slits2.hsize, 10,
                      slits3.vsize, 10,
                      slits3.hsize, 10)
def slits_in_WAXS():
    yield from bps.mv(slits1.vsize, 0.05,
                      slits1.vcenter, -0.55,
                      slits1.hsize, 0.3,
                      slits1.hcenter, 0.55,
                      slits2.vsize, 0.45,
                      slits2.vcenter, -1.05,
                      slits2.hsize, 0.5,
                      slits2.hcenter, 0.45,
                      slits3.vsize, 1.1,
                      slits3.vcenter, -0.625,
                      slits3.hsize, 1.2,
                      slits3.hcenter, 0.55)

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
    yield from psh10.close()
    yield from slits_in_SAXS()
    yield from bps.mv(Shutter_Y, 2.2,
                      Izero_Y, -29,
                      Det_S, 0,
                      Det_W, -94,
                      BeamStopW, 3,
                      BeamStopS, 67)


def SAXS():
    return [[{
        'motor':    slits1.vsize,
        'position': 0.025,
        'order': 0},
        {
        'motor':    slits1.vcenter,
        'position': -0.55,
        'order': 0},
        {
        'motor':    slits1.hsize,
        'position': 0.153,
        'order': 0},
        {
        'motor':    slits1.hcenter,
        'position': 0.7,
        'order': 0},
        {
        'motor':    slits2.vsize,
        'position': 0.4,
        'order': 0},
        {
        'motor':    slits2.vcenter,
        'position': -0.9,
        'order': 0},
        {
        'motor':    slits2.hsize,
        'position': 0.5,
        'order': 0},
        {
        'motor':    slits2.hcenter,
        'position': 0.7,
        'order': 0},
        {
        'motor':    slits3.vsize,
        'position': 1,
        'order': 0},
        {
        'motor':    slits3.vcenter,
        'position': -0.5,
        'order': 0},
        {
        'motor':    slits3.hsize,
        'position': 1,
        'order': 0},
        {
        'motor':    slits3.hcenter,
        'position': 0.9,
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
        'position': 67.7,
        'order': 0},
        {
        'motor':    BeamStopW,
        'position': 3,
        'order': 1},
    ],
    {'RSoXS_Config': 'SAXS',
      'RSoXS_Main_DET':'SAXS',
      'RSoXS_WAXS_SDD': None,
      'RSoXS_WAXS_BCX': None,
      'RSoXS_WAXS_BCY': None,
      'RSoXS_SAXS_SDD': 521.8,
      'RSoXS_SAXS_BCX': 489.86,
      'RSoXS_SAXS_BCY': 491,}]

def SAXSNEXAFS():
    return [[{
        'motor':    slits1.vsize,
        'position': 0.025,
        'order': 0},
        {
        'motor':    slits1.vcenter,
        'position': -0.55,
        'order': 0},
        {
        'motor':    slits1.hsize,
        'position': 0.153,
        'order': 0},
        {
        'motor':    slits1.hcenter,
        'position': 0.7,
        'order': 0},
        {
        'motor':    slits2.vsize,
        'position': 0.4,
        'order': 0},
        {
        'motor':    slits2.vcenter,
        'position': -0.9,
        'order': 0},
        {
        'motor':    slits2.hsize,
        'position': 0.5,
        'order': 0},
        {
        'motor':    slits2.hcenter,
        'position': 0.7,
        'order': 0},
        {
        'motor':    slits3.vsize,
        'position': 1,
        'order': 0},
        {
        'motor':    slits3.vcenter,
        'position': -0.5,
        'order': 0},
        {
        'motor':    slits3.hsize,
        'position': 1,
        'order': 0},
        {
        'motor':    slits3.hcenter,
        'position': 0.9,
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
        'position': -94,
        'order': 0},
        {
        'motor':    BeamStopS,
        'position': 67.7,
        'order': 0},
        {
        'motor':    BeamStopW,
        'position': 3,
        'order': 1},
    ],
    {'RSoXS_Config': 'SAXSNEXAFS',
      'RSoXS_Main_DET': 'Beamstop_SAXS',
      'RSoXS_WAXS_SDD': None,
      'RSoXS_WAXS_BCX': None,
      'RSoXS_WAXS_BCY': None,
      'RSoXS_SAXS_SDD': None,
      'RSoXS_SAXS_BCX': None,
      'RSoXS_SAXS_BCY': None,}]

def TEYNEXAFS():
    return [[{
        'motor':    slits1.vsize,
        'position': 0.025,
        'order': 0},
        {
        'motor':    slits1.vcenter,
        'position': -0.55,
        'order': 0},
        {
        'motor':    slits1.hsize,
        'position': 0.153,
        'order': 0},
        {
        'motor':    slits1.hcenter,
        'position': 0.5,
        'order': 0},
        {
        'motor':    slits2.vsize,
        'position': 0.35,
        'order': 0},
        {
        'motor':    slits2.vcenter,
        'position': -0.73,
        'order': 0},
        {
        'motor':    slits2.hsize,
        'position': 0.4,
        'order': 0},
        {
        'motor':    slits2.hcenter,
        'position': 0.423,
        'order': 0},
        {
        'motor':    slits3.vsize,
        'position': 1.6,
        'order': 0},
        {
        'motor':    slits3.vcenter,
        'position': -0.17,
        'order': 0},
        {
        'motor':    slits3.hsize,
        'position': 1,
        'order': 0},
        {
        'motor':    slits3.hcenter,
        'position': 0.49,
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
        'position': -94,
        'order': 0},
        {
        'motor':    BeamStopS,
        'position': 3,
        'order': 0},
        {
        'motor':    BeamStopW,
        'position': 3,
        'order': 1},
    ],
    {'RSoXS_Config': 'TEYNEXAFS',
      'RSoXS_Main_DET': 'Beamstop_SAXS',
      'RSoXS_WAXS_SDD': None,
      'RSoXS_WAXS_BCX': None,
      'RSoXS_WAXS_BCY': None,
      'RSoXS_SAXS_SDD': None,
      'RSoXS_SAXS_BCX': None,
      'RSoXS_SAXS_BCY': None,}]

def WAXSmode():
    yield from psh10.close()
    yield from slits_in_WAXS()
    yield from bps.mv(Shutter_Y, 2.2,
                      Izero_Y, -29,
                      Det_W, -10,
                      BeamStopW, 71.4,
                      sam_Y, -125)

def WAXS():
    return [[{
        'motor':    slits1.vsize,
        'position': .05,
        'order': 1},
        {
        'motor':    slits1.vcenter,
        'position': -0.55,
        'order': 1},
        {
        'motor':    slits1.hsize,
        'position': 0.3,
        'order': 1},
        {
        'motor':    slits1.hcenter,
        'position': 0.55,
        'order': 1},
        {
        'motor':    slits2.vsize,
        'position': 0.45,
        'order': 1},
        {
        'motor':    slits2.vcenter,
        'position': -1.05,
        'order': 1},
        {
        'motor':    slits2.hsize,
        'position': 0.5,
        'order': 1},
        {
        'motor':    slits2.hcenter,
        'position': 0.45,
        'order': 1},
        {
        'motor':    slits3.vsize,
        'position': 1.1,
        'order': 1},
        {
        'motor':    slits3.vcenter,
        'position': -0.625,
        'order': 1},
        {
        'motor':    slits3.hsize,
        'position': 1.2,
        'order': 1},
        {
        'motor':    slits3.hcenter,
        'position': 0.55,
        'order': 1},
        {
        'motor':    Shutter_Y,
        'position': 2.2,
        'order': 0},
        {
        'motor':    Izero_Y,
        'position': -29,
        'order': 1},
        {
        'motor':    Det_W,
        'position': -10,
        'order': 1},
        {
        'motor':    BeamStopW,
        'position': 71.4,
        'order': 1},
    ],
    {'RSoXS_Config': 'WAXS',
      'RSoXS_Main_DET': 'WAXS',
      'RSoXS_WAXS_SDD': 38.7,
      'RSoXS_WAXS_BCX': 400.5,
      'RSoXS_WAXS_BCY': 531,
      'RSoXS_SAXS_SDD': None,
      'RSoXS_SAXS_BCX': None,
      'RSoXS_SAXS_BCY': None,}]


def WAXSNEXAFS():
    return [[{
        'motor':    slits1.vsize,
        'position': .05,
        'order': 1},
        {
        'motor':    slits1.vcenter,
        'position': -0.55,
        'order': 1},
        {
        'motor':    slits1.hsize,
        'position': 0.3,
        'order': 1},
        {
        'motor':    slits1.hcenter,
        'position': 0.55,
        'order': 1},
        {
        'motor':    slits2.vsize,
        'position': 0.45,
        'order': 1},
        {
        'motor':    slits2.vcenter,
        'position': -1.05,
        'order': 1},
        {
        'motor':    slits2.hsize,
        'position': 0.5,
        'order': 1},
        {
        'motor':    slits2.hcenter,
        'position': 0.45,
        'order': 1},
        {
        'motor':    slits3.vsize,
        'position': 1.1,
        'order': 1},
        {
        'motor':    slits3.vcenter,
        'position': -0.625,
        'order': 1},
        {
        'motor':    slits3.hsize,
        'position': 1.2,
        'order': 1},
        {
        'motor':    slits3.hcenter,
        'position': 0.55,
        'order': 1},
        {
        'motor':    Shutter_Y,
        'position': 2.2,
        'order': 0},
        {
        'motor':    Izero_Y,
        'position': -29,
        'order': 1},
        {
        'motor':    Det_W,
        'position': -94,
        'order': 1},
        {
        'motor':    Det_S,
        'position': -94,
        'order': 1},
        {
        'motor':    BeamStopW,
        'position': 71.4,
        'order': 1},
    ],
    {'RSoXS_Config': 'WAXSNEXAFS',
      'RSoXS_Main_DET': 'Beamstop_WAXS',
      'RSoXS_WAXS_SDD': None,
      'RSoXS_WAXS_BCX': None,
      'RSoXS_WAXS_BCY': None,
      'RSoXS_SAXS_SDD': None,
      'RSoXS_SAXS_BCX': None,
      'RSoXS_SAXS_BCY': None,}]


def oldTEYNEXAFS():
    return [[{
        'motor':    slits1.vsize,
        'position': .025,
        'order': 1},
        {
        'motor':    slits1.vcenter,
        'position': -0.55,
        'order': 1},
        {
        'motor':    slits1.hsize,
        'position': 0.4,
        'order': 1},
        {
        'motor':    slits1.hcenter,
        'position': 0.5,
        'order': 1},
        {
        'motor':    slits2.vsize,
        'position': 0.6,
        'order': 1},
        {
        'motor':    slits2.vcenter,
        'position': -1.05,
        'order': 1},
        {
        'motor':    slits2.hsize,
        'position': 0.6,
        'order': 1},
        {
        'motor':    slits2.hcenter,
        'position': 0.31,
        'order': 1},
        {
        'motor':    slits3.vsize,
        'position': 0.9,
        'order': 1},
        {
        'motor':    slits3.vcenter,
        'position': -0.625,
        'order': 1},
        {
        'motor':    slits3.hsize,
        'position': 1.3,
        'order': 1},
        {
        'motor':    slits3.hcenter,
        'position': 0.25,
        'order': 1},
        {
        'motor':    Shutter_Y,
        'position': 2.2,
        'order': 1},
        {
        'motor':    Izero_Y,
        'position': -29,
        'order': 1},
        {
        'motor':    Det_W,
        'position': -94,
        'order': 1},
        {
        'motor':    Det_S,
        'position': -94,
        'order': 1},
        {
        'motor':    BeamStopW,
        'position': 71.4,
        'order': 0},
        {
        'motor':    BeamStopS,
        'position': 3,
        'order': 1},
    ],
    {'RSoXS_Config': 'TEYWAXS',
      'RSoXS_Main_DET': 'RSoXS_Sample_TEY',
      'RSoXS_WAXS_SDD': None,
      'RSoXS_WAXS_BCX': None,
      'RSoXS_WAXS_BCY': None,
      'RSoXS_SAXS_SDD': None,
      'RSoXS_SAXS_BCX': None,
      'RSoXS_SAXS_BCY': None,}]


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
    RE.md.update({'RSoXS_Config': 'inactive',
      'RSoXS_Main_DET': None,
      'RSoXS_WAXS_SDD': None,
      'RSoXS_WAXS_BCX': None,
      'RSoXS_WAXS_BCY': None,
      'RSoXS_SAXS_SDD': None,
      'RSoXS_SAXS_BCX': None,
      'RSoXS_SAXS_BCY': None,})
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

