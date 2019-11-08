
from IPython.core.magic import register_line_magic
from operator import itemgetter
import collections, json
import pandas as pd
from copy import deepcopy
import numpy as np
from math import floor
import datetime

def user():
    title = "User metadata - stored in every scan:"
    text = ""
    if len(RE.md["proposal_id"]) > 0 :
        text += '   proposal ID:         '+colored('{}'.format(str(RE.md["proposal_id"])).center(40,' '),'yellow')
    if len(RE.md["user_name"]) > 0 :
        text += '\n   User Name:           '+colored('{}'.format(RE.md["user_name"]).center(40,' '),'yellow')
    if len(RE.md["user_email"]) > 0 :
        text += '\n   User Email:           '+colored('{}'.format(RE.md["user_name"]).center(40,' '),'yellow')
    if len(RE.md["user_start_date"]) > 0 :
        text += '\n   User Start Date:     '+colored('{}'.format(RE.md["user_start_date"]).center(40,' '),'yellow')
    if len(RE.md["user_id"]) > 0 :
        text += '\n   User ID:             '+colored('{}'.format(str(RE.md["user_id"])).center(40,' '),'yellow')
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
    if len(str(RE.md["proposal_id"])) > 0 :
        text += '   proposal ID:           '+colored('{}'.format(str(RE.md["proposal_id"])).center(38,' '),'cyan')
    if len(str(RE.md["user_name"])) > 0 :
        text += '\n   User Name:             '+colored('{}'.format(RE.md["user_name"]).center(38,' '),'cyan')
    if len(str(RE.md["institution"])) > 0 :
        text += '\n   Institution:           '+colored('{}'.format(RE.md["institution"]).center(38,' '),'cyan')
    if len(str(RE.md["sample_name"])) > 0 :
        text += '\n   Sample Name:           '+colored('{}'.format(RE.md["sample_name"]).center(38,' '),'cyan')
    if len(str(RE.md["sample_desc"])) > 0 :
        text += '\n   Sample Description:    '+colored('{}'.format(RE.md["sample_desc"]).center(38,' '),'cyan')
    if len(str(RE.md["sample_id"])) > 0 :
        text += '\n   Sample ID:             '+colored('{}'.format(str(RE.md["sample_id"])).center(38,' '),'cyan')
    if len(str(RE.md["sample_set"])) > 0 :
        text += '\n   Sample Set:            '+colored('{}'.format(RE.md["sample_set"]).center(38,' '),'cyan')
    if len(str(RE.md["sample_date"])) > 0 :
        text += '\n   Sample Creation Date:  '+colored('{}'.format(RE.md["sample_date"]).center(38,' '),'cyan')
    if len(str(RE.md["project_name"])) > 0 :
        text += '\n   Project name:          '+colored('{}'.format(RE.md["project_name"]).center(38,' '),'cyan')
    if len(str(RE.md["project_desc"])) > 0 :
        text += '\n   Project Description:   '+colored('{}'.format(RE.md["project_desc"]).center(38,' '),'cyan')
    if len(str(RE.md["samp_user_id"])) > 0 :
        text += '\n   Creator User ID:       '+colored('{}'.format(str(RE.md["samp_user_id"])).center(38,' '),'cyan')
    if len(str(RE.md["composition"])) > 0 :
        text += '\n   Composition(formula):  '+colored('{}'.format(RE.md["composition"]).center(38,' '),'cyan')
    if len(str(RE.md["density"])) > 0 :
        text += '\n   Density:               '+colored('{}'.format(str(RE.md["density"])).center(38,' '),'cyan')
    if len(str(RE.md["components"])) > 0 :
        text += '\n   List of Components:    '+colored('{}'.format(RE.md["components"]).center(38,' '),'cyan')
    if len(str(RE.md["thickness"])) > 0 :
        text += '\n   Thickness:             '+colored('{}'.format(str(RE.md["thickness"])).center(38,' '),'cyan')
    if len(str(RE.md["sample_state"])) > 0 :
        text += '\n   Sample state:          '+colored('{}'.format(RE.md["sample_state"]).center(38,' '),'cyan')
    if len(str(RE.md["notes"])) > 0 :
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

    proposal_id = input('Your SAF id ({}): '.format(RE.md['proposal_id']))
    if proposal_id is not '':
        RE.md['SAF_id'] = proposal_id

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


