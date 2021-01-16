import datetime
import glob
import json
import os
from random import random

import cv2
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter

UNITS = {'temperature:': 'C', 'rain': 'mm', 'wind_speed:': 'km/h', 'pressure': 'hpa', }


def draw_wth_trend(data_custom, measure, start_time, end_time):
    data_custom = data_custom
    data_custom.index = pd.to_datetime(data_custom['datetime:'])
    data_custom = data_custom[~data_custom.index.duplicated(keep='first')]
    print(data_custom)
    for file in glob.glob('static/images/*custom_plot1.png'):
        os.remove(file)
    plt.rcParams.update({'font.size': 16})
    fig, ax = plt.subplots(figsize=(20, 10))

    start_time = pd.to_datetime(start_time)
    end_time = pd.to_datetime(end_time)
    ax.set_xlim([pd.to_datetime(start_time), pd.to_datetime(end_time)])
    data_custom = data_custom[(data_custom.index >= start_time) & (data_custom.index <= end_time)]
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d %H:%M'))
    ax.plot(data_custom[measure], 'bo', markersize=15)
    #idx = pd.period_range(start_time, end_time, freq='H')
    #data_custom = data_custom.reindex(idx.to_timestamp(), fill_value=None)
    # print(x)
    x = np.arange(len(data_custom.index))

    print(x)
    y = data_custom[measure].values
    print(y)

    z = np.polyfit(x[~np.isnan(y)], y[~np.isnan(y)], 1)
    p = np.poly1d(z)
    trend = pd.DataFrame(p(x), index=data_custom.index)
    ax.plot(trend, "r-", linewidth=3)
    ax.grid()
    plt.xticks(rotation=30)
    plt.ylabel(measure + ' (' + UNITS[measure] + ')')
    plt.xlabel("time")
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.xaxis.label.set_fontsize(20)
    ax.yaxis.label.set_fontsize(20)

    ax.tick_params(colors='white')
    plt.show()
    image_name = "static/images/{}custom_plot1.png".format(
        datetime.datetime.utcnow().isoformat())  # could be a uuid instead of datetime
    # image_name='luj'
    print(image_name)

    plt.savefig(image_name, dpi=300, transparent=True)
    edges = cv2.imread(image_name)
    scale_percent = 30
    # calculate the 50 percent of original dimensions
    width = int(edges.shape[1] * scale_percent / 100)
    height = int(edges.shape[0] * scale_percent / 100)
    # dsize
    dsize = (width, height)
    edges = cv2.resize(edges, dsize)
    cv2.imwrite(image_name, edges)
    return image_name


def mydraw(data, measure, start_time, end_time):
    with open('/home/paszko/PycharmProjects/flaskProject/epkt.json') as f:
        data_custom = pd.DataFrame(json.load(f)['airport_info'])

    data_custom.drop_duplicates(subset ="datetime:",
                     keep = 'first', inplace = True)

    data_custom['datetime:'] = pd.to_datetime(data_custom['datetime:'])
    data_custom.index = data_custom['datetime:']
    data_custom = data_custom[~data_custom.index.duplicated(keep='first')]
    print(data_custom)
    for file in glob.glob('static/images/*custom_plot1.png'):
        os.remove(file)

    fig, ax = plt.subplots(figsize=(20, 10))

    start_time = pd.to_datetime(start_time)
    end_time = pd.to_datetime(end_time)
    ax.set_xlim([pd.to_datetime(start_time), pd.to_datetime(end_time)])
    data_custom = data_custom[(data_custom.index >= start_time) & (data_custom.index <= end_time)]
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d %H:%M'))
    start_time = pd.to_datetime(start_time)
    end_time = pd.to_datetime(end_time)
    print(start_time)

    #data_custom = data_custom[(data_custom['datetime:'] >= start_time)
    #                          & (data_custom['datetime:'] <= end_time)]
    plt.plot(data_custom[measure])
    plt.xticks(rotation=30)
    print(data_custom)

    image_name = "static/images/{}custom_plot1.png".format(random())  # could be a uuid instead of datetime
    # image_name='luj'
    # print(image_name)

    # plt.show()
    plt.savefig(image_name, dpi=300, transparent=True)

    edges = cv2.imread(image_name)
    scale_percent = 30
    # calculate the 50 percent of original dimensions
    width = int(edges.shape[1] * scale_percent / 100)
    height = int(edges.shape[0] * scale_percent / 100)
    # dsize
    dsize = (width, height)
    edges = cv2.resize(edges, dsize)
    cv2.imwrite(image_name, edges)

    return image_name
