from flask import Flask, request
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.ext.flask.middleware import XRayMiddleware
import logging
from random import randint


app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure the X-Ray recorder
xray_recorder.configure(service='flask-demo', sampling=False)

# Add X-Ray middleware to Flask
XRayMiddleware(app, xray_recorder)

@app.route('/')
def index():
    return 'Hello, World!'

@app.route("/rolldice")
def roll_dice():
    player = request.args.get('player', default=None, type=str)
    result = str(roll())
    if player:
        logger.warning("%s is rolling the dice: %s", player, result)
    else:
        logger.warning("Anonymous player is rolling the dice: %s", result)
    return result


def roll():
    return randint(1, 6)

@app.route('/trace')
def trace():
    # Example of a traced function
    subsegment = xray_recorder.begin_subsegment('trace_example')
    subsegment.put_annotation('example', 'trace')
    xray_recorder.end_subsegment()
    return 'Tracing example!'

if __name__ == '__main__':
    app.run(debug=True)
