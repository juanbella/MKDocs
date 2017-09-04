#!/usr/bin/env python

import netCDF4 as nc
import datetime
import pandas as pd

def netcdf_to_df():
    group = nc.Dataset("/home/iic/Escritorio/sf_Compartida/wind_deterministic_20170301.nc",'r', format='NETCDF3_64BIT_OFFSET')
    #group = nc.Dataset("test.nc", "r")

    offset_date = datetime.datetime(1900,1,1,0,0)
    date = offset_date + datetime.timedelta(hours=int(group.variables['time'][0]))
    lat_shape = group.variables['latitude'].size
    lon_shape = group.variables['longitude'].size

    print(group.variables['time'])
    print(group.variables['time'][0])
    print(date)

    times = []
    for i,t in enumerate(group.variables['time'][:]):
        times.append(offset_date + datetime.timedelta(hours=int(t)))
        print(times[i])


    dicc = {}
    latitudes = group.variables['latitude'][:]
    longitudes = group.variables['longitude'][:]

    #lat_shape = 10
    #lon_shape = 10

    for t,time in enumerate(group.variables['time'][:]):
        for v in group.variables:
            if v == 'time' or v == 'longitude' or v == 'latitude':
                continue
            variable = group.variables[v]
            date = offset_date + datetime.timedelta(hours=int(time))
            if not date in dicc:
                dicc[date] = {}
            for i in range(lat_shape):
                for j in range(lon_shape):
                    coords = latitudes[i], longitudes[j]
                    key = variable.long_name + str(coords)
                    dicc[date][key] = variable[t][i][j]


    file = open('netcdf_dataframe.txt', 'w')
    df = pd.DataFrame.from_dict(dicc,orient='index')
    file.write(str(df))
    file.close()


if __name__ == '__main__':
    netcdf_to_df()