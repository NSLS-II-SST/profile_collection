print(f'Loading {__file__}...')

import pytz
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import requests
import matplotlib.pyplot as plt



class plotpvs(list):
    archiver_addr = "http://xf07id1-ca1.cs.nsls2.local:17668/retrieval/data/getData.json"
    timezone = 'US/Eastern'
    pvdict = {}

    def __init__(self, pvdict = {}, hours = 0, minutes = 0, seconds = 0, days = 0, weeks = 0):
        list.__init__(self)
        self.figure = plt.figure('Archiver Plot')
        until = datetime.today()
        since = until - timedelta(days=days, seconds=seconds,  minutes=minutes, hours=hours, weeks=weeks)
        #since = datetime(2019, 1, 1)
        #until = datetime(2019, 2, 12)

        # request data from archiver

        since = pytz.timezone(self.timezone).localize(since).replace(microsecond=0).isoformat()
        until = pytz.timezone(self.timezone).localize(until).replace(microsecond=0).isoformat()
        for pvname in pvdict:
            params = {'pv': pvdict[pvname], 'from': since, 'to': until}
            req = requests.get(self.archiver_addr, params=params, stream=True)
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
            df = pd.DataFrame()
            df[pvname+'t'] = datetimes
            df[pvname] = data
            df[pvname] = pd.to_numeric(df[pvname],errors='coerce')
            df[pvname+'t'] = df[pvname+'t'].dt.tz_localize('UTC').dt.tz_convert(self.timezone)
            df = df.set_index(pvname+'t')
            #df.plot(pvname+'t',pvname,logy=1,linewidth=.2,figure=self.figure)
            if weeks:
                df = df.resample('1H').mean()
            elif days:
                df = df.resample('10M').mean()
            elif hours:
                df = df.resample('10S').mean()
            else:
                df = df.resample('1S').mean()
            self.append(df)

pvdictionary = {'Main Chamber Pressure':'XF:07IDB-VA:2{RSoXS:Main-CCG:1}P:Raw-I'}
pvdictionary['Load Lock Pressure']='XF:07IDB-VA:2{RSoXS:LL-CCG:1}P:Raw-I'
