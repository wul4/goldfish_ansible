import datetime
import connexion
import logging

import goldfish.errors as err

from goldfish.config import config, config_validator
from goldfish.services.api import app, logger

config.validators.register(
    config_validator('EXAMPLE_SETTING', must_exist=True),
)

config.validators.validate()

def render_nobar(exception):
    logger.error("Invalid request body seen!")
    return {'error': 'No bar in request body!'}, 404

app.add_error_handler(err.NoBar, render_nobar)

def get_bar():
    example = config.EXAMPLE_SETTING
    return {'message': 'Hello world! Example setting is: %s' % example}, 200

def post_bar(body):
    data = body
    bar = data.get('bar', None)
    if not bar:
        raise err.NoBar

    logger.info("Processing Hello World..")

    return {'status': 'Posted to Hello World!'}, 201
    
def delete_bar():
    logger.info("Processing Hello World..")

    return {'message': 'Hello from Bar DELETE'}, 200