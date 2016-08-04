from string import Template

data = [{
    "label": "Jan",
    "value": "420000"
}, {
    "label": "Feb",
    "value": "810000"
}, {
    "label": "Mar",
    "value": "720000"
}, {
    "label": "Apr",
    "value": "550000"
}, {
    "label": "May",
    "value": "910000"
}, {
    "label": "Jun",
    "value": "510000"
}, {
    "label": "Jul",
    "value": "680000"
}, {
    "label": "Aug",
    "value": "620000"
}, {
    "label": "Sep",
    "value": "610000"
}, {
    "label": "Oct",
    "value": "490000"
}, {
    "label": "Nov",
   "value": "900000"
}, {
    "label": "Dec",
    "value": "730000"
}]

type = 'bar2d'
width =  "1920"
height =  "1080"
dataSource =  {
    "chart": {
        "bgColor":"#000000,#000000",
        "caption": "Monthly revenue for last year",
        "subCaption": "Harry's SuperMart",
        "xAxisName": "Month",
        "yAxisName": "Revenues (In USD)",
        "numberPrefix": "$",
        "canvasBgAlpha":"0",
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
        "plotFillAlpha": "50"
    },
    "data": data
}

s = Template(open("Chart.html").read())
f = s.safe_substitute({'dataSource':dataSource, "height":height, "width":width, "type":type})
print f

with open("out.html","w") as fl:
    fl.write(f)