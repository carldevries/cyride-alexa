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

    logger = configure_logger()
    logger.info('***Start processing a new request.***')
    logger.debug(event)

    request = event['request']
    response = {}

    if 'IntentRequest' == request['type'] and 'intent' in request:

        response = intent_request_handler(event)
    else:
        response = build_response('The request type is not valid.')

    return response

# intent_request_handler determines if an intent is speciefied and if so maps
# the request to the correct handler for the intent.
# Inputs:
#   event - The event object containing cyride, application, and user request
#      which is an argument passed to the lambda handler.
# Outputs:
#   A JSON response to be processed by Alexa/Echo unit.


def intent_request_handler(event):

    intent = event['request']['intent']

    if 'name' in intent:
        if 'NextArrival' == intent['name']:
            return next_arrival_handler(event)
        elif 'ClosestStop' == intent['name']:
            pass

# configure_logger configures the root logger for the Cyride-Alexa application
# based on the environment the application is running in. In production, the
# logger is set to log at the INFO level and updates the handlers set by
# Amazon to use a different formater. In all other environments (i.e. testing)
# The root logger is returned with no modifications and all settings are
# configured at the test class level.
# Inputs:
#   NA
# Outputs:
#   logger - A logger configured for either production or defined elsewhere.


def configure_logger():

    line_format = '%(asctime)s - %(levelname)s - %(module)s.%(funcName)s %(lineno)d: %(message)s'
    
    if 'PROD' == os.environ['ENV']:

        formatter = logging.Formatter(line_format)
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)

        if logger.handlers:
            for handler in logger.handlers:
                handler.setFormatter(formatter)
                
        return logger

    return logging.getLogger()