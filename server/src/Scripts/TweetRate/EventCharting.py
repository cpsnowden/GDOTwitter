import json
import logging
import os
from string import Template

import numpy as np
from dateutil import parser

import AnalysisEngine.Util

DIR_NAME = os.path.dirname(__file__)
logger = logging.getLogger(__name__)
from AnalysisEngine.EventDetection import Event
from datetime import datetime

def get_html(data_source, type, width="100%", height="100%"):
    default_chart_properties = {
        "bgColor": "#000000,#000000",
        "captionHorizontalPadding": "2",
        "captionOnTop": "0",
        "captionAlignment": "right",
        "canvasBgAlpha": "0",
        "bgAlpha": "100",
        "theme": "fint",
        "exportEnabled": "1",
        "captionFont": "Verdana",
        "captionFontSize": "30",
        "captionFontColor": "#FFFFFF",
        "captionFontBold": "1",
        "subcaptionFont": "Verdana",
        "subcaptionFontSize": "25",
        "subcaptionFontColor": "#FFFFFF",
        "subcaptionFontBold": "0",
        "baseFont": "Verdana",
        "baseFontSize": "20",
        "baseFontColor": "#FFFFFF",
        "plotFillAlpha": "50",
        "plotHighlightEffect": "fadeout",
        "legendItemFontSize": "20",
        "legendItemFontColor": "#666666",
    }
    if "chart" not in data_source:
        data_source["chart"] = {}
    for property in default_chart_properties:
        if property not in data_source["chart"]:
            data_source["chart"][property] = default_chart_properties[property]

    logger.info("Using chart format: " + str(data_source["chart"]))

    s = Template(open(os.path.join(DIR_NAME, "Templates", "Chart.html")).read())
    return s.safe_substitute({'dataSource': json.dumps(data_source, default=AnalysisEngine.Util.date_encoder),
                              "height": height,
                              "width": width,
                              "type": type})


def get_event_chart(data, events):
    properties = {
        "drawAnchors" : 0,
        "labelStep" : 24*14,
        "slantLabels" : "1",
        "showValues" : "0",
        "showTickMarks":"1"
    }

    values = [{"label": i[0], "value":i[1]} for i in data]

    x_categories_parsed = {parser.parse(i[0]).replace(tzinfo=None):j for j,i in enumerate(data)}

    annotations = {"autoscale": "1",
                   "groups": []}
    v_trend_line = {"line": []}

    for event in events:
        annotations["groups"].append(make_annotation(event, x_categories_parsed))
        v_trend_line["line"].append(make_trend_line(event, x_categories_parsed))

    return get_html({"chart": properties,
                     "data": values,
                     "annotations": annotations,
                     "vtrendlines": v_trend_line}, "line")

def make_trend_line(event, datetime_to_index):

    start_index = datetime_to_index[event.start]
    end_index = datetime_to_index[event.end]

    zone = {
        "startValue": start_index,
        "endValue": end_index,
        "isTrendZone": "1",
        "color": "#FFFFFF",
        "alpha": "10",
        "displayValue": " ",
    }

    return zone


def make_annotation(event, datetime_to_index):

    start_index = datetime_to_index[event.start]
    end_index = datetime_to_index[event.end]
    label = event.get_chart_label()

    start_line_annotation = {
        "id": "end_high-line",
        "type": "line",
        "y": "$canvasStartY",
        "x": "$dataset.0.set." + str(start_index) + ".x",
        "toy": "$canvasEndY",
        "tox": "$dataset.0.set." + str(start_index) + ".x",
        "color": "#6baa01",
        "dashed": "1",
        "thickness": "1",
    }
    end_line_annotation = {
        "id": "start_high-line",
        "type": "line",
        "y": "$canvasStartY",
        "x": "$dataset.0.set." + str(end_index) + ".x",
        "toy": "$canvasEndY",
        "tox": "$dataset.0.set." + str(end_index) + ".x",
        "color": "#6baa01",
        "dashed": "1",
        "thickness": "1",
    }
    label_annotation = {
        "id": "dyn-label",
        "type": "text",
        "text": label,
        "wrap": 1,
        "wrapWidth": 100,
        "fillcolor": "#ffffff",
        "fontsize": "7",
        "x": "$dataset.0.set." + str(int(np.mean([start_index, end_index]))) + ".x",
        "y": "$canvasStartY",
        "bgColor": '#0075c2'
    }

    return {"items":[start_line_annotation, end_line_annotation,label_annotation]}


if __name__ == "__main__":
    dt = json.load(open("Untitled.json"))

    e = Event(datetime(2016,02,19,15,0,0), datetime(2016,02,20,15,0,0))

    e.guardian_titles = ["Sample 1", "Sample 2"]
    e.top_words = ["TW1", "TW2"]

    e2 = Event(datetime(2016,03,19,15,0,0), datetime(2016,03,20,15,0,0))
    e2.guardian_titles = ["Sample 1", "Sample 2"]
    e2.top_words = ["TW1", "TW2"]

    html = get_event_chart(dt, [e, e2])
    with open("out.html", "w") as f:
        f.write(html)


