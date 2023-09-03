import os, logging
from os.path import isfile, join
from os import listdir
from flask import Flask

CONF_FILE_NAME_SUFFIX = ".metric.txt"
METRIC_FILE_DIR_DEFAULT = "/static_metrics"

app = Flask(__name__)
app.logger.setLevel(logging.INFO)
static_metrics = {}

@app.route('/<path>')
def serve_static(path):
    if path == "rescan":
        build_metrics()
        return "", 201
    else:
        metrics = static_metrics[path]
        if metrics:
            return metrics, 200
        else:
            return "", 404

def build_metrics():
    # read the config dif from an envvar
    metrics_dir = os.environ.get("METRIC_FILE_DIR") or METRIC_FILE_DIR_DEFAULT
    
    # find all files names *.metric.txt in the dir
    metric_files = [f for f in listdir(metrics_dir) if isfile(join(metrics_dir, f)) and CONF_FILE_NAME_SUFFIX in f]

    # load metrics
    for f in metric_files:
        with open(join(metrics_dir, f)) as metrics_file:
            route_name = f.split(CONF_FILE_NAME_SUFFIX)[0]
            static_metrics[route_name] = metrics_file.read()
            app.logger.info(f"-- Found metrics file {f}, creating route /{route_name}")

if __name__ == "__main__":
    build_metrics()

    # run the server
    app.run(debug=True, host="0.0.0.0", port=5001)
else:
    build_metrics()

