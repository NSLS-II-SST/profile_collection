print(f'Loading {__file__}...')
import bluesky.plans as bp
import bluesky.plan_stubs as bps

def Shutter_in():
    yield from bps.mv(Shutter_Y, 3)
def Shutter_out():
    yield from bps.mv(Shutter_Y,44)

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
    yield from bps.mv(BSw,3)

def BSs_in():
    yield from bps.mv(BSs,67.4)
def BSs_out():
    yield from bps.mv(BSs,3)

def Detectors_out():
    yield from bps.mv(Det_S,-94,
                      Det_W,-94)

def Detectors_edge():
    yield from bps.mv(Det_S,-50,
                      Det_W,-50)

def BS_out():
    yield from bps.mv(BSw,3,
                      BSs,3)

def all_out():
    yield from bps.mv(BSw,3,
                      BSs,3,
                      Det_S,-94,
                      Det_W,-94,
                      slits1.vsize, 10,
                      slits1.hsize, 10,
                      slits2.vsize, 10,
                      slits2.hsize, 10,
                      slits3.vsize, 10,
                      slits3.hsize, 10,
                      Shutter_Y,44,
                      Izero_Y, 145,
                      sam_Y, 345)

def slits_in():
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

def mirror3_pos():
    yield from bps.mv(mir3.Pitch, 8.031)
    yield from bps.mv(mir3.X, 26.15)
    yield from bps.mv(mir3.Y, 18.05)
    yield from bps.mv(mir3.Z, 0)
    yield from bps.mv(mir3.Roll, 0)
    yield from bps.mv(mir3.Yaw, 0)

def mirror3_NEXAFSpos():
    yield from bps.mv(mir3.Pitch, 8.151)
    yield from bps.mv(mir3.X, 26.15)
    yield from bps.mv(mir3.Y, 18.05)
    yield from bps.mv(mir3.Z, 0)
    yield from bps.mv(mir3.Roll, 0)
    yield from bps.mv(mir3.Yaw, 0)

def mirror1_pos():
    yield from bps.mv(mir1.X, 0,
                      mir1.Y, -18,
                      mir1.Z, 0,
                      mir1.Roll, 0,
                      mir1.Pitch, 0.679,
                      mir1.Yaw, 0)


def mirror1_NEXAFSpos():
    yield from bps.mv(mir1.Pitch, 0.691,
                      mir1.X, 0,
                      mir1.Y, -18,
                      mir1.Z, 0,
                      mir1.Roll, 0,
                      mir1.Yaw, 0)