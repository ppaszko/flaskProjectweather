import datetime
import glob
import json
import os
from random import random

import pandas as  pd
import cv2
import numpy as np
import matplotlib.pyplot as plt
import pytz
import datetime
import pytz
from matplotlib.dates import DateFormatter

unaware = datetime.datetime(2011, 8, 15, 8, 15, 12, 0)
aware = datetime.datetime(2011, 8, 15, 8, 15, 12, 0, pytz.UTC)

now_aware = pytz.utc.localize(unaware)
assert aware == now_aware


def draw_ceiling_clouds(data, time):
    data_ceiling =data
    if time:

        luj=pd.Index(data_ceiling['datetime:']).get_loc(time)
    else:
        luj=-1
    for file in glob.glob('static/images/*ceiling.png'):
        os.remove(file)
    t = ['']
    s = [1000]
    plt.figure(figsize=(3.5, 5))
    plt.plot(t, s)
    plt.axhline(y=0,linewidth=0, color='#d62728')
    plt.axhline(y=data_ceiling['ceiling_level:'][luj],linewidth=2, color='#d62728')
    plt.text(0,data_ceiling['ceiling_level:'][luj]+1, data_ceiling['ceiling:'][luj], fontsize=12)
    plt.text(0,data_ceiling['ceiling_level:'][luj]-45, 'Ceiling: ' + str(data_ceiling['ceiling_level:'][luj]), fontsize=12)
    if data_ceiling['ceiling_level:'][luj]!=data_ceiling['clouds1_level:'][luj]:
        plt.axhline(y=data_ceiling['clouds1_level:'][luj], linewidth=2, color='#d62728')
        plt.text(0, data_ceiling['clouds1_level:'][luj] + 1, data_ceiling['clouds1:'][luj], fontsize=12)
        plt.text(0, data_ceiling['clouds1_level:'][luj] - 45, 'Clouds:' + str(data_ceiling['clouds1_level:'][luj]), fontsize=12)
    plt.subplots_adjust(top = 1, bottom = 0, hspace = 0, wspace = 0)
    image_name = "static/images/{}ceiling.png".format(random())
    saver_resizer(image_name, 30)

    return image_name


def mydraw(data, measure, start_time, end_time):
    data_custom=data

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
    plt.plot(data_custom[measure])
    plt.xticks(rotation=30)

    image_name = "static/images/{}custom_plot1.png".format(random())  # could be a uuid instead of datetime
    saver_resizer(image_name, 30)


    return image_name


def saver_resizer(image_name, scale):
    plt.savefig(image_name, dpi=300, transparent=True)
    edges = cv2.imread(image_name)
    scale_percent = scale
    width = int(edges.shape[1] * scale_percent / 100)
    height = int(edges.shape[0] * scale_percent / 100)
    dsize = (width, height)
    edges = cv2.resize(edges, dsize)
    cv2.imwrite(image_name, edges)