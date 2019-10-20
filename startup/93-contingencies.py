import bluesky.plan_stubs as bps
from bluesky.suspenders import SuspendBoolHigh, SuspendFloor
import logging

run_report(__file__)


bls_email = 'egann@bnl.gov'


def send_notice(email,subject,msg):
    os.system('echo '+msg+' | mail -s "'+subject+'" '+email)


def send_notice_plan(email,subject,msg):
    yield from bps.sleep(.1)
    send_notice(email,subject,msg)

def enc_clr_x():
    send_notice('egann@bnl.gov','SST HAS FALLEN','the encoder loss has happened on the RSoXS beamline')
    xpos = sam_X.user_readback.value
    yield from sam_X.clear_encoder_loss()
    yield from sam_X.home()
    yield from bps.sleep(30)
    yield from bps.mv(sam_X,xpos)


def beamdown_notice():
    user_email = RE.md['user_email']
    send_notice(bls_email+','+user_email,'SST HAS FALLEN','Beam to RSoXS has been lost')


def beamup_notice():
    user_email = RE.md['user_email']
    send_notice(bls_email+','+user_email,'SST HAS RISEN','Nevermind all good here')



suspend_shutter = SuspendBoolHigh(psh1.state,sleep = 10,
                                  tripped_message="Beam Shutter Closed, waiting for it to open",
                                  pre_plan=beamdown_notice, post_plan=beamup_notice)
suspend_current = SuspendFloor(ring_current, resume_thresh=350, suspend_thresh=250,sleep = 10,
                               tripped_message="Beam Current is below threshold, will resume when above 350 eV",
                               pre_plan=beamdown_notice, post_plan=beamup_notice)
RE.install_suspender(suspend_shutter)
RE.install_suspender(suspend_current)
suspendx = SuspendBoolHigh(sam_X.enc_lss,sleep = 10, tripped_message="Sample X Encoder Loss has been tripped",
                           pre_plan=enc_clr_x)
RE.install_suspender(suspendx)



class OSEmailHandler(logging.Handler):
    def emit(self, record):
        user_email = RE.md['user_email']
        send_notice(bls_email+','+user_email, 'SST IS SO SORRY', record.getMessage())
       # Send email or whatever.

logger = logging.getLogger('bluesky.RE')
handler = OSEmailHandler()
handler.setLevel('ERROR')  # Only email for if the level is ERROR or higher (CRITICAL).
logger.addHandler(handler)


