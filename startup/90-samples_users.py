
from IPython.core.magic import register_line_magic
from operator import itemgetter
import collections



def user():
    title = ("User metadata - stored in every scan:")
    text=''
    if len(RE.md["proposal_id"]) > 0 :
        text += '   proposal ID:         '+colored('{}'.format(RE.md["proposal_id"]).center(40,' '),'yellow')
    if len(RE.md["user_name"]) > 0 :
        text += '\n   User Name:           '+colored('{}'.format(RE.md["user_name"]).center(40,' '),'yellow')
    if len(RE.md["user_start_date"]) > 0 :
        text += '\n   User Start Date:     '+colored('{}'.format(RE.md["user_start_date"]).center(40,' '),'yellow')
    if len(RE.md["user_id"]) > 0 :
        text += '\n   User ID:             '+colored('{}'.format(RE.md["user_id"]).center(40,' '),'yellow')
    if len(RE.md["institution"]) > 0 :
        text += '\n   Institution:         '+colored('{}'.format(RE.md["institution"]).center(40,' '),'yellow')
    if len(RE.md["project_name"]) > 0 :
        text += '\n   project:             '+colored('{}'.format(RE.md["project_name"]).center(40,' '),'yellow')
    if len(RE.md["project_desc"]) > 0 :
        text += '\n   Project Description: '+colored('{}'.format(RE.md["project_desc"]).center(40,' '),'yellow')
    boxed_text(title, text, 'green',80,shrink=True)


def sample():
    title = "Sample metadata - stored in every scan:"
    text = ''
    if len(RE.md["proposal_id"]) > 0 :
        text += '   proposal ID:           '+colored('{}'.format(RE.md["proposal_id"]).center(38,' '),'cyan')
    if len(RE.md["user_name"]) > 0 :
        text += '\n   User Name:             '+colored('{}'.format(RE.md["user_name"]).center(38,' '),'cyan')
    if len(RE.md["institution"]) > 0 :
        text += '\n   Institution:           '+colored('{}'.format(RE.md["institution"]).center(38,' '),'cyan')
    if len(RE.md["sample_name"]) > 0 :
        text += '\n   Sample Name:           '+colored('{}'.format(RE.md["sample_name"]).center(38,' '),'cyan')
    if len(RE.md["sample_desc"]) > 0 :
        text += '\n   Sample Description:    '+colored('{}'.format(RE.md["sample_desc"]).center(38,' '),'cyan')
    if len(RE.md["sample_id"]) > 0 :
        text += '\n   Sample ID:             '+colored('{}'.format(RE.md["sample_id"]).center(38,' '),'cyan')
    if len(RE.md["sample_set"]) > 0 :
        text += '\n   Sample Set:            '+colored('{}'.format(RE.md["sample_set"]).center(38,' '),'cyan')
    if len(RE.md["sample_date"]) > 0 :
        text += '\n   Sample Creation Date:  '+colored('{}'.format(RE.md["sample_date"]).center(38,' '),'cyan')
    if len(RE.md["project_name"]) > 0 :
        text += '\n   Project name:          '+colored('{}'.format(RE.md["project_name"]).center(38,' '),'cyan')
    if len(RE.md["project_desc"]) > 0 :
        text += '\n   Project Description:   '+colored('{}'.format(RE.md["project_desc"]).center(38,' '),'cyan')
    if len(RE.md["samp_user_id"]) > 0 :
        text += '\n   Creator User ID:       '+colored('{}'.format(RE.md["samp_user_id"]).center(38,' '),'cyan')
    if len(RE.md["composition"]) > 0 :
        text += '\n   Composition(formula):  '+colored('{}'.format(RE.md["composition"]).center(38,' '),'cyan')
    if len(RE.md["density"]) > 0 :
        text += '\n   Density:               '+colored('{}'.format(RE.md["density"]).center(38,' '),'cyan')
    if len(RE.md["components"]) > 0 :
        text += '\n   List of Components:    '+colored('{}'.format(RE.md["components"]).center(38,' '),'cyan')
    if len(RE.md["thickness"]) > 0 :
        text += '\n   Thickness:             '+colored('{}'.format(RE.md["thickness"]).center(38,' '),'cyan')
    if len(RE.md["sample_state"]) > 0 :
        text += '\n   Sample state:          '+colored('{}'.format(RE.md["sample_state"]).center(38,' '),'cyan')
    if len(RE.md["notes"]) > 0 :
        text += '\n   Notes:                 '+colored('{}'.format(RE.md["notes"]).center(38,' '),'cyan')
    boxed_text(title, text, 'red',80,shrink=True)


