from IPython.core.magic import register_line_magic
from ophyd import EpicsMotor, EpicsSignal
from ophyd.sim import motor1
from ophyd import Component as Cpt


run_report(__file__)

class FMBOEpicsMotor(EpicsMotor):
    resolution = Cpt(EpicsSignal, '.MRES')
    encoder = Cpt(EpicsSignal, '.REP')
    clr_enc_lss = Cpt(EpicsSignal, '_ENC_LSS_CLR_CMD.PROC')
    home_cmd = Cpt(EpicsSignal, '_HOME_CMD.PROC')
    enable = Cpt(EpicsSignal, '_ENA_CMD.PROC')
    kill = Cpt(EpicsSignal, '_KILL_CMD.PROC')

    status_list = ('MTACT', 'MLIM', 'PLIM', 'AMPEN', 'LOOPM', 'TIACT', 'INTMO',
                   'DWPRO', 'DAERR', 'DVZER', 'ABDEC', 'UWPEN', 'UWSEN', 'ERRTAG',
                   'SWPOC', 'ASSCS', 'FRPOS', 'HSRCH', 'SODPL', 'SOPL', 'HOCPL',
                   'PHSRA', 'PREFE', 'TRMOV', 'IFFE', 'AMFAE', 'AMFE', 'FAFOE',
                   'WFOER', 'INPOS', 'ENC_LSS')

    ###################################################################
    # this is the complete list of status signals defined in the FMBO #
    # IOC for thier MCS8 motor controllers                            #
    ###################################################################
    mtact      = Cpt(EpicsSignal, '_MTACT_STS')
    mtact_desc = Cpt(EpicsSignal, '_MTACT_STS.DESC')
    mlim       = Cpt(EpicsSignal, '_MLIM_STS')
    mlim_desc  = Cpt(EpicsSignal, '_MLIM_STS.DESC')
    plim       = Cpt(EpicsSignal, '_PLIM_STS')
    plim_desc  = Cpt(EpicsSignal, '_PLIM_STS.DESC')
    ampen      = Cpt(EpicsSignal, '_AMPEN_STS')
    ampen_desc = Cpt(EpicsSignal, '_AMPEN_STS.DESC')
    loopm      = Cpt(EpicsSignal, '_LOOPM_STS')
    loopm_desc = Cpt(EpicsSignal, '_LOOPM_STS.DESC')
    tiact      = Cpt(EpicsSignal, '_TIACT_STS')
    tiact_desc = Cpt(EpicsSignal, '_TIACT_STS.DESC')
    intmo      = Cpt(EpicsSignal, '_INTMO_STS')
    intmo_desc = Cpt(EpicsSignal, '_INTMO_STS.DESC')
    dwpro      = Cpt(EpicsSignal, '_DWPRO_STS')
    dwpro_desc = Cpt(EpicsSignal, '_DWPRO_STS.DESC')
    daerr      = Cpt(EpicsSignal, '_DAERR_STS')
    daerr_desc = Cpt(EpicsSignal, '_DAERR_STS.DESC')
    dvzer      = Cpt(EpicsSignal, '_DVZER_STS')
    dvzer_desc = Cpt(EpicsSignal, '_DVZER_STS.DESC')
    abdec      = Cpt(EpicsSignal, '_ABDEC_STS')
    abdec_desc = Cpt(EpicsSignal, '_ABDEC_STS.DESC')
    uwpen      = Cpt(EpicsSignal, '_UWPEN_STS')
    uwpen_desc = Cpt(EpicsSignal, '_UWPEN_STS.DESC')
    uwsen      = Cpt(EpicsSignal, '_UWSEN_STS')
    uwsen_desc = Cpt(EpicsSignal, '_UWSEN_STS.DESC')
    errtg      = Cpt(EpicsSignal, '_ERRTG_STS')
    errtg_desc = Cpt(EpicsSignal, '_ERRTG_STS.DESC')
    swpoc      = Cpt(EpicsSignal, '_SWPOC_STS')
    swpoc_desc = Cpt(EpicsSignal, '_SWPOC_STS.DESC')
    asscs      = Cpt(EpicsSignal, '_ASSCS_STS')
    asscs_desc = Cpt(EpicsSignal, '_ASSCS_STS.DESC')
    frpos      = Cpt(EpicsSignal, '_FRPOS_STS')
    frpos_desc = Cpt(EpicsSignal, '_FRPOS_STS.DESC')
    hsrch      = Cpt(EpicsSignal, '_HSRCH_STS')
    hsrch_desc = Cpt(EpicsSignal, '_HSRCH_STS.DESC')
    sodpl      = Cpt(EpicsSignal, '_SODPL_STS')
    sodpl_desc = Cpt(EpicsSignal, '_SODPL_STS.DESC')
    sopl       = Cpt(EpicsSignal, '_SOPL_STS')
    sopl_desc  = Cpt(EpicsSignal, '_SOPL_STS.DESC')
    hocpl      = Cpt(EpicsSignal, '_HOCPL_STS')
    hocpl_desc = Cpt(EpicsSignal, '_HOCPL_STS.DESC')
    phsra      = Cpt(EpicsSignal, '_PHSRA_STS')
    phsra_desc = Cpt(EpicsSignal, '_PHSRA_STS.DESC')
    prefe      = Cpt(EpicsSignal, '_PREFE_STS')
    prefe_desc = Cpt(EpicsSignal, '_PREFE_STS.DESC')
    trmov      = Cpt(EpicsSignal, '_TRMOV_STS')
    trmov_desc = Cpt(EpicsSignal, '_TRMOV_STS.DESC')
    iffe       = Cpt(EpicsSignal, '_IFFE_STS')
    iffe_desc  = Cpt(EpicsSignal, '_IFFE_STS.DESC')
    amfae      = Cpt(EpicsSignal, '_AMFAE_STS')
    amfae_desc = Cpt(EpicsSignal, '_AMFAE_STS.2ESC')
    amfe       = Cpt(EpicsSignal, '_AMFE_STS')
    amfe_desc  = Cpt(EpicsSignal, '_AMFE_STS.DESC')
    fafoe      = Cpt(EpicsSignal, '_FAFOE_STS')
    fafoe_desc = Cpt(EpicsSignal, '_FAFOE_STS.DESC')
    wfoer      = Cpt(EpicsSignal, '_WFOER_STS')
    wfoer_desc = Cpt(EpicsSignal, '_WFOER_STS.DESC')
    inpos      = Cpt(EpicsSignal, '_INPOS_STS')
    inpos_desc = Cpt(EpicsSignal, '_INPOS_STS.DESC')
    enc_lss      = Cpt(EpicsSignal, '_ENC_LSS_STS')
    enc_lss_desc = Cpt(EpicsSignal, '_ENC_LSS_STS.DESC')


    def home(self,*args,**kwargs):
        yield from bps.mv(self.home_cmd,1)

    def clear_encoder_loss(self):
        yield from bps.mv(self.clr_enc_lss,1)

    def status(self):
        text = '\n  EPICS PV base : %s\n\n' % (self.prefix)
        for signal in self.status_list:
            if signal.upper() not in self.status_list:
                continue
            suffix = getattr(self, signal).pvname.replace(self.prefix, '')
            if getattr(self, signal).get():
                value_color = 'lightgreen'
            else:
                value_color = 'lightred'

            text += '  %-26s : %-35s  %s   %s \n' % (
                getattr(self, signal+'_desc').get(),
                colored(getattr(self, signal).enum_strs[getattr(self, signal).get()],value_color),
                colored(getattr(self, signal).get(),value_color),
                whisper(suffix))
        boxed_text('%s status signals' % self.name, text, 'green',shrink=True)

class prettymotor(FMBOEpicsMotor):
    def __init__(self,*args,**kwargs):
        super(prettymotor, self).__init__(*args,**kwargs)
        self.read_attrs = ['user_readback', 'user_setpoint']
    def where(self):
        return ('{} : {}').format(
            colored(self.name, 'lightblue'),
            colored('{:.2f}'.format(self.user_readback.get()).rstrip('0').rstrip('.'), 'yellow'))

    def where_sp(self):
        return ('{} Setpoint : {}\n{} Readback : {}').format(
            colored(self.name, 'lightblue'),
            colored('{:.2f}'.format(self.user_readback.get()).rstrip('0').rstrip('.'), 'yellow'),
            colored(self.name, 'lightblue'),
            colored('{:.2f}'.format(self.user_setpoint.get()).rstrip('0').rstrip('.'), 'yellow'))

    def wh(self):
        boxed_text(self.name+" location", self.where_sp(), 'green',shrink=True)

    def status_or_rel_move(self,line):
        try:
            loc = float(line)
        except:
            if len(line)>0:
                if line[0] is 's':
                    self.status() # followed by an s, display status
                elif line[0] is 'a':
                    try:
                        loc = float(line[1:])
                    except:
                        #followed by an a but not a number, just display location
                        boxed_text(self.name, self.where_sp(), 'lightgray', shrink=True)
                    else:
                        # followed by an a and a number, do absolute move
                        RE(bps.mv(self, loc))
                        boxed_text(self.name, self.where_sp(), 'lightgray', shrink=True)
                else:
                    # followed by something besides a number, a or s, just show location
                    boxed_text(self.name, self.where_sp(), 'lightgray', shrink=True)
            else:
                # followed by something besides a number, a or s, just show location
                boxed_text(self.name, self.where_sp(), 'lightgray', shrink=True)
        else:
            # followed by a number - relative move
            RE(bps.mvr(self, loc))
            boxed_text(self.name, self.where(), 'lightgray', shrink=True)




