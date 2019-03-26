print(f'Loading {__file__}...')

import datetime
import bluesky.plans as bp
import bluesky.plan_stubs as bps
import bluesky.preprocessors as bpp

def newuser(user='nochange',userid='nochange',proposal_id='nochange',institution='nochange',project='nochange'):
    if(user is not 'nochange'):
        RE.md['user'] = user
    if (project is not 'nochange'):
        RE.md['project'] = project
    if (proposal_id is not 'nochange'):
        RE.md['proposal_id'] = proposal_id
    if (institution is not 'nochange'):
        RE.md['institution'] = institution
    if (userid is not 'nochange'):
        RE.md['userid'] = userid
def newsample(sample,sampleid='',sample_desc='',sampleset='',creator='',institution='',project='',project_desc='',project_id='',chemical_formula='', density='',components='',dim1='',dim2='',dim3='',notes=''):
    RE.md['sample']=sample
    RE.md['sample_desc']=sample_desc
    RE.md['sampleid']=sampleid
    RE.md['sampleset']=sampleset
    RE.md['creator']=creator
    RE.md['institution']=institution
    RE.md['project']=project
    RE.md['project']=project_desc
    RE.md['project']=project_id
    RE.md['chemical_formula']=chemical_formula
    RE.md['density']=density
    RE.md['components']=components
    RE.md['dim1']=dim1
    RE.md['dim2']=dim2
    RE.md['dim3']=dim3
    RE.md['notes']=notes

def snapsw(seconds,samplename='snap',sampleid='', md={}):
    # TODO: do it more generally
    # yield from bps.mv(sw_det.setexp, seconds)
    yield from bps.mv(sw_det.waxs.cam.acquire_time, seconds)
    yield from bps.mv(sw_det.saxs.cam.acquire_time, seconds)

    md['sample'] = samplename
    md['sampleid'] = sampleid
    uid = (yield from bp.count([sw_det], num=1, md=md))
    hdr = db[uid]
    dt = datetime.datetime.fromtimestamp(hdr.start['time'])
    formatted_date = dt.strftime('%Y-%m-%d')
    tiff_series.export(hdr.documents(fill=True),
        file_prefix=('{start[institution]}/'
                    '{start[user]}/'
                    '{start[project]}/'
                    f'{formatted_date}/'
                    '{start[scan_id]}-{start[sample]}-'),
        directory='Z:/images/users/'
    )

def myplan(dets, motor, start, stop, num):
    yield from bp.scan(dets, motor, start, stop, num)

