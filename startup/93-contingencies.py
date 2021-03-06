import bluesky.plan_stubs as bps
from bluesky.suspenders import SuspendBoolHigh, SuspendFloor, SuspendBoolLow
import logging
import datetime

run_report(__file__)

bls_email = 'egann@bnl.gov'
global no_notifications_until


def pause_notices(until=None, **kwargs):
    # pause_notices turns off emails on errors either until a specified time or for a specified duration.
    #
    # for set end time, use until = string (compatible with strptime() in datetime)
    #
    # for duration, use parameters for the datetime.timedelta kwargs: hours= minutes= seconds= days=
    #

    global no_notifications_until
    if (until is None and len(kwargs) is 0):
        print("You need to specify either a duration or a timeout.")
    elif (until is None):
        no_notifications_until = datetime.datetime.now() + datetime.timedelta(**kwargs)
    elif (until is not None):
        no_notifications_until = datetime.datetime.strptime(until)


def resume_notices():
    global no_notifications_until

    no_notifications_until = None


def send_notice(email, subject, msg):
    # os.system('echo '+msg+' | mail -s "'+subject+'" '+email)
    try:
        rsoxs_bot.send_message(subject + '\n' + msg)
    except Exception:
        pass


def send_notice_plan(email, subject, msg):
    send_notice(email, subject, msg)
    yield from bps.sleep(.1)


def enc_clr_x():
    send_notice('egann@bnl.gov', 'SST had a small problem', 'the encoder loss has happened on the RSoXS beamline'
                                                            '\rEverything is probably just fine')
    xpos = sam_X.user_readback.get()
    yield from sam_X.clear_encoder_loss()
    yield from sam_X.home()
    yield from bps.sleep(30)
    yield from bps.mv(sam_X, xpos)


def beamdown_notice():
    user_email = RE.md['user_email']
    send_notice(bls_email + ',' + user_email, 'SST-1 has lost beam', 'Beam to RSoXS has been lost.'
                                                                     '\rYour scan has been paused automatically.'
                                                                     '\rNo intervention needed, but thought you might '
                                                                     'like to know.')
    yield from bps.null()


def beamup_notice():
    user_email = RE.md['user_email']
    send_notice(bls_email + ',' + user_email, 'SST-1 beam restored', 'Beam to RSoXS has been restored.'
                                                                     '\rYour scan has resumed running.'
                                                                     '\rIf able, you may want to check the data and '
                                                                     'make sure intensity is still OK. '
                                                                     '\rOne exposure may have been affected')
    yield from bps.null()


suspend_gvll = SuspendBoolLow(gvll.state, sleep=30,
                              tripped_message="Gate valve to load lock is closed, waiting for it to open", )

suspend_shutter4 = SuspendBoolHigh(psh4.state, sleep=30,
                                   tripped_message="Shutter 4 Closed, waiting for it to open",
                                   pre_plan=beamdown_notice, post_plan=beamup_notice)

suspend_shutter1 = SuspendBoolHigh(psh1.state, sleep=30,
                                   tripped_message="Front End Shutter Closed, waiting for it to open",
                                   pre_plan=beamdown_notice, post_plan=beamup_notice)

RE.install_suspender(suspend_shutter1)
# RE.install_suspender(suspend_shutter4)
RE.install_suspender(suspend_gvll)

suspend_current = SuspendFloor(ring_current, resume_thresh=350, suspend_thresh=250, sleep=30,
                               tripped_message="Beam Current is below threshold, will resume when above 350 mA",
                               pre_plan=beamdown_notice, post_plan=beamup_notice)

RE.install_suspender(suspend_current)

suspendx = SuspendBoolHigh(sam_X.enc_lss, sleep=40,
                           tripped_message="Sample X has lost encoder position, resetting, please wait, scan will "
                                           "resume automatically.",
                           pre_plan=enc_clr_x)
RE.install_suspender(suspendx)


# if there is no scatter, pause


class OSEmailHandler(logging.Handler):
    def emit(self, record):
        user_email = RE.md['user_email']
        send_notice(bls_email + ',' + user_email, '<@U016YV35UAJ> SST has thrown an exception',
                    record.getMessage())  # record.stack_info


class MakeSafeHandler(logging.Handler):
    def emit(self, record):
        print('close the shutter here')
        # @TODO insert code to make instrument 'safe', e.g. close shutter


logger = logging.getLogger('bluesky')
mail_handler = OSEmailHandler()
mail_handler.setLevel('ERROR')  # Only email for if the level is ERROR or higher (CRITICAL).
logger.addHandler(mail_handler)

safe_handler = MakeSafeHandler()
safe_handler.setLevel('ERROR')  # is this correct?
logger.addHandler(safe_handler)


def turn_on_checks():
    RE.install_suspender(suspend_shutter1)
    # RE.install_suspender(suspend_shutter4)
    RE.install_suspender(suspend_gvll)
    RE.install_suspender(suspend_current)
    RE.install_suspender(suspendx)
    logger.addHandler(safe_handler)
    logger.addHandler(mail_handler)


def turn_off_checks():
    RE.remove_suspender(suspend_shutter1)
    # RE.remove_suspender(suspend_shutter4)
    RE.remove_suspender(suspend_gvll)
    RE.remove_suspender(suspend_current)
    RE.remove_suspender(suspendx)
    logger.removeHandler(safe_handler)
    logger.removeHandler(mail_handler)
