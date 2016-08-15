from AnalysisEngine.Charting.Charting import get_html
import json

raw = json.load(open("gbp-usd.json"))

demo = {"USD": 1.4627, "IDR": 20410.0, "BGN": 2.6631, "ILS": 5.7719, "DKK": 10.158, "CAD": 2.0611, "JPY": 173.19, \
                                                                                                  "HUF": 428.66, "RON": 6.158, "MYR": 6.4526, "SEK": 12.572, "SGD": 2.0982, "HKD": 11.339, "AUD": 2.0679, "CHF": 1.4769, "KRW": 1755.4, "CNY": 9.5844, "TRY": 4.4002, "HRK": 10.404, "NZD": 2.2013, "THB": 52.992, "EUR": 1.3617, "NOK": 13.103, "RUB": 108.92, "INR": 97.8, "MXN": 25.528, "CZK": 36.8, "BRL": 5.9002, "PLN": 5.906, "PHP": 68.883, "ZAR": 23.153}

demo = {"USD":1}
x_categories  = [{"label":i} for i in raw["dates"]]

mapping = dict([(s,[]) for s in demo.keys()])

series = [{"seriesname": s, "data":mapping[s]} for s in mapping.keys()]


for day in raw["usd-gbp"]:
    for fx in day:
        if fx in mapping:
            mapping[fx].append({"value": day[fx]})


date_source  = {
    "chart" : {"setAdaptiveYMin":1,"showValues":"0"},
    "dataset": series,
    "categories": {"category": x_categories}}


html = get_html(date_source, "msline")


with open("gdbfx.html","w") as f:
    f.write(html)