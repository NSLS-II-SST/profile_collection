from ..CommonFunctions.functions import run_report
run_report(__file__)

from ..SSTBase.motors import *

Exit_Slit = prettymotor('XF:07ID2-BI{Slt:11-Ax:YGap}Mtr', name='Exit Slit of Mono Vertical Gap',kind='hinted')
grating = prettymotor('XF:07ID1-OP{Mono:PGM1-Ax:GrtP}Mtr',name="Mono Grating",kind='hinted')
mirror2 = prettymotor('XF:07ID1-OP{Mono:PGM1-Ax:MirP}Mtr',name="Mono Mirror",kind='hinted')
gratingx = prettymotor('XF:07ID1-OP{Mono:PGM1-Ax:GrtX}Mtr',name="Mono Grating",kind='hinted')
mirror2x = prettymotor('XF:07ID1-OP{Mono:PGM1-Ax:MirX}Mtr',name="Mono Mirror",kind='hinted')