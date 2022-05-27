import time
import datetime
import os
import re
import json
import logging
from flask import (
    Flask,
    request,
    session,
    g,
    redirect,
    url_for,
    abort,
    render_template,
    flash,
)
from revprox import ReverseProxied

# configuration
IMAGEDIR = "/data/images/"
LABELDIR = "/data/labels/"
CONFIG_FILE = "/data/config.json"
DEBUG = False
SECRET_KEY = os.environ.get("SECRETKEY", "development key")
for d in (IMAGEDIR, LABELDIR):
    try:
        os.makedirs(d)
    except FileExistsError:
        pass

app = Flask(__name__)
app.config.from_object(__name__)
app.wsgi_app = ReverseProxied(app.wsgi_app)


@app.before_request
def before_request_func():
    try:
        with open(app.config["CONFIG_FILE"], "rt") as fp:
            g.config = json.load(fp)
            g.labels = g.config["labels"]
    except Exception as e:
        logging.warning(e)
        logging.warning("config.json could not be read. using defaults.")
        g.labels = [
            {"type": "checkbox", "name": "my_check", "default": "off"},
            {"type": "text", "name": "my_text", "default": "1.0"},
            {
                "type": "range",
                "name": "my_slider",
                "default": "75",
                "min": "0",
                "max": "100",
            },
        ]
        g.config = {"title": "Labeler", "labels": g.labels}

    for label in g.labels:
        label['value'] = label['default']

def natural_key(string_):
    """See http://www.codinghorror.com/blog/archives/001018.html"""
    return [int(s) if s.isdigit() else s for s in re.split(r"(\d+)", string_)]


def get_metadata_path(image_path):
    base, ext = os.path.splitext(os.path.basename(image_path))
    jsonpath = os.path.join(app.config["LABELDIR"], base + ".json")
    return jsonpath


def get_current_image(images):
    for i, f in enumerate(images):
        jsonpath = get_metadata_path(f)
        if not os.path.exists(jsonpath):
            return i
    return i


def get_image_list():
    return sorted(
        [
            os.path.join(app.config["IMAGEDIR"], x)
            for x in os.listdir(app.config["IMAGEDIR"])
            if not x.endswith("json")
        ],
        key=natural_key,
    )


def get_metadata(imagepath):
    try:
        with open(get_metadata_path(imagepath), "rt") as fp:
            values = json.load(fp)
            metadata = [x.copy() for x in g.labels.copy()]
            for label in metadata:
                if label["name"] in values:
                    label["value"] = values[label["name"]]
                else:
                    label["value"] = label["default"]

            return metadata
    except FileNotFoundError:
        # Return defaults
        return g.labels
    except Exception as e:
        logging.error(e)
        # Return defaults
        return g.labels


def set_metadata(values, imagepath):

    metadata = [x.copy() for x in g.labels.copy()]
    for label in metadata:
        if not label["name"] in values:
            values[label["name"]] = label["default"]

    # logging.warning((path, values))
    if not os.path.exists(
        os.path.join(app.config["IMAGEDIR"], os.path.basename(imagepath))
    ):
        return
    with open(get_metadata_path(imagepath), "wt") as fp:
        return json.dump(values, fp, indent=2, sort_keys=True)


@app.route("/", methods=["GET", "POST"])
@app.route("/image:<int:id>", methods=["GET", "POST"])
def show_image(id=None):

    if request.method == "POST":
        # parse form
        image_name = request.form["image_name"]
        metadata = {}
        for key in request.form:
            if key.startswith("label_"):
                dictkey = key[6:]
                metadata[dictkey] = str(request.form[key])
        set_metadata(metadata, image_name)

    images = get_image_list()
    if id == None:
        id = get_current_image(images)
    else:
        id = max(0, min(len(images) - 1, int(id)))
    labels = get_metadata(images[id])
    id_minus = max(0, min(len(images) - 1, int(id - 1)))
    id_plus = max(0, min(len(images) - 1, int(id + 1)))
    return render_template(
        "show_image.html",
        id=id,
        count=len(images),
        image=images[id],
        image_name=os.path.basename(images[id]),
        image_plus=images[id_plus],
        labels=labels,
        id_minus=id_minus,
        id_plus=id_plus,
        title=g.config.get("title", "Labeler"),
    )