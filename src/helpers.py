# get_geocode_lat_lon_coordinates comment


def get_geocode_lat_lon_coordinates(geocode_data):

    if 'results' in geocode_data and len(geocode_data['results']) > 0:
        result = geocode_data['results'][0]
        if 'locations' in result and len(result['locations']) > 0:
            location = result['locations'][0]
            if 'latLng' in location:
                lat_lon = location['latLng']
                if 'lat' in lat_lon and 'lng' in lat_lon:
                    lat = lat_lon['lat']
                    lon = lat_lon['lng']
                    if lat is not None and lon is not None:
                        return {
                                'lat': lat,
                                'lon': lon
                               }

    return None

# get_alexa_device_location_inputs comment


def get_alexa_device_location_inputs(context):

    device_id = None
    consent_token = None
    api_endpoint = None

    if 'System' in context:
        system = context['System']

        if 'device' in system:
            if 'deviceId' in system['device']:
                device_id = system['device']['deviceId']

        if 'user' in system:
            if 'permissions' in system['user']:
                if 'consentToken' in system['user']['permissions']:
                    user = system['user']
                    consent_token = user['permissions']['consentToken']

        if 'apiEndpoint' in system:
            api_endpoint = system['apiEndpoint']

    return {
            'device_id': device_id,
            'consent_token': consent_token,
            'api_endpoint': api_endpoint
           }

# get_slot_inputs comment


def get_slot_inputs(slots):

    slot_inputs = {}
    for slot_key, slot_value in slots.iteritems():
        for slot_data_key, slot_data_value in slot_value.iteritems():
            # Check for a value key. Some slots come in with name but no value.
            if slot_data_key == 'value':
                slot_inputs[slot_key] = slot_data_value

    return slot_inputs

# build_response comment


def build_response(text, type='PlainText', shouldEndSession=True):

    return {
            'version': '1.0',
            'response': {
                'outputSpeech': {
                    'type': type,
                    'text': text
                },
                'shouldEndSession': shouldEndSession
            }
           }
