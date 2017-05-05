# amazon is a module for requesting an Alexa enabled device's location using
# the Device Address API.
import httpgetclient

# get_device_address requests the address of the Alexa enabled device.
# Inputs:
#   device_id - The Alexa enabled device's unique id.
#   consent_token - The user's consent token.  It may not be None or ''.
# Outputs:
#   response - A string representation of the content returned in the response.


def get_device_address(device_id, consent_token, host):

    address_path = '/v1/devices/' + device_id + '/settings/address'
    headers = {
                'Accept': 'application/json',
                'Authorization': 'Bearer ' + consent_token,
                'Host': host.replace('https://', '')
              }

    return _process_request(address_path, headers, host)

# _process_request invokes httpgetclient to send the request and extracts the
# content as a string from the response.


def _process_request(path, headers, host):

    response = httpgetclient.send_request(host, path, None, headers)
    return response.read()
