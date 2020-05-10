import datetime
import connexion
import logging

import goldfish.errors as err

from goldfish.services.api import app, logger

def render_nopebble(exception):
    logger.error("Invalid request body seen!")
    return {'error': 'No pebble in request body!'}, 404

app.add_error_handler(err.NoPebble, render_nopebble)

def get_pebble():
    return {'payload': 'Pebble logo yelling back!'}, 200

def post_pebble(body):
    data = body
    pebble = data.get('pebble', None)
    if not pebble:
        raise err.NoPebble

    logger.info("Processing Pebble..")

    return {'status': 'You posted Pebble: %s' % pebble}, 201
    
def delete_pebble():
    logger.info("Processing Pebble..")

    return {'message': 'Don\'t delete the Pebble \:\('}, 200