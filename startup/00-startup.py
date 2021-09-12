
from .CommonFunctions.functions import *
run_report(__file__)

# SST devices  These all reference the base classes and instantiate the objects themselves into the current namespace (I hope)
from .SSTObjects.gatevalves import *
from .SSTObjects.shutters import *
from .SSTObjects.vacuum import *
from startup.RSoXSObjects.energy import *
from .SSTObjects.motors import *
from .SSTObjects.mirrors import *
from .SSTObjects.diode import *

# SST code  # Common code
from .SSTBase.archiver import *

# RSoXS startup - bluesky RE / db / md definitions
from .RSoXSBase.startup import *

# RSoXS specific devices
from .RSoXSObjects.motors import *
from .RSoXSObjects.cameras import *
from .RSoXSObjects.signals import *
from .RSoXSObjects.detectors import *
from .RSoXSObjects.slits import *
from .RSoXSObjects.syringepump import *

# RSoXS specific code
from .RSoXSBase.configurations import *
from .RSoXSBase.schemas import *
from .RSoXSBase.PVdictionary import *
from .RSoXSBase.common_procedures import *
from .RSoXSBase.common_metadata import *
from .RSoXSBase.energyscancore import *
from .RSoXSBase.energyscans import *
from .RSoXSBase.NEXAFSscans import *
from .RSoXSBase.alignment import *

user() # print out the current user metadata
beamline_status() # print out the current sample metadata, motor position and detector status
