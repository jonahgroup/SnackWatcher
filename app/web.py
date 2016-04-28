from flask import Flask, render_template, request, redirect
from flask import Blueprint
from errors import *
from utils import (
    take_and_process_image,
    track_click,
    take_background
)
from filters import human_date
from db import *

web = Blueprint('web', __name__)


@web.route('/')
def index():
    log("index()")
    db = db_open()
    db_images = db_images_read_latest_n(db, 10)
    db_close(db)
    return render_template('index.jinja2.html',
                           db_images=db_images,
                           page_links="active")


@web.route('/calibrate/')
def calibrate():
    log("calibrate()")
    take_background()
    return render_template('success.jinja2.html',
                           msg="Calibration is complete.",
                           page_calibrate="active")


@web.route('/teach/')
def teach():
    log("teach()")
    return render_template('teach.jinja2.html',
                           page_teach="active")


@web.route('/snap/')
def snap():
    log("snap()")
    try:
        take_and_process_image()
        return render_template('success.jinja2.html',
                               msg="Your request snack has been watched.",
                               page_submit="active")
    except NotCalibratedException as e:
        return render_template('failure.jinja2.html',
                               msg=e.message,
                               page_submit="active")
    except NoBlobChangesDetectedException as e:
        return render_template('nochanges.jinja2.html',
                               msg=e.message,
                               page_submit="active")
    except NoBlobsDetectedException as e:
        return render_template('noblobs.jinja2.html',
                               msg=e.message,
                               page_submit="active")


@web.route('/click/')
def click():
    log("click()")
    url = request.args["url"]
    track_click(url)
    return redirect(url)


def create_app():
    app = Flask(__name__, static_folder="../static", static_url_path="/static")

    from api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    app.register_blueprint(web, url_prefix='')
    app.debug = True
    app.add_template_filter(human_date)

    return app
