import bluesky.plan_stubs as bps
from bluesky.suspenders import SuspendBoolHigh
import logging

run_report(__file__)


bls_email = 'egann@bnl.gov'
user_email = RE.md['user_email']

def send_notice(email,subject,msg):
    os.system(msg+' | mail -s "'+subject+'" '+email)

def enc_clr_x():
    send_notice('egann@bnl.gov','SST HAS FALLEN','the encoder loss has happened on the RSoXS beamline')
    xpos = sam_X.user_readback.value
    yield from sam_X.clear_encoder_loss()
    yield from sam_X.home()
    yield from bps.mv(sam_X,xpos)


def beamdown_notice():
    send_notice(bls_email+','+user_email,'SST HAS FALLEN','Shutter 1 has been closed on the RSoXS beamline')


def beamup_notice():
    send_notice(bls_email+','+user_email,'SST HAS RISEN','Nevermind all good here')



suspend = SuspendBoolHigh(psh1.state,sleep = 10, tripped_message="Beam Shutter Closed, waiting for it to open",
                          pre_plan=beamdown_notice, post_plan=beamup_notice)
RE.install_suspender(suspend)
suspendx = SuspendBoolHigh(sam_X.enc_lss,sleep = 10, tripped_message="Sample X Encoder Loss has been tripped",
                           pre_plan=enc_clr_x)
RE.install_suspender(suspendx)



class OSEmailHandler(logging.Handler):
    def emit(self, record):
        send_notice(bls_email+','+user_email, 'SST IS SO SORRY', record)
       # Send email or whatever.

logger = logging.getLogger('bluesky.RE')
handler = OSEmailHandler()
handler.setLevel('ERROR')  # Only email for if the level is ERROR or higher (CRITICAL).
logger.addHandler(handler)