@register_line_magic
def md(line):
    sample()


@register_line_magic
def u(line):
    user()

del md, u



@register_line_magic
def status(line):
    beamline_status()
del status


def newuser():
    print("This information will tag future data until this changes, please be as thorough as possible\n"
          "current values in parentheses, leave blank for no change")

    proposal_id = input('Your proposal id ({}): '.format(RE.md['proposal_id']))
    if proposal_id is not '':
        RE.md['proposal_id'] = proposal_id

    institution = input('Your institution ({}): '.format(RE.md['institution']))
    if institution is not '':
        RE.md['institution'] = institution

    user_name = input('Your name ({}): '.format(RE.md['user_name']))
    if user_name is not '':
        RE.md['user_name'] = user_name

    project_name = input('Your project ({}): '.format(RE.md['project_name']))
    if project_name is not '':
        RE.md['project_name'] = project_name

    project_desc = input('Your project description ({}): '.format(RE.md['project_desc']))
    if project_desc is not '':
        RE.md['project_desc'] = project_desc
    # if new, add user to database get unique ID.

    dt = datetime.now()
    user_start_date = dt.strftime('%Y-%m-%d')
    RE.md['user_start_date'] = user_start_date
    user_id = '0'
    RE.md['user_id'] = user_id
    user()
    return user_dict()



def add_acq(sample_dict,plan_name='full_carbon_scan',arguments=''):
    sample_dict['acquisitions'].append({'plan_name':plan_name,'arguments':arguments})
    return sample_dict


def get_location(sample_dict,motorlist):
    locs = []
    for motor in motorlist:
        locs.append({'motor' : motor,
                     'position': motor.user_readback.value,
                     'order':0})


def sample_set_location(sample_dict):
    sample_dict['location'] = get_sample_location()
    return sample_set_location


def get_sample_location():
    locs = []
    locs.append({'motor': sam_X, 'position': sam_X.user_readback.value, 'order': 0})
    locs.append({'motor': sam_Y, 'position': sam_Y.user_readback.value, 'order': 0})
    locs.append({'motor': sam_Z, 'position': sam_Z.user_readback.value, 'order': 0})
    locs.append({'motor': sam_Th, 'position': sam_Th.user_readback.value, 'order': 0})
    return locs

def move_to_location(locs=get_sample_location()):
    locs = sorted(locs, key=itemgetter('order'))
    orderlist = [o for o in collections.Counter([d['order'] for d in locs]).keys()]
    for order in orderlist:
        outputlist = [[items['motor'], float(items['position'])] for items in locs if items['order'] == order]
        flat_list = [item for sublist in outputlist for item in sublist]
        yield from bps.mv(*flat_list)


def get_location_from_config(config):
    return eval(config+'()')


def do_acquisitions(acq_list):
    for acq in acq_list:
        yield from move_to_location(get_configuration_location(acq['configuration']))
        yield from eval(acq['plan_name']+'('+acq['arguments']+')')


def sample_dict(acq = [],locations = get_sample_location(),sample_name = RE.md['sample_name'],
                sample_desc = RE.md['sample_desc'],
                sample_id = RE.md['sample_id'],
                sample_set = RE.md['sample_set'],
                sample_date = RE.md['sample_date'],
                project_name = RE.md['project_name'],
                project_desc = RE.md['project_desc'],
                samp_user_id = RE.md['samp_user_id'],
                composition = RE.md['composition'],
                density = RE.md['density'],
                components = RE.md['components'],
                thickness = RE.md['thickness'],
                sample_state = RE.md['sample_state'],
                notes = RE.md['notes'],
                ):
    return {'sample_name': sample_name,
            'sample_desc': sample_desc,
            'sample_id': sample_id,
            'sample_set': sample_set,
            'sample_date': sample_date,
            'project_name': project_name,
            'project_desc': project_desc,
            'samp_user_id': samp_user_id,
            'composition': composition,
            'density': density,
            'components': components,
            'thickness': thickness,
            'sample_state': sample_state,
            'notes': notes,
            'location': locations,
            'acquisitions': acq}


