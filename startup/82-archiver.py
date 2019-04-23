print(f'Loading {__file__}...')

import pytz
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import requests



def plotpvs(pvlist={},hours=0, minutes=0, seconds=0, days=0, weeks=0):
    # define the ESM archiver address
    archiver_addr = "http://xf07id1-ca1.cs.nsls2.local:17668/retrieval/data/getData.json"
    # http://xf07id1-ca1.cs.nsls2.local:17665/mgmt/ui/index.html
    # define the EPICS pv and time interval

    #pv = 'XF:21ID-EPS{PLC}Fuse-Sts'
    until = datetime.today()
    since = until - timedelta(days=days, seconds=seconds,  minutes=minutes, hours=hours, weeks=weeks)
    #since = datetime(2019, 1, 1)
    #until = datetime(2019, 2, 12)

    # request data from archiver

    timezone = 'US/Eastern'
    since = pytz.timezone(timezone).localize(since).replace(microsecond=0).isoformat()
    until = pytz.timezone(timezone).localize(until).replace(microsecond=0).isoformat()
    df = pd.DataFrame()
    for pvname in pvlist:
        params = {'pv': pvlist[pvname], 'from': since, 'to': until}
        req = requests.get(archiver_addr, params=params, stream=True)
        req.raise_for_status()

        # process data

        raw, = req.json()

        secs = [x['secs'] for x in raw['data']]
        nanos = [x['nanos'] for x in raw['data']]
        data = [x['val'] for x in raw['data']]

        asecs = np.asarray(secs)
        ananos = np.asarray(nanos)

        times = asecs * 1.0e+3 + ananos * 1.0e-6
        datetimes = pd.to_datetime(times, unit='ms')

        # create and print the DataFrame\

        df[pvname+'t'] = datetimes
        df[pvname] = data
        df[pvname] = pd.to_numeric(df[pvname+'t'],errors='coerce')
        df.time = df.time.dt.tz_localize('UTC').dt.tz_convert(timezone)
        df.plot(pvname+'t',pvname,logy=1)
