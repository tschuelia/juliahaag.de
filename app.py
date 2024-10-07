import json
from collections import OrderedDict
from datetime import datetime
from typing import Dict, Optional, Union

from flask import Flask, render_template, request

app = Flask(__name__)

clusters = {
    "cascade": ("No data", ""),
    "haswell": ("No data", ""),
    "tom": ("No data", ""),
    "jerry": ("No data", ""),
    "phobos": ("No data", ""),
    "deimos": ("No data", ""),
    "amy": ("No data", ""),
    "fry": ("No data", ""),
    "mlserver": ("No data", ""),
    "jonas": ("No data", ""),
}

month_to_number = {
    "January": 1,
    "February": 2,
    "March": 3,
    "April": 4,
    "May": 5,
    "June": 6,
    "July": 7,
    "August": 8,
    "September": 9,
    "October": 10,
    "November": 11,
    "December": 12,
}


def load_data(file_name: str) -> Dict[str, Dict[str, str]]:
    return json.load(open(f"static/data/{file_name}.json"))


def sort_by_year_month(
    data: Dict[str, Dict[str, str]],
    date_field: str = "date",
    date_format: Optional[str] = "%m-%Y",
) -> OrderedDict[str, Dict[str, Union[str, datetime]]]:
    for key, value in data.items():
        value[date_field] = datetime.strptime(value[date_field], date_format)

    return OrderedDict(
        sorted(data.items(), key=lambda item: (item[1][date_field]), reverse=True)
    )


def sort_by_start_end(
    data: Dict[str, Dict[str, str]],
    start_field: str = "start",
    end_field: str = "end",
    date_format: Optional[str] = "%m-%Y",
    start_first: bool = True,
) -> OrderedDict[str, Dict[str, Union[str, datetime]]]:
    for key, value in data.items():
        value[start_field] = datetime.strptime(value[start_field], date_format)

        if value.get(end_field):
            value[end_field] = datetime.strptime(value[end_field], date_format)

    if start_first:
        # sorts the data by start date and end date in descending order, uses only start date if end date is not available
        def sort_fct(item):
            return item[1][start_field], item[1].get(end_field, datetime.max)
    else:

        def sort_fct(item):
            return item[1].get(end_field, datetime.max), item[1][start_field]

    return OrderedDict(
        sorted(
            data.items(),
            key=sort_fct,
            reverse=True,
        )
    )


@app.route("/", methods=["GET"])
def cv_homepage():
    return render_template(
        "index.html",
        educations=sort_by_start_end(load_data("educations")),
        further_educations=sort_by_year_month(load_data("further_educations")),
        experiences=sort_by_start_end(load_data("experiences"), start_first=False),
        projects=load_data("projects"),
        publications=sort_by_year_month((load_data("publications"))),
        preprints=sort_by_year_month((load_data("preprints"))),
        talks=sort_by_year_month(load_data("talks")),
    )


@app.route("/monitoring", methods=["GET", "POST"])
def monitor_clusters():
    if request.method == "POST":
        try:
            data = request.get_json()
            cluster = data["cluster"]
            if cluster not in clusters:
                return render_template("monitoring.html", clusters=clusters)
            info = data["info"]
            time = data["time"]
            clusters[cluster] = (info, time)
            return (
                json.dumps({"success": True}),
                200,
                {"ContentType": "application/json"},
            )
        except Exception:
            return render_template("monitoring.html", clusters=clusters)

    else:
        return render_template("monitoring.html", clusters=clusters)
