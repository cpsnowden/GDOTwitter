import json
import logging
import os
from collections import OrderedDict
from string import Template

import AnalysisEngine.Util

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
    chart_data["details"]["chartProperties"]["labelStep"] = 6
    chart_data["details"]["chartProperties"]["slantLabels"] = 1
    chart_data["details"]["chartProperties"]["showValues"] = "0"

    return get_html({"chart": chart_data["details"]["chartProperties"], "dataset": series, "categories": {
        "category": x_categories}}, "msline")


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
    return get_html({"chart": chart_data["details"]["chartProperties"], "data": plot_data}, "doughnut3d")


def create_ranking_chart(chart_data):
    plot_data = [{"label": i["_id"], "value": i["count"]} for i in chart_data["data"]]
    return get_html({"chart": chart_data["details"]["chartProperties"], "data": plot_data}, "bar2d")


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
        "msline": create_time_graph,
        "bar2d": create_ranking_chart,
        "doughnut2d": create_pie_chart,
        "doughnut3d": create_3d_pie_chart,
    }
    return options[data["details"]["chartType"]](data)


if __name__ == "__main__":
    d = {
        "data": [
            {
                "_id": "imwithher",
                "count": 47964
            },
            {
                "_id": "feelthebern",
                "count": 39029
            },
            {
                "_id": "makeamericagreatagain",
                "count": 36757
            },
            {
                "_id": "trump2016",
                "count": 17056
            },
            {
                "_id": "bernieorbust",
                "count": 10287
            },
            {
                "_id": "trumptrain",
                "count": 8181
            },
            {
                "_id": "neverhillary",
                "count": 7692
            },
            {
                "_id": "stillsanders",
                "count": 7272
            },
            {
                "_id": "stoptpp",
                "count": 5530
            },
            {
                "_id": "americafirst",
                "count": 5195
            }
        ],
        "details": {
            "chartType": "doughnut2d",
            "chartProperties": {"yAxisName": "Number of Occurences",
                                "xAxisName": "Hashtag",
                                "caption": "blash",
                                "subcaption": "Top Hashtags"}
        }
    }
    html = create_chart(d)
    with open("out.html", "w") as f:
        f.write(html)
