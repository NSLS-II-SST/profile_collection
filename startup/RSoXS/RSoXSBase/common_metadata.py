from IPython.core.magic import register_line_magic
from operator import itemgetter
import collections, json
import pandas as pd
from copy import deepcopy
import numpy as np
from math import floor
import datetime
from ophyd import Device

#TODO: RE probably can't be referenced as it is here ....
from .configurations import *
from .startup import RE,db,bec,db0
from ..RSoXSObjects.slackbot import rsoxs_bot
from ..RSoXSObjects.motors import sam_X,sam_Y,sam_Th,sam_Z,Shutter_Y,Izero_Y,Det_S,Det_W,BeamStopW,BeamStopS
from ..RSoXSObjects.slits import slits1,slits2,slits3
from ..RSoXSObjects.cameras import SampleViewer_cam
from ..SSTObjects.diode import Shutter_enable,Shutter_control
from ..SSTObjects.motors import Exit_Slit
from ..RSoXSObjects.signals import Beamstop_SAXS,Beamstop_WAXS,DiodeRange
from .CommonFunctions.functions import boxed_text,colored


def user():
    title = "User metadata - stored in every scan:"
    text = ""
    if len(RE.md["proposal_id"]) > 0:
        text += '   proposal ID:           ' + colored('{}'.format(str(RE.md["proposal_id"])).center(50, ' '), 'yellow')
    if len(str(RE.md["saf_id"])) > 0:
        text += '\n   saf ID:              ' + colored('{}'.format(str(RE.md["saf_id"])).center(50, ' '), 'yellow')
    if len(RE.md["user_name"]) > 0:
        text += '\n   User Name:           ' + colored('{}'.format(RE.md["user_name"]).center(50, ' '), 'yellow')
    if len(RE.md["user_email"]) > 0:
        text += '\n   User Email:          ' + colored('{}'.format(RE.md["user_name"]).center(50, ' '), 'yellow')
    if len(RE.md["user_start_date"]) > 0:
        text += '\n   User Start Date:     ' + colored('{}'.format(RE.md["user_start_date"]).center(50, ' '), 'yellow')
    if len(RE.md["user_id"]) > 0:
        text += '\n   User ID:             ' + colored('{}'.format(str(RE.md["user_id"])).center(50, ' '), 'yellow')
    if len(RE.md["institution"]) > 0:
        text += '\n   Institution:         ' + colored('{}'.format(RE.md["institution"]).center(50, ' '), 'yellow')
    if len(RE.md["project_name"]) > 0:
        text += '\n   project:             ' + colored('{}'.format(RE.md["project_name"]).center(50, ' '), 'yellow')
    if len(RE.md["project_desc"]) > 0:
        text += '\n   Project Description: ' + colored('{}'.format(RE.md["project_desc"]).center(50, ' '), 'yellow')
    boxed_text(title, text, 'green', 80, shrink=False)


