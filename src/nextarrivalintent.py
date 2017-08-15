# The nextarrivalintent processes NextArrival intents.

import logging
from json import loads
import os
import xml.etree.ElementTree as ET

from helpers import get_slot_inputs, get_alexa_device_location_inputs, build_response, get_geocode_lat_lon_coordinates, build_prediction_response
from nextbus import get_route_list, get_route_config, get_predictions
from nextbusdataparser import get_route_tags, get_closest_stop_tag, get_next_vehicle_prediction
from mapquest import geocode, reverse_geocode
from amazon import get_device_address

# next_bus_handler comment


def next_bus_handler(requested_route, echo_coordinates):

    logging.info('Requesting NextBus data.')

    agency_name = os.environ['AGENCY_NAME']
    if agency_name is not None and agency_name is not '':

        route_list = get_route_list(agency_name)
        route_list_elements = ET.fromstring(route_list)
        requested_route_tags = get_route_tags(requested_route, route_list_elements)

        # Determine which route to use.
        requested_route_tag = requested_route_tags[0]
        logging.debug(requested_route_tag)
        requested_route_config = get_route_config(agency_name, requested_route_tag, True)
        route_config_elements = ET.fromstring(requested_route_config)
        latitude = echo_coordinates['lat']
        longitude = echo_coordinates['lon']
        closest_stop_tag = get_closest_stop_tag(latitude, longitude, route_config_elements)

        if closest_stop_tag is not None:

            predictions = get_predictions(agency_name, requested_route_tag, closest_stop_tag)
            predictions_elements = ET.fromstring(predictions)
            prediction = get_next_vehicle_prediction(predictions_elements)
            return prediction

    return None

# next_arrival_handler comment


def next_arrival_handler(event):

    logging.info('Processing Next Arrival Intent.')
    request = event['request']
    context = event['context']
    slot_inputs = get_slot_inputs(request['intent']['slots'])

    # Concatenate the requested route components
    requested_route = format_route_name(slot_inputs)

    # Using user given address.
    if 'StreetAddress' in slot_inputs:

        logging.info('The user supplied and adress.')

        street_address = slot_inputs['StreetAddress']
        echo_coordinates = request_mapquest_coordinates(street_address)

        # If the geocode coordinates exist process the response.  If they do
        # not ask the user to provide them or use the device location if a
        # consent_token is available.
        if echo_coordinates is not None:

            # Process with given address
            prediction = next_bus_handler(requested_route, echo_coordinates)
            response_text = 'Valid Address provided by user and found.'
        else:
            # Respond with an invalid address message ask for new address
            # or possibly get address if consent is given
            response_text = '''Coordinates for the address given could not be
                found. Please say your address again.'''
            device_location_inputs = get_alexa_device_location_inputs(context)

            if device_location_inputs['device_id'] is not None and device_location_inputs['consent_token'] is not None and device_location_inputs['api_endpoint'] is not None:
                response_text = response_text + '''You may also say. device
                    location. to use the location you assigned to your Alexa
                    enabled device.'''

            return build_response(response_text, 'PlainText', False)
    else:

        logging.info('No address given')
        device_location_inputs = get_alexa_device_location_inputs(context)

        # An address was not given so if a consent token exists then request
        # the address.
        if device_location_inputs['consent_token'] is not None:

            logging.info('Found a consent token.')

            device_id = device_location_inputs['device_id']
            consent_token = device_location_inputs['consent_token']
            api_endpoint = device_location_inputs['api_endpoint']

            address_response = get_device_address(device_id, consent_token, api_endpoint)
            address_data = loads(address_response)

            # Even if a token exists an address may not be returned. Check it.
            # Working under the assumption that if at least one line is present
            # we are good to go. Additional address lines can still be used
            # later if present.
            if address_data['addressLine1'] is not None and address_data['city'] is not None and address_data['stateOrRegion'] is not None:
                logging.info('Received minimum address components from Amazon.')
                # Process the request with the address provided from the device
                # api.
                echo_address = concatenate_alexa_address(address_data)
                echo_coordinates = request_mapquest_coordinates(echo_address)

                if echo_coordinates is not None:

                    prediction = next_bus_handler(requested_route, echo_coordinates)
                else:
                    # MapQuest oops
                    pass

                minutes_str = str(prediction['minutes'])
                minutes_str = minutes_str.split('.')[0]
                response_text = 'The next ' + requested_route
                response_text = response_text + ' bus will arrive in <time>.'
                # response_text = response_text + minutes_str + ' minutes.'
                return build_prediction_response(response_text, minutes_str)
            else:
                # Consent token exists, but not address was returned.
                # Try something...
                response_text = '''A valid address could not be found for your
                    device.  Please say your address'''

                return build_response(response_text, 'PlainText', False)
        else:

            logging.info('No consent token found')
            # Consent token does not exist and user didn't provide an address
            response_text = '''You have not provided an address and you have
                not given consent to look up your address.  Please say your
                address or update your consent settings via the Alexa mobile
                app.'''

            return build_response(response_text, 'PlainText', False)

# request_mapquest_coordinates comment


def request_mapquest_coordinates(address):

    mapquest_api_key = os.environ['MAPQUEST_API_KEY']

    geocode_response = geocode(address, mapquest_api_key)
    geocode_data = loads(geocode_response)

    echo_coordinates = get_geocode_lat_lon_coordinates(geocode_data)

    return echo_coordinates

# concatenate_alexa_address comment


def concatenate_alexa_address(address_data):

    address = ''

    if not is_blank(address_data['addressLine1']):
        address = address_data['addressLine1'].strip()

    if not is_blank(address_data['addressLine2']):
        address = address + ' ' + address_data['addressLine2'].strip()

    if not is_blank(address_data['addressLine3']):
        address = address + ' ' + address_data['addressLine3'].strip()

    if not is_blank(address_data['city']):
        address = address + ' ' + address_data['city'].strip()

    if not is_blank(address_data['stateOrRegion']):
        address = address + ', ' + address_data['stateOrRegion'].strip()

    return address

# format_route_name comment


def format_route_name(slot_inputs):

    number_raw = slot_inputs['RouteNumber']
    number = '' if is_blank(number_raw) else number_raw.strip().replace(' ', '').upper()

    color_raw = slot_inputs['RouteColor']
    color = '' if is_blank(color_raw) else color_raw.strip()

    direction_raw = slot_inputs['RouteDirection']
    direction = '' if is_blank(direction_raw) else direction_raw.strip()

    name = number + ' ' + color + ' ' + direction
    return name

# is_blank comment


def is_blank(s):

    if s is None or len(s.strip()) == 0:
        return True

    return False
