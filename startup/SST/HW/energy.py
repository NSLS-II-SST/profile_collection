from ophyd import (
    PVPositioner,
    EpicsSignalRO,
    PseudoPositioner,SoftPositioner,
    PVPositionerPC,
    PseudoSingle,
    EpicsMotor,
    EpicsSignal,
    Signal,
)
from ophyd import Component as Cpt
import bluesky.plan_stubs as bps
from ophyd.pseudopos import pseudo_position_argument, real_position_argument
import pathlib
import numpy as np
import xarray as xr
from ..CommonFunctions.functions import boxed_text, colored, run_report
from ..Base.motors import PrettyMotorFMBO, DeadbandMixin
from ..Base.mirrors import FMBHexapodMirrorAxisStandAlonePitch
from ..HW.shutters import psh4
from ..HW.motors import grating, mirror2
from ..HW.mirrors import mir3


run_report(__file__)


class UndulatorMotor(DeadbandMixin,EpicsMotor):
    user_setpoint = Cpt(EpicsSignal, "-SP", limits=True)



class EpuMode(DeadbandMixin,PVPositionerPC):
    setpoint = Cpt(EpicsSignal,"-SP", kind="normal")
    readback = Cpt(EpicsSignal,"-RB", kind="normal")


#epu_mode = EpicsSignal(
#    "SR:C07-ID:G1A{SST1:1-Ax:Phase}Phs:Mode-SP", name="EPU 60 Mode", kind="normal"
#)
class FMB_Mono_Grating_Type(PVPositioner):
    setpoint = Cpt(EpicsSignal,'_TYPE_SP',string=True)
    readback = Cpt(EpicsSignal,'_TYPE_MON',string=True)
    actuate = Cpt(EpicsSignal,'_DCPL_CALC.PROC')
    enable = Cpt(EpicsSignal,'_ENA_CMD.PROC')
    kill = Cpt(EpicsSignal,'_KILL_CMD.PROC')
    home = Cpt(EpicsSignal,'_HOME_CMD.PROC')
    clear_encoder_loss = Cpt(EpicsSignal,'_ENC_LSS_CLR_CMD.PROC')
    done = Cpt(EpicsSignal,'_AXIS_STS')

class Monochromator(DeadbandMixin,PVPositioner):
    setpoint = Cpt(EpicsSignal, ":ENERGY_SP", kind="normal")
    readback = Cpt(EpicsSignalRO, ":ENERGY_MON", kind="hinted")

    grating = Cpt(PrettyMotorFMBO, "GrtP}Mtr", name="Mono Grating", kind="normal")
    mirror2 = Cpt(PrettyMotorFMBO, "MirP}Mtr", name="Mono Mirror", kind="normal")
    cff = Cpt(EpicsSignal, ":CFF_SP", name="Mono CFF", kind="normal", auto_monitor=True)
    vls = Cpt(EpicsSignal, ":VLS_B2.A", name="Mono VLS", kind="normal", auto_monitor=True)
    gratingx = Cpt(FMB_Mono_Grating_Type,"GrtX}Mtr",kind="normal")
    mirror2x = Cpt(FMB_Mono_Grating_Type,"MirX}Mtr",kind="normal")

    Scan_Start_ev = Cpt(EpicsSignal,":EVSTART_SP", name="MONO scan start energy", kind="normal")
    Scan_Stop_ev = Cpt(EpicsSignal,":EVSTOP_SP", name="MONO scan stop energy", kind="normal")
    Scan_Speed_ev = Cpt(EpicsSignal,":EVVELO_SP", name="MONO scan speed", kind="normal")
    Scan_Start = Cpt(EpicsSignal,":START_CMD.PROC",name="MONO scan start command",kind="normal")
    Scan_Stop = Cpt(EpicsSignal,":ENERGY_ST_CMD.PROC",name="MONO scan start command",kind="normal")

    scanlock = Cpt(Signal,value=0,name='lock flag for during scans')
    done = Cpt(EpicsSignalRO, ":ERDY_STS")
    done_value = 1
    stop_signal = Cpt(EpicsSignal, ":ENERGY_ST_CMD")

    def _setup_move(self, position):
        """Move and do not wait until motion is complete (asynchronous)"""
        self.log.debug("%s.setpoint = %s", self.name, position)
        # copy from pv_positioner, with wait changed to false
        # possible problem with IOC not returning from a set
        self.setpoint.put(position, wait=False)
        if self.actuate is not None:
            self.log.debug("%s.actuate = %s", self.name, self.actuate_value)
            self.actuate.put(self.actuate_value, wait=False)


# mono_en= Monochromator('XF:07ID1-OP{Mono:PGM1-Ax:', name='Monochromator Energy',kind='normal')