def sample():
    title = "Sample metadata - stored in every scan:"
    text = ''
    if len(str(RE.md["proposal_id"])) > 0:
        text += '   proposal ID:           ' + colored('{}'.format(RE.md["proposal_id"]).center(48, ' '), 'cyan')
    if len(str(RE.md["saf_id"])) > 0:
        text += '\n   SAF id:                ' + colored('{}'.format(RE.md["saf_id"]).center(48, ' '), 'cyan')
    if len(str(RE.md["user_name"])) > 0:
        text += '\n   User Name:             ' + colored('{}'.format(RE.md["user_name"]).center(48, ' '), 'cyan')
    if len(str(RE.md["institution"])) > 0:
        text += '\n   Institution:           ' + colored('{}'.format(RE.md["institution"]).center(48, ' '), 'cyan')
    if len(str(RE.md["sample_name"])) > 0:
        text += '\n   Sample Name:           ' + colored('{}'.format(RE.md["sample_name"]).center(48, ' '), 'cyan')
    if len(str(RE.md["sample_priority"])) > 0:
        text += '\n   Sample Priority:       ' + colored('{}'.format(RE.md["sample_priority"]).center(48, ' '), 'cyan')
    if len(str(RE.md["sample_desc"])) > 0:
        text += '\n   Sample Description:    ' + colored('{}'.format(RE.md["sample_desc"]).center(48, ' '), 'cyan')
    if len(str(RE.md["sample_id"])) > 0:
        text += '\n   Sample ID:             ' + colored('{}'.format(str(RE.md["sample_id"])).center(48, ' '), 'cyan')
    if len(str(RE.md["sample_set"])) > 0:
        text += '\n   Sample Set:            ' + colored('{}'.format(RE.md["sample_set"]).center(48, ' '), 'cyan')
    if len(str(RE.md["sample_date"])) > 0:
        text += '\n   Sample Creation Date:  ' + colored('{}'.format(RE.md["sample_date"]).center(48, ' '), 'cyan')
    if len(str(RE.md["project_name"])) > 0:
        text += '\n   Project name:          ' + colored('{}'.format(RE.md["project_name"]).center(48, ' '), 'cyan')
    if len(str(RE.md["project_desc"])) > 0:
        text += '\n   Project Description:   ' + colored('{}'.format(RE.md["project_desc"]).center(48, ' '), 'cyan')
    if len(str(RE.md["samp_user_id"])) > 0:
        text += '\n   Creator User ID:       ' + colored('{}'.format(str(RE.md["samp_user_id"])).center(48, ' '),
                                                         'cyan')
    if len(str(RE.md["bar_loc"]['spot'])) > 0:
        text += '\n   Location on Bar:       ' + colored('{}'.format(RE.md["bar_loc"]['spot']).center(48, ' '), 'cyan')
    if len(str(RE.md["bar_loc"]['th'])) > 0:
        text += '\n   Angle of incidence:    ' + colored('{}'.format(RE.md["bar_loc"]['th']).center(48, ' '), 'cyan')
    if len(str(RE.md["composition"])) > 0:
        text += '\n   Composition(formula):  ' + colored('{}'.format(RE.md["composition"]).center(48, ' '), 'cyan')
    if len(str(RE.md["density"])) > 0:
        text += '\n   Density:               ' + colored('{}'.format(str(RE.md["density"])).center(48, ' '), 'cyan')
    if len(str(RE.md["components"])) > 0:
        text += '\n   List of Components:    ' + colored('{}'.format(RE.md["components"]).center(48, ' '), 'cyan')
    if len(str(RE.md["thickness"])) > 0:
        text += '\n   Thickness:             ' + colored('{}'.format(str(RE.md["thickness"])).center(48, ' '), 'cyan')
    if len(str(RE.md["sample_state"])) > 0:
        text += '\n   Sample state:          ' + colored('{}'.format(RE.md["sample_state"]).center(48, ' '), 'cyan')
    if len(str(RE.md["notes"])) > 0:
        text += '\n   Notes:                 ' + colored('{}'.format(RE.md["notes"]).center(48, ' '), 'cyan')
    boxed_text(title, text, 'red', 80, shrink=False)


def newuser():
    print("This information will tag future data until this changes, please be as thorough as possible\n"
          "current values in parentheses, leave blank for no change")

    proposal_id = input('Your proposal id ({}): '.format(RE.md['proposal_id']))
    if proposal_id is not '':
        RE.md['proposal_id'] = proposal_id

    SAF_id = input('Your SAF id ({}): '.format(RE.md['saf_id']))
    if SAF_id is not '':
        RE.md['saf_id'] = SAF_id

    institution = input('Your institution ({}): '.format(RE.md['institution']))
    if institution is not '':
        RE.md['institution'] = institution

    user_name = input('Your name ({}): '.format(RE.md['user_name']))
    if user_name is not '':
        RE.md['user_name'] = user_name

    user_email = input('Your email for beamline status notifications ({}): '.format(RE.md['user_email']))
    if user_email is not '':
        RE.md['user_email'] = user_email

    project_name = input('Your project ({}): '.format(RE.md['project_name']))
    if project_name is not '':
        RE.md['project_name'] = project_name

    project_desc = input('Your project description ({}): '.format(RE.md['project_desc']))
    if project_desc is not '':
        RE.md['project_desc'] = project_desc
    # if new, add user to database get unique ID.

    dt = datetime.datetime.now()
    user_start_date = dt.strftime('%Y-%m-%d')
    RE.md['user_start_date'] = user_start_date
    user_id = '0'
    RE.md['user_id'] = user_id
    user()
    return user_dict()


def add_acq(sample_dict, plan_name='full_carbon_scan', arguments='', config='WAXS', priority=50):
    sample_dict['acquisitions'].append({'plan_name': plan_name,
                                        'arguments': arguments,
                                        'configuration': config,
                                        'priority': priority})
    return sample_dict


def get_location(motor_list):
    locs = []
    for motor in motor_list:
        locs.append({'motor': motor,
                     'position': motor.user_readback.get(),
                     'order': 0})
    return locs


