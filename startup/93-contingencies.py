import bluesky.plan_stubs as bps
from bluesky.suspenders import SuspendBoolHigh, SuspendFloor
import logging
import datetime

run_report(__file__)


bls_email = 'egann@bnl.gov'

def pause_notices(until=None,**kwargs):
    ##pause_notices turns off emails on errors either until a specified time or for a specified duration.
    #
    #for set end time, use until = string (compatible with strptime() in datetime)
    #
    #for duration, use parametrs for the datetime.timedelta kwargs: hours= minutes= seconds= days=
    #

    global no_notifications_until
    if(until is None and len(kwargs) is 0):
      print("You need to specify either a duration or a timeout.")
    elif(until is None):
      no_notifications_until = datetime.datetime.now() + datetime.timedelta(**kwargs)
    elif(until is not None):
      no_notifications_until = datetime.datetime.strptime(until)

def resume_notices():
    global no_notifications_until

    no_notifications_until = None

def send_notice(email,subject,msg):
    os.system('echo '+msg+' | mail -s "'+subject+'" '+email)


def send_notice_plan(email,subject,msg):
    send_notice(email,subject,msg)
    yield from bps.sleep(.1)

def enc_clr_x():
    send_notice('egann@bnl.gov','SST HAS FALLEN','the encoder loss has happened on the RSoXS beamline')
    xpos = sam_X.user_readback.value
    yield from sam_X.clear_encoder_loss()
    yield from sam_X.home()
    yield from bps.sleep(30)
    yield from bps.mv(sam_X,xpos)


def beamdown_notice():
    user_email = RE.md['user_email']
    send_notice(bls_email+','+user_email,'SST has lost beam','Beam to RSoXS has been lost.\n\n Your scan has been paused automatically.\n\nNo intervention needed, but thought you might like to know.')


def beamup_notice():
    user_email = RE.md['user_email']
    send_notice(bls_email+','+user_email,'SST beam restored','Beam to RSoXS has been restored.\n\nYour scan has resumed running.\n\nIf able, you may want to check the data and make sure intensity is still OK.')



suspend_shutter = SuspendBoolHigh(psh1.state,sleep = 10,
                                  tripped_message="Beam Shutter Closed, waiting for it to open",
                                  pre_plan=beamdown_notice, post_plan=beamup_notice)
suspend_current = SuspendFloor(ring_current, resume_thresh=350, suspend_thresh=250,sleep = 10,
                               tripped_message="Beam Current is below threshold, will resume when above 350 mA",
                               pre_plan=beamdown_notice, post_plan=beamup_notice)
RE.install_suspender(suspend_shutter)
RE.install_suspender(suspend_current)
suspendx = SuspendBoolHigh(sam_X.enc_lss,sleep = 40, tripped_message="Sample X has lost encoder position, resetting, please wait, scan will resume automatically.",
                           pre_plan=enc_clr_x)
RE.install_suspender(suspendx)



class OSEmailHandler(logging.Handler):
    def emit(self, record):
        global no_notifications_until
        user_email = RE.md['user_email']

        if((no_notifications_until is None) or (datetime.datetime.now() > no_notifications_until)):
            send_notice(bls_email+','+user_email, 'SST has thrown an exception', record.getMessage()) # record.stack_info
       # Send email or whatever.

logger = logging.getLogger('bluesky.RE')
handler = OSEmailHandler()
handler.setLevel('ERROR')  # Only email for if the level is ERROR or higher (CRITICAL).
logger.addHandler(handler)


