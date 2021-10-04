from startup.SST.CommonFunctions.functions import run_report
from startup.SST.RSoXS.Base.syringepump import Syringe_Pump

run_report(__file__)

SP = Syringe_Pump("XF:07ID1-ES", name="sp")
