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
from suitcase import tiff_series, tiff_stack
from event_model import Filler

USERDIR = 'Z:/images/users/{}'

filler = Filler(db.reg.handler_reg)
RE.subscribe(filler)

serializer = tiff_series.Serializer(file_prefix='{start[institution]}-Eph={event[data][energy]}-{start[scan_id]}-',
                                    directory=USERDIR.format('DAMA'))

# TODO: figure out how to properly use it as a callback.