def sample_set_location(sample_dict):
    sample_dict['location'] = get_sample_location()  # set the location metadata
    sample_recenter_sample(sample_dict)  # change the x0, y0, theta to result in this new position (including angle)
    return sample_dict


def get_sample_location():
    locs = []
    locs.append({'motor': 'x', 'position': sam_X.user_readback.get(), 'order': 0})
    locs.append({'motor': 'y', 'position': sam_Y.user_readback.get(), 'order': 0})
    locs.append({'motor': 'z', 'position': sam_Z.user_readback.get(), 'order': 0})
    locs.append({'motor': 'th', 'position': sam_Th.user_readback.get(), 'order': 0})
    #  locs = get_location([sam_X,sam_Y,sam_Z,sam_Th])
    return locs


def move_to_location(locs=get_sample_location()):
    for item in locs:
        item.setdefault('order', 0)
    locs = sorted(locs, key=itemgetter('order'))
    orderlist = [o for o in collections.Counter([d['order'] for d in locs]).keys()]

    switch = {'x': sam_X,
              'y': sam_Y,
              'z': sam_Z,
              'th': sam_Th,
              sam_X: sam_X,
              sam_Y: sam_Y,
              sam_Z: sam_Z,
              sam_Th: sam_Th,
              slits1.vsize: slits1.vsize,
              slits1.hsize: slits1.hsize,
              slits2.vsize: slits2.vsize,
              slits2.hsize: slits2.hsize,
              slits3.vsize: slits3.vsize,
              slits3.hsize: slits3.hsize,
              slits1.vcenter: slits1.vcenter,
              slits1.hcenter: slits1.hcenter,
              slits2.vcenter: slits2.vcenter,
              slits2.hcenter: slits2.hcenter,
              slits3.vcenter: slits3.vcenter,
              slits3.hcenter: slits3.hcenter,
              Shutter_Y: Shutter_Y,
              Izero_Y: Izero_Y,
              Det_W: Det_W,
              Det_S: Det_S,
              BeamStopS: BeamStopS,
              BeamStopW: BeamStopW,
              Exit_Slit: Exit_Slit}
    for order in orderlist:
        outputlist = [[switch[items['motor']], float(items['position'])] for items in locs if items['order'] == order]
        flat_list = [item for sublist in outputlist for item in sublist]
        yield from bps.mv(*flat_list)


def get_location_from_config(config):
    return eval(config + '()[0]')


def get_md_from_config(config):
    return eval(config + '()[1]')


def load_configuration(config):
    '''

    :param config: string containing a name of a configuration
    :return:
    '''
    yield from move_to_location(get_location_from_config(config))
    RE.md.update(get_md_from_config(config))


def do_acquisitions(acq_list):
    uid=none
    for acq in acq_list:
        yield from load_configuration(acq['configuration'])
        uid = yield from eval(acq['plan_name'] + '(' + acq['arguments'] + ')')
    return uid

def get_sample_dict(acq=[], locations=None):
    if locations is None:
        locations = get_sample_location()
    sample_name = RE.md['sample_name']
    sample_priority = RE.md['sample_priority']
    sample_desc = RE.md['sample_desc']
    sample_id = RE.md['sample_id']
    sample_set = RE.md['sample_set']
    sample_date = RE.md['sample_date']
    project_name = RE.md['project_name']
    proposal_id = RE.md['proposal_id']
    saf_id = RE.md['saf_id']
    project_desc = RE.md['project_desc']
    samp_user_id = RE.md['samp_user_id']
    composition = RE.md['composition']
    bar_loc = RE.md['bar_loc']
    density = RE.md['density']
    grazing = RE.md['grazing']
    bar_spot = RE.md['bar_spot']
    front = RE.md['front']
    height = RE.md['height']
    angle = RE.md['angle']
    components = RE.md['components']
    thickness = RE.md['thickness']
    sample_state = RE.md['sample_state']
    notes = RE.md['notes']
    history = RE.md['acq_history']

    return {'sample_name': sample_name,
            'sample_desc': sample_desc,
            'sample_id': sample_id,
            'sample_priority': sample_priority,
            'proposal_id': proposal_id,
            'saf_id': saf_id,
            'sample_set': sample_set,
            'sample_date': sample_date,
            'project_name': project_name,
            'project_desc': project_desc,
            'samp_user_id': samp_user_id,
            'composition': composition,
            'bar_loc': bar_loc,
            'density': density,
            'grazing': grazing,
            'bar_spot': bar_spot,
            'front': front,
            'height': height,
            'angle': angle,
            'components': components,
            'thickness': thickness,
            'sample_state': sample_state,
            'notes': notes,
            'location': locations,
            'acquisitions': acq,
            'acq_history':history}


