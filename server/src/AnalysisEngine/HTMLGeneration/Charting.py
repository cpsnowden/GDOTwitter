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


def create_time_graph(chart_data):
    x_categories = [{"label": i} for i in chart_data["data"]["categories"]]
    values = OrderedDict.fromkeys(chart_data["data"]["categories"], 0)

    series = []
    for s in chart_data["data"]["values"]:
        for entry in s["data"]:
            values[entry["dt"]] = entry["count"]
        series.append({"seriesname": s["_id"], "data": [{"value": j} for (i, j) in values.items()]})
        values = OrderedDict.fromkeys(chart_data["data"]["categories"], 0)

    chart_data["details"]["chartProperties"]["drawAnchors"] = 0
    # chart_data["details"]["chartProperties"]["labelStep"] = 6
    chart_data["details"]["chartProperties"]["slantLabels"] = 1
    chart_data["details"]["chartProperties"]["showValues"] = "0"

    return get_html({"chart": chart_data["details"]["chartProperties"], "dataset": series, "categories": {
        "category": x_categories}}, chart_data["details"]["chartType"])


def create_pie_chart(chart_data):
    plot_data = [{"label": i["_id"], "value": i["count"]} for i in chart_data["data"]]
    chart_data["details"]["chartProperties"]["startingAngle"] = "310"
    chart_data["details"]["chartProperties"]["decimals"] = "0"
    chart_data["details"]["chartProperties"]["showLegend"] = "1"
    chart_data["details"]["chartProperties"]["labelFontColor"] = "#FFFFFF"
    chart_data["details"]["chartProperties"]["labelFontSize"] = "20"
    chart_data["details"]["chartProperties"]["centerLabelColor"] = "#FFFFFF"
    chart_data["details"]["chartProperties"]["centerLabelFontSize"] = "30"
    return get_html({"chart": chart_data["details"]["chartProperties"], "data": plot_data}, "doughnut2d")


def create_3d_pie_chart(chart_data):
    plot_data = [{"label": i["_id"], "value": i["count"]} for i in chart_data["data"]]
    chart_data["details"]["chartProperties"]["startingAngle"] = "310"
    chart_data["details"]["chartProperties"]["decimals"] = "0"
    chart_data["details"]["chartProperties"]["showLegend"] = "1"
    chart_data["details"]["chartProperties"]["labelFontColor"] = "#FFFFFF"
    chart_data["details"]["chartProperties"]["labelFontSize"] = "20"
    chart_data["details"]["chartProperties"]["enableRotation"] = "0"
    return get_html({"chart": chart_data["details"]["chartProperties"], "data": plot_data}, "doughnut3d")


def create_ranking_chart(chart_data):
    plot_data = [{"label": i["_id"], "value": i["count"]} for i in chart_data["data"]]
    return get_html({"chart": chart_data["details"]["chartProperties"], "data": plot_data}, "bar2d")


def create_event_chart(data):
    data["details"]["chartProperties"]["drawAnchors"] = 0
    data["details"]["chartProperties"]["slantLabels"] = "1"
    data["details"]["chartProperties"]["showValues"] = "0"
    data["details"]["chartProperties"]["showTickMarks"] = "1"
    data["details"]["chartProperties"]["chartTopMargin"] = 175
    data["details"]["chartProperties"]["chartBottomMargin"] = 175
    data["details"]["chartProperties"]["captionAlignment"] = "left"

    values = [{"label": i[0], "value": i[1]} for i in data["data"]["series"]]
    x_categories_parsed = {i[0].replace(tzinfo=None): j for j, i in enumerate(data["data"]["series"])}

    annotations = {"autoscale": "1",
                   "groups": []}
    v_trend_line = {"line": []}

    for i, event in enumerate(data["data"]["events"]):
        annotations["groups"].append(make_annotation(event, x_categories_parsed, divmod(i, 4)[1]))
        v_trend_line["line"].append(make_trend_line(event, x_categories_parsed))

    return get_html({"chart": data["details"]["chartProperties"],
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


def make_annotation(event, datetime_to_index, cycle):
    start_index = datetime_to_index[event.start]
    end_index = datetime_to_index[event.end]
    label = event.get_chart_label()

    top_top = -200
    top_bottom = -5
    bottom_top = 120
    bottom_bottom = 320

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
        "wrapWidth": 150,
        "fillcolor": "#ffffff",
        "fontsize": "15",
        "x": "$dataset.0.set." + str(int(np.mean([start_index, end_index]))) + ".x",
        "y": "$canvasStartY",
        "bgColor": '#0075c2',
        "wrapHeight": 95
    }

    if cycle == 0:
        start_line_annotation["y"] += " - " + str(top_top)
        end_line_annotation["y"] += " -  " + str(top_top)
        label_annotation["y"] += " -  " + str(top_top)
        label_annotation["vAlign"] = "bottom"
    elif cycle == 1:
        start_line_annotation["y"] += " - " + str(top_bottom)
        end_line_annotation["y"] += " - " + str(top_bottom)
        label_annotation["y"] += " - " + str(top_bottom)
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


def create_chart(data):
    options = {
        "zoomline": create_time_graph,
        "msline": create_time_graph,
        "bar2d": create_ranking_chart,
        "doughnut2d": create_pie_chart,
        "doughnut3d": create_3d_pie_chart,
        "event": create_event_chart,
    }
    return options[data["details"]["chartType"]](data)


if __name__ == "__main__":
    html = None
    with open("out.html", "w") as f:
        f.write(html)
