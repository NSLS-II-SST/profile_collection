print(f'Loading {__file__}...')

import numpy as np
import datetime
import bluesky.plans as bp
import bluesky.plan_stubs as bps
import bluesky.preprocessors as bpp
from suitcase import tiff_series, json_metadata, csv


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

def snapsw(seconds,samplename='snap',sampleid='', num_images=1):
    # TODO: do it more generally
    # yield from bps.mv(sw_det.setexp, seconds)
    yield from bps.mv(sw_det.waxs.cam.acquire_time, seconds)
    yield from bps.mv(sw_det.saxs.cam.acquire_time, seconds)
    md=RE.md
    md['sample'] = samplename
    md['sampleid'] = sampleid
    uid = (yield from bp.count([sw_det], num=num_images, md=md))
    hdr = db[uid]
    dt = datetime.datetime.fromtimestamp(hdr.start['time'])
    formatted_date = dt.strftime('%Y-%m-%d')
    energy = hdr.table(stream_name='baseline')['Beamline Energy_energy'][1]
    tiff_series.export(hdr.documents(fill=True),
        file_prefix=('{start[institution]}/'
                    '{start[user]}/'
                    '{start[project]}/'
                    f'{formatted_date}/'
                    '{start[scan_id]}-{start[sample]}-'
                    f'{energy:.2f}eV-'),
        directory='Z:/images/users/')
    csv.export(hdr.documents(stream_name='baseline'),
        file_prefix=('{institution}/'
                     '{user}/'
                     '{project}/'
                     f'{formatted_date}/'
                     '{scan_id}-{sample}-'
                     f'{energy:.2f}eV-'),
        directory='Z:/images/users/')
    csv.export(hdr.documents(stream_name='Izero Mesh Drain Current_monitor'),
        file_prefix=('{institution}/'
                     '{user}/'
                     '{project}/'
                     f'{formatted_date}/'
                     '{scan_id}-{sample}-'
                     f'{energy:.2f}eV-'),
        directory='Z:/images/users/')

def enscansw(seconds, enstart, enstop, steps,samplename='enscan',sampleid=''):
    # TODO: do it more generally
    # yield from bps.mv(sw_det.setexp, seconds)
    yield from bps.mv(sw_det.waxs.cam.acquire_time, seconds)
    yield from bps.mv(sw_det.saxs.cam.acquire_time, seconds)
    md = RE.md
    md['sample'] = samplename
    md['sampleid'] = sampleid
    first_scan_id = None
    for i, pos in enumerate(np.linspace(enstart, enstop, steps)):
        yield from bps.mv(en, pos)
        uid = (yield from bp.count([sw_det], md=md))
        hdr = db[uid]
        if i == 0:
            first_scan_id = hdr.start['scan_id']
        dt = datetime.datetime.fromtimestamp(hdr.start['time'])
        formatted_date = dt.strftime('%Y-%m-%d')
        tiff_series.export(hdr.documents(fill=True),
            file_prefix=('{start[institution]}/'
                         '{start[user]}/'
                         '{start[project]}/'
                         f'{formatted_date}/'
                         f'{first_scan_id}-'
                         f'{first_scan_id}'
                         '-{start[sample]}-'
                         f'{pos:.2f}eV-'),
            directory='Z:/images/users/')
        csv.export(hdr.documents(stream_name='baseline'),
            file_prefix=('{institution}/'
                         '{user}/'
                         '{project}/'
                         f'{formatted_date}/'
                         '{scan_id}-{sample}-'
                         f'{pos:.2f}eV-'),
            directory='Z:/images/users/')
        csv.export(hdr.documents(stream_name='Izero Mesh Drain Current_monitor'),
            file_prefix=('{institution}/'
                         '{user}/'
                         '{project}/'
                         f'{formatted_date}/'
                         '{scan_id}-{sample}-'
                         f'{pos:.2f}eV-'),
            directory='Z:/images/users/')

    # uid = (yield from bp.scan([sw_det], en, enstart, enstop,steps, md=md))
    # hdr = db[uid]
    # dt = datetime.datetime.fromtimestamp(hdr.start['time'])
    # formatted_date = dt.strftime('%Y-%m-%d')
    # tiff_series.export(hdr.documents(fill=True),
    #     file_prefix=('{start[institution]}/'
    #                 '{start[user]}/'
    #                 '{start[project]}/'
    #                 f'{formatted_date}/'
    #                 '{start[scan_id]}-{start[sample]}-{event[data][en_energy]:.2f}eV-'), # not working, need energy in each filename
    #     directory='Z:/images/users/')
def motscansw(seconds,motor, start, stop, steps,samplename='motscan',sampleid=''):
    # TODO: do it more generally
    # yield from bps.mv(sw_det.setexp, seconds)
    yield from bps.mv(sw_det.waxs.cam.acquire_time, seconds)
    yield from bps.mv(sw_det.saxs.cam.acquire_time, seconds)
    md = RE.md
    md['sample'] = samplename
    md['sampleid'] = sampleid
    first_scan_id = None
    for i, pos in enumerate(np.linspace(start, stop, steps)):
        yield from bps.mv(motor, pos)
        uid = (yield from bp.count([sw_det], md=md))
        hdr = db[uid]
        if i == 0:
            first_scan_id = hdr.start['scan_id']
        dt = datetime.datetime.fromtimestamp(hdr.start['time'])
        formatted_date = dt.strftime('%Y-%m-%d')
        tiff_series.export(hdr.documents(fill=True),
            file_prefix=('{start[institution]}/'
                         '{start[user]}/'
                         '{start[project]}/'
                         f'{formatted_date}/'
                         f'{first_scan_id}-'
                         '{start[scan_id]}'
                         '-{start[sample]}-'
                         f'{pos:.2f}-'),
            directory='Z:/images/users/')
        csv.export(hdr.documents(stream_name='baseline'),
            file_prefix=('{institution}/'
                         '{user}/'
                         '{project}/'
                         f'{formatted_date}/'
                         f'{first_scan_id}-'
                         '{scan_id}-{sample}-'
                         f'{pos:.2f}-'),
            directory='Z:/images/users/')
        csv.export(hdr.documents(stream_name='Izero Mesh Drain Current_monitor'),
            file_prefix=('{institution}/'
                         '{user}/'
                         '{project}/'
                         f'{formatted_date}/'
                         f'{first_scan_id}-'
                         '{scan_id}-{sample}-'
                         f'{pos:.2f}-'),
            directory='Z:/images/users/')
def myplan(dets, motor, start, stop, num):
    yield from bp.scan(dets, motor, start, stop, num)