def user_dict(user_id=RE.md['user_id'],
              proposal_id=RE.md['proposal_id'],
              saf_id=RE.md['saf_id'],
              institution=RE.md['institution'],
              user_name=RE.md['user_name'],
              user_start_date=RE.md['user_start_date'],
              project_name=RE.md['project_name'],
              project_desc=RE.md['project_desc'],
              ):
    return {'user_id': user_id,
            'proposal_id': proposal_id,
            'saf_id': saf_id,
            'institution': institution,
            'user_name': user_name,
            'user_start_date': user_start_date,
            'project_name': project_name,
            'project_desc': project_desc}


def load_sample(sam_dict):
    '''
    move to a sample location and load the metadata with the sample information

    :param sam_dict: sample dictionary containing all metadata and sample location
    :return:
    '''
    RE.md.update(sam_dict)
    yield from move_to_location(locs=sam_dict['location'])
    # sample()


def run_sample(sam_dict):
    yield from load_sample(sam_dict)
    yield from do_acquisitions(sam_dict['acquisitions'])


def load_user_dict_to_md(user_dict):
    RE.md.update(user_dict)


def newsample():
    '''
    ceate a new sample dictionary interactively

    :return: a sample dictionary
    '''
    print("This information will tag future data until this changes, please be as thorough as possible\n"
          "current values in parentheses, leave blank for no change")
    sample_name = input('Your sample name  - be concise ({}): '.format(RE.md['sample_name']))
    if sample_name is not '':
        RE.md['sample_name'] = sample_name

    sample_priority = input('Your sample priority  - 0 - highest to 100-lowest ({}): '.format(RE.md['sample_priority']))
    if sample_priority is not '':
        RE.md['sample_priority'] = sample_priority

    sample_desc = input('Describe your sample - be thorough ({}): '.format(RE.md['sample_desc']))
    if sample_desc is not '':
        RE.md['sample_desc'] = sample_desc

    sample_id = input('Your sample id - if you have one ({}): '.format(RE.md['sample_id']))
    if sample_id is not '':
        RE.md['sample_id'] = sample_id

    proposal_id = input('Your Proposal ID from PASS ({}): '.format(RE.md['proposal_id']))
    if proposal_id is not '':
        RE.md['proposal_id'] = proposal_id

    saf_id = input('Your SAF ID number from PASS ({}): '.format(RE.md['saf_id']))
    if saf_id is not '':
        RE.md['saf_id'] = saf_id

    sample_set = input('What set does this sample belong to ({}): '.format(RE.md['sample_set']))
    if sample_set is not '':
        RE.md['sample_set'] = sample_set

    sample_date = input('Sample creation date ({}): '.format(RE.md['sample_date']))
    if sample_date is not '':
        RE.md['sample_date'] = sample_date

    project_name = input('Is there an associated project name ({}): '.format(RE.md['project_name']))
    if project_name is not '':
        RE.md['project_name'] = project_name

    project_desc = input('Describe the project ({}): '.format(RE.md['project_desc']))
    if project_desc is not '':
        RE.md['project_desc'] = project_desc

    samp_user_id = input('Associated User ID ({}): '.format(RE.md['samp_user_id']))
    if samp_user_id is not '':
        RE.md['samp_user_id'] = samp_user_id

    bar_loc = input('Location on the Bar ({}): '.format(RE.md['bar_loc']['spot']))
    if bar_loc is not '':
        RE.md['bar_loc']['spot'] = bar_loc
        RE.md['bar_spot'] = bar_loc

    th = input(
        'Angle desired for sample acquisition (-180 for transmission from back) ({}): '.format(RE.md['bar_loc']['th']))
    if th is not '':
        RE.md['bar_loc']['th'] = th
        RE.md['angle'] = th

    composition = input('Sample composition or chemical formula ({}): '.format(RE.md['composition']))
    if composition is not '':
        RE.md['composition'] = composition

    density = input('Sample density ({}): '.format(RE.md['density']))
    if density is not '':
        RE.md['density'] = density

    components = input('Sample components ({}): '.format(RE.md['components']))
    if components is not '':
        RE.md['components'] = components

    thickness = input('Sample thickness ({}): '.format(RE.md['thickness']))
    if thickness is not '':
        RE.md['thickness'] = thickness

    sample_state = input('Sample state "Broken/Fresh" ({}): '.format(RE.md['sample_state']))
    if sample_state is not '':
        RE.md['sample_state'] = sample_state

    notes = input('Sample notes ({}): '.format(RE.md['notes']))
    if notes is not '':
        RE.md['notes'] = notes

    grazing = input('Is the sample for grazing incidence? ({}): '.format(RE.md['grazing']))
    if grazing is not '':
        RE.md['grazing'] = eval(grazing)
    front = input('Is the sample on the front of the bar? ({}): '.format(RE.md['front']))
    if front is not '':
        RE.md['front'] = eval(front)
    height = input('Sample height? ({}): '.format(RE.md['height']))
    if height is not '':
        RE.md['height'] = eval(height)

    acquisitions = []
    add_default_acq = input('add acquisition (full_carbon_scan - WAXS)? : ')
    if add_default_acq is '':
        acquisitions.append({'plan_name': 'full_carbon_scan', 'arguments': '', 'configuration': 'WAXS'})

    loc = input('New Location? (if blank use current location x={:.2f},y={:.2f},z={:.2f},th={:.2f}): '.format(
        sam_X.user_readback.get(),
        sam_Y.user_readback.get(),
        sam_Z.user_readback.get(),
        sam_Th.user_readback.get()
    ))
    if loc is not '':
        locs = []
        xval = input('X ({:.2f}): '.format(sam_X.user_readback.get()))
        if xval is not '':
            locs.append({'motor': 'x', 'position': xval, 'order': 0})
        else:
            locs.append({'motor': 'x', 'position': sam_X.user_readback.get(), 'order': 0})
        yval = input('Y ({:.2f}): '.format(sam_Y.user_readback.get()))
        if yval is not '':
            locs.append({'motor': 'y', 'position': yval, 'order': 0})
        else:
            locs.append({'motor': 'y', 'position': sam_Y.user_readback.get(), 'order': 0})

        zval = input('Z ({:.2f}): '.format(sam_Z.user_readback.get()))
        if zval is not '':
            locs.append({'motor': 'z', 'position': zval, 'order': 0})
        else:
            locs.append({'motor': 'z', 'position': sam_Z.user_readback.get(), 'order': 0})

        thval = input('Theta ({:.2f}): '.format(sam_Th.user_readback.get()))
        if thval is not '':
            locs.append({'motor': 'th', 'position': thval, 'order': 0})
        else:
            locs.append({'motor': 'th', 'position': sam_Th.user_readback.get(), 'order': 0})
        return get_sample_dict(locations=locs, acq=acquisitions)
    else:
        return get_sample_dict(acq=acquisitions)  # uses current location by default