def add_acq(sample_dict,plan_name='full_carbon_scan',arguments='',config='WAXS'):
    sample_dict['acquisitions'].append({'plan_name': plan_name,
                                        'arguments': arguments,
                                        'configuration': config})
    return sample_dict


def get_location(motor_list):
    locs = []
    for motor in motor_list:
        locs.append({'motor' : motor,
                     'position': motor.user_readback.value,
                     'order':0})
    return locs


def sample_set_location(sample_dict):
    sample_dict['location'] = get_sample_location()
    return sample_dict


def get_sample_location():
    locs = []
    locs.append({'motor': 'x', 'position': sam_X.user_readback.value, 'order': 0})
    locs.append({'motor': 'y', 'position': sam_Y.user_readback.value, 'order': 0})
    locs.append({'motor': 'z', 'position': sam_Z.user_readback.value, 'order': 0})
    locs.append({'motor': 'th', 'position': sam_Th.user_readback.value, 'order': 0})
    #  locs = get_location([sam_X,sam_Y,sam_Z,sam_Th])
    return locs

def move_to_location(locs=get_sample_location()):
    for item in locs:
        item.setdefault('order',0)
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
              BeamStopW: BeamStopW}
    for order in orderlist:
        outputlist = [[switch[items['motor']], float(items['position'])] for items in locs if items['order'] == order]
        flat_list = [item for sublist in outputlist for item in sublist]
        yield from bps.mv(*flat_list)


def get_location_from_config(config):
    return eval(config+'()')


def do_acquisitions(acq_list):
    for acq in acq_list:
        yield from move_to_location(get_location_from_config(acq['configuration']))
        yield from eval(acq['plan_name']+'('+acq['arguments']+')')


def get_sample_dict(acq = [],locations = []):
    if locations is []:
        locations = get_sample_location()
    sample_name = RE.md['sample_name']
    sample_desc = RE.md['sample_desc']
    sample_id = RE.md['sample_id']
    sample_set = RE.md['sample_set']
    sample_date = RE.md['sample_date']
    project_name = RE.md['project_name']
    project_desc = RE.md['project_desc']
    samp_user_id = RE.md['samp_user_id']
    composition = RE.md['composition']
    density = RE.md['density']
    components = RE.md['components']
    thickness = RE.md['thickness']
    sample_state = RE.md['sample_state']
    notes = RE.md['notes']

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
    # sample()


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
            locs.append({'motor': 'x', 'position': xval, 'order': 0})
        else:
            locs.append({'motor': 'x', 'position': sam_X.user_readback.value, 'order': 0})
        yval = input('X ({:.2f}): '.format(sam_Y.user_readback.value))
        if yval is not '':
            locs.append({'motor': 'y', 'position': yval, 'order': 0})
        else:
            locs.append({'motor': 'y', 'position': sam_Y.user_readback.value, 'order': 0})

        zval = input('X ({:.2f}): '.format(sam_Z.user_readback.value))
        if zval is not '':
            locs.append({'motor': 'z', 'position': zval, 'order': 0})
        else:
            locs.append({'motor': 'z', 'position': sam_Z.user_readback.value, 'order': 0})

        thval = input('X ({:.2f}): '.format(sam_Th.user_readback.value))
        if thval is not '':
            locs.append({'motor': 'th', 'position': thval, 'order': 0})
        else:
            locs.append({'motor': 'th', 'position': sam_Th.user_readback.value, 'order': 0})
        return get_sample_dict(locations = locs, acq = acquisitions)
    else:
        return get_sample_dict(acq = acquisitions) #uses current location by default

def avg_scan_time(plan_name,nscans=50,new_scan_duration=600):
    scans = db(plan_name=plan_name)
    durations = np.array([])
    for i,sc in enumerate(scans):
        if(sc.stop['exit_status']=='success'):
            durations = np.append(durations,sc.stop['time'] - sc.start['time'])
        if i > nscans:
            break
    if len(durations) > 0:
        return np.mean(durations)
    else:  
        #we have never run a scan of this type before (?!?) - assume it takes some default value (10 min)
        return new_scan_duration

def run_bar(bar,sortby=['p','c','a','s'],dryrun=0,rev=[False,False,False,False]):
    '''
    run all sample dictionaries stored in the list bar
    :param bar: simply a list of sample dictionaries
    :param sortby: list of strings determining the sorting of scans
        string starting with c means configuration
                             p means project
                             s means sample
                             a means acquisition
        ['p','c','a','s'] means to all of one project first, within which all of one configurations,
            within which all of one acquisition, etc
    :return: none


    I guess the order should default to alphabetical - more options to be added??
    '''
    config_change_time = 360  # time to change between configurations, in seconds.
    listout = []
    for s in bar:
        sample = s
        sample_id = s['sample_id']
        sample_project = s['project_name']
        for a in s['acquisitions']:
            listout.append([sample_id, sample_project, a['configuration'],a['plan_name'],avg_scan_time(a['plan_name']),sample,a])
    switcher = {'p':1,'s':0,'c':2,'a':3}
    try:
        sortby.reverse()
    except AttributeError:
        if isinstance(sortby,str):
            sortby = [sortby]
        else:
            print('sortby needs to be a list of strings\n p - project\n c - configuration\n s - sample \n a - scantype')
            return
    try:
        for k,r in zip(sortby,rev):
            listout = sorted(listout, key=itemgetter(switcher[k]),reverse = r)
    except KeyError:
        print('sortby needs to be a list of strings\n p - project\n c - configuration\n s - sample \n a - scantype')
        return
    if dryrun:
        text = ''
        total_time = 0
        for i,step in enumerate(listout):
            text += 'move to {} from {}, load configuration {}, scan {}, starts @ {} min and takes {} min\n'.format(
                step[5]['sample_name'],step[1],step[2],step[3],floor(total_time/60),floor(step[4]/60))
            total_time += step[4]
            if(step[2] != listout[i-1][2]):
                total_time += config_change_time
        text += f'\n\nTotal estimated time {floor(total_time/3600)} h, {floor((total_time%3600)/60)} m... have fun!'
        boxed_text('Dry Run',text,'lightblue',width=120,shrink=True)
    else:
        for i,step in enumerate(listout):
            time_remaining = sum([row[4] for row in listout[i:]])
            boxed_text('Scan Status',f'\n\nStarting scan #{i+1} out of {len(listout)}, '
                                     f'time remaining approx {floor(time_remaining/3600)} h '
                                     f'{floor((time_remaining % 3600) / 60)} m \n\n',
                       'red',width=120,shrink=True)
            yield from load_sample(step[5]) # move to sample / load sample metadata
            yield from move_to_location(get_location_from_config(step[2])) # move to configuration
            yield from do_acquisitions([step[6]]) # run scan

def list_samples(bar):
    samples = [s['sample_name'] for s in bar]
    text = '  i        Sample Name'
    for index,sample in enumerate(samples):
        text += '\n  {}        {}'.format(index, sample)
        acqs = bar[index]['acquisitions']
        for acq in acqs:
            text +='\n            {}({}) in {} configuration'.format(acq['plan_name'],acq['arguments'],acq['configuration'])
    boxed_text('Samples on bar',text,'lightblue',shrink=True)


def save_samples(sample,filename):
    switch= {sam_X.name:'x',
             sam_Y.name:'y',
             sam_Z.name:'z',
             sam_Th.name:'th',
             'x':  'x',
             'y':  'y',
             'z':  'z',
             'th': 'th'}
    samplenew = deepcopy(sample)
    if isinstance(samplenew,list):
        for i,sam in enumerate(samplenew):
            for j,loc in enumerate(sam['location']):
                if isinstance(switch[loc['motor'],Device]) :
                    samplenew[i]['location'][j]['motor']= switch[loc['motor'].name]
    else:
        for j,loc in enumerate(samplenew['location']):
            if isinstance(switch[loc['motor'], Device]):
                samplenew['location'][j]['motor'] = switch[loc['motor'].name]
    with open(filename,'w') as f:
        json.dump(samplenew,f,indent=2)


def save_samplesxls(sample,filename):
    switch= {sam_X.name:'x',
             sam_Y.name:'y',
             sam_Z.name:'z',
             sam_Th.name:'th',
             'x':'x',
             'y':'y',
             'z':'z',
             'th':'th'}
    sampledf = pd.DataFrame.from_dict(sample, orient='columns')
    sampledf.to_excel('temp.xls')

    df = pd.read_excel('temp.xls',na_values='')
    df.replace(np.nan, '', regex=True,inplace=True)
    testdict = df.to_dict(orient='records')
    if isinstance(testdict,list):
        for i,sam in enumerate(testdict):
            testdict[i]['location'] = eval(sam['location'])
            testdict[i]['acquisitions'] = eval(sam['acquisitions'])
    else:
        testdict['location'] = eval(testdict['location'])
        testdict['acquisitions'] = eval(testdict['acquisitions'])

    if isinstance(testdict,list):
        for i,sam in enumerate(testdict):
            for j,loc in enumerate(sam['location']):
                if isinstance(loc['motor'],Device):
                    testdict[i]['location'][j]['motor']= switch[loc['motor'].name]
    else:
        for j,loc in enumerate(testdict['location']):
            if isinstance(loc['motor'], Device):
                testdict['location'][j]['motor'] = switch[loc['motor'].name]
    sampledf = pd.DataFrame.from_dict(testdict,orient='columns')
    sampledf.to_excel(filename)


def load_samples(filename):
    with open(filename,'r') as f:
        samplenew = json.loads(f.read())
    return samplenew


def load_samplesxls(filename):
    df = pd.read_excel(filename,na_values='',converters= {'sample_date': str})
    df.replace(np.nan, '', regex=True,inplace=True)
    samplenew = df.to_dict(orient='records')
    if isinstance(samplenew,list):
        for i,sam in enumerate(samplenew):
            samplenew[i]['location'] = eval(sam['location'])
            samplenew[i]['acquisitions'] = eval(sam['acquisitions'])
            for key in [key for key, value in sam.items() if 'named' in key.lower()]:
                del samplenew[i][key]
    else:
        samplenew['location'] = eval(samplenew['location'])
        samplenew['acquisitions'] = eval(samplenew['acquisitions'])
        for key in [key for key, value in samplenew.items() if 'named' in key.lower()]:
            del samplenew[key]
    return samplenew


def sample_by_value_match(bar,key,string):
    results = [d for (index, d) in enumerate(bar) if d[key].find(string) >= 0]
    if len(results) == 1 :
        return results[0]
    elif len(results) < 1 :
        print('No Match')
        return None
    elif len(results) > 1 :
        print('More than one result found, returning them all')
        return results


def sample_by_name(bar,name):
    return sample_by_value_match(bar,'sample_name',name)


def NEXAFS_WAXS_bar(barin,start_en,stop_en,num_en):
    yield from bps.mv(Shutter_Y,30)
    for sample in barin:
        yield from load_sample(sample)
        RE.md['project_name'] = 'NEXAFS'
        yield from bp.scan([en.energy],en,start_en,stop_en,num_en)


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


def flip_bar(bar):
    for samp in bar:
        for mot in samp['location']:
            if mot['motor'] is 'x':
                mot['position'] = .5 - mot['position']
            if mot['motor'] is 'th':
                mot['position'] = 180

def straighten_bar(bar,d_y, d_x, y_center):
 for samp in bar:
     xpos = samp['location'][0]['position']
     ypos = samp['location'][1]['position']
     samp['location'][0]['position'] = straighten_x(xpos,ypos,d_x,d_y,y_center)

def straighten_x(x, y, dx, dy, y_center ):
    return x - (y+y_center)*dx/dy

def correct_bar(bar,af1x,af1y,af2x,af2y):
    x_offset = af1x - bar[0]['location'][0]['position']
    y_offset = af1y - bar[0]['location'][1]['position']
    x_image_offset = bar[0]['location'][0]['position'] - bar[-1]['location'][0]['position']

    dx = (af2x-af1x) + x_image_offset
    dy = af2y-af1y


    for samp in bar:
        xpos = samp['location'][0]['position']
        ypos = samp['location'][1]['position']

        xpos = xpos + x_offset
        ypos = ypos + y_offset

        newx = xpos + (ypos - af1y) * dx/dy

        samp['location'][0]['position'] = newx
        samp['location'][1]['position'] = ypos

