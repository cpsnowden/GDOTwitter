import json
import logging
import os
from collections import OrderedDict
from string import Template
import copy
import AnalysisEngine.Util
import numpy as np

DIR_NAME = os.path.dirname(__file__)
logger = logging.getLogger(__name__)


def add_default_properties(properties):
    default_chart_properties = {
        "bgColor": "#000000,#000000",
        "captionHorizontalPadding": "2",
        "captionOnTop": "0",
        "captionAlignment": "right",
        "canvasBgAlpha": "0",
        "bgAlpha": "100",
        "theme": "fint",
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
    for property in default_chart_properties:
        if property not in properties:
            properties[property] = default_chart_properties[property]

    return properties


def create_time_graph(data, properties, chartType):
    x_categories = [{"label": i} for i in data["categories"]]
    values = OrderedDict.fromkeys(data["categories"], 0)
    series = []
    for s in data["values"]:
        for entry in s["data"]:
            values[entry["dt"]] = entry["count"]
        series.append({"seriesname": s["_id"], "data": [{"value": j} for (i, j) in values.items()]})
        values = OrderedDict.fromkeys(data["categories"], 0)

    properties["drawAnchors"] = 0
    properties["slantLabels"] = 1
    properties["showValues"] = "0"

    return {"dataSource": {"chart": add_default_properties(properties),
                           "dataset": series,
                           "categories": {"category": x_categories}},
            "chartType": chartType}


def create_pie_chart(data, properties, chartType):
    properties["startingAngle"] = "310"
    properties["decimals"] = "0"
    properties["showLegend"] = "1"
    properties["labelFontColor"] = "#FFFFFF"
    properties["labelFontSize"] = "20"
    properties["centerLabelColor"] = "#FFFFFF"
    properties["centerLabelFontSize"] = "30"
    properties["enableRotation"] = "0"

    return {"dataSource": {"chart": add_default_properties(properties),
                           "data": [{"label": i["_id"],
                                     "value": i["count"]} for i in data]},
            "chartType": chartType}


def create_ranking_chart(data, properties, chartType):

    return {"dataSource": {"chart": add_default_properties(properties),
                           "data": [{"label": i["_id"],
                                     "value": i["count"]} for i in data]},
            "chartType": chartType}


def create_event_chart(data, properties, chartType):

    properties["drawAnchors"] = 0
    properties["slantLabels"] = "1"
    properties["showValues"] = "0"
    properties["showTickMarks"] = "1"
    properties["chartTopMargin"] = 300
    properties["chartBottomMargin"] = 180
    properties["captionAlignment"] = "left"

    values = [{"label": i[0], "value": i[1]} for i in data["series"]]
    x_categories_parsed = {i[0].replace(tzinfo=None): j for j, i in enumerate(data["series"])}

    annotations = {"autoscale": "1",
                   "groups": []}
    v_trend_line = {"line": []}

    for i, event in enumerate(data["events"]):
        annotations["groups"].append(make_annotation(event, x_categories_parsed, divmod(i, 4)[1]))
        v_trend_line["line"].append(make_trend_line(event, x_categories_parsed))

    return {"dataSource":{"chart": add_default_properties(properties),
                          "data": values,
                          "annotations": annotations,
                          "vtrendlines": v_trend_line},
            "chartType": chartType}

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


def make_annotation(event, datetime_to_index, cycle):
    start_index = datetime_to_index[event.start]
    end_index = datetime_to_index[event.end]
    label = event.get_chart_label()

    top_top = -305
    top_bottom = -5
    bottom_top = 30
    bottom_bottom = 330

    default = {
        "id": "end_high-line",
        "type": "line",
        "color": "#6baa01",
        "dashed": "1",
        "thickness": "1"
    }

    start_line_annotation = copy.deepcopy(default)
    start_line_annotation["y"] = "$canvasStartY"
    start_line_annotation["x"] = "$dataset.0.set." + str(start_index) + ".x"
    start_line_annotation["toy"] = "$canvasEndY"
    start_line_annotation["tox"] = "$dataset.0.set." + str(start_index) + ".x"
    end_line_annotation = copy.deepcopy(default)
    end_line_annotation["y"] = "$canvasStartY"
    end_line_annotation["x"] = "$dataset.0.set." + str(end_index) + ".x"
    end_line_annotation["toy"] = "$canvasEndY"
    end_line_annotation["tox"] = "$dataset.0.set." + str(end_index) + ".x"

    label_annotation = {
        "id": "dyn-label",
        "type": "text",
        "text": label,
        "wrap": 1,
        "wrapWidth": 200,
        "fillcolor": "#ffffff",
        "fontsize": "12",
        "x": "$dataset.0.set." + str(int(np.mean([start_index, end_index]))) + ".x",
        "y": "$canvasStartY",
        "bgColor": '#0075c2',
        "wrapHeight": 140
    }

    if cycle == 0:
        start_line_annotation["y"] +=  str(top_top)
        end_line_annotation["y"] +=  str(top_top)
        label_annotation["y"] +=  str(top_top)
        label_annotation["vAlign"] = "bottom"
    elif cycle == 1:
        start_line_annotation["y"] +=  str(top_bottom)
        end_line_annotation["y"] +=  str(top_bottom)
        label_annotation["y"] +=  str(top_bottom)
        label_annotation["vAlign"] = "top"
    elif cycle == 2:
        start_line_annotation["toy"] = "$canvasEndY + " + str(bottom_top)
        end_line_annotation["toy"] = "$canvasEndY + " + str(bottom_top)
        label_annotation["y"] = "$canvasEndY + " + str(bottom_top)
        label_annotation["vAlign"] = "bottom"
    elif cycle == 3:
        start_line_annotation["toy"] = "$canvasEndY + " + str(bottom_bottom)
        end_line_annotation["toy"] = "$canvasEndY + " + str(bottom_bottom)
        label_annotation["y"] = "$canvasEndY + " + str(bottom_bottom)
        label_annotation["vAlign"] = "top"

    return {"items": [start_line_annotation, end_line_annotation, label_annotation]}


def get_fusion_html(data_source, type, width="100%", height="100%"):

    s = Template(open(os.path.join(DIR_NAME, "Templates", "Chart.html")).read())
    return s.safe_substitute({'dataSource': json.dumps(data_source, default=AnalysisEngine.Util.date_encoder),
                              "height": height,
                              "width": width,
                              "type": type})


def get_fusion_chart_data(data, properties, analysisType ,chartType):

    options = {
        "time": create_time_graph,
        "ranking": create_ranking_chart,
        "proportion": create_pie_chart,
        "event": create_event_chart,
    }

    return options[analysisType](data, properties, chartType)


if __name__ == "__main__":
    html = None
    with open("out.html", "w") as f:
        f.write(html)