class EnPos(PseudoPositioner):
    """Energy pseudopositioner class.

    Parameters:
    -----------


    """

    # synthetic axis
    energy = Cpt(PseudoSingle, kind="hinted", limits=(71, 2250), name="Beamline Energy")
    polarization = Cpt(
        PseudoSingle, kind="hinted", limits=(-1, 180), name="X-ray Polarization"
    )
    sample_polarization = Cpt(
        PseudoSingle, kind="hinted", name="Sample X-ray polarization"
    )
    # real motors

    monoen = Cpt(
        Monochromator, "XF:07ID1-OP{Mono:PGM1-Ax:", kind="hinted", name="Mono Energy"
    )
    epugap = Cpt(
        UndulatorMotor,
        "SR:C07-ID:G1A{SST1:1-Ax:Gap}-Mtr",
        kind="normal",
        name="EPU Gap",
    )
    epuphase = Cpt(
        UndulatorMotor,
        "SR:C07-ID:G1A{SST1:1-Ax:Phase}-Mtr",
        kind="normal",
        name="EPU Phase",
    )
    mir3Pitch = Cpt(
        FMBHexapodMirrorAxisStandAlonePitch,
        "XF:07ID1-OP{Mir:M3ABC",
        kind="normal",
        name="M3Pitch",
    )
    epumode = Cpt(EpuMode,'SR:C07-ID:G1A{SST1:1-Ax:Phase}Phs:Mode',
                          name='EPU Mode', kind='normal')


    sim_epu_mode = Cpt(Signal,value=0,name='dont interact with the real EPU',kind='config')
    scanlock = Cpt(Signal,value=0,name="Lock Harmonic, Pitch, Grating for scan",kind='config')
    harmonic = Cpt(Signal, value=1, name="EPU Harmonic",kind='config')
    m3offset = Cpt(Signal, value=7.91, name="EPU Harmonic",kind='config')
    rotation_motor = None

    @pseudo_position_argument
    def forward(self, pseudo_pos):
        """Run a forward (pseudo -> real) calculation"""
        # print('In forward')
        ret = self.RealPosition(
            epugap=self.gap(pseudo_pos.energy, pseudo_pos.polarization,self.scanlock.get(),self.sim_epu_mode.get()),
            monoen=pseudo_pos.energy,
            epuphase=abs(self.phase(pseudo_pos.energy, pseudo_pos.polarization,self.sim_epu_mode.get())),
            mir3Pitch=self.m3pitchcalc(pseudo_pos.energy,self.scanlock.get()),
            epumode=self.mode(pseudo_pos.polarization,self.sim_epu_mode.get()),
            #harmonic=self.choose_harmonic(pseudo_pos.energy,pseudo_pos.polarization,self.scanlock.get())
        )
        # print('finished forward')
        return ret

    @real_position_argument
    def inverse(self, real_pos):
        """Run an inverse (real -> pseudo) calculation"""
        # print('in Inverse')
        ret = self.PseudoPosition(
            energy=real_pos.monoen,
            polarization=self.pol(real_pos.epuphase, real_pos.epumode),
            sample_polarization=self.sample_pol(
                self.pol(real_pos.epuphase, real_pos.epumode)
            ),
        )
        # print('Finished inverse')
        return ret

    def where_sp(self):
        return (
            "Beamline Energy Setpoint : {}"
            "\nMonochromator Readback : {}"
            "\nEPU Gap Setpoint : {}"
            "\nEPU Gap Readback : {}"
            "\nEPU Phase Setpoint : {}"
            "\nEPU Phase Readback : {}"
            "\nEPU Mode Setpoint : {}"
            "\nEPU Mode Readback : {}"
            "\nGrating Setpoint : {}"
            "\nGrating Readback : {}"
            "\nGratingx Setpoint : {}"
            "\nGratingx Readback : {}"
            "\nMirror2 Setpoint : {}"
            "\nMirror2 Readback : {}"
            "\nMirror2x Setpoint : {}"
            "\nMirror2x Readback : {}"
            "\nCFF : {}"
            "\nVLS : {}"
        ).format(
            colored(
                "{:.2f}".format(self.monoen.setpoint.get()).rstrip("0").rstrip("."),
                "yellow",
            ),
            colored(
                "{:.2f}".format(self.monoen.readback.get()).rstrip("0").rstrip("."),
                "yellow",
            ),
            colored(
                "{:.2f}".format(self.epugap.user_setpoint.get())
                    .rstrip("0")
                    .rstrip("."),
                "yellow",
            ),
            colored(
                "{:.2f}".format(self.epugap.user_readback.get())
                    .rstrip("0")
                    .rstrip("."),
                "yellow",
            ),
            colored(
                "{:.2f}".format(self.epuphase.user_setpoint.get())
                    .rstrip("0")
                    .rstrip("."),
                "yellow",
            ),
            colored(
                "{:.2f}".format(self.epuphase.user_readback.get())
                    .rstrip("0")
                    .rstrip("."),
                "yellow",
            ),
            colored(
                "{:.2f}".format(self.epumode.setpoint.get())
                    .rstrip("0")
                    .rstrip("."),
                "yellow",
            ),
            colored(
                "{:.2f}".format(self.epumode.readback.get())
                    .rstrip("0")
                    .rstrip("."),
                "yellow",
            ),
            colored(
                "{:.2f}".format(self.monoen.grating.user_setpoint.get())
                    .rstrip("0")
                    .rstrip("."),
                "yellow",
            ),
            colored(
                "{:.2f}".format(self.monoen.grating.user_readback.get())
                    .rstrip("0")
                    .rstrip("."),
                "yellow",
            ),
            colored(self.monoen.gratingx.setpoint.get(),
                    "yellow",
                    ),
            colored(self.monoen.gratingx.readback.get(),
                    "yellow",
                    ),
            colored(
                "{:.2f}".format(self.monoen.mirror2.user_setpoint.get())
                    .rstrip("0")
                    .rstrip("."),
                "yellow",
            ),
            colored(
                "{:.2f}".format(self.monoen.mirror2.user_readback.get())
                    .rstrip("0")
                    .rstrip("."),
                "yellow",
            ),
            colored(self.monoen.mirror2x.setpoint.get(),
                    "yellow",
                    ),
            colored(self.monoen.mirror2x.readback.get(),
                    "yellow",
                    ),
            colored(
                "{:.2f}".format(self.monoen.cff.get()).rstrip("0").rstrip("."), "yellow"
            ),
            colored(
                "{:.2f}".format(self.monoen.vls.get()).rstrip("0").rstrip("."), "yellow"
            ),
        )

    def where(self):
        return (
            "Beamline Energy : {}\nPolarization : {}\nSample Polarization : {}"
        ).format(
            colored(
                "{:.2f}".format(self.monoen.readback.get()).rstrip("0").rstrip("."),
                "yellow",
            ),
            colored(
                "{:.2f}".format(self.polarization.readback.get())
                    .rstrip("0")
                    .rstrip("."),
                "yellow",
            ),
            colored(
                "{:.2f}".format(self.sample_polarization.readback.get())
                    .rstrip("0")
                    .rstrip("."),
                "yellow",
            ),
        )

    def wh(self):
        boxed_text(self.name + " location", self.where_sp(), "green", shrink=True)

    def _sequential_move(self, real_pos, timeout=None, **kwargs):
        raise Exception("nope")

    # end class methods, begin internal methods

    # begin LUT Functions

    def __init__(
        self,
        a,
        rotation_motor=None,
        configpath=pathlib.Path(__file__).parent.absolute() / "config",
        **kwargs,
    ):
        super().__init__(a, **kwargs)
        self.gap_fit = np.zeros((10, 10))
        self.gap_fit[0][:] = [889.981, 222.966, -0.945368, 0.00290731, -5.87973e-06, 7.80556e-09, -6.69661e-12,
                              3.56679e-15, -1.07195e-18, 1.39775e-22]
        self.gap_fit[1][:] = [-51.6545, -1.60757, 0.00914746, -2.65003e-05, 4.46303e-08, -4.8934e-11, 3.51531e-14,
                              -1.4802e-17, 2.70647e-21, 0]
        self.gap_fit[2][:] = [9.74128, 0.0528884, -0.000270428, 6.71135e-07, -6.68204e-10, 2.71974e-13, -2.82766e-17,
                              -3.77566e-21, 0, 0]
        self.gap_fit[3][:] = [-2.94165, -0.00110173, 3.13309e-06, -1.21787e-08, 1.21638e-11, -4.27216e-15, 3.59552e-19,
                              0, 0, 0]
        self.gap_fit[4][:] = [0.19242, 2.19545e-05, 6.11159e-08, 4.21707e-11, -6.84942e-14, 1.84302e-17, 0, 0, 0, 0]
        self.gap_fit[5][:] = [-0.00615458, -9.55015e-07, -1.28929e-09, 4.28363e-13, 3.26302e-17, 0, 0, 0, 0, 0]
        self.gap_fit[6][:] = [0.000113341, 1.90112e-08, 6.92088e-12, -1.87659e-15, 0, 0, 0, 0, 0, 0]
        self.gap_fit[7][:] = [-1.22095e-06, -1.5686e-10, -1.09857e-14, 0, 0, 0, 0, 0, 0, 0]
        self.gap_fit[8][:] = [7.13593e-09, 4.69949e-13, 0, 0, 0, 0, 0, 0, 0, 0]
        self.gap_fit[9][:] = [-1.74622e-11, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        self.polphase = xr.load_dataarray(configpath / "polphase.nc")
        self.phasepol = xr.DataArray(
            data=self.polphase.pol,
            coords={"phase": self.polphase.values},
            dims={"phase"},
        )
        self.rotation_motor = rotation_motor

    def gap(
        self,
        energy,
        pol,
        locked,
        sim=0,
    ):
        if(sim):
            return self.epugap.get() # never move the gap if we are in simulated gap mode
            # this might cause problems if someone else is moving the gap, we might move it back
            # but I think this is not a common reason for this mode

        self.harmonic.set(self.choose_harmonic(energy, pol, locked))
        energy = energy / self.harmonic.get()

        if (pol == -1):
            encalc = energy - 105.002
            gap = 13979.0
            gap +=   82.857      * encalc ** 1
            gap +=   -0.26294    * encalc ** 2
            gap +=    0.00090199 * encalc ** 3
            gap +=   -2.3176e-06 * encalc ** 4
            gap +=    4.205e-09  * encalc ** 5
            gap +=   -5.139e-12  * encalc ** 6
            gap +=    4.0034e-15 * encalc ** 7
            gap +=   -1.7862e-18 * encalc ** 8
            gap +=    3.4687e-22 * encalc ** 9
            return max(14000.0,min(100000.0, gap))
        elif (pol == -0.5):
            encalc = energy - 104.996
            gap = 14013.0
            gap +=   82.76       * encalc ** 1
            gap +=   -0.26128    * encalc ** 2
            gap +=    0.00088353 * encalc ** 3
            gap +=   -2.2149e-06 * encalc ** 4
            gap +=    3.8919e-09 * encalc ** 5
            gap +=   -4.5887e-12 * encalc ** 6
            gap +=    3.4467e-15 * encalc ** 7
            gap +=   -1.4851e-18 * encalc ** 8
            gap +=    2.795e-22  * encalc ** 9
            return max(14000.0,min(100000.0, gap))
        elif 0 <= pol <= 90:
            return max(14000.0,min(100000.0, self.epu_gap(energy,pol)))
        elif 90 < pol <= 180:
            return max(14000.0,min(100000.0, self.epu_gap(energy,180.0-pol)))
        else:
            return np.nan


    def epu_gap(self, en, pol):
        """
        calculate the epu gap from the energy and polarization, using a 2D polynomial fit
        @param en: energy (valid between ~70 and 1300
        @param pol: polarization (valid between 0 and 90)
        @return: gap in microns
        """
        x = float(en)
        y = float(pol)
        z = 0.0
        for i in np.arange(self.gap_fit.shape[0]):
            for j in np.arange(self.gap_fit.shape[1]):
                z += self.gap_fit[j, i] * (x ** i) * (y ** j)
        return z

    def phase(self, en, pol,sim=0):
        if(sim):
            return self.epuphase.get() # never move the gap if we are in simulated gap mode
            # this might cause problems if someone else is moving the gap, we might move it back
            # but I think this is not a common reason for this mode
        if pol == -1:
            return 15000
        elif pol == -0.5:
            return 15000
        elif 90 < pol <= 180:
            return -min(29500.0, max(0.0,float(self.polphase.interp(pol=180 - pol, method="cubic"))))
        else:
            return min(29500.0, max(0.0, float(self.polphase.interp(pol=pol, method="cubic"))))

    def pol(self, phase, mode):
        if mode == 0:
            return -1
        elif mode == 1:
            return -0.5
        elif mode == 2:
            return float(self.phasepol.interp(phase=np.abs(phase), method="cubic"))
        elif mode == 3:
            return 180 - float(
                self.phasepol.interp(phase=np.abs(phase), method="cubic")
            )

    def mode(self, pol,sim=0):
        """

        @param pol:
        @return:
        """
        if(sim):
            return self.epumode.get() # never move the gap if we are in simulated gap mode
            # this might cause problems if someone else is moving the gap, we might move it back
            # but I think this is not a common reason for this mode
        if pol == -1:
            return 0
        elif pol == -0.5:
            return 1
        elif 90 < pol <= 180:
            return 3
        else:
            return 2

    def sample_pol(self, pol):
        th = self.rotation_motor.user_setpoint.get()
        return (
            np.arccos(np.cos(pol * np.pi / 180) * np.sin(th * np.pi / 180))
            * 180
            / np.pi
        )

    def m3pitchcalc(self,energy,locked):
        pitch = self.mir3Pitch.setpoint.get()
        if locked:
            return pitch
        elif "1200" in self.monoen.gratingx.readback.get():
            pitch =  self.m3offset.get()+0.038807*np.exp(-(energy-100)/91.942)+0.050123*np.exp(-(energy-100)/1188.9)
        elif "250" in self.monoen.gratingx.readback.get():
            pitch =  self.m3offset.get()+0.022665*np.exp(-(energy-90)/37.746)+0.024897*np.exp(-(energy-90)/450.9)
        return round(100*pitch)/100

    def choose_harmonic(self,energy,pol,locked):
        if locked:
            return self.harmonic.get()
        elif energy < 1200:
            return 1
        else:
            return 3


def base_set_polarization(pol, en):
    yield from bps.mv(en.polarization, pol)
    return 0


def base_grating_to_250(mono_en, en):
    type = mono_en.gratingx.readback.get()
    if '250' in type:
        print("the grating is already at 250 l/mm")
        return 0  # the grating is already here
    print("Moving the grating to 250 l/mm.  This will take a minute...")
    yield from psh4.close_plan()
    yield from bps.abs_set(mono_en.gratingx, 2, wait=True)
    #yield from bps.sleep(60)
    yield from bps.mv(mirror2.user_offset, 0.04) #0.0315)
    yield from bps.mv(grating.user_offset, -0.0874)#-0.0959)
    yield from bps.mv(mono_en.cff, 1.385)
    yield from bps.mv(en, 270)
    yield from psh4.open_plan()
    print("the grating is now at 250 l/mm")
    return 1


def base_grating_to_1200(mono_en, en):
    type = mono_en.gratingx.readback.get()
    if '1200' in type:
        print("the grating is already at 1200 l/mm")
        return 0  # the grating is already here
    print("Moving the grating to 1200 l/mm.  This will take a minute...")
    yield from psh4.close_plan()
    yield from bps.abs_set(mono_en.gratingx, 9, wait=True)
    #yield from bps.sleep(60)
    yield from bps.mv(mirror2.user_offset, 0.2044) #0.1962) #0.2052) # 0.1745)  # 8.1264)
    yield from bps.mv(grating.user_offset, 0.0769) #0.0687) # 0.0777) # 0.047)  # 7.2964)  # 7.2948)#7.2956
    yield from bps.mv(mono_en.cff, 1.7)

    yield from bps.mv(en, 270)
    yield from psh4.open_plan()
    print("the grating is now at 1200 l/mm")
    return 1


def epugap_from_en_pol(energy, polarization):
    gap = None
    if polarization == 190:  # vertical polarization (29500 phase)
        if 145.212 <= energy < 1100:
            enoff = energy - 145.212
            gap = (
                (enoff ** 0) * 14012.9679723399
                + (enoff ** 1) * 50.90077784479197
                + (enoff ** 2) * -0.151128059295173
                + (enoff ** 3) * 0.0007380466942855418
                + (enoff ** 4) * -2.88796126025716e-06
                + (enoff ** 5) * 7.334088791503296e-09
                + (enoff ** 6) * -1.138174337292876e-11
                + (enoff ** 7) * 1.043317214147193e-14
                + (enoff ** 8) * -5.190019656736424e-18
                + (enoff ** 9) * 1.081963010325867e-21
            )
        elif 1100 <= energy < 2200:  # third harmonic
            enoff = (energy / 3) - 145.212
            gap = (
                (enoff ** 0) * 14012.9679723399
                + (enoff ** 1) * 50.90077784479197
                + (enoff ** 2) * -0.151128059295173
                + (enoff ** 3) * 0.0007380466942855418
                + (enoff ** 4) * -2.88796126025716e-06
                + (enoff ** 5) * 7.334088791503296e-09
                + (enoff ** 6) * -1.138174337292876e-11
                + (enoff ** 7) * 1.043317214147193e-14
                + (enoff ** 8) * -5.190019656736424e-18
                + (enoff ** 9) * 1.081963010325867e-21
            )
        else:
            gap = None

    elif polarization == 126:  # 26000 phase

        if 159.381 <= energy < 1100:
            enoff = energy - 159.381
            gap = (
                (enoff ** 0) * 14016.21086765142
                + (enoff ** 1) * 47.07181476458327
                + (enoff ** 2) * -0.1300551161025656
                + (enoff ** 3) * 0.0006150285348211382
                + (enoff ** 4) * -2.293881944658508e-06
                + (enoff ** 5) * 5.587375098889097e-09
                + (enoff ** 6) * -8.43630153398218e-12
                + (enoff ** 7) * 7.633856981759912e-15
                + (enoff ** 8) * -3.794296038862279e-18
                + (enoff ** 9) * 7.983637046811202e-22
            )
        elif 1100 <= energy < 2200:  # third harmonic
            enoff = (energy / 3) - 159.381
            gap = (
                (enoff ** 0) * 14016.21086765142
                + (enoff ** 1) * 47.07181476458327
                + (enoff ** 2) * -0.1300551161025656
                + (enoff ** 3) * 0.0006150285348211382
                + (enoff ** 4) * -2.293881944658508e-06
                + (enoff ** 5) * 5.587375098889097e-09
                + (enoff ** 6) * -8.43630153398218e-12
                + (enoff ** 7) * 7.633856981759912e-15
                + (enoff ** 8) * -3.794296038862279e-18
                + (enoff ** 9) * 7.983637046811202e-22
            )
        else:
            gap = None
    elif polarization == 123:  # 23000 phase

        if 182.5 <= energy < 1100:
            enoff = energy - 182.5
            gap = (
                (enoff ** 0) * 14003.31346237464
                + (enoff ** 1) * 40.94577604418467
                + (enoff ** 2) * -0.06267710555062726
                + (enoff ** 3) * 0.0001737842192174001
                + (enoff ** 4) * -7.357701847539232e-07
                + (enoff ** 5) * 2.558819479531793e-09
                + (enoff ** 6) * -5.240182651164082e-12
                + (enoff ** 7) * 6.024494955600835e-15
                + (enoff ** 8) * -3.616738308743303e-18
                + (enoff ** 9) * 8.848652101678885e-22
            )
        elif 1100 <= energy < 2200:  # third harmonic
            enoff = (energy / 3) - 182.5
            gap = (
                (enoff ** 0) * 14003.31346237464
                + (enoff ** 1) * 40.94577604418467
                + (enoff ** 2) * -0.06267710555062726
                + (enoff ** 3) * 0.0001737842192174001
                + (enoff ** 4) * -7.357701847539232e-07
                + (enoff ** 5) * 2.558819479531793e-09
                + (enoff ** 6) * -5.240182651164082e-12
                + (enoff ** 7) * 6.024494955600835e-15
                + (enoff ** 8) * -3.616738308743303e-18
                + (enoff ** 9) * 8.848652101678885e-22
            )
        else:
            gap = None
    elif polarization == 121:  # 21000 phase

        if 198.751 <= energy < 1100:
            enoff = energy - 198.751
            gap = (
                (enoff ** 0) * 14036.87876588605
                + (enoff ** 1) * 36.26534721487319
                + (enoff ** 2) * -0.02493769623114209
                + (enoff ** 3) * 7.394536103134409e-05
                + (enoff ** 4) * -7.431387500375352e-07
                + (enoff ** 5) * 3.111643242754014e-09
                + (enoff ** 6) * -6.397457929818655e-12
                + (enoff ** 7) * 7.103146460443289e-15
                + (enoff ** 8) * -4.1024632494443e-18
                + (enoff ** 9) * 9.715673261754361e-22
            )
        elif 1100 <= energy < 2200:  # third harmonic
            enoff = (energy / 3) - 198.751
            gap = (
                (enoff ** 0) * 14036.87876588605
                + (enoff ** 1) * 36.26534721487319
                + (enoff ** 2) * -0.02493769623114209
                + (enoff ** 3) * 7.394536103134409e-05
                + (enoff ** 4) * -7.431387500375352e-07
                + (enoff ** 5) * 3.111643242754014e-09
                + (enoff ** 6) * -6.397457929818655e-12
                + (enoff ** 7) * 7.103146460443289e-15
                + (enoff ** 8) * -4.1024632494443e-18
                + (enoff ** 9) * 9.715673261754361e-22
            )
        else:
            gap = None
    elif polarization == 118:  # 18000 phase
        if 207.503 <= energy < 1100:
            enoff = energy - 207.503
            gap = (
                (enoff ** 0) * 14026.99244058688
                + (enoff ** 1) * 41.45793369967348
                + (enoff ** 2) * -0.05393526187293287
                + (enoff ** 3) * 0.000143951535786684
                + (enoff ** 4) * -3.934262835746608e-07
                + (enoff ** 5) * 6.627045869131144e-10
                + (enoff ** 6) * -4.544338541442881e-13
                + (enoff ** 7) * -8.922084434570775e-17
                + (enoff ** 8) * 2.598052818031009e-19
                + (enoff ** 9) * -8.57226301371417e-23
            )
        elif 1100 <= energy < 2200:  # third harmonic
            enoff = (energy / 3) - 207.503
            gap = (
                (enoff ** 0) * 14026.99244058688
                + (enoff ** 1) * 41.45793369967348
                + (enoff ** 2) * -0.05393526187293287
                + (enoff ** 3) * 0.000143951535786684
                + (enoff ** 4) * -3.934262835746608e-07
                + (enoff ** 5) * 6.627045869131144e-10
                + (enoff ** 6) * -4.544338541442881e-13
                + (enoff ** 7) * -8.922084434570775e-17
                + (enoff ** 8) * 2.598052818031009e-19
                + (enoff ** 9) * -8.57226301371417e-23
            )
        else:
            gap = None
    elif polarization == 115:  # 15000 phase
        if 182.504 <= energy < 1100:
            enoff = energy - 182.504
            gap = (
                (enoff ** 0) * 13992.18828384784
                + (enoff ** 1) * 53.60817055119084
                + (enoff ** 2) * -0.1051753524422272
                + (enoff ** 3) * 0.0003593146854690839
                + (enoff ** 4) * -1.31756627781552e-06
                + (enoff ** 5) * 3.797812404620049e-09
                + (enoff ** 6) * -7.051992603620334e-12
                + (enoff ** 7) * 7.780656762625199e-15
                + (enoff ** 8) * -4.613775121707344e-18
                + (enoff ** 9) * 1.130384721733557e-21
            )
        elif 1100 <= energy < 2200:  # third harmonic
            enoff = (energy / 3) - 182.504
            gap = (
                (enoff ** 0) * 13992.18828384784
                + (enoff ** 1) * 53.60817055119084
                + (enoff ** 2) * -0.1051753524422272
                + (enoff ** 3) * 0.0003593146854690839
                + (enoff ** 4) * -1.31756627781552e-06
                + (enoff ** 5) * 3.797812404620049e-09
                + (enoff ** 6) * -7.051992603620334e-12
                + (enoff ** 7) * 7.780656762625199e-15
                + (enoff ** 8) * -4.613775121707344e-18
                + (enoff ** 9) * 1.130384721733557e-21
            )
        else:
            gap = None
    elif polarization == 112:  # 12000 phase
        if 144.997 <= energy < 1100:
            enoff = energy - 144.997
            gap = (
                (enoff ** 0) * 13989.91908871217
                + (enoff ** 1) * 79.52996467926575
                + (enoff ** 2) * -0.397042588553584
                + (enoff ** 3) * 0.002410883165646499
                + (enoff ** 4) * -9.116960991617411e-06
                + (enoff ** 5) * 2.050737514265884e-08
                + (enoff ** 6) * -2.757338309663122e-11
                + (enoff ** 7) * 2.170984724060052e-14
                + (enoff ** 8) * -9.195312153413385e-18
                + (enoff ** 9) * 1.610241510211877e-21
            )
        elif 1100 <= energy < 2200:  # third harmonic
            enoff = (energy / 3) - 144.997
            gap = (
                (enoff ** 0) * 13989.91908871217
                + (enoff ** 1) * 79.52996467926575
                + (enoff ** 2) * -0.397042588553584
                + (enoff ** 3) * 0.002410883165646499
                + (enoff ** 4) * -9.116960991617411e-06
                + (enoff ** 5) * 2.050737514265884e-08
                + (enoff ** 6) * -2.757338309663122e-11
                + (enoff ** 7) * 2.170984724060052e-14
                + (enoff ** 8) * -9.195312153413385e-18
                + (enoff ** 9) * 1.610241510211877e-21
            )
        else:
            gap = None
    elif polarization == 108:  # 8000 phase

        if 130.875 <= energy < 1040:
            enoff = energy - 130.875
            gap = (
                (enoff ** 0) * 16104.67059771744
                + (enoff ** 1) * 98.54001020289179
                + (enoff ** 2) * -0.5947064552024715
                + (enoff ** 3) * 0.004033533429002568
                + (enoff ** 4) * -1.782124825808961e-05
                + (enoff ** 5) * 4.847183095095359e-08
                + (enoff ** 6) * -8.068283751628014e-11
                + (enoff ** 7) * 8.010337241397708e-14
                + (enoff ** 8) * -4.353748003371495e-17
                + (enoff ** 9) * 9.967428321189753e-21
            )
        elif 1040 <= energy < 2200:  # third harmonic
            enoff = (energy / 3) - 130.875
            gap = (
                (enoff ** 0) * 16104.67059771744
                + (enoff ** 1) * 98.54001020289179
                + (enoff ** 2) * -0.5947064552024715
                + (enoff ** 3) * 0.004033533429002568
                + (enoff ** 4) * -1.782124825808961e-05
                + (enoff ** 5) * 4.847183095095359e-08
                + (enoff ** 6) * -8.068283751628014e-11
                + (enoff ** 7) * 8.010337241397708e-14
                + (enoff ** 8) * -4.353748003371495e-17
                + (enoff ** 9) * 9.967428321189753e-21
            )
        else:
            gap = None
    elif polarization == 104:  # 4000 phase

        if 129.248 <= energy < 986:
            enoff = energy - 129.248
            gap = (
                (enoff ** 0) * 18071.42451568721
                + (enoff ** 1) * 105.3373080773754
                + (enoff ** 2) * -0.6939864876005439
                + (enoff ** 3) * 0.004579806360258253
                + (enoff ** 4) * -1.899845179678045e-05
                + (enoff ** 5) * 4.885880764915016e-08
                + (enoff ** 6) * -7.850671908438762e-11
                + (enoff ** 7) * 7.704987833035725e-14
                + (enoff ** 8) * -4.23491772565011e-17
                + (enoff ** 9) * 1.000126057875859e-20
            )
        elif 986 <= energy < 2200:  # third harmonic
            enoff = (energy / 3) - 129.248
            gap = (
                (enoff ** 0) * 18071.42451568721
                + (enoff ** 1) * 105.3373080773754
                + (enoff ** 2) * -0.6939864876005439
                + (enoff ** 3) * 0.004579806360258253
                + (enoff ** 4) * -1.899845179678045e-05
                + (enoff ** 5) * 4.885880764915016e-08
                + (enoff ** 6) * -7.850671908438762e-11
                + (enoff ** 7) * 7.704987833035725e-14
                + (enoff ** 8) * -4.23491772565011e-17
                + (enoff ** 9) * 1.000126057875859e-20
            )
        else:
            gap = None
    elif polarization == 1:  # circular polarization

        if 233.736 <= energy < 1800:
            enoff = energy - 233.736
            gap = (
                (enoff ** 0) * 15007.3400729319
                + (enoff ** 1) * 40.66671812653791
                + (enoff ** 2) * -0.07652786157391561
                + (enoff ** 3) * 0.0002182211302350642
                + (enoff ** 4) * -5.623344130428556e-07
                + (enoff ** 5) * 1.006174849255388e-09
                + (enoff ** 6) * -1.118133612192828e-12
                + (enoff ** 7) * 7.294270087002236e-16
                + (enoff ** 8) * -2.546331275323855e-19
                + (enoff ** 9) * 3.661307542366029e-23
            )
    else:
        # polarization is 100: # horizontal polarization - default

        if 80.0586 <= energy < 1100:
            enoff = energy - 80.0586
            gap = (
                (enoff ** 0) * 13999.72137152461
                + (enoff ** 1) * 123.5660983013199
                + (enoff ** 2) * -0.5357230317064841
                + (enoff ** 3) * 0.00207025419625126
                + (enoff ** 4) * -5.279184665398675e-06
                + (enoff ** 5) * 8.561167840842576e-09
                + (enoff ** 6) * -8.648473125484471e-12
                + (enoff ** 7) * 5.239890404156463e-15
                + (enoff ** 8) * -1.734402937759189e-18
                + (enoff ** 9) * 2.419654287110562e-22
            )
        elif 1100 <= energy < 2200:  # third harmonic
            enoff = (energy / 3) - 80.0586
            gap = (
                (enoff ** 0) * 13999.72137152461
                + (enoff ** 1) * 123.5660983013199
                + (enoff ** 2) * -0.5357230317064841
                + (enoff ** 3) * 0.00207025419625126
                + (enoff ** 4) * -5.279184665398675e-06
                + (enoff ** 5) * 8.561167840842576e-09
                + (enoff ** 6) * -8.648473125484471e-12
                + (enoff ** 7) * 5.239890404156463e-15
                + (enoff ** 8) * -1.734402937759189e-18
                + (enoff ** 9) * 2.419654287110562e-22
            )
        else:
            gap = None
    return gap



class EnSimEPUPos(PseudoPositioner):
        """Energy pseudopositioner class.

        Parameters:
        -----------


        """

        # synthetic axis
        energy = Cpt(PseudoSingle, kind="hinted", limits=(71, 2250), name="Beamline Energy")
        polarization = Cpt(
            PseudoSingle, kind="hinted", limits=(-1, 180), name="X-ray Polarization"
        )
        sample_polarization = Cpt(
            PseudoSingle, kind="hinted", name="Sample X-ray polarization"
        )
        # real motors

        monoen = Cpt(
            Monochromator, "XF:07ID1-OP{Mono:PGM1-Ax:", kind="hinted", name="Mono Energy"
        )
        epugap = Cpt(
            SoftPositioner,
            kind="normal",
            name="Fake EPU Gap",
        )
        epuphase = Cpt(
            SoftPositioner,
            kind="normal",
            name="Fake EPU Phase",
        )
        mir3Pitch = Cpt(
            FMBHexapodMirrorAxisStandAlonePitch,
            "XF:07ID1-OP{Mir:M3ABC",
            kind="normal",
            name="M3Pitch",
        )
        epumode = Cpt(SoftPositioner,
                              name='Fake EPU Mode', kind='normal')


        sim_epu_mode = Cpt(Signal,value=0,name='dont interact with the real EPU',kind='config')
        scanlock = Cpt(Signal,value=0,name="Lock Harmonic, Pitch, Grating for scan",kind='config')
        harmonic = Cpt(Signal, value=1, name="EPU Harmonic",kind='config')
        m3offset = Cpt(Signal, value=7.91, name="EPU Harmonic",kind='config')
        rotation_motor = None

        @pseudo_position_argument
        def forward(self, pseudo_pos):
            """Run a forward (pseudo -> real) calculation"""
            # print('In forward')
            ret = self.RealPosition(
                epugap=self.gap(pseudo_pos.energy, pseudo_pos.polarization,self.scanlock.get(),self.sim_epu_mode.get()),
                monoen=pseudo_pos.energy,
                epuphase=abs(self.phase(pseudo_pos.energy, pseudo_pos.polarization,self.sim_epu_mode.get())),
                mir3Pitch=self.m3pitchcalc(pseudo_pos.energy,self.scanlock.get()),
                epumode=self.mode(pseudo_pos.polarization,self.sim_epu_mode.get()),
                #harmonic=self.choose_harmonic(pseudo_pos.energy,pseudo_pos.polarization,self.scanlock.get())
            )
            # print('finished forward')
            return ret

        @real_position_argument
        def inverse(self, real_pos):
            """Run an inverse (real -> pseudo) calculation"""
            # print('in Inverse')
            ret = self.PseudoPosition(
                energy=real_pos.monoen,
                polarization=self.pol(real_pos.epuphase, real_pos.epumode),
                sample_polarization=self.sample_pol(
                    self.pol(real_pos.epuphase, real_pos.epumode)
                ),
            )
            # print('Finished inverse')
            return ret

        def where_sp(self):
            return (
                "Beamline Energy Setpoint : {}"
                "\nMonochromator Readback : {}"
                "\nEPU Gap Setpoint : {}"
                "\nEPU Gap Readback : {}"
                "\nEPU Phase Setpoint : {}"
                "\nEPU Phase Readback : {}"
                "\nEPU Mode Setpoint : {}"
                "\nEPU Mode Readback : {}"
                "\nGrating Setpoint : {}"
                "\nGrating Readback : {}"
                "\nGratingx Setpoint : {}"
                "\nGratingx Readback : {}"
                "\nMirror2 Setpoint : {}"
                "\nMirror2 Readback : {}"
                "\nMirror2x Setpoint : {}"
                "\nMirror2x Readback : {}"
                "\nCFF : {}"
                "\nVLS : {}"
            ).format(
                colored(
                    "{:.2f}".format(self.monoen.setpoint.get()).rstrip("0").rstrip("."),
                    "yellow",
                ),
                colored(
                    "{:.2f}".format(self.monoen.readback.get()).rstrip("0").rstrip("."),
                    "yellow",
                ),
                colored(
                    "{:.2f}".format(self.epugap.user_setpoint.get())
                        .rstrip("0")
                        .rstrip("."),
                    "yellow",
                ),
                colored(
                    "{:.2f}".format(self.epugap.user_readback.get())
                        .rstrip("0")
                        .rstrip("."),
                    "yellow",
                ),
                colored(
                    "{:.2f}".format(self.epuphase.user_setpoint.get())
                        .rstrip("0")
                        .rstrip("."),
                    "yellow",
                ),
                colored(
                    "{:.2f}".format(self.epuphase.user_readback.get())
                        .rstrip("0")
                        .rstrip("."),
                    "yellow",
                ),
                colored(
                    "{:.2f}".format(self.epumode.setpoint.get())
                        .rstrip("0")
                        .rstrip("."),
                    "yellow",
                ),
                colored(
                    "{:.2f}".format(self.epumode.readback.get())
                        .rstrip("0")
                        .rstrip("."),
                    "yellow",
                ),
                colored(
                    "{:.2f}".format(self.monoen.grating.user_setpoint.get())
                        .rstrip("0")
                        .rstrip("."),
                    "yellow",
                ),
                colored(
                    "{:.2f}".format(self.monoen.grating.user_readback.get())
                        .rstrip("0")
                        .rstrip("."),
                    "yellow",
                ),
                colored(self.monoen.gratingx.setpoint.get(),
                        "yellow",
                        ),
                colored(self.monoen.gratingx.readback.get(),
                        "yellow",
                        ),
                colored(
                    "{:.2f}".format(self.monoen.mirror2.user_setpoint.get())
                        .rstrip("0")
                        .rstrip("."),
                    "yellow",
                ),
                colored(
                    "{:.2f}".format(self.monoen.mirror2.user_readback.get())
                        .rstrip("0")
                        .rstrip("."),
                    "yellow",
                ),
                colored(self.monoen.mirror2x.setpoint.get(),
                        "yellow",
                        ),
                colored(self.monoen.mirror2x.readback.get(),
                        "yellow",
                        ),
                colored(
                    "{:.2f}".format(self.monoen.cff.get()).rstrip("0").rstrip("."), "yellow"
                ),
                colored(
                    "{:.2f}".format(self.monoen.vls.get()).rstrip("0").rstrip("."), "yellow"
                ),
            )

        def where(self):
            return (
                "Beamline Energy : {}\nPolarization : {}\nSample Polarization : {}"
            ).format(
                colored(
                    "{:.2f}".format(self.monoen.readback.get()).rstrip("0").rstrip("."),
                    "yellow",
                ),
                colored(
                    "{:.2f}".format(self.polarization.readback.get())
                        .rstrip("0")
                        .rstrip("."),
                    "yellow",
                ),
                colored(
                    "{:.2f}".format(self.sample_polarization.readback.get())
                        .rstrip("0")
                        .rstrip("."),
                    "yellow",
                ),
            )

        def wh(self):
            boxed_text(self.name + " location", self.where_sp(), "green", shrink=True)

        def _sequential_move(self, real_pos, timeout=None, **kwargs):
            raise Exception("nope")

        # end class methods, begin internal methods

        # begin LUT Functions

        def __init__(
            self,
            a,
            rotation_motor=None,
            configpath=pathlib.Path(__file__).parent.absolute() / "config",
            **kwargs,
        ):
            super().__init__(a, **kwargs)
            self.gap_fit = np.zeros((10, 10))
            self.gap_fit[0][:] = [889.981, 222.966, -0.945368, 0.00290731, -5.87973e-06, 7.80556e-09, -6.69661e-12,
                                  3.56679e-15, -1.07195e-18, 1.39775e-22]
            self.gap_fit[1][:] = [-51.6545, -1.60757, 0.00914746, -2.65003e-05, 4.46303e-08, -4.8934e-11, 3.51531e-14,
                                  -1.4802e-17, 2.70647e-21, 0]
            self.gap_fit[2][:] = [9.74128, 0.0528884, -0.000270428, 6.71135e-07, -6.68204e-10, 2.71974e-13, -2.82766e-17,
                                  -3.77566e-21, 0, 0]
            self.gap_fit[3][:] = [-2.94165, -0.00110173, 3.13309e-06, -1.21787e-08, 1.21638e-11, -4.27216e-15, 3.59552e-19,
                                  0, 0, 0]
            self.gap_fit[4][:] = [0.19242, 2.19545e-05, 6.11159e-08, 4.21707e-11, -6.84942e-14, 1.84302e-17, 0, 0, 0, 0]
            self.gap_fit[5][:] = [-0.00615458, -9.55015e-07, -1.28929e-09, 4.28363e-13, 3.26302e-17, 0, 0, 0, 0, 0]
            self.gap_fit[6][:] = [0.000113341, 1.90112e-08, 6.92088e-12, -1.87659e-15, 0, 0, 0, 0, 0, 0]
            self.gap_fit[7][:] = [-1.22095e-06, -1.5686e-10, -1.09857e-14, 0, 0, 0, 0, 0, 0, 0]
            self.gap_fit[8][:] = [7.13593e-09, 4.69949e-13, 0, 0, 0, 0, 0, 0, 0, 0]
            self.gap_fit[9][:] = [-1.74622e-11, 0, 0, 0, 0, 0, 0, 0, 0, 0]

            self.polphase = xr.load_dataarray(configpath / "polphase.nc")
            self.phasepol = xr.DataArray(
                data=self.polphase.pol,
                coords={"phase": self.polphase.values},
                dims={"phase"},
            )
            self.rotation_motor = rotation_motor

        def gap(
            self,
            energy,
            pol,
            locked,
            sim=0,
        ):
            if(sim):
                return self.epugap.get() # never move the gap if we are in simulated gap mode
                # this might cause problems if someone else is moving the gap, we might move it back
                # but I think this is not a common reason for this mode

            self.harmonic.set(self.choose_harmonic(energy, pol, locked))
            energy = energy / self.harmonic.get()

            if (pol == -1):
                encalc = energy - 105.002
                gap = 13979.0
                gap +=   82.857      * encalc ** 1
                gap +=   -0.26294    * encalc ** 2
                gap +=    0.00090199 * encalc ** 3
                gap +=   -2.3176e-06 * encalc ** 4
                gap +=    4.205e-09  * encalc ** 5
                gap +=   -5.139e-12  * encalc ** 6
                gap +=    4.0034e-15 * encalc ** 7
                gap +=   -1.7862e-18 * encalc ** 8
                gap +=    3.4687e-22 * encalc ** 9
                return max(14000.0,min(100000.0, gap))
            elif (pol == -0.5):
                encalc = energy - 104.996
                gap = 14013.0
                gap +=   82.76       * encalc ** 1
                gap +=   -0.26128    * encalc ** 2
                gap +=    0.00088353 * encalc ** 3
                gap +=   -2.2149e-06 * encalc ** 4
                gap +=    3.8919e-09 * encalc ** 5
                gap +=   -4.5887e-12 * encalc ** 6
                gap +=    3.4467e-15 * encalc ** 7
                gap +=   -1.4851e-18 * encalc ** 8
                gap +=    2.795e-22  * encalc ** 9
                return max(14000.0,min(100000.0, gap))
            elif 0 <= pol <= 90:
                return max(14000.0,min(100000.0, self.epu_gap(energy,pol)))
            elif 90 < pol <= 180:
                return max(14000.0,min(100000.0, self.epu_gap(energy,180.0-pol)))
            else:
                return np.nan


        def epu_gap(self, en, pol):
            """
            calculate the epu gap from the energy and polarization, using a 2D polynomial fit
            @param en: energy (valid between ~70 and 1300
            @param pol: polarization (valid between 0 and 90)
            @return: gap in microns
            """
            x = float(en)
            y = float(pol)
            z = 0.0
            for i in np.arange(self.gap_fit.shape[0]):
                for j in np.arange(self.gap_fit.shape[1]):
                    z += self.gap_fit[j, i] * (x ** i) * (y ** j)
            return z

        def phase(self, en, pol,sim=0):
            if(sim):
                return self.epuphase.get() # never move the gap if we are in simulated gap mode
                # this might cause problems if someone else is moving the gap, we might move it back
                # but I think this is not a common reason for this mode
            if pol == -1:
                return 15000
            elif pol == -0.5:
                return 15000
            elif 90 < pol <= 180:
                return -min(29500.0, max(0.0,float(self.polphase.interp(pol=180 - pol, method="cubic"))))
            else:
                return min(29500.0, max(0.0, float(self.polphase.interp(pol=pol, method="cubic"))))

        def pol(self, phase, mode):
            if mode == 0:
                return -1
            elif mode == 1:
                return -0.5
            elif mode == 2:
                return float(self.phasepol.interp(phase=np.abs(phase), method="cubic"))
            elif mode == 3:
                return 180 - float(
                    self.phasepol.interp(phase=np.abs(phase), method="cubic")
                )

        def mode(self, pol,sim=0):
            """

            @param pol:
            @return:
            """
            if(sim):
                return self.epumode.get() # never move the gap if we are in simulated gap mode
                # this might cause problems if someone else is moving the gap, we might move it back
                # but I think this is not a common reason for this mode
            if pol == -1:
                return 0
            elif pol == -0.5:
                return 1
            elif 90 < pol <= 180:
                return 3
            else:
                return 2

        def sample_pol(self, pol):
            th = self.rotation_motor.user_setpoint.get()
            return (
                np.arccos(np.cos(pol * np.pi / 180) * np.sin(th * np.pi / 180))
                * 180
                / np.pi
            )

        def m3pitchcalc(self,energy,locked):
            pitch = self.mir3Pitch.setpoint.get()
            if locked:
                return pitch
            elif "1200" in self.monoen.gratingx.readback.get():
                pitch =  self.m3offset.get()+0.038807*np.exp(-(energy-100)/91.942)+0.050123*np.exp(-(energy-100)/1188.9)
            elif "250" in self.monoen.gratingx.readback.get():
                pitch =  self.m3offset.get()+0.022665*np.exp(-(energy-90)/37.746)+0.024897*np.exp(-(energy-90)/450.9)
            return round(100*pitch)/100

        def choose_harmonic(self,energy,pol,locked):
            if locked:
                return self.harmonic.get()
            elif energy < 1200:
                return 1
            else:
                return 3