def user_dict(user_id = RE.md['user_id'],
                proposal_id = RE.md['proposal_id'],
                institution = RE.md['institution'],
                user_name = RE.md['user_name'],
                user_start_date = RE.md['user_start_date'],
                project_name = RE.md['project_name'],
                project_desc = RE.md['project_desc'],
                ):
    return {'user_id': user_id,
            'proposal_id': proposal_id,
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
    RE.md['sample_name'] = sam_dict['sample_name']
    RE.md['sample_desc'] = sam_dict['sample_desc']
    RE.md['sample_id'] = sam_dict['sample_id']
    RE.md['sample_set'] = sam_dict['sample_set']
    RE.md['sample_date'] = sam_dict['sample_date']
    RE.md['project_name'] = sam_dict['project_name']
    RE.md['project_desc'] = sam_dict['project_desc']
    RE.md['samp_user_id'] = sam_dict['samp_user_id']
    RE.md['composition'] = sam_dict['composition']
    RE.md['density'] = sam_dict['density']
    RE.md['components'] = sam_dict['components']
    RE.md['thickness'] = sam_dict['thickness']
    RE.md['sample_state'] = sam_dict['sample_state']
    RE.md['notes'] = sam_dict['notes']
    yield from move_to_location(locs=sam_dict['location'])
    sample()

def run_sample(sam_dict):
    yield from load_sample(sam_dict)
    yield from do_acquisitions(sam_dict['acquisitions'])


def load_user_dict_to_md(user_dict):
    RE.md['user_id'] = user_dict['user_id']
    RE.md['proposal_id'] = user_dict['proposal_id']
    RE.md['institution'] = user_dict['institution']
    RE.md['user_name'] = user_dict['user_name']
    RE.md['project_name'] = user_dict['project_name']
    RE.md['project_desc'] = user_dict['project_desc']


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

    sample_desc = input('Describe your sample - be thorough ({}): '.format(RE.md['sample_desc']))
    if sample_desc is not '':
        RE.md['sample_desc'] = sample_desc

    sample_id = input('Your sample id - if you have one ({}): '.format(RE.md['sample_id']))
    if sample_id is not '':
        RE.md['sample_id'] = sample_id

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

    acquisitions = []
    add_default_acq = input('add acquisition (full_carbon_scan - WAXS)? : ')
    if add_default_acq is '':
        acquisitions.append({'plan_name': 'full_carbon_scan','arguments': '','configuration':'WAXS'})

    loc = input('New Location? (if blank use current location x={:.2f},y={:.2f},z={:.2f},th={:.2f}): '.format(
        sam_X.user_readback.value,
        sam_Y.user_readback.value,
        sam_Z.user_readback.value,
        sam_Th.user_readback.value
    ))
    if loc is not '':
        locs = []
        xval = input('X ({:.2f}): '.format(sam_X.user_readback.value))
        if xval is not '':
            locs.append({'motor': sam_X, 'position': xval, 'order': 0})
        else:
            locs.append({'motor': sam_X, 'position': sam_X.user_readback.value, 'order': 0})
        yval = input('X ({:.2f}): '.format(sam_Y.user_readback.value))
        if yval is not '':
            locs.append({'motor': sam_Y, 'position': yval, 'order': 0})
        else:
            locs.append({'motor': sam_Y, 'position': sam_Y.user_readback.value, 'order': 0})

        zval = input('X ({:.2f}): '.format(sam_Z.user_readback.value))
        if zval is not '':
            locs.append({'motor': sam_Z, 'position': zval, 'order': 0})
        else:
            locs.append({'motor': sam_Z, 'position': sam_Z.user_readback.value, 'order': 0})

        thval = input('X ({:.2f}): '.format(sam_Th.user_readback.value))
        if thval is not '':
            locs.append({'motor': sam_Th, 'position': thval, 'order': 0})
        else:
            locs.append({'motor': sam_Th, 'position': sam_Th.user_readback.value, 'order': 0})
        return sample_dict(locs, acq = acquisitions)
    else:
        return sample_dict(acq = acquisitions) #uses current location by default


def run_bar(bar):
    '''
    run all sample dictionaries stored in the list bar
    :param bar: simply a list of sample dictionaries
    :return: none
    '''
    for sample in bar:
        yield from run_sample(sample)


def list_samples(bar):
    samples = [s['sample_name'] for s in bar]
    text = '  i        Sample Name'
    for index,sample in enumerate(samples):
        text += '\n  {}        {}'.format(index, sample)
        acqs = bar[index]['acquisitions']
        for acq in acqs:
            text +='\n            {}({}) in {} configuration'.format(acq['plan_name'],acq['arguments'],acq['configuration'])
    boxed_text('Samples on bar',text,'lightblue',shrink=True)
