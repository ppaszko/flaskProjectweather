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


def draw_ceiling_clouds(data):
    #ta funkcja psuje to gowno
    data_ceiling =data


    #data_ceiling.index = pd.to_datetime(data_ceiling['datetime:'])
    #data_ceiling = data_ceiling[~data_ceiling.index.duplicated(keep='first')]
# ceiling pułap chmur
    for file in glob.glob('static/images/*ceiling.png'):
        os.remove(file)
    t = ['']
    s = [1000]

    plt.figure(figsize=(3.5, 5))
    plt.plot(t, s)
    plt.axhline(y=0,linewidth=0, color='#d62728')
    #print(data_ceiling)

    plt.axhline(y=data_ceiling['ceiling_level:'][-1],linewidth=2, color='#d62728')
    plt.text(0,data_ceiling['ceiling_level:'][-1]+1, data_ceiling['ceiling:'][-1], fontsize=12)
    plt.text(0,data_ceiling['ceiling_level:'][-1]-45, 'Ceiling: ' + str(data_ceiling['ceiling_level:'][-1]), fontsize=12)

    if data_ceiling['ceiling_level:'][-1]!=data_ceiling['clouds1_level:'][-1]:
        plt.axhline(y=data_ceiling['clouds1_level:'][-1], linewidth=2, color='#d62728')
        plt.text(0, data_ceiling['clouds1_level:'][-1] + 1, data_ceiling['clouds1:'][-1], fontsize=12)
        plt.text(0, data_ceiling['clouds1_level:'][-1] - 45, 'Clouds:' + str(data_ceiling['clouds1_level:'][-1]), fontsize=12)

    plt.subplots_adjust(top = 1, bottom = 0,
            hspace = 0, wspace = 0)
    #print(data_ceiling)
    image_name = "static/images/{}ceiling.png".format(random()) # could be a uuid instead of datetime
    plt.savefig(image_name, dpi=300,transparent = True)
    edges = cv2.imread(image_name)
    scale_percent = 30
    #calculate the 50 percent of original dimensions
    width = int(edges.shape[1] * scale_percent / 100)
    height = int(edges.shape[0] * scale_percent / 100)
    # dsize
    dsize = (width, height)
    edges=cv2.resize(edges,dsize)
    cv2.imwrite(image_name,edges)
    # utc_dt = datetime.datetime(2009, 7, 10, 18, 44, 59, 193982, tzinfo=pytz.utc)
    return image_name


def mydraw(data, measure, start_time, end_time):
    data_custom=data
    #print(data_custom)
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
    #print(start_time)

    plt.plot(data_custom[measure])
    plt.xticks(rotation=30)
    #print(data_custom)

    image_name = "static/images/{}custom_plot1.png".format(random())  # could be a uuid instead of datetime

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