def avg_scan_time(plan_name, nscans=50, new_scan_duration=600):
    if plan_name is 'normal_incidence_rotate_pol_nexafs':
        multiple = 6
        plan_name = 'fly_Carbon_NEXAFS'
    elif plan_name is 'fixed_pol_rotate_sample_nexafs' or plan_name is 'fixed_sample_rotate_pol_nexafs':
        multiple = 5
        plan_name = 'fly_Carbon_NEXAFS'
    else:
        multiple = 1
    scans = db0(plan_name=plan_name)
    durations = np.array([])
    for i, sc in enumerate(scans):
        if ('exit_status' in sc.stop.keys()):
            if (sc.stop['exit_status'] == 'success'):
                durations = np.append(durations, sc.stop['time'] - sc.start['time'])
            if i > nscans:
                break
    if len(durations) > 0:
        return np.mean(durations) * multiple
    else:
        # we have never run a scan of this type before (?!?) - assume it takes some default value (10 min)
        scans = db0(master_plan=plan_name)
        durations = np.array([])
        for i, sc in enumerate(scans):
            if ('exit_status' in sc.stop.keys()):
                if (sc.stop['exit_status'] == 'success'):
                    durations = np.append(durations, sc.stop['time'] - sc.start['time'])
                if i > nscans:
                    break
        if len(durations) > 0:
            return np.mean(durations) * multiple
        else:
            return new_scan_duration


