from flask import Flask, request, render_template
import json

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


@app.route("/", methods=["GET"])
def cv_homepage():
    return render_template('index.html')


@app.route("/monitoring", methods=["GET", "POST"])
def monitor_clusters():
    if request.method == "POST":
        try:
            data = request.get_json()
            cluster = data["cluster"]
            if cluster not in clusters:
                return render_template('monitoring.html', clusters=clusters)
            info = data["info"]
            time = data["time"]
            clusters[cluster] = (info, time)
            return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
        except:
            return render_template('monitoring.html', clusters=clusters)

    else:
        return render_template('monitoring.html', clusters=clusters)
