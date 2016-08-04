import matplotlib.pyplot as plt
import numpy as np
import mpld3
from dateutil import parser
import matplotlib.dates as md
from matplotlib import font_manager as fm
import random
from collections import OrderedDict
tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),
             (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),
             (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),
             (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),
             (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]
for i in range(len(tableau20)):
    r, g, b = tableau20[i]
    tableau20[i] = (r / 255., g / 255., b / 255.)

def RankingBarChart(datas, f, dpi = 48):

    data = datas["data"]
    properties = datas["details"]

    labels, val = zip(*[(i["_id"],i["count"]) for i in data])
    pos = np.arange(len(labels))+ 0.5

    fig, ax = plt.subplots(figsize=(1920/dpi, 1080/dpi), dpi=dpi, subplot_kw=dict(axisbg='#EEEEEE'))
    boxes = ax.barh(pos,val, align='center', alpha = 0.3, color = tableau20[0])
    for i,box in enumerate(boxes):
        box.set_color(tableau20[i])

    ax.tick_params(axis='x', labelsize=25)
    ax.tick_params(axis='y', labelsize=25)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_yticks(pos)
    ax.set_yticklabels(labels)
    ax.set_xlabel(properties["xLabel"], size=30)
    plt.title(properties["title"], size=35)

    tooltip = None
    for i, box in enumerate(boxes.get_children()):
        tooltip = mpld3.plugins.LineLabelTooltip(box, label=labels[i])
        mpld3.plugins.connect(fig, tooltip)

    mpld3.save_html(fig, f)
    plt.close("all")

def TimeChart(datas, f, dpi = 48):

    data = datas["data"]
    properties = datas["details"]

    x_categories = [parser.parse(i) for i in data["categories"]]
    y_labels = OrderedDict.fromkeys(x_categories, 0)

    fig = plt.figure( figsize=(1920 / dpi, 1080 / dpi), dpi=dpi, )
    ax = plt.subplot2grid((3,1),(0,0),rowspan=2, axisbg='#EEEEEE')

    for series in data["values"]:
        for entry in series["data"]:
            y_labels[parser.parse(entry["dt"])] = entry["count"]
        l = ax.plot(x_categories, list(y_labels.values()), label = series["_id"], lw=5, alpha = 0.3)
        tooltip = mpld3.plugins.LineLabelTooltip(l[0], 'Hashtag \'{0}\''.format(series["_id"]))
        mpld3.plugins.connect(fig, tooltip)
        y_labels = OrderedDict.fromkeys(x_categories, 0)

    xfmt = md.DateFormatter('%Y-%m-%d\n %H:%M:%S')

    ax.tick_params(axis='x', labelsize=25)
    ax.tick_params(axis='y', labelsize=25)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.legend(fontsize = 30)
    ax.xaxis.set_major_formatter(xfmt)
    ax.set_ylabel(properties["yLabel"], size=30)
    ax.set_xlabel(properties["xLabel"], size=30)
    plt.title(properties["title"], size=35)

    mpld3.save_html(fig, f)
    plt.close("all")


def PiChart(datas, f, dpi = 48):

    data = datas["data"]
    properties = datas["details"]

    val_labels = [(i["count"],i["_id"]) for i in data]
    ordered_va_labels = sorted(val_labels, reverse=True)
    large = ordered_va_labels[:len(ordered_va_labels) / 2]
    small = ordered_va_labels[len(ordered_va_labels) / 2:]
    reordered = large[::2] + small[::2] + large[1::2] + small[1::2]
    val,labels = zip(*reordered)
    angle = 180 + float(sum([i[0] for i in small][::2])) / sum([i[0] for i in reordered]) * 360

    fig, ax = plt.subplots(figsize=(1080/ dpi, 1080 / dpi), dpi=dpi, subplot_kw=dict(axisbg='#EEEEEE'))

    pieWedgesCollection,texts,autotexts = plt.pie(val, explode=[0] * len(val),
                                                  labels=labels, colors=tableau20[:len(val)],
            autopct='%1.1f%%', shadow=False, labeldistance=1.05, startangle=angle)

    for i, pie_wedge in enumerate(pieWedgesCollection):
        tooltip = mpld3.plugins.LineLabelTooltip(pie_wedge, label='Language {0}: {1}'.format(labels[i], val[i]))
        mpld3.plugins.connect(fig, tooltip)
        pie_wedge.set_edgecolor('white')

    proptease = fm.FontProperties()
    proptease.set_size(25)
    plt.setp(autotexts, fontproperties=proptease)
    plt.setp(texts, fontproperties=proptease)
    #
    # centre_circle = plt.Circle((0, 0), 0.75, color='black', fc='white', linewidth=1.25)
    # # fig = plt.gcf()
    # ax.add_artist(centre_circle)
    # ax.text(0, 0, properties["title"], ha='center', size=35)


    mpld3.show()
    # plt.show()
    # for i, box in enumerate(boxes.get_children()):
    #     tooltip = mpld3.plugins.LineLabelTooltip(box, label=labels[i])
    #     mpld3.plugins.connect(fig, tooltip)
    #
    # mpld3.save_html(fig, f)
    # plt.close("all")