sam_viewer = prettymotor('XF:07ID2-ES1{ImgY-Ax:1}Mtr', name='RSoXS Sample Imager',kind='hinted')
sam_X = prettymotor('XF:07ID2-ES1{Stg-Ax:X}Mtr', name='RSoXS Sample Outboard-Inboard',kind='hinted')
sam_Y = prettymotor('XF:07ID2-ES1{Stg-Ax:Y}Mtr', name='RSoXS Sample Up-Down',kind='hinted')
sam_Z = prettymotor('XF:07ID2-ES1{Stg-Ax:Z}Mtr', name='RSoXS Sample Downstream-Upstream',kind='hinted')
sam_Th = prettymotor('XF:07ID2-ES1{Stg-Ax:Yaw}Mtr', name='RSoXS Sample Rotation',kind='hinted')
BeamStopW = prettymotor('XF:07ID2-ES1{BS-Ax:1}Mtr', name='Beam Stop WAXS',kind='hinted')
BeamStopS = prettymotor('XF:07ID2-ES1{BS-Ax:2}Mtr', name='Beam Stop SAXS',kind='hinted')
Det_W = prettymotor('XF:07ID2-ES1{Det-Ax:2}Mtr', name='Detector WAXS Translation',kind='hinted')
Det_S = prettymotor('XF:07ID2-ES1{Det-Ax:1}Mtr', name='Detector SAXS Translation',kind='hinted')
Shutter_Y = prettymotor('XF:07ID2-ES1{FSh-Ax:1}Mtr', name='Shutter Vertical Translation',kind='hinted')
Izero_Y = prettymotor('XF:07ID2-ES1{Scr-Ax:1}Mtr', name='Izero Assembly Vertical Translation',kind='hinted')
Izero_ds = prettymotor('XF:07ID2-BI{Diag:07-Ax:Y}Mtr', name='Downstream Izero DM7 Vertical Translation',kind='hinted')
Exit_Slit = prettymotor('XF:07ID2-BI{Slt:11-Ax:YGap}Mtr', name='Exit Slit of Mono Vertical Gap',kind='hinted')
grating = prettymotor('XF:07ID1-OP{Mono:PGM1-Ax:GrtP}Mtr',name="Mono Grating",kind='hinted')
mirror2 = prettymotor('XF:07ID1-OP{Mono:PGM1-Ax:MirP}Mtr',name="Mono Mirror",kind='hinted')




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


Shutter_enable   = EpicsSignal('XF:07IDB-CT{DIODE-MTO:1}OutMaskBit:2-Sel',
                           name = 'RSoXS Shutter Toggle Enable', kind='normal')
Shutter_enable1   = EpicsSignal('XF:07IDB-CT{DIODE-MTO:1}InMaskBit:1-Sel',
                           name = 'RSoXS Shutter Toggle Enable In', kind='normal')
Shutter_enable2   = EpicsSignal('XF:07IDB-CT{DIODE-MTO:1}InMaskBit:2-Sel',
                           name = 'RSoXS Shutter Toggle Enable In2', kind='normal',put_complete=False,auto_monitor=False)
Shutter_enable3   = EpicsSignal('XF:07IDB-CT{DIODE-MTO:1}InMaskBit:3-Sel',
                           name = 'RSoXS Shutter Toggle Enable In3', kind='normal')
Shutter_control   = EpicsSignal('XF:07IDB-CT{DIODE-Local:1}OutPt01:Data-Sel',
                           name = 'RSoXS Shutter Toggle', kind='normal')
Shutter_delay   = EpicsSignal('XF:07IDB-CT{DIODE-MTO:1}OutDelaySet:2-SP',
                           name = 'RSoXS Shutter Delay (ms)', kind='normal')
Shutter_open_time   = EpicsSignal('XF:07IDB-CT{DIODE-MTO:1}OutWidthSet:2-SP',
                           name = 'RSoXS Shutter Opening Time (ms)', kind='normal')
Shutter_trigger   = EpicsSignal('XF:07IDB-CT{DIODE-MTO:1}Trigger:PV-Cmd',
                           name = 'RSoXS Shutter Trigger', kind='normal')
Light_control   = EpicsSignal('XF:07IDB-CT{DIODE-Local:1}OutPt05:Data-Sel',
                           name = 'RSoXS Light Toggle', kind='normal')

sd.monitors.extend([Shutter_control]) # this will give us a monitor to time the shutter opens and close

sd.baseline.extend([sam_viewer, sam_X, sam_Y, sam_Z, sam_Th, BeamStopS, BeamStopW, Det_S, Det_W,
                    Shutter_Y, Izero_Y, Izero_ds, grating, mirror2])
# s