def run_bar(bar, sort_by=['sample_num'], dryrun=0, rev=[False], delete_as_complete=True,
            retract_when_done=False, save_as_complete=''):
    '''
    run all sample dictionaries stored in the list bar
    @param bar: a list of sample dictionaries
    @param sort_by: list of strings determining the sorting of scans
                    strings include project, configuration, sample_id, plan, plan_args, spriority, apriority
                    within which all of one acquisition, etc
    @param dryrun: Print out the list of plans instead of actually doing anything - safe to do during setup
    @param rev: list the same length of sort_by, or booleans, wetierh to reverse that sort
    @param delete_as_complete: remove the acquisitions from the bar as we go, so we can automatically start back up
    @param retract_when_done: go to throughstation mode at the end of all runs.
    @param save_as_complete: if a valid path, will save the running bar to this position in case of failure
    @return:
    '''

    config_change_time = 120  # time to change between configurations, in seconds.
    save_to_file = False
    try:
        open(save_as_complete, 'w')
    except OSError:
        save_to_file = False
        pass
    else:
        save_to_file = True

    list_out = []
    for samp_num, s in enumerate(bar):
        sample = s
        sample_id = s['sample_id']
        sample_project = s['project_name']
        for acq_num, a in enumerate(s['acquisitions']):
            if 'priority' not in a.keys():
                a['priority'] = 50
            list_out.append([sample_id,  # 0  X
                             sample_project,  # 1  X
                             a['configuration'],  # 2  X
                             a['plan_name'],  # 3
                             avg_scan_time(a['plan_name'], 50),  # 4 calculated plan time
                             sample,  # 5 full sample dict
                             a,  # 6 full acquisition dict
                             samp_num,  # 7 sample index
                             acq_num,  # 8 acq index
                             a['arguments'],  # 9  X
                             s['density'],  # 10
                             s['proposal_id'],  # 11 X
                             s['sample_priority'],  # 12 X
                             a['priority']])  # 13 X
    switcher = {
        'sample_id': 0,
        'project': 1,
        'config': 2,
        'plan': 3,
        'plan_args': 9,
        'proposal': 11,
        'spriority': 12,
        'apriority': 13,
        'sample_num': 7, }
    # add anything to the above list, and make a key in the above dictionary,
    # using that element to sort by something else
    try:
        sort_by.reverse()
        rev.reverse()
    except AttributeError:
        if isinstance(sort_by, str):
            sort_by = [sort_by]
            rev = [rev]
        else:
            print('sort_by needs to be a list of strings\n'
                  'such as project, configuration, sample_id, plan, plan_args, spriority, apriority')
            return
    try:
        for k, r in zip(sort_by, rev):
            list_out = sorted(list_out, key=itemgetter(switcher[k]), reverse=r)
    except KeyError:
        print('sort_by needs to be a list of strings\n'
              'such as project, configuration, sample_id, plan, plan_args, spriority, apriority')
        return
    if dryrun:
        text = ''
        total_time = 0
        for i, step in enumerate(list_out):
            text += 'load {} from {}, config {}, run {} (p {} a {}), starts @ {} takes {}\n'.format(
                step[5]['sample_name'],
                step[1],
                step[2],
                step[3],
                step[12],
                step[13],
                time_sec(total_time),
                time_sec(step[4]))
            total_time += step[4]
            if step[2] != list_out[i - 1][2]:
                total_time += config_change_time
        text += f'\n\nTotal estimated time including config changes {time_sec(total_time)}'
        boxed_text('Dry Run', text, 'lightblue', width=120, shrink=True)
    else:
        run_start_time = datetime.datetime.now()
        for i, step in enumerate(list_out):
            time_remaining = sum([avg_scan_time(row[3]) for row in list_out[i:]])
            this_step_time = avg_scan_time(step[3])
            start_time = datetime.datetime.now()
            total_time = datetime.datetime.now() - run_start_time
            boxed_text('Scan Status',
                       '\nTime so far: {}'.format(str(total_time)) +
                       '\nStarting scan {} out of {}'.format(colored(f'#{i + 1}', 'blue'), len(list_out)) +
                       '{} of {} in project {} Proposal # {}\n which should take {}\n'.format(
                           colored(step[3], 'blue'),  # plan
                           colored(step[0], 'blue'),  # sample_id
                           colored(step[1], 'blue'),  # project
                           colored(step[11], 'blue'),  # proposal
                           time_sec(this_step_time)) +
                       f'time remaining approx {time_sec(time_remaining)} \n\n',
                       'red', width=120, shrink=True)
            rsoxs_bot.send_message(f'Starting scan {i + 1} out of {len(list_out)}\n' +
                                   f'{step[3]} of {step[0]} in project {step[1]} Proposal # {step[11]}'
                                   f'\nwhich should take {time_sec(this_step_time)}' +
                                   f'\nTime so far: {str(total_time)}'
                                   f'time remaining approx {time_sec(time_remaining)}')
            yield from load_configuration(step[2])  # move to configuration
            yield from load_sample(step[5])  # move to sample / load sample metadata
            yield from do_acquisitions([step[6]])  # run acquisition (will load configuration again)
            uid = db[-1].uid
            print(f'acq uid = {uid}')
            scan_id = db[uid].start['scan_id']
            timestamp = db[uid].start['time']
            success = db[uid].stop['exit_status']
            bar[step[7]].setdefault('acq_history', []).append({'uid': uid,
                                                             'scan_id': scan_id,
                                                             'acq': step[6],
                                                             'time': timestamp,
                                                             'status': success})
            if delete_as_complete:
                bar[step[7]]['acquisitions'].remove(step[6])
            if save_to_file:
                save_samplesxls(bar, save_as_complete)
            elapsed_time = datetime.datetime.now() - start_time
            rsoxs_bot.send_message(f'Acquisition {scan_id} complete. Actual time : {str(elapsed_time)},')
        rsoxs_bot.send_message('All scans complete!')
        if retract_when_done:
            yield from all_out()


def time_sec(seconds):
    dt = datetime.timedelta(seconds=seconds)
    return str(dt).split(".")[0]


def list_samples(bar):
    text = '  i   priority  Sample Name'
    for index, sample in enumerate(bar):
        text += '\n {}  {} {}'.format(index, sample['sample_priority'], sample['sample_name'])
        acqs = bar[index]['acquisitions']
        for acq in acqs:
            text += '\n   {}({}) in {} config, priority {}'.format(acq['plan_name'], acq['arguments'],
                                                                   acq['configuration'], acq['priority'])
    boxed_text('Samples on bar', text, 'lightblue', shrink=False)


def save_samplesxls(bar, filename):
    switch = {sam_X.name: 'x',
              sam_Y.name: 'y',
              sam_Z.name: 'z',
              sam_Th.name: 'th',
              'x': 'x',
              'y': 'y',
              'z': 'z',
              'th': 'th'}
    sampledf = pd.DataFrame.from_dict(bar, orient='columns')
    sampledf.to_excel('temp.xls', index=False)

    df = pd.read_excel('temp.xls', na_values='')
    df.replace(np.nan, '', regex=True, inplace=True)
    testdict = df.to_dict(orient='records')
    for i, sam in enumerate(testdict):
        testdict[i]['location'] = eval(sam['location'])
        testdict[i]['acquisitions'] = eval(sam['acquisitions'])
        if 'acq_history' not in testdict[i].keys():
            testdict[i]['acq_history']=[]
        elif testdict[i]['acq_history'] is '':
            testdict[i]['acq_history'] = []
        else:
            testdict[i]['acq_history'] = eval(sam['acq_history'])
        testdict[i]['bar_loc'] = eval(sam['bar_loc'])
        testdict[i]['bar_loc']['spot'] = sam['bar_spot']
    acqlist = []
    for i, sam in enumerate(testdict):
        for j, loc in enumerate(sam['location']):
            if isinstance(loc['motor'], Device):
                testdict[i]['location'][j]['motor'] = switch[loc['motor'].name]
        for acq in sam['acquisitions']:
            acq.update({'sample_id': sam['sample_id']})
            acqlist.append(acq)

    sampledf = pd.DataFrame.from_dict(testdict, orient='columns')
    sampledf = sampledf.loc[:, df.columns != 'acquisitions']
    acqdf = pd.DataFrame.from_dict(acqlist, orient='columns')
    writer = pd.ExcelWriter(filename)
    sampledf.to_excel(writer, index=False, sheet_name='Samples')
    acqdf.to_excel(writer, index=False, sheet_name='Acquisitions')
    writer.close()


