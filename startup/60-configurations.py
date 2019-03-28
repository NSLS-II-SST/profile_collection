print(f'Loading {__file__}...')
import bluesky.plans as bp
import bluesky.plan_stubs as bps

def Shutter_in():
    yield from bps.mv(Shutter_Y, 2)
def Shutter_out():
    yield from bps.mv(Shuter_Y,44)

def Izero_screen():
    yield from bps.mv(Izero_Y, 2)
def Izero_mesh():
    yield from bps.mv(Izero_Y, -29)
def Izero_out():
    yield from bps.mv(Izero_Y, 145)

def DetS_edge():
    yield from bps.mv(Det_S,-50)
def DetS_out():
    yield from bps.mv(Det_S,-94)

def DetW_edge():
    yield from bps.mv(Det_W,-50)
def DetW_out():
    yield from bps.mv(Det_W,-94)

def BSw_in():
    yield from bps.mv(BSw,68)
def BSw_out():
    yield from bps.mv(BSw,2)

def BSs_in():
    yield from bps.mv(BSs,70.4)
def BSs_out():
    yield from bps.mv(BSs,2)

def Detectors_out():
    DetW_out()
    DetS_out()

def Detectors_edge():
    DetW_edge()
    DetS_edge()

def BS_out():
    BSs_out()
    BSw_out()

def all_out():
    BS_out()
    Detectors_out()
    Shutter_out()