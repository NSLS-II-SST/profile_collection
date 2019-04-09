print(f'Loading {__file__}...')

import numpy as np
import datetime
import bluesky.plans as bp
import bluesky.plan_stubs as bps
from suitcase import tiff_series, csv


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



def snapsw(seconds,samplename='',sampleid='', num_images=1,dark=0):
    # TODO: do it more generally
    # yield from bps.mv(sw_det.setexp, seconds)
    yield from bps.mv(sw_det.waxs.cam.acquire_time, seconds)
    yield from bps.mv(sw_det.saxs.cam.acquire_time, seconds)
    yield from bps.mv(sw_det.waxs.cam.shutter_close_delay,200)
    yield from bps.mv(sw_det.saxs.cam.shutter_close_delay,200)
    yield from bps.mv(sw_det.waxs.cam.shutter_open_delay,200)
    yield from bps.mv(sw_det.saxs.cam.shutter_open_delay,200)
    if(dark):
        yield from bps.mv(sw_det.saxs.cam.shutter_mode, 0)
        if samplename is "":
            samplename = "dark"
    else:
        yield from bps.mv(sw_det.saxs.cam.shutter_mode, 2)
        if samplename is "":
            samplename = "snap"
    md=RE.md
    md['sample'] = samplename
    md['sampleid'] = sampleid
    md['exptime'] = seconds
    uid = (yield from bp.count([sw_det], num=num_images, md=md))
    hdr = db[uid]
    quick_view(hdr)
    dt = datetime.datetime.fromtimestamp(hdr.start['time'])
    formatted_date = dt.strftime('%Y-%m-%d')
    energy = hdr.table(stream_name='baseline')['Beamline Energy_energy'][1]
    tiff_series.export(hdr.documents(fill=True),
        file_prefix=('{start[institution]}/'
                    '{start[user]}/'
                    '{start[project]}/'
                    f'{formatted_date}/'
                    '{start[scan_id]}-'
                    '{start[sample]}-'
                    f'{energy:.2f}eV-'),
        directory='Z:/images/users/')
    csv.export(hdr.documents(stream_name='baseline'),
        file_prefix=('{institution}/'
                     '{user}/'
                     '{project}/'
                     f'{formatted_date}/'
                     '{scan_id}-'
                     '{sample}-'
                     f'{energy:.2f}eV-'),
        directory='Z:/images/users/')
    csv.export(hdr.documents(stream_name='Izero Mesh Drain Current_monitor'),
        file_prefix=('{institution}/'
                     '{user}/'
                     '{project}/'
                     f'{formatted_date}/'
                     '{scan_id}-'
                     '{sample}-'
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
    dt = datetime.datetime.now()
    formatted_date = dt.strftime('%Y-%m-%d')
    for i, pos in enumerate(np.linspace(enstart, enstop, steps)):
        yield from bps.mv(en, pos)
        uid = (yield from bp.count([sw_det], md=md))
        hdr = db[uid]
        quick_view(hdr)
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
                         '-{start[scan_id]}-'
                         '-{start[sample]}-'
                         f'{pos:.2f}eV-'),
            directory='Z:/images/users/')
        csv.export(hdr.documents(stream_name='baseline'),
            file_prefix=('{institution}/'
                         '{user}/'
                         '{project}/'
                         f'{formatted_date}/'
                         f'{first_scan_id}-'
                         '{scan_id}-'
                         '{sample}-'
                         f'{pos:.2f}eV-'),
            directory='Z:/images/users/')
        csv.export(hdr.documents(stream_name='Izero Mesh Drain Current_monitor'),
            file_prefix=('{institution}/'
                         '{user}/'
                         '{project}/'
                         f'{formatted_date}/'
                         f'{first_scan_id}-'
                         '{scan_id}-'
                         '{sample}-'
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
    dt = datetime.datetime.now()
    formatted_date = dt.strftime('%Y-%m-%d')
    for i, pos in enumerate(np.linspace(start, stop, steps)):
        yield from bps.mv(motor, pos)
        uid = (yield from bp.count([sw_det], md=md))
        hdr = db[uid]
        quick_view(hdr)
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



def buildeputable():
    ens = [250,260,270,280,285,290,300,310,320,340,350,370,390,400,410,420,450,470,490,500,520,550,575,600,625,650,675,700,725,750,800,850,900,950,1000]
    gaps = []
    IzeroMesh.kind= 'hinted'
    startinggap = epugap_from_energy(250)
    for energy in ens:
        yield from bps.mv(mono_en,energy)
        yield from bps.mv(epu_gap,startinggap-500)
        yield from bp.scan([IzeroMesh],epu_gap,startinggap-500,startinggap+1500,21)
        gaps.append(bec.peaks.max["Izero Mesh Drain Current"][0])
        startinggap = bec.peaks.max["Izero Mesh Drain Current"][0]
    print(ens,gaps)