def sanatize_angle(samp, force=False):
    # translates a requested angle (something in sample['angle']) into an actual angle depending on the kind of sample
    if type(samp['angle']) == int or type(samp['angle']) == float:
        goodnumber = True  # make the number fall in the necessary range
    else:
        goodnumber = False  # make all transmission 90 degrees from the back, and all grading 20 deg
    if force and -95 < samp['angle'] < 185:
        samp['bar_loc']['th'] = samp['angle']
        return
    if samp['grazing']:
        if samp['front']:
            if goodnumber:
                samp['bar_loc']['th'] = np.mod(np.abs(90 - samp['angle']), 180)
            else:
                samp['bar_loc']['th'] = 70
                samp['angle'] = 70
                # front grazing sample angle is interpreted as grazing angle
        else:
            if goodnumber:
                samp['bar_loc']['th'] = 90 + np.round(np.mod(100 * samp['angle'] - 9000.01, 9000.01)) / 100
            else:
                samp['bar_loc']['th'] = 110
                samp['angle'] = 110
            # back grazing sample angle is interpreted as grazing angle but subtracted from 180
    else:
        if samp['front']:
            if goodnumber:
                samp['bar_loc']['th'] = 90 + np.round(np.mod(100 * samp['angle'] - 9000.01, 9000.01)) / 100
                if samp['bar_loc']['x0'] < -1.8 and samp['bar_loc']['th'] < 155:
                    # transmission from the left side of the bar at a incident angle more than 20 degrees,
                    # flip sample around to come from the other side - this can take a minute or two
                    samp['bar_loc']['th'] = - 90 - np.round(np.mod(100 * samp['angle'] - 9000.01, 9000.01)) / 100
            else:
                samp['bar_loc']['th'] = 180
                samp['angle'] = 180
        else:
            if goodnumber:
                samp['bar_loc']['th'] = np.mod(np.abs(90 - samp['angle']), 180)
                if samp['bar_loc']['x0'] > -1.8 and samp['bar_loc']['th'] < 160:
                    # transmission from the right side of the bar at a incident angle more than 20 degrees,
                    # flip to come from the left side
                    samp['bar_loc']['th'] = - np.mod(np.abs(90 - samp['angle']), 180)
            else:
                samp['bar_loc']['th'] = 0
                samp['angle'] = 0


def load_samplesxls(filename):
    df = pd.read_excel(filename,
                       na_values='',
                       engine='openpyxl',
                       keep_default_na=True,
                       converters={'sample_date': str},
                       sheet_name='Samples',
                       verbose=True)
    df.replace(np.nan, '', regex=True, inplace=True)
    samplenew = df.to_dict(orient='records')
    if not isinstance(samplenew, list):
        samplenew = [samplenew]
    if 'acquisitions' not in samplenew[0].keys():
        for samp in samplenew:
            samp['acquisitions'] = []
        acqsdf = pd.read_excel(filename,
                               na_values='',
                               engine='openpyxl',
                               keep_default_na=True,
                               sheet_name='Acquisitions',
                               usecols='A:E',
                               verbose=True)
        acqs = acqsdf.to_dict(orient='records')
        if not isinstance(acqs, list):
            acqs = [acqs]
        for acq in acqs:
            if np.isnan(acq['priority']):
                break
            samp = next(dict for dict in samplenew if dict['sample_id'] == acq['sample_id'])
            add_acq(samp, acq['plan_name'], acq['arguments'], acq['configuration'], acq['priority'])
    else:
        for i, sam in enumerate(samplenew):
            samplenew[i]['acquisitions'] = eval(sam['acquisitions'])
    for i, sam in enumerate(samplenew):
        samplenew[i]['location'] = eval(sam['location'])
        samplenew[i]['bar_loc'] = eval(sam['bar_loc'])
        if 'acq_history' in sam.keys():
            samplenew[i]['acq_history'] = eval(sam['acq_history'])
        else:
            samplenew[i]['acq_history'] = []
        samplenew[i]['bar_loc']['spot'] = sam['bar_spot']
        for key in [key for key, value in sam.items() if 'named' in key.lower()]:
            del samplenew[i][key]
    return samplenew


def sample_by_value_match(bar, key, string):
    results = [d for (index, d) in enumerate(bar) if d[key].find(string) >= 0]
    if len(results) == 1:
        return results[0]
    elif len(results) < 1:
        print('No Match')
        return None
    elif len(results) > 1:
        print('More than one result found, returning them all')
        return results


def sample_by_name(bar, name):
    return sample_by_value_match(bar, 'sample_name', name)


def offset_bar(bar, xoff, yoff, zoff, thoff):
    for samp in bar:
        for mot in samp['location']:
            if mot['motor'] is 'x':
                mot['position'] += xoff
            if mot['motor'] is 'y':
                mot['position'] += yoff
            if mot['motor'] is 'z':
                mot['position'] += zoff
            if mot['motor'] is 'th':
                mot['position'] += thoff
        sample_recenter_sample(samp)