print(f'Loading {__file__}...')
from pathlib import Path

"""
Example:
--------

In [20]: tiff_series.export(db[-3].documents(fill=True), file_prefix='{start[institution]}-Eph={event[data][energy]}-{s
    ...: tart[scan_id]}-', directory=f'Z:/images/users/{hdr.start["user"]}')
Out[20]:
{'stream_data': [WindowsPath('//XF07ID1-WS17/RSoXS Documents/images/users/Eliot/NIST-Eph=459.987181-40-primary-sw_det_saxs_image-0.tiff'),
  WindowsPath('//XF07ID1-WS17/RSoXS Documents/images/users/Eliot/NIST-Eph=459.987181-40-primary-sw_det_waxs_image-0.tiff'),
  WindowsPath('//XF07ID1-WS17/RSoXS Documents/images/users/Eliot/NIST-Eph=459.9903474-40-primary-sw_det_saxs_image-1.tiff'),
  WindowsPath('//XF07ID1-WS17/RSoXS Documents/images/users/Eliot/NIST-Eph=459.9903474-40-primary-sw_det_waxs_image-1.tiff'),
  WindowsPath('//XF07ID1-WS17/RSoXS Documents/images/users/Eliot/NIST-Eph=460.0084854-40-primary-sw_det_saxs_image-2.tiff'),
  WindowsPath('//XF07ID1-WS17/RSoXS Documents/images/users/Eliot/NIST-Eph=460.0084854-40-primary-sw_det_waxs_image-2.tiff')]}
"""
from event_model import Filler, RunRouter
from suitcase import tiff_series,csv, json_metadata
from datetime import datetime

USERDIR = 'Z:/images/users/'

glob_start_doc = None

def factory(name, start_doc):
    filler = Filler(db.reg.handler_reg)

    # filler(name, start_doc)  # modifies doc in place

    def subfactory(name, descriptor_doc):

        if descriptor_doc['name']  == 'primary':
            dt = datetime.now()
            formatted_date = dt.strftime('%Y-%m-%d')
            #energy = hdr.table(stream_name='baseline')['Beamline Energy_energy'][1]
            serializer = tiff_series.Serializer(file_prefix=('{start[institution]}/'
                                                             '{start[user]}/'
                                                             '{start[project]}/'
                                                             f'{formatted_date}/'
                                                             '{start[scan_id]}-'
                                                             '{start[sample]}-'
                                                             '{event[data][Beamline Energy_energy]:.2f}eV-'
                                                             ),
                                                directory=USERDIR)
            serializer('start', start_doc)
            serializer('descriptor', descriptor_doc)
            serializerjson = json_metadata.Serializer(file_prefix=('{institution}/'
                                                                   '{user}/'
                                                                   '{project}/'
                                                                   f'{formatted_date}/'
                                                                   '{scan_id}-'
                                                                   '{sample}-'
                                                                   #'{event[data][Beamline Energy_energy]:.2f}eV-'
                                                                   ),
                                                      directory=USERDIR,
                                                      sort_keys=True,
                                                      indent=2)
            serializerjson('start', start_doc)
            serializerjson('descriptor', descriptor_doc)
            serializercsv = csv.Serializer(file_prefix=('{start[institution]}/'
                                                        '{start[user]}/'
                                                        '{start[project]}/'
                                                        f'{formatted_date}/'
                                                        '{start[scan_id]}-'
                                                        '{start[sample]}-'
                                                        #'{event[data][Beamline Energy_energy]:.2f}eV-'
                                                        ),
                                           directory=USERDIR,
                                           flush=True,
                                           line_terminator='\n')
            serializercsv('start', start_doc)
            serializercsv('descriptor', descriptor_doc)
            return [serializer,serializerjson,serializercsv]
        elif descriptor_doc['name'] == 'baseline':
            dt = datetime.now()
            formatted_date = dt.strftime('%Y-%m-%d')
            # energy = hdr.table(stream_name='baseline')['Beamline Energy_energy'][1]
            serializer = csv.Serializer(file_prefix=('{start[institution]}/'
                                                     '{start[user]}/'
                                                     '{start[project]}/'
                                                     f'{formatted_date}/'
                                                     '{start[scan_id]}-'
                                                     '{start[sample]}-'
                                                     #'{event[data][Beamline Energy_energy]:.2f}eV-'
                                                     ),
                                        directory=USERDIR,
                                        flush=True,
                                        line_terminator='\n')
            serializer('start', start_doc)
            serializer('descriptor', descriptor_doc)
            return [serializer]

        else:
            return []

    def cb(name, doc):
        filler(name, doc)  # Fill in place any externally-stored data written by area detector.
        # if name == 'event_page':
        #     if 'Beamline Energy_energy' in doc['data'] and 'Izero Mesh Drain Current' in doc['data']:
        #         dt = datetime.now()
        #         formatted_date = dt.strftime('%Y-%m-%d')
        #         filename = ('{start[institution]}/'
        #                     '{start[user]}/'
        #                     '{start[project]}/'
        #                    f'{formatted_date}/'
        #                     '{start[scan_id]}-'
        #                     '{start[sample]}-'
        #                     #'{energy:.2f}eV'
        #                     '.txt'
        #                     ).format(start=start_doc, energy=doc['data']['Beamline Energy_energy'][-1])
        #
        #         filename = Path(USERDIR) / Path(filename)
        #         #print(f'!!!! filename: {filename}')
        #         with open(filename, 'a+') as fp:
        #             fp.write(f"{doc['data']['Beamline Energy_energy'][-1]}, {doc['data']['Izero Mesh Drain Current'][-1]}\n")
        #     else:
        #         pass
        # else:
        #     pass

    return [cb], [subfactory]


rr = RunRouter([factory])

rr_token = RE.subscribe(rr)  # This should be subscribed *after* db so filling happens after db.insert.