import logging
import mapquest
import os

def lambda_handler(event, context):

    agency_name = os.environ['AGENCY_NAME']
    configure_logger()
    logging.info('***Start processing a new request.***')

    request = event['request']
    slot_input = get_slot_data(request['intent']['slots'])

    if not reduce(lambda one, two : (True == one or 'StreetAddress' == one) or 'StreetAddress' == two, slot_input):
        return build_response('You must provide a street address. Please try again.')


    if 'IntentRequest' == request['type']:
        intent = request['intent']
        if 'NextArrival' == intent['name']:
            handle_when_intent(slot_input)
        elif 'ClosestStop' == intent['name']:
            handle_closest_stop(slot_input)

    return build_response('Hello!')

def handle_next_arrival(slots):
    pass


def handle_closest_stop(slots):

    agency_name = os.environ('AGENCY_NAME')

def get_slot_data(slots):

    slot_input = {}
    for slot_key, slot_value in slots.iteritems():
        slot_input[slot_key] = ''
        for slot_data_key, slot_data_value in slot_value.iteritems():
            if slot_data_key == 'value':
                logging.info('Slot name: ' + slot_key + ', Data: ' + slot_data_key + '=' + slot_data_value)
                slot_input[slot_key] = slot_data_value

    return slot_input

def build_response(text, type = 'PlainText', shouldEndSession = True):

    return {
    'version' : '1.0',
    'response' : {
        'outputSpeech' : {
            'type' : type,
            'text' : text
        },
    'shouldEndSession' : shouldEndSession
    }
            }

def configure_logger():

    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(module)s.%(funcName)s %(lineno)d: %(message)s', filename='..\\logs\\cyride.log', level=logging.INFO)
