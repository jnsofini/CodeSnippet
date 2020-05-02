#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""


@author: github/com/jnsofini
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import urllib.request
#from io import StringIO
#import requests
from datetime import datetime

#==================   Package improvements ======================

plt.style.use('ggplot')

url = 'https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/gsn/CM000064870.dly'
#the data of the stations are stored in stations
#urllib.request.urlretrieve('ftp://ftp.ncdc.noaa.gov/pub/data/ghcn/daily/ghcnd-stations.txt','stations.txt')
#open('stations.txt','r').readlines()[:10]

class GSM_TempRecord:

    def __init__(self, url):
        self.url = url

    def get_data(self):

        return urllib.request.urlretrieve(self.url)[0]

# =============================================================================
#     def get_text(self):
#         data = requests.get(self.url).text
#         return data StringIO(data).readlines()
# =============================================================================

    def parsefile(self):
        dly_delimiter = [11,4,2,4] + [5,1,1,1] * 31
        dly_usecols = [1,2,3] + [4*i for i in range(1,32)]
        dly_dtype = [np.int32,np.int32,(np.str_,4)] + [np.int32] * 31
        dly_names = ['year','month','obs'] + [str(day) for day in range(1,31+1)]

        file_data = self.get_data()

        return np.genfromtxt(file_data,
                             delimiter = dly_delimiter,
                             usecols = dly_usecols,
                             dtype = dly_dtype,
                             names = dly_names
                             )

    def unroll(self, record):

        startdate = np.datetime64('{}-{:02}'.format(record['year'], record['month']))
        dates = np.arange(startdate,startdate + np.timedelta64(1,'M'), np.timedelta64(1,'D'))
        rows = [(date,record[str(i+1)]/10) for i,date in enumerate(dates)]

        return np.array(rows,dtype=[('date','M8[D]'),('value','d')])


    def getobs(self, obs):
        data = np.concatenate([self.unroll(row) for row in self.parsefile() if row[2] == obs])

        data['value'][data['value'] == -999.9] = np.nan

        return data


def plot_min_max_temperature(data):

    # Plotting
    ax = data.loc[datetime(1976, 1, 1): datetime(1986, 1, 1)].plot(
        figsize=(12,5), title='High Temperature in Ngaoundere', linewidth=1
        )

    ax.set_xlabel('Date')
    ax.set_ylabel('Temperature')
    plt.show()

#--------------------------------------------------------------------------------

NG_temp = GSM_TempRecord(url)
NGN_tmax = NG_temp.getobs('TMAX')
NGN_tmin = NG_temp.getobs('TMIN')

data = pd.DataFrame(NGN_tmax)
data.set_index('date', inplace=True)
data.columns = ['Max']

t = pd.DataFrame(NGN_tmin)
t.set_index('date', inplace=True)

data['Min'] = t

plot_min_max_temperature(data)
