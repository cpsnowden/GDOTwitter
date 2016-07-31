level_map = {
    "Minute": 1,
    "Hour": 2,
    "Day": 3,
    "Week": 4,
}


def get_date_projection(key, level):
    n=level_map[level] + 1

    first_o = [("ml", {"$millisecond": key}),
               ("s", {"$second": key}),
               ("m", {"$minute": key}),
               ("h", {"$hour": key}),
               ("d", {"$dayOfWeek": key})]

    first_projection = dict(first_o[:n])
    first_projection["date"] = key

    second_o = ["$ml",
                {"$multiply": ["$s", 1000]},
                {"$multiply": ["$m", 60, 1000]},
                {"$multiply": ["$h", 60, 60, 1000]},
                {"$multiply": [{"$subtract":["$d",1]}, 60, 60, 1000, 24]}]

    addition = second_o[:n]
    secondary_projection = {"date": {"$subtract": ["$date", {"$add": addition}]}}

    return first_projection, secondary_projection