from flask import Flask, request, render_template
import json

app = Flask(__name__)

clusters = {
    "cascade": "No data",
    "haswell": "No data",
    "tom": "No data",
    "jerry": "No data",
    "phobos": "No data",
    "deimos": "No data",
    "amy": "No data",
    "fry": "No data",
}

@app.route("/", methods=["GET", "POST"])
def monitor_clusters():
    if request.method == "POST":
        data = request.get_json()
        cluster = data["cluster"]
        info = data["info"]
        clusters[cluster] = info
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}

    else:
        return render_template('monitoring.html', clusters=clusters)