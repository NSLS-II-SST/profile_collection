print(f'Loading {__file__}...')

from ophyd import EpicsMotor
sam_X = EpicsMotor('XF:07ID2-ES1{Stg-Ax:X}Mtr', name='RSoXS Sample Outboard-Inboard',kind='hinted')
sam_Y = EpicsMotor('XF:07ID2-ES1{Stg-Ax:Y}Mtr', name='RSoXS Sample Up-Down',kind='hinted')
sam_Z = EpicsMotor('XF:07ID2-ES1{Stg-Ax:Z}Mtr', name='RSoXS Sample Downstream-Upstream',kind='hinted')
sam_Th = EpicsMotor('XF:07ID2-ES1{Stg-Ax:Yaw}Mtr', name='RSoXS Sample Rotation',kind='hinted')
BSw = BeamStopW = EpicsMotor('XF:07ID2-ES1{BS-Ax:1}Mtr', name='Beam Stop WAXS',kind='hinted')
BSs = BeamStopS = EpicsMotor('XF:07ID2-ES1{BS-Ax:2}Mtr', name='Beam Stop SAXS',kind='hinted')
Det_W = EpicsMotor('XF:07ID2-ES1{Det-Ax:1}Mtr', name='Detector WAXS Translation',kind='hinted')
Det_S = EpicsMotor('XF:07ID2-ES1{Det-Ax:2}Mtr', name='Detector SAXS Translation',kind='hinted')
Shutter_Y = EpicsMotor('XF:07ID2-ES1{FSh-Ax:1}Mtr', name='Shutter Vertical Translation',kind='hinted')
Izero_Y = EpicsMotor('XF:07ID2-ES1{Scr-Ax:1}Mtr', name='Izero Assembly Vertical Translation',kind='hinted')
Izero_ds = EpicsMotor('XF:07ID2-BI{Diag:07-Ax:Y}Mtr', name='Downstream Izero DM7 Vertical Translation',kind='hinted')
Exit_Slit = EpicsMotor('XF:07ID2-BI{Slt:11-Ax:YGap}Mtr', name='Exit Slit of Mono Vertical Gap',kind='hinted')

sd.baseline.extend([sam_X, sam_Y, sam_Z, sam_Th, BeamStopS, BeamStopW, Det_S, Det_W, Shutter_Y, Izero_Y, Izero_ds])

