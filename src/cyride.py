# cyride is the main entry point for the cyride-alexa web application.  The
# module inspects the requests and delegates the processing of the request to
# modules designed to handle the request.
import logging
import os

from helpers import build_response
from nextarrivalintent import next_arrival_handler

# The ride module configures the logger and determines if the request is an
# intent which should be processed, otherwise it returns a response indicating
# the request is invalid.
# Inputs:
#   event - A dictionary created from the Alexa request which contains
#       information given by the user as well as unique keys and tokens.
#   context - A dictionary created from the Alexa request which contains
#       runtime information as well as unique keys and tokens
# Outputs:
#   response - A dictionary containing a response for the user as well as
#       session details.


def ride(event, context):

    configure_logger()
    logging.info('***Start processing a new request.***')
    logging.debug(event)

    request = event['request']
    response = {}

    if 'IntentRequest' == request['type'] and 'intent' in request:

        response = intent_request_handler(event)
    else:
        response = build_response('The request type is not valid.')

    return response

# intent_request_handler comment


def intent_request_handler(event):

    intent = event['request']['intent']

    if 'name' in intent:
        if 'NextArrival' == intent['name']:
            return next_arrival_handler(event)
        elif 'ClosestStop' == intent['name']:
            pass

# configure_logger comment


def configure_logger():

    line_format = '%(asctime)s - %(levelname)s - %(module)s.%(funcName)s %(lineno)d: %(message)s'
    logfile = 'cyride.log'
    if 'PROD' != os.environ['ENVIRONMENT']:
        log_file = 'logs\\cyride.log'

    logging.basicConfig(format=line_format, filename=logfile, level=logging.INFO)