d = {
    "data": [
        {
            "_id": "en",
            "count": 101925
        },
        {
            "_id": "und",
            "count": 15510
        },
        {
            "_id": "fr",
            "count": 538
        },
        {
            "_id": "es",
            "count": 194
        },
        {
            "_id": "in",
            "count": 142
        },
        {
            "_id": "de",
            "count": 107
        },
        {
            "_id": "tl",
            "count": 75
        },
        {
            "_id": "et",
            "count": 53
        },
        {
            "_id": "ht",
            "count": 45
        },
        {
            "_id": "pt",
            "count": 31
        },
        {
            "_id": "it",
            "count": 30
        },
        {
            "_id": "lt",
            "count": 27
        },
        {
            "_id": "ro",
            "count": 26
        },
        {
            "_id": "pl",
            "count": 26
        },
        {
            "_id": "nl",
            "count": 22
        },
        {
            "_id": "cy",
            "count": 17
        },
        {
            "_id": "sv",
            "count": 14
        },
        {
            "_id": "ko",
            "count": 14
        },
        {
            "_id": "cs",
            "count": 12
        },
        {
            "_id": "da",
            "count": 11
        },
        {
            "_id": "tr",
            "count": 10
        },
        {
            "_id": "sl",
            "count": 10
        },
        {
            "_id": "hu",
            "count": 9
        },
        {
            "_id": "eu",
            "count": 7
        },
        {
            "_id": "ja",
            "count": 7
        },
        {
            "_id": "no",
            "count": 7
        },
        {
            "_id": "lv",
            "count": 5
        },
        {
            "_id": "hi",
            "count": 3
        },
        {
            "_id": "is",
            "count": 3
        },
        {
            "_id": "fi",
            "count": 2
        },
        {
            "_id": "fa",
            "count": 2
        },
        {
            "_id": "ar",
            "count": 1
        },
        {
            "_id": "vi",
            "count": 1
        }
    ],
    "details": {
        "chartType": "pie",
                "title":"Blah"
    }
}
PiChart(d,None)
#
#
# d = {
#     "data": {
#         "categories": [
#             "2016-06-28T18:00:00Z",
#             "2016-06-28T19:00:00Z",
#             "2016-06-28T20:00:00Z",
#             "2016-06-28T21:00:00Z",
#             "2016-06-28T22:00:00Z",
#             "2016-06-28T23:00:00Z",
#             "2016-06-29T11:00:00Z",
#             "2016-06-29T12:00:00Z",
#             "2016-06-29T13:00:00Z",
#             "2016-06-29T14:00:00Z",
#             "2016-06-29T15:00:00Z",
#             "2016-06-29T16:00:00Z",
#             "2016-06-29T17:00:00Z",
#             "2016-06-29T18:00:00Z",
#             "2016-06-29T19:00:00Z",
#             "2016-06-29T20:00:00Z",
#             "2016-06-29T21:00:00Z",
#             "2016-06-29T22:00:00Z",
#             "2016-06-29T23:00:00Z",
#             "2016-06-30T00:00:00Z",
#             "2016-06-30T01:00:00Z",
#             "2016-06-30T02:00:00Z",
#             "2016-06-30T03:00:00Z",
#             "2016-06-30T04:00:00Z",
#             "2016-06-30T05:00:00Z",
#             "2016-06-30T06:00:00Z",
#             "2016-06-30T07:00:00Z",
#             "2016-06-30T08:00:00Z",
#             "2016-06-30T09:00:00Z",
#             "2016-06-30T10:00:00Z",
#             "2016-06-30T11:00:00Z",
#             "2016-06-30T12:00:00Z",
#             "2016-06-30T13:00:00Z",
#             "2016-06-30T14:00:00Z",
#             "2016-06-30T15:00:00Z",
#             "2016-06-30T16:00:00Z",
#             "2016-06-30T17:00:00Z",
#             "2016-06-30T18:00:00Z",
#             "2016-06-30T19:00:00Z",
#             "2016-06-30T20:00:00Z",
#             "2016-06-30T21:00:00Z",
#             "2016-06-30T22:00:00Z",
#             "2016-06-30T23:00:00Z",
#             "2016-07-01T00:00:00Z",
#             "2016-07-01T01:00:00Z",
#             "2016-07-01T02:00:00Z",
#             "2016-07-01T03:00:00Z",
#             "2016-07-01T08:00:00Z",
#             "2016-07-03T19:00:00Z"
#         ],
#         "values": [
#             {
#                 "_id": "makeamericagreatagain",
#                 "data": [
#                     {
#                         "count": 429,
#                         "dt": "2016-06-28T18:00:00Z"
#                     },
#                     {
#                         "count": 914,
#                         "dt": "2016-06-28T19:00:00Z"
#                     },
#                     {
#                         "count": 1099,
#                         "dt": "2016-06-28T20:00:00Z"
#                     },
#                     {
#                         "count": 843,
#                         "dt": "2016-06-28T21:00:00Z"
#                     },
#                     {
#                         "count": 788,
#                         "dt": "2016-06-28T22:00:00Z"
#                     },
#                     {
#                         "count": 467,
#                         "dt": "2016-06-28T23:00:00Z"
#                     },
#                     {
#                         "count": 203,
#                         "dt": "2016-06-29T11:00:00Z"
#                     },
#                     {
#                         "count": 589,
#                         "dt": "2016-06-29T12:00:00Z"
#                     },
#                     {
#                         "count": 928,
#                         "dt": "2016-06-29T13:00:00Z"
#                     },
#                     {
#                         "count": 1054,
#                         "dt": "2016-06-29T14:00:00Z"
#                     },
#                     {
#                         "count": 880,
#                         "dt": "2016-06-29T15:00:00Z"
#                     },
#                     {
#                         "count": 694,
#                         "dt": "2016-06-29T16:00:00Z"
#                     },
#                     {
#                         "count": 648,
#                         "dt": "2016-06-29T17:00:00Z"
#                     },
#                     {
#                         "count": 590,
#                         "dt": "2016-06-29T18:00:00Z"
#                     },
#                     {
#                         "count": 776,
#                         "dt": "2016-06-29T19:00:00Z"
#                     },
#                     {
#                         "count": 795,
#                         "dt": "2016-06-29T20:00:00Z"
#                     },
#                     {
#                         "count": 880,
#                         "dt": "2016-06-29T21:00:00Z"
#                     },
#                     {
#                         "count": 1008,
#                         "dt": "2016-06-29T22:00:00Z"
#                     },
#                     {
#                         "count": 1205,
#                         "dt": "2016-06-29T23:00:00Z"
#                     },
#                     {
#                         "count": 872,
#                         "dt": "2016-06-30T00:00:00Z"
#                     },
#                     {
#                         "count": 1268,
#                         "dt": "2016-06-30T01:00:00Z"
#                     },
#                     {
#                         "count": 1045,
#                         "dt": "2016-06-30T02:00:00Z"
#                     },
#                     {
#                         "count": 777,
#                         "dt": "2016-06-30T03:00:00Z"
#                     },
#                     {
#                         "count": 820,
#                         "dt": "2016-06-30T04:00:00Z"
#                     },
#                     {
#                         "count": 734,
#                         "dt": "2016-06-30T05:00:00Z"
#                     },
#                     {
#                         "count": 548,
#                         "dt": "2016-06-30T06:00:00Z"
#                     },
#                     {
#                         "count": 344,
#                         "dt": "2016-06-30T07:00:00Z"
#                     },
#                     {
#                         "count": 313,
#                         "dt": "2016-06-30T08:00:00Z"
#                     },
#                     {
#                         "count": 286,
#                         "dt": "2016-06-30T09:00:00Z"
#                     },
#                     {
#                         "count": 396,
#                         "dt": "2016-06-30T10:00:00Z"
#                     },
#                     {
#                         "count": 597,
#                         "dt": "2016-06-30T11:00:00Z"
#                     },
#                     {
#                         "count": 696,
#                         "dt": "2016-06-30T12:00:00Z"
#                     },
#                     {
#                         "count": 813,
#                         "dt": "2016-06-30T13:00:00Z"
#                     },
#                     {
#                         "count": 1154,
#                         "dt": "2016-06-30T14:00:00Z"
#                     },
#                     {
#                         "count": 862,
#                         "dt": "2016-06-30T15:00:00Z"
#                     },
#                     {
#                         "count": 885,
#                         "dt": "2016-06-30T16:00:00Z"
#                     },
#                     {
#                         "count": 867,
#                         "dt": "2016-06-30T17:00:00Z"
#                     },
#                     {
#                         "count": 715,
#                         "dt": "2016-06-30T18:00:00Z"
#                     },
#                     {
#                         "count": 806,
#                         "dt": "2016-06-30T19:00:00Z"
#                     },
#                     {
#                         "count": 705,
#                         "dt": "2016-06-30T20:00:00Z"
#                     },
#                     {
#                         "count": 697,
#                         "dt": "2016-06-30T21:00:00Z"
#                     },
#                     {
#                         "count": 999,
#                         "dt": "2016-06-30T22:00:00Z"
#                     },
#                     {
#                         "count": 1164,
#                         "dt": "2016-06-30T23:00:00Z"
#                     },
#                     {
#                         "count": 966,
#                         "dt": "2016-07-01T00:00:00Z"
#                     },
#                     {
#                         "count": 873,
#                         "dt": "2016-07-01T01:00:00Z"
#                     },
#                     {
#                         "count": 1016,
#                         "dt": "2016-07-01T02:00:00Z"
#                     },
#                     {
#                         "count": 745,
#                         "dt": "2016-07-01T03:00:00Z"
#                     },
#                     {
#                         "count": 4,
#                         "dt": "2016-07-03T19:00:00Z"
#                     }
#                 ]
#             },
#             {
#                 "_id": "stoptpp",
#                 "data": [
#                     {
#                         "count": 1,
#                         "dt": "2016-06-28T18:00:00Z"
#                     },
#                     {
#                         "count": 2,
#                         "dt": "2016-06-28T19:00:00Z"
#                     },
#                     {
#                         "count": 1,
#                         "dt": "2016-06-28T20:00:00Z"
#                     },
#                     {
#                         "count": 1,
#                         "dt": "2016-06-28T21:00:00Z"
#                     },
#                     {
#                         "count": 2,
#                         "dt": "2016-06-28T22:00:00Z"
#                     },
#                     {
#                         "count": 1,
#                         "dt": "2016-06-28T23:00:00Z"
#                     },
#                     {
#                         "count": 1,
#                         "dt": "2016-06-29T12:00:00Z"
#                     },
#                     {
#                         "count": 3,
#                         "dt": "2016-06-29T13:00:00Z"
#                     },
#                     {
#                         "count": 89,
#                         "dt": "2016-06-29T16:00:00Z"
#                     },
#                     {
#                         "count": 1555,
#                         "dt": "2016-06-29T17:00:00Z"
#                     },
#                     {
#                         "count": 246,
#                         "dt": "2016-06-29T18:00:00Z"
#                     },
#                     {
#                         "count": 82,
#                         "dt": "2016-06-29T19:00:00Z"
#                     },
#                     {
#                         "count": 91,
#                         "dt": "2016-06-29T20:00:00Z"
#                     },
#                     {
#                         "count": 66,
#                         "dt": "2016-06-29T21:00:00Z"
#                     },
#                     {
#                         "count": 22,
#                         "dt": "2016-06-29T22:00:00Z"
#                     },
#                     {
#                         "count": 270,
#                         "dt": "2016-06-29T23:00:00Z"
#                     },
#                     {
#                         "count": 416,
#                         "dt": "2016-06-30T00:00:00Z"
#                     },
#                     {
#                         "count": 559,
#                         "dt": "2016-06-30T01:00:00Z"
#                     },
#                     {
#                         "count": 1107,
#                         "dt": "2016-06-30T02:00:00Z"
#                     },
#                     {
#                         "count": 319,
#                         "dt": "2016-06-30T03:00:00Z"
#                     },
#                     {
#                         "count": 273,
#                         "dt": "2016-06-30T04:00:00Z"
#                     },
#                     {
#                         "count": 54,
#                         "dt": "2016-06-30T05:00:00Z"
#                     },
#                     {
#                         "count": 17,
#                         "dt": "2016-06-30T06:00:00Z"
#                     },
#                     {
#                         "count": 23,
#                         "dt": "2016-06-30T07:00:00Z"
#                     },
#                     {
#                         "count": 19,
#                         "dt": "2016-06-30T08:00:00Z"
#                     },
#                     {
#                         "count": 2,
#                         "dt": "2016-06-30T09:00:00Z"
#                     },
#                     {
#                         "count": 2,
#                         "dt": "2016-06-30T10:00:00Z"
#                     },
#                     {
#                         "count": 9,
#                         "dt": "2016-06-30T11:00:00Z"
#                     },
#                     {
#                         "count": 2,
#                         "dt": "2016-06-30T12:00:00Z"
#                     },
#                     {
#                         "count": 14,
#                         "dt": "2016-06-30T13:00:00Z"
#                     },
#                     {
#                         "count": 12,
#                         "dt": "2016-06-30T14:00:00Z"
#                     },
#                     {
#                         "count": 25,
#                         "dt": "2016-06-30T15:00:00Z"
#                     },
#                     {
#                         "count": 60,
#                         "dt": "2016-06-30T16:00:00Z"
#                     },
#                     {
#                         "count": 29,
#                         "dt": "2016-06-30T17:00:00Z"
#                     },
#                     {
#                         "count": 13,
#                         "dt": "2016-06-30T18:00:00Z"
#                     },
#                     {
#                         "count": 10,
#                         "dt": "2016-06-30T19:00:00Z"
#                     },
#                     {
#                         "count": 16,
#                         "dt": "2016-06-30T20:00:00Z"
#                     },
#                     {
#                         "count": 9,
#                         "dt": "2016-06-30T21:00:00Z"
#                     },
#                     {
#                         "count": 23,
#                         "dt": "2016-06-30T22:00:00Z"
#                     },
#                     {
#                         "count": 46,
#                         "dt": "2016-06-30T23:00:00Z"
#                     },
#                     {
#                         "count": 16,
#                         "dt": "2016-07-01T00:00:00Z"
#                     },
#                     {
#                         "count": 9,
#                         "dt": "2016-07-01T01:00:00Z"
#                     },
#                     {
#                         "count": 7,
#                         "dt": "2016-07-01T02:00:00Z"
#                     },
#                     {
#                         "count": 6,
#                         "dt": "2016-07-01T03:00:00Z"
#                     }
#                 ]
#             },
#             {
#                 "_id": "neverhillary",
#                 "data": [
#                     {
#                         "count": 92,
#                         "dt": "2016-06-28T18:00:00Z"
#                     },
#                     {
#                         "count": 139,
#                         "dt": "2016-06-28T19:00:00Z"
#                     },
#                     {
#                         "count": 217,
#                         "dt": "2016-06-28T20:00:00Z"
#                     },
#                     {
#                         "count": 229,
#                         "dt": "2016-06-28T21:00:00Z"
#                     },
#                     {
#                         "count": 342,
#                         "dt": "2016-06-28T22:00:00Z"
#                     },
#                     {
#                         "count": 85,
#                         "dt": "2016-06-28T23:00:00Z"
#                     },
#                     {
#                         "count": 32,
#                         "dt": "2016-06-29T11:00:00Z"
#                     },
#                     {
#                         "count": 116,
#                         "dt": "2016-06-29T12:00:00Z"
#                     },
#                     {
#                         "count": 107,
#                         "dt": "2016-06-29T13:00:00Z"
#                     },
#                     {
#                         "count": 238,
#                         "dt": "2016-06-29T14:00:00Z"
#                     },
#                     {
#                         "count": 167,
#                         "dt": "2016-06-29T15:00:00Z"
#                     },
#                     {
#                         "count": 136,
#                         "dt": "2016-06-29T16:00:00Z"
#                     },
#                     {
#                         "count": 149,
#                         "dt": "2016-06-29T17:00:00Z"
#                     },
#                     {
#                         "count": 256,
#                         "dt": "2016-06-29T18:00:00Z"
#                     },
#                     {
#                         "count": 214,
#                         "dt": "2016-06-29T19:00:00Z"
#                     },
#                     {
#                         "count": 129,
#                         "dt": "2016-06-29T20:00:00Z"
#                     },
#                     {
#                         "count": 212,
#                         "dt": "2016-06-29T21:00:00Z"
#                     },
#                     {
#                         "count": 126,
#                         "dt": "2016-06-29T22:00:00Z"
#                     },
#                     {
#                         "count": 228,
#                         "dt": "2016-06-29T23:00:00Z"
#                     },
#                     {
#                         "count": 237,
#                         "dt": "2016-06-30T00:00:00Z"
#                     },
#                     {
#                         "count": 249,
#                         "dt": "2016-06-30T01:00:00Z"
#                     },
#                     {
#                         "count": 145,
#                         "dt": "2016-06-30T02:00:00Z"
#                     },
#                     {
#                         "count": 170,
#                         "dt": "2016-06-30T03:00:00Z"
#                     },
#                     {
#                         "count": 170,
#                         "dt": "2016-06-30T04:00:00Z"
#                     },
#                     {
#                         "count": 143,
#                         "dt": "2016-06-30T05:00:00Z"
#                     },
#                     {
#                         "count": 156,
#                         "dt": "2016-06-30T06:00:00Z"
#                     },
#                     {
#                         "count": 74,
#                         "dt": "2016-06-30T07:00:00Z"
#                     },
#                     {
#                         "count": 34,
#                         "dt": "2016-06-30T08:00:00Z"
#                     },
#                     {
#                         "count": 37,
#                         "dt": "2016-06-30T09:00:00Z"
#                     },
#                     {
#                         "count": 96,
#                         "dt": "2016-06-30T10:00:00Z"
#                     },
#                     {
#                         "count": 122,
#                         "dt": "2016-06-30T11:00:00Z"
#                     },
#                     {
#                         "count": 113,
#                         "dt": "2016-06-30T12:00:00Z"
#                     },
#                     {
#                         "count": 156,
#                         "dt": "2016-06-30T13:00:00Z"
#                     },
#                     {
#                         "count": 166,
#                         "dt": "2016-06-30T14:00:00Z"
#                     },
#                     {
#                         "count": 137,
#                         "dt": "2016-06-30T15:00:00Z"
#                     },
#                     {
#                         "count": 146,
#                         "dt": "2016-06-30T16:00:00Z"
#                     },
#                     {
#                         "count": 172,
#                         "dt": "2016-06-30T17:00:00Z"
#                     },
#                     {
#                         "count": 134,
#                         "dt": "2016-06-30T18:00:00Z"
#                     },
#                     {
#                         "count": 133,
#                         "dt": "2016-06-30T19:00:00Z"
#                     },
#                     {
#                         "count": 156,
#                         "dt": "2016-06-30T20:00:00Z"
#                     },
#                     {
#                         "count": 206,
#                         "dt": "2016-06-30T21:00:00Z"
#                     },
#                     {
#                         "count": 171,
#                         "dt": "2016-06-30T22:00:00Z"
#                     },
#                     {
#                         "count": 232,
#                         "dt": "2016-06-30T23:00:00Z"
#                     },
#                     {
#                         "count": 202,
#                         "dt": "2016-07-01T00:00:00Z"
#                     },
#                     {
#                         "count": 352,
#                         "dt": "2016-07-01T01:00:00Z"
#                     },
#                     {
#                         "count": 229,
#                         "dt": "2016-07-01T02:00:00Z"
#                     },
#                     {
#                         "count": 139,
#                         "dt": "2016-07-01T03:00:00Z"
#                     },
#                     {
#                         "count": 1,
#                         "dt": "2016-07-03T19:00:00Z"
#                     }
#                 ]
#             },
#             {
#                 "_id": "trump2016",
#                 "data": [
#                     {
#                         "count": 123,
#                         "dt": "2016-06-28T18:00:00Z"
#                     },
#                     {
#                         "count": 228,
#                         "dt": "2016-06-28T19:00:00Z"
#                     },
#                     {
#                         "count": 443,
#                         "dt": "2016-06-28T20:00:00Z"
#                     },
#                     {
#                         "count": 1572,
#                         "dt": "2016-06-28T21:00:00Z"
#                     },
#                     {
#                         "count": 816,
#                         "dt": "2016-06-28T22:00:00Z"
#                     },
#                     {
#                         "count": 121,
#                         "dt": "2016-06-28T23:00:00Z"
#                     },
#                     {
#                         "count": 62,
#                         "dt": "2016-06-29T11:00:00Z"
#                     },
#                     {
#                         "count": 254,
#                         "dt": "2016-06-29T12:00:00Z"
#                     },
#                     {
#                         "count": 482,
#                         "dt": "2016-06-29T13:00:00Z"
#                     },
#                     {
#                         "count": 453,
#                         "dt": "2016-06-29T14:00:00Z"
#                     },
#                     {
#                         "count": 388,
#                         "dt": "2016-06-29T15:00:00Z"
#                     },
#                     {
#                         "count": 284,
#                         "dt": "2016-06-29T16:00:00Z"
#                     },
#                     {
#                         "count": 309,
#                         "dt": "2016-06-29T17:00:00Z"
#                     },
#                     {
#                         "count": 237,
#                         "dt": "2016-06-29T18:00:00Z"
#                     },
#                     {
#                         "count": 259,
#                         "dt": "2016-06-29T19:00:00Z"
#                     },
#                     {
#                         "count": 208,
#                         "dt": "2016-06-29T20:00:00Z"
#                     },
#                     {
#                         "count": 415,
#                         "dt": "2016-06-29T21:00:00Z"
#                     },
#                     {
#                         "count": 329,
#                         "dt": "2016-06-29T22:00:00Z"
#                     },
#                     {
#                         "count": 454,
#                         "dt": "2016-06-29T23:00:00Z"
#                     },
#                     {
#                         "count": 400,
#                         "dt": "2016-06-30T00:00:00Z"
#                     },
#                     {
#                         "count": 735,
#                         "dt": "2016-06-30T01:00:00Z"
#                     },
#                     {
#                         "count": 577,
#                         "dt": "2016-06-30T02:00:00Z"
#                     },
#                     {
#                         "count": 468,
#                         "dt": "2016-06-30T03:00:00Z"
#                     },
#                     {
#                         "count": 475,
#                         "dt": "2016-06-30T04:00:00Z"
#                     },
#                     {
#                         "count": 383,
#                         "dt": "2016-06-30T05:00:00Z"
#                     },
#                     {
#                         "count": 224,
#                         "dt": "2016-06-30T06:00:00Z"
#                     },
#                     {
#                         "count": 185,
#                         "dt": "2016-06-30T07:00:00Z"
#                     },
#                     {
#                         "count": 143,
#                         "dt": "2016-06-30T08:00:00Z"
#                     },
#                     {
#                         "count": 141,
#                         "dt": "2016-06-30T09:00:00Z"
#                     },
#                     {
#                         "count": 154,
#                         "dt": "2016-06-30T10:00:00Z"
#                     },
#                     {
#                         "count": 206,
#                         "dt": "2016-06-30T11:00:00Z"
#                     },
#                     {
#                         "count": 269,
#                         "dt": "2016-06-30T12:00:00Z"
#                     },
#                     {
#                         "count": 357,
#                         "dt": "2016-06-30T13:00:00Z"
#                     },
#                     {
#                         "count": 473,
#                         "dt": "2016-06-30T14:00:00Z"
#                     },
#                     {
#                         "count": 405,
#                         "dt": "2016-06-30T15:00:00Z"
#                     },
#                     {
#                         "count": 415,
#                         "dt": "2016-06-30T16:00:00Z"
#                     },
#                     {
#                         "count": 422,
#                         "dt": "2016-06-30T17:00:00Z"
#                     },
#                     {
#                         "count": 265,
#                         "dt": "2016-06-30T18:00:00Z"
#                     },
#                     {
#                         "count": 365,
#                         "dt": "2016-06-30T19:00:00Z"
#                     },
#                     {
#                         "count": 286,
#                         "dt": "2016-06-30T20:00:00Z"
#                     },
#                     {
#                         "count": 268,
#                         "dt": "2016-06-30T21:00:00Z"
#                     },
#                     {
#                         "count": 325,
#                         "dt": "2016-06-30T22:00:00Z"
#                     },
#                     {
#                         "count": 351,
#                         "dt": "2016-06-30T23:00:00Z"
#                     },
#                     {
#                         "count": 318,
#                         "dt": "2016-07-01T00:00:00Z"
#                     },
#                     {
#                         "count": 489,
#                         "dt": "2016-07-01T01:00:00Z"
#                     },
#                     {
#                         "count": 343,
#                         "dt": "2016-07-01T02:00:00Z"
#                     },
#                     {
#                         "count": 177,
#                         "dt": "2016-07-01T03:00:00Z"
#                     }
#                 ]
#             },
#             {
#                 "_id": "bernieorbust",
#                 "data": [
#                     {
#                         "count": 126,
#                         "dt": "2016-06-28T18:00:00Z"
#                     },
#                     {
#                         "count": 260,
#                         "dt": "2016-06-28T19:00:00Z"
#                     },
#                     {
#                         "count": 191,
#                         "dt": "2016-06-28T20:00:00Z"
#                     },
#                     {
#                         "count": 224,
#                         "dt": "2016-06-28T21:00:00Z"
#                     },
#                     {
#                         "count": 408,
#                         "dt": "2016-06-28T22:00:00Z"
#                     },
#                     {
#                         "count": 112,
#                         "dt": "2016-06-28T23:00:00Z"
#                     },
#                     {
#                         "count": 55,
#                         "dt": "2016-06-29T11:00:00Z"
#                     },
#                     {
#                         "count": 166,
#                         "dt": "2016-06-29T12:00:00Z"
#                     },
#                     {
#                         "count": 212,
#                         "dt": "2016-06-29T13:00:00Z"
#                     },
#                     {
#                         "count": 259,
#                         "dt": "2016-06-29T14:00:00Z"
#                     },
#                     {
#                         "count": 339,
#                         "dt": "2016-06-29T15:00:00Z"
#                     },
#                     {
#                         "count": 229,
#                         "dt": "2016-06-29T16:00:00Z"
#                     },
#                     {
#                         "count": 228,
#                         "dt": "2016-06-29T17:00:00Z"
#                     },
#                     {
#                         "count": 452,
#                         "dt": "2016-06-29T18:00:00Z"
#                     },
#                     {
#                         "count": 354,
#                         "dt": "2016-06-29T19:00:00Z"
#                     },
#                     {
#                         "count": 197,
#                         "dt": "2016-06-29T20:00:00Z"
#                     },
#                     {
#                         "count": 259,
#                         "dt": "2016-06-29T21:00:00Z"
#                     },
#                     {
#                         "count": 212,
#                         "dt": "2016-06-29T22:00:00Z"
#                     },
#                     {
#                         "count": 322,
#                         "dt": "2016-06-29T23:00:00Z"
#                     },
#                     {
#                         "count": 274,
#                         "dt": "2016-06-30T00:00:00Z"
#                     },
#                     {
#                         "count": 305,
#                         "dt": "2016-06-30T01:00:00Z"
#                     },
#                     {
#                         "count": 214,
#                         "dt": "2016-06-30T02:00:00Z"
#                     },
#                     {
#                         "count": 208,
#                         "dt": "2016-06-30T03:00:00Z"
#                     },
#                     {
#                         "count": 175,
#                         "dt": "2016-06-30T04:00:00Z"
#                     },
#                     {
#                         "count": 166,
#                         "dt": "2016-06-30T05:00:00Z"
#                     },
#                     {
#                         "count": 171,
#                         "dt": "2016-06-30T06:00:00Z"
#                     },
#                     {
#                         "count": 90,
#                         "dt": "2016-06-30T07:00:00Z"
#                     },
#                     {
#                         "count": 60,
#                         "dt": "2016-06-30T08:00:00Z"
#                     },
#                     {
#                         "count": 128,
#                         "dt": "2016-06-30T09:00:00Z"
#                     },
#                     {
#                         "count": 150,
#                         "dt": "2016-06-30T10:00:00Z"
#                     },
#                     {
#                         "count": 227,
#                         "dt": "2016-06-30T11:00:00Z"
#                     },
#                     {
#                         "count": 188,
#                         "dt": "2016-06-30T12:00:00Z"
#                     },
#                     {
#                         "count": 232,
#                         "dt": "2016-06-30T13:00:00Z"
#                     },
#                     {
#                         "count": 196,
#                         "dt": "2016-06-30T14:00:00Z"
#                     },
#                     {
#                         "count": 192,
#                         "dt": "2016-06-30T15:00:00Z"
#                     },
#                     {
#                         "count": 210,
#                         "dt": "2016-06-30T16:00:00Z"
#                     },
#                     {
#                         "count": 213,
#                         "dt": "2016-06-30T17:00:00Z"
#                     },
#                     {
#                         "count": 215,
#                         "dt": "2016-06-30T18:00:00Z"
#                     },
#                     {
#                         "count": 184,
#                         "dt": "2016-06-30T19:00:00Z"
#                     },
#                     {
#                         "count": 152,
#                         "dt": "2016-06-30T20:00:00Z"
#                     },
#                     {
#                         "count": 260,
#                         "dt": "2016-06-30T21:00:00Z"
#                     },
#                     {
#                         "count": 300,
#                         "dt": "2016-06-30T22:00:00Z"
#                     },
#                     {
#                         "count": 336,
#                         "dt": "2016-06-30T23:00:00Z"
#                     },
#                     {
#                         "count": 239,
#                         "dt": "2016-07-01T00:00:00Z"
#                     },
#                     {
#                         "count": 236,
#                         "dt": "2016-07-01T01:00:00Z"
#                     },
#                     {
#                         "count": 215,
#                         "dt": "2016-07-01T02:00:00Z"
#                     },
#                     {
#                         "count": 145,
#                         "dt": "2016-07-01T03:00:00Z"
#                     },
#                     {
#                         "count": 1,
#                         "dt": "2016-07-03T19:00:00Z"
#                     }
#                 ]
#             },
#             {
#                 "_id": "americafirst",
#                 "data": [
#                     {
#                         "count": 37,
#                         "dt": "2016-06-28T18:00:00Z"
#                     },
#                     {
#                         "count": 108,
#                         "dt": "2016-06-28T19:00:00Z"
#                     },
#                     {
#                         "count": 160,
#                         "dt": "2016-06-28T20:00:00Z"
#                     },
#                     {
#                         "count": 90,
#                         "dt": "2016-06-28T21:00:00Z"
#                     },
#                     {
#                         "count": 149,
#                         "dt": "2016-06-28T22:00:00Z"
#                     },
#                     {
#                         "count": 196,
#                         "dt": "2016-06-28T23:00:00Z"
#                     },
#                     {
#                         "count": 7,
#                         "dt": "2016-06-29T11:00:00Z"
#                     },
#                     {
#                         "count": 148,
#                         "dt": "2016-06-29T12:00:00Z"
#                     },
#                     {
#                         "count": 318,
#                         "dt": "2016-06-29T13:00:00Z"
#                     },
#                     {
#                         "count": 248,
#                         "dt": "2016-06-29T14:00:00Z"
#                     },
#                     {
#                         "count": 186,
#                         "dt": "2016-06-29T15:00:00Z"
#                     },
#                     {
#                         "count": 134,
#                         "dt": "2016-06-29T16:00:00Z"
#                     },
#                     {
#                         "count": 180,
#                         "dt": "2016-06-29T17:00:00Z"
#                     },
#                     {
#                         "count": 133,
#                         "dt": "2016-06-29T18:00:00Z"
#                     },
#                     {
#                         "count": 74,
#                         "dt": "2016-06-29T19:00:00Z"
#                     },
#                     {
#                         "count": 59,
#                         "dt": "2016-06-29T20:00:00Z"
#                     },
#                     {
#                         "count": 78,
#                         "dt": "2016-06-29T21:00:00Z"
#                     },
#                     {
#                         "count": 77,
#                         "dt": "2016-06-29T22:00:00Z"
#                     },
#                     {
#                         "count": 286,
#                         "dt": "2016-06-29T23:00:00Z"
#                     },
#                     {
#                         "count": 94,
#                         "dt": "2016-06-30T00:00:00Z"
#                     },
#                     {
#                         "count": 51,
#                         "dt": "2016-06-30T01:00:00Z"
#                     },
#                     {
#                         "count": 87,
#                         "dt": "2016-06-30T02:00:00Z"
#                     },
#                     {
#                         "count": 33,
#                         "dt": "2016-06-30T03:00:00Z"
#                     },
#                     {
#                         "count": 30,
#                         "dt": "2016-06-30T04:00:00Z"
#                     },
#                     {
#                         "count": 15,
#                         "dt": "2016-06-30T05:00:00Z"
#                     },
#                     {
#                         "count": 12,
#                         "dt": "2016-06-30T06:00:00Z"
#                     },
#                     {
#                         "count": 8,
#                         "dt": "2016-06-30T07:00:00Z"
#                     },
#                     {
#                         "count": 11,
#                         "dt": "2016-06-30T08:00:00Z"
#                     },
#                     {
#                         "count": 7,
#                         "dt": "2016-06-30T09:00:00Z"
#                     },
#                     {
#                         "count": 13,
#                         "dt": "2016-06-30T10:00:00Z"
#                     },
#                     {
#                         "count": 13,
#                         "dt": "2016-06-30T11:00:00Z"
#                     },
#                     {
#                         "count": 21,
#                         "dt": "2016-06-30T12:00:00Z"
#                     },
#                     {
#                         "count": 111,
#                         "dt": "2016-06-30T13:00:00Z"
#                     },
#                     {
#                         "count": 196,
#                         "dt": "2016-06-30T14:00:00Z"
#                     },
#                     {
#                         "count": 174,
#                         "dt": "2016-06-30T15:00:00Z"
#                     },
#                     {
#                         "count": 195,
#                         "dt": "2016-06-30T16:00:00Z"
#                     },
#                     {
#                         "count": 211,
#                         "dt": "2016-06-30T17:00:00Z"
#                     },
#                     {
#                         "count": 106,
#                         "dt": "2016-06-30T18:00:00Z"
#                     },
#                     {
#                         "count": 147,
#                         "dt": "2016-06-30T19:00:00Z"
#                     },
#                     {
#                         "count": 84,
#                         "dt": "2016-06-30T20:00:00Z"
#                     },
#                     {
#                         "count": 110,
#                         "dt": "2016-06-30T21:00:00Z"
#                     },
#                     {
#                         "count": 123,
#                         "dt": "2016-06-30T22:00:00Z"
#                     },
#                     {
#                         "count": 273,
#                         "dt": "2016-06-30T23:00:00Z"
#                     },
#                     {
#                         "count": 143,
#                         "dt": "2016-07-01T00:00:00Z"
#                     },
#                     {
#                         "count": 102,
#                         "dt": "2016-07-01T01:00:00Z"
#                     },
#                     {
#                         "count": 90,
#                         "dt": "2016-07-01T02:00:00Z"
#                     },
#                     {
#                         "count": 67,
#                         "dt": "2016-07-01T03:00:00Z"
#                     }
#                 ]
#             },
#             {
#                 "_id": "stillsanders",
#                 "data": [
#                     {
#                         "count": 84,
#                         "dt": "2016-06-28T18:00:00Z"
#                     },
#                     {
#                         "count": 145,
#                         "dt": "2016-06-28T19:00:00Z"
#                     },
#                     {
#                         "count": 110,
#                         "dt": "2016-06-28T20:00:00Z"
#                     },
#                     {
#                         "count": 243,
#                         "dt": "2016-06-28T21:00:00Z"
#                     },
#                     {
#                         "count": 330,
#                         "dt": "2016-06-28T22:00:00Z"
#                     },
#                     {
#                         "count": 100,
#                         "dt": "2016-06-28T23:00:00Z"
#                     },
#                     {
#                         "count": 51,
#                         "dt": "2016-06-29T11:00:00Z"
#                     },
#                     {
#                         "count": 90,
#                         "dt": "2016-06-29T12:00:00Z"
#                     },
#                     {
#                         "count": 109,
#                         "dt": "2016-06-29T13:00:00Z"
#                     },
#                     {
#                         "count": 136,
#                         "dt": "2016-06-29T14:00:00Z"
#                     },
#                     {
#                         "count": 205,
#                         "dt": "2016-06-29T15:00:00Z"
#                     },
#                     {
#                         "count": 157,
#                         "dt": "2016-06-29T16:00:00Z"
#                     },
#                     {
#                         "count": 139,
#                         "dt": "2016-06-29T17:00:00Z"
#                     },
#                     {
#                         "count": 290,
#                         "dt": "2016-06-29T18:00:00Z"
#                     },
#                     {
#                         "count": 229,
#                         "dt": "2016-06-29T19:00:00Z"
#                     },
#                     {
#                         "count": 162,
#                         "dt": "2016-06-29T20:00:00Z"
#                     },
#                     {
#                         "count": 216,
#                         "dt": "2016-06-29T21:00:00Z"
#                     },
#                     {
#                         "count": 194,
#                         "dt": "2016-06-29T22:00:00Z"
#                     },
#                     {
#                         "count": 295,
#                         "dt": "2016-06-29T23:00:00Z"
#                     },
#                     {
#                         "count": 199,
#                         "dt": "2016-06-30T00:00:00Z"
#                     },
#                     {
#                         "count": 221,
#                         "dt": "2016-06-30T01:00:00Z"
#                     },
#                     {
#                         "count": 121,
#                         "dt": "2016-06-30T02:00:00Z"
#                     },
#                     {
#                         "count": 113,
#                         "dt": "2016-06-30T03:00:00Z"
#                     },
#                     {
#                         "count": 104,
#                         "dt": "2016-06-30T04:00:00Z"
#                     },
#                     {
#                         "count": 138,
#                         "dt": "2016-06-30T05:00:00Z"
#                     },
#                     {
#                         "count": 152,
#                         "dt": "2016-06-30T06:00:00Z"
#                     },
#                     {
#                         "count": 79,
#                         "dt": "2016-06-30T07:00:00Z"
#                     },
#                     {
#                         "count": 33,
#                         "dt": "2016-06-30T08:00:00Z"
#                     },
#                     {
#                         "count": 99,
#                         "dt": "2016-06-30T09:00:00Z"
#                     },
#                     {
#                         "count": 108,
#                         "dt": "2016-06-30T10:00:00Z"
#                     },
#                     {
#                         "count": 98,
#                         "dt": "2016-06-30T11:00:00Z"
#                     },
#                     {
#                         "count": 70,
#                         "dt": "2016-06-30T12:00:00Z"
#                     },
#                     {
#                         "count": 115,
#                         "dt": "2016-06-30T13:00:00Z"
#                     },
#                     {
#                         "count": 119,
#                         "dt": "2016-06-30T14:00:00Z"
#                     },
#                     {
#                         "count": 71,
#                         "dt": "2016-06-30T15:00:00Z"
#                     },
#                     {
#                         "count": 179,
#                         "dt": "2016-06-30T16:00:00Z"
#                     },
#                     {
#                         "count": 206,
#                         "dt": "2016-06-30T17:00:00Z"
#                     },
#                     {
#                         "count": 140,
#                         "dt": "2016-06-30T18:00:00Z"
#                     },
#                     {
#                         "count": 147,
#                         "dt": "2016-06-30T19:00:00Z"
#                     },
#                     {
#                         "count": 149,
#                         "dt": "2016-06-30T20:00:00Z"
#                     },
#                     {
#                         "count": 231,
#                         "dt": "2016-06-30T21:00:00Z"
#                     },
#                     {
#                         "count": 200,
#                         "dt": "2016-06-30T22:00:00Z"
#                     },
#                     {
#                         "count": 219,
#                         "dt": "2016-06-30T23:00:00Z"
#                     },
#                     {
#                         "count": 163,
#                         "dt": "2016-07-01T00:00:00Z"
#                     },
#                     {
#                         "count": 200,
#                         "dt": "2016-07-01T01:00:00Z"
#                     },
#                     {
#                         "count": 220,
#                         "dt": "2016-07-01T02:00:00Z"
#                     },
#                     {
#                         "count": 93,
#                         "dt": "2016-07-01T03:00:00Z"
#                     }
#                 ]
#             },
#             {
#                 "_id": "trumptrain",
#                 "data": [
#                     {
#                         "count": 62,
#                         "dt": "2016-06-28T18:00:00Z"
#                     },
#                     {
#                         "count": 124,
#                         "dt": "2016-06-28T19:00:00Z"
#                     },
#                     {
#                         "count": 121,
#                         "dt": "2016-06-28T20:00:00Z"
#                     },
#                     {
#                         "count": 108,
#                         "dt": "2016-06-28T21:00:00Z"
#                     },
#                     {
#                         "count": 208,
#                         "dt": "2016-06-28T22:00:00Z"
#                     },
#                     {
#                         "count": 83,
#                         "dt": "2016-06-28T23:00:00Z"
#                     },
#                     {
#                         "count": 39,
#                         "dt": "2016-06-29T11:00:00Z"
#                     },
#                     {
#                         "count": 179,
#                         "dt": "2016-06-29T12:00:00Z"
#                     },
#                     {
#                         "count": 232,
#                         "dt": "2016-06-29T13:00:00Z"
#                     },
#                     {
#                         "count": 228,
#                         "dt": "2016-06-29T14:00:00Z"
#                     },
#                     {
#                         "count": 178,
#                         "dt": "2016-06-29T15:00:00Z"
#                     },
#                     {
#                         "count": 161,
#                         "dt": "2016-06-29T16:00:00Z"
#                     },
#                     {
#                         "count": 212,
#                         "dt": "2016-06-29T17:00:00Z"
#                     },
#                     {
#                         "count": 233,
#                         "dt": "2016-06-29T18:00:00Z"
#                     },
#                     {
#                         "count": 160,
#                         "dt": "2016-06-29T19:00:00Z"
#                     },
#                     {
#                         "count": 112,
#                         "dt": "2016-06-29T20:00:00Z"
#                     },
#                     {
#                         "count": 213,
#                         "dt": "2016-06-29T21:00:00Z"
#                     },
#                     {
#                         "count": 344,
#                         "dt": "2016-06-29T22:00:00Z"
#                     },
#                     {
#                         "count": 309,
#                         "dt": "2016-06-29T23:00:00Z"
#                     },
#                     {
#                         "count": 191,
#                         "dt": "2016-06-30T00:00:00Z"
#                     },
#                     {
#                         "count": 223,
#                         "dt": "2016-06-30T01:00:00Z"
#                     },
#                     {
#                         "count": 203,
#                         "dt": "2016-06-30T02:00:00Z"
#                     },
#                     {
#                         "count": 180,
#                         "dt": "2016-06-30T03:00:00Z"
#                     },
#                     {
#                         "count": 278,
#                         "dt": "2016-06-30T04:00:00Z"
#                     },
#                     {
#                         "count": 230,
#                         "dt": "2016-06-30T05:00:00Z"
#                     },
#                     {
#                         "count": 122,
#                         "dt": "2016-06-30T06:00:00Z"
#                     },
#                     {
#                         "count": 106,
#                         "dt": "2016-06-30T07:00:00Z"
#                     },
#                     {
#                         "count": 116,
#                         "dt": "2016-06-30T08:00:00Z"
#                     },
#                     {
#                         "count": 91,
#                         "dt": "2016-06-30T09:00:00Z"
#                     },
#                     {
#                         "count": 73,
#                         "dt": "2016-06-30T10:00:00Z"
#                     },
#                     {
#                         "count": 105,
#                         "dt": "2016-06-30T11:00:00Z"
#                     },
#                     {
#                         "count": 119,
#                         "dt": "2016-06-30T12:00:00Z"
#                     },
#                     {
#                         "count": 203,
#                         "dt": "2016-06-30T13:00:00Z"
#                     },
#                     {
#                         "count": 265,
#                         "dt": "2016-06-30T14:00:00Z"
#                     },
#                     {
#                         "count": 140,
#                         "dt": "2016-06-30T15:00:00Z"
#                     },
#                     {
#                         "count": 150,
#                         "dt": "2016-06-30T16:00:00Z"
#                     },
#                     {
#                         "count": 128,
#                         "dt": "2016-06-30T17:00:00Z"
#                     },
#                     {
#                         "count": 122,
#                         "dt": "2016-06-30T18:00:00Z"
#                     },
#                     {
#                         "count": 131,
#                         "dt": "2016-06-30T19:00:00Z"
#                     },
#                     {
#                         "count": 112,
#                         "dt": "2016-06-30T20:00:00Z"
#                     },
#                     {
#                         "count": 120,
#                         "dt": "2016-06-30T21:00:00Z"
#                     },
#                     {
#                         "count": 398,
#                         "dt": "2016-06-30T22:00:00Z"
#                     },
#                     {
#                         "count": 325,
#                         "dt": "2016-06-30T23:00:00Z"
#                     },
#                     {
#                         "count": 208,
#                         "dt": "2016-07-01T00:00:00Z"
#                     },
#                     {
#                         "count": 217,
#                         "dt": "2016-07-01T01:00:00Z"
#                     },
#                     {
#                         "count": 207,
#                         "dt": "2016-07-01T02:00:00Z"
#                     },
#                     {
#                         "count": 112,
#                         "dt": "2016-07-01T03:00:00Z"
#                     }
#                 ]
#             },
#             {
#                 "_id": "feelthebern",
#                 "data": [
#                     {
#                         "count": 724,
#                         "dt": "2016-06-28T18:00:00Z"
#                     },
#                     {
#                         "count": 1265,
#                         "dt": "2016-06-28T19:00:00Z"
#                     },
#                     {
#                         "count": 1047,
#                         "dt": "2016-06-28T20:00:00Z"
#                     },
#                     {
#                         "count": 2326,
#                         "dt": "2016-06-28T21:00:00Z"
#                     },
#                     {
#                         "count": 1832,
#                         "dt": "2016-06-28T22:00:00Z"
#                     },
#                     {
#                         "count": 568,
#                         "dt": "2016-06-28T23:00:00Z"
#                     },
#                     {
#                         "count": 263,
#                         "dt": "2016-06-29T11:00:00Z"
#                     },
#                     {
#                         "count": 715,
#                         "dt": "2016-06-29T12:00:00Z"
#                     },
#                     {
#                         "count": 824,
#                         "dt": "2016-06-29T13:00:00Z"
#                     },
#                     {
#                         "count": 1072,
#                         "dt": "2016-06-29T14:00:00Z"
#                     },
#                     {
#                         "count": 995,
#                         "dt": "2016-06-29T15:00:00Z"
#                     },
#                     {
#                         "count": 955,
#                         "dt": "2016-06-29T16:00:00Z"
#                     },
#                     {
#                         "count": 852,
#                         "dt": "2016-06-29T17:00:00Z"
#                     },
#                     {
#                         "count": 1108,
#                         "dt": "2016-06-29T18:00:00Z"
#                     },
#                     {
#                         "count": 983,
#                         "dt": "2016-06-29T19:00:00Z"
#                     },
#                     {
#                         "count": 916,
#                         "dt": "2016-06-29T20:00:00Z"
#                     },
#                     {
#                         "count": 893,
#                         "dt": "2016-06-29T21:00:00Z"
#                     },
#                     {
#                         "count": 739,
#                         "dt": "2016-06-29T22:00:00Z"
#                     },
#                     {
#                         "count": 964,
#                         "dt": "2016-06-29T23:00:00Z"
#                     },
#                     {
#                         "count": 968,
#                         "dt": "2016-06-30T00:00:00Z"
#                     },
#                     {
#                         "count": 890,
#                         "dt": "2016-06-30T01:00:00Z"
#                     },
#                     {
#                         "count": 913,
#                         "dt": "2016-06-30T02:00:00Z"
#                     },
#                     {
#                         "count": 753,
#                         "dt": "2016-06-30T03:00:00Z"
#                     },
#                     {
#                         "count": 622,
#                         "dt": "2016-06-30T04:00:00Z"
#                     },
#                     {
#                         "count": 511,
#                         "dt": "2016-06-30T05:00:00Z"
#                     },
#                     {
#                         "count": 480,
#                         "dt": "2016-06-30T06:00:00Z"
#                     },
#                     {
#                         "count": 372,
#                         "dt": "2016-06-30T07:00:00Z"
#                     },
#                     {
#                         "count": 278,
#                         "dt": "2016-06-30T08:00:00Z"
#                     },
#                     {
#                         "count": 356,
#                         "dt": "2016-06-30T09:00:00Z"
#                     },
#                     {
#                         "count": 432,
#                         "dt": "2016-06-30T10:00:00Z"
#                     },
#                     {
#                         "count": 525,
#                         "dt": "2016-06-30T11:00:00Z"
#                     },
#                     {
#                         "count": 543,
#                         "dt": "2016-06-30T12:00:00Z"
#                     },
#                     {
#                         "count": 700,
#                         "dt": "2016-06-30T13:00:00Z"
#                     },
#                     {
#                         "count": 763,
#                         "dt": "2016-06-30T14:00:00Z"
#                     },
#                     {
#                         "count": 736,
#                         "dt": "2016-06-30T15:00:00Z"
#                     },
#                     {
#                         "count": 835,
#                         "dt": "2016-06-30T16:00:00Z"
#                     },
#                     {
#                         "count": 909,
#                         "dt": "2016-06-30T17:00:00Z"
#                     },
#                     {
#                         "count": 851,
#                         "dt": "2016-06-30T18:00:00Z"
#                     },
#                     {
#                         "count": 900,
#                         "dt": "2016-06-30T19:00:00Z"
#                     },
#                     {
#                         "count": 679,
#                         "dt": "2016-06-30T20:00:00Z"
#                     },
#                     {
#                         "count": 783,
#                         "dt": "2016-06-30T21:00:00Z"
#                     },
#                     {
#                         "count": 940,
#                         "dt": "2016-06-30T22:00:00Z"
#                     },
#                     {
#                         "count": 931,
#                         "dt": "2016-06-30T23:00:00Z"
#                     },
#                     {
#                         "count": 925,
#                         "dt": "2016-07-01T00:00:00Z"
#                     },
#                     {
#                         "count": 968,
#                         "dt": "2016-07-01T01:00:00Z"
#                     },
#                     {
#                         "count": 853,
#                         "dt": "2016-07-01T02:00:00Z"
#                     },
#                     {
#                         "count": 571,
#                         "dt": "2016-07-01T03:00:00Z"
#                     },
#                     {
#                         "count": 1,
#                         "dt": "2016-07-01T08:00:00Z"
#                     }
#                 ]
#             },
#             {
#                 "_id": "imwithher",
#                 "data": [
#                     {
#                         "count": 582,
#                         "dt": "2016-06-28T18:00:00Z"
#                     },
#                     {
#                         "count": 1401,
#                         "dt": "2016-06-28T19:00:00Z"
#                     },
#                     {
#                         "count": 1343,
#                         "dt": "2016-06-28T20:00:00Z"
#                     },
#                     {
#                         "count": 2645,
#                         "dt": "2016-06-28T21:00:00Z"
#                     },
#                     {
#                         "count": 1843,
#                         "dt": "2016-06-28T22:00:00Z"
#                     },
#                     {
#                         "count": 597,
#                         "dt": "2016-06-28T23:00:00Z"
#                     },
#                     {
#                         "count": 288,
#                         "dt": "2016-06-29T11:00:00Z"
#                     },
#                     {
#                         "count": 692,
#                         "dt": "2016-06-29T12:00:00Z"
#                     },
#                     {
#                         "count": 705,
#                         "dt": "2016-06-29T13:00:00Z"
#                     },
#                     {
#                         "count": 873,
#                         "dt": "2016-06-29T14:00:00Z"
#                     },
#                     {
#                         "count": 1036,
#                         "dt": "2016-06-29T15:00:00Z"
#                     },
#                     {
#                         "count": 1248,
#                         "dt": "2016-06-29T16:00:00Z"
#                     },
#                     {
#                         "count": 2307,
#                         "dt": "2016-06-29T17:00:00Z"
#                     },
#                     {
#                         "count": 1332,
#                         "dt": "2016-06-29T18:00:00Z"
#                     },
#                     {
#                         "count": 1412,
#                         "dt": "2016-06-29T19:00:00Z"
#                     },
#                     {
#                         "count": 1239,
#                         "dt": "2016-06-29T20:00:00Z"
#                     },
#                     {
#                         "count": 1201,
#                         "dt": "2016-06-29T21:00:00Z"
#                     },
#                     {
#                         "count": 1304,
#                         "dt": "2016-06-29T22:00:00Z"
#                     },
#                     {
#                         "count": 1411,
#                         "dt": "2016-06-29T23:00:00Z"
#                     },
#                     {
#                         "count": 1524,
#                         "dt": "2016-06-30T00:00:00Z"
#                     },
#                     {
#                         "count": 1685,
#                         "dt": "2016-06-30T01:00:00Z"
#                     },
#                     {
#                         "count": 2202,
#                         "dt": "2016-06-30T02:00:00Z"
#                     },
#                     {
#                         "count": 1096,
#                         "dt": "2016-06-30T03:00:00Z"
#                     },
#                     {
#                         "count": 984,
#                         "dt": "2016-06-30T04:00:00Z"
#                     },
#                     {
#                         "count": 431,
#                         "dt": "2016-06-30T05:00:00Z"
#                     },
#                     {
#                         "count": 368,
#                         "dt": "2016-06-30T06:00:00Z"
#                     },
#                     {
#                         "count": 252,
#                         "dt": "2016-06-30T07:00:00Z"
#                     },
#                     {
#                         "count": 152,
#                         "dt": "2016-06-30T08:00:00Z"
#                     },
#                     {
#                         "count": 213,
#                         "dt": "2016-06-30T09:00:00Z"
#                     },
#                     {
#                         "count": 314,
#                         "dt": "2016-06-30T10:00:00Z"
#                     },
#                     {
#                         "count": 477,
#                         "dt": "2016-06-30T11:00:00Z"
#                     },
#                     {
#                         "count": 567,
#                         "dt": "2016-06-30T12:00:00Z"
#                     },
#                     {
#                         "count": 773,
#                         "dt": "2016-06-30T13:00:00Z"
#                     },
#                     {
#                         "count": 701,
#                         "dt": "2016-06-30T14:00:00Z"
#                     },
#                     {
#                         "count": 814,
#                         "dt": "2016-06-30T15:00:00Z"
#                     },
#                     {
#                         "count": 857,
#                         "dt": "2016-06-30T16:00:00Z"
#                     },
#                     {
#                         "count": 943,
#                         "dt": "2016-06-30T17:00:00Z"
#                     },
#                     {
#                         "count": 927,
#                         "dt": "2016-06-30T18:00:00Z"
#                     },
#                     {
#                         "count": 934,
#                         "dt": "2016-06-30T19:00:00Z"
#                     },
#                     {
#                         "count": 1033,
#                         "dt": "2016-06-30T20:00:00Z"
#                     },
#                     {
#                         "count": 1081,
#                         "dt": "2016-06-30T21:00:00Z"
#                     },
#                     {
#                         "count": 1192,
#                         "dt": "2016-06-30T22:00:00Z"
#                     },
#                     {
#                         "count": 905,
#                         "dt": "2016-06-30T23:00:00Z"
#                     },
#                     {
#                         "count": 1085,
#                         "dt": "2016-07-01T00:00:00Z"
#                     },
#                     {
#                         "count": 1257,
#                         "dt": "2016-07-01T01:00:00Z"
#                     },
#                     {
#                         "count": 1119,
#                         "dt": "2016-07-01T02:00:00Z"
#                     },
#                     {
#                         "count": 615,
#                         "dt": "2016-07-01T03:00:00Z"
#                     },
#                     {
#                         "count": 3,
#                         "dt": "2016-07-01T08:00:00Z"
#                     },
#                     {
#                         "count": 1,
#                         "dt": "2016-07-03T19:00:00Z"
#                     }
#                 ]
#             }
#         ]
#     },
#     "details": {
#         "chartType": "time",
#         "xLabel": "Date (UTC)",
#         "yLabel": "Tweets per minute",
#         "title":"Blah"
#     }
# }
#
# TimeChart(d,None)

#
# d = {
#     "data": [
#         {
#             "_id": "imwithher",
#             "count": 47964
#         },
#         {
#             "_id": "feelthebern",
#             "count": 39029
#         },
#         {
#             "_id": "makeamericagreatagain",
#             "count": 36757
#         },
#         {
#             "_id": "trump2016",
#             "count": 17056
#         },
#         {
#             "_id": "bernieorbust",
#             "count": 10287
#         },
#         {
#             "_id": "trumptrain",
#             "count": 8181
#         },
#         {
#             "_id": "neverhillary",
#             "count": 7692
#         },
#         {
#             "_id": "stillsanders",
#             "count": 7272
#         },
#         {
#             "_id": "stoptpp",
#             "count": 5530
#         },
#         {
#             "_id": "americafirst",
#             "count": 5195
#         }
#     ],
#     "details": {
#         "chartType": "bar",
#         "xLabel":"Number of Occurences",
#         "title":"Top Hashtags"
#     }
